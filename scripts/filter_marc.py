import json
import gzip
import re
import argparse


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--output", dest="output", help="Output file")
    parser.add_argument("--hathitrust_root", dest="hathitrust_root", help="Path to HathiTrust")
    args, rest = parser.parse_known_args()
    
    is_subset_rx=r"(^|\s)((Armen.*)|(Turkish)|(Ottoman)|(Istʻanpōlta)|(Istʻanpōl)|(Stʻanpōlta)|(Stʻanpōl)|(Beçte)|(Stanpol)|(Vēnētik)|(Pasmakhanē)|(Mkhitʻarean)|(Constantinople)|(Viēna))" 
    record_list = []

    def get_id(obj):
        data = json.loads(obj)
        for item in data["fields"]:
            if "974" in item.keys():
                for subf in item["974"]["subfields"]:
                    var_keys = subf.keys()
                    if 'u' in var_keys:
                        return (subf['u'])
        
        #i=0
    with gzip.open(args.hathitrust_root+'/full_marc.json.gz', 'rt') as fh:
        for record in fh:
            #i+=1
            #if i>1000000:
        #       break
            if re.search(is_subset_rx, record, re.IGNORECASE): 
                record_list.append(record)
                        
    with gzip.open(args.output, 'wt') as ofh:
        for line in record_list:
            j = {
                #"htid":get_id(line),
                "marc":json.loads(line)
                    }   
            ofh.write(json.dumps(j)+"\n")
                        
                
                
