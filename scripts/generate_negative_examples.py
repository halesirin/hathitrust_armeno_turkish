import re
import argparse
import gzip
import json
import csv
import random
import os.path
import unicodedata
import zipfile
from pairtree import PairtreeStorageFactory

csv.field_size_limit(1000000000)

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--hathitrust_root", dest="hathitrust_root", help="Path to Hathi Trust")
    parser.add_argument("--unicode_scripts", dest="unicode_scripts", default="data/Scripts.txt", help="Unicode Script.txt file")
    parser.add_argument("--per_language", dest="per_language", default=3, type=int, help="Number of documents per language")
    parser.add_argument("--random_seed", dest="random_seed", default=None, type=int, help="Random seed")
    parser.add_argument("--output", dest="output", help="Output file")
    args = parser.parse_args()
    
    if args.random_seed:
        random.seed(args.random_seed)

    script_lookup = {}
    with open(args.unicode_scripts, "rt") as ifd:
        for line in ifd:
            m = re.match(r"^(\S+?)(?:\.\.(\S+))?\s+;\s+([^\#]+)\s+\#.*$", line)
            if m:
                start, end, script = m.groups()
                start = int(start, base=16)
                for i in range(start, 1 + (start if not end else int(end, base=16))):
                    script_lookup[i] = script
    langs = {}
    with gzip.open(os.path.join(args.hathitrust_root, "hathi_full_20211001.txt.gz"), "rt") as ifd:
        for row in csv.reader(ifd, delimiter="\t"):
            if len(row) < 19:
                continue
            lang = row[18]
            htid = row[0]
            status = row[1]
            if status != "deny":
                langs[lang] = langs.get(lang, [])
                langs[lang].append(htid)
    langs = {k : v for k, v in langs.items() if re.match(r"[a-z]{3}", k) and len(v) > args.per_language * 4}
    psf = PairtreeStorageFactory()
    with gzip.open(args.output, "wt") as ofd:
        for lang, htids in langs.items():
            random.shuffle(htids)
            count = 0
            for htid in htids:
                subcollection, ident = re.match(r"^([^\.]+)\.(.*)$", htid).groups()
                try:
                    store = psf.get_store(
                        store_dir=os.path.join(
                            args.hathitrust_root,
                            subcollection
                        )
                    )
                except:
                    continue
                try:
                    obj = store.get_object(ident, create_if_doesnt_exist=False)
                except:                
                    continue
                pages = []
                for subpath in obj.list_parts():
                    for fname in obj.list_parts(subpath):
                        if fname.endswith("zip"):
                            with zipfile.ZipFile(
                                    obj.get_bytestream(
                                        "{}/{}".format(subpath, fname),
                                        streamable=True
                                    )
                            ) as izf:                            
                                for page in sorted(izf.namelist()):
                                    if page.endswith("txt"):
                                        txt = izf.read(page).decode("utf-8")
                                        pages.append(txt)

                txt = "\n".join(pages)
                script_counts = {}
                for c in txt:
                    e = script_lookup.get(ord(c), "Common")
                    if e != "Common":
                        script_counts[e] = script_counts.get(e, 0) + 1
                if len(script_counts) == 0:
                    continue
                maj_script = sorted([(v, k) for k, v in script_counts.items()], reverse=True)[0][1]
                final_txt = ""
                while len(txt) > 0:
                    cand = txt[:400]
                    txt = txt[400:]
                    script_counts = {}
                    for c in cand:
                        e = script_lookup.get(ord(c), "Common")
                        script_counts[e] = script_counts.get(e, 0) + 1
                    if script_counts.get(maj_script, 0) == max(script_counts.values()):
                        final_txt += cand
                if len(final_txt) == 0:
                    continue
                ofd.write(json.dumps({"script" : maj_script, "language" : lang, "content" : final_txt}) + "\n")
                count += 1
                if count >= args.per_language:
                    break
