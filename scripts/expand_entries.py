import argparse
import gzip
import zipfile
import json
import os.path
import re
from pairtree import PairtreeStorageFactory

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--input", dest="input", help="Input file")
    parser.add_argument("--output", dest="output", help="Output file")
    parser.add_argument("--hathitrust_root", dest="hathitrust_root", help="Path to HathiTrust")
    args, rest = parser.parse_known_args()

    psf = PairtreeStorageFactory()
    with gzip.open(args.input, "rt") as ifd, gzip.open(args.output, "wt") as ofd:
        for line in ifd:
            j = json.loads(line)
            subcollection, ident = re.match(r"^([^\.]+)\.(.*)$", j["htid"]).groups()
            store = psf.get_store(
                store_dir=os.path.join(
                    args.hathitrust_root,
                    subcollection
                )
            )
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

            j["content"] = "\n".join(pages)
            ofd.write(json.dumps(j) + "\n")
