import json
import subprocess

if __name__ =="__main__": 
    with open("./DNSSEC.json", 'r') as f:
        contenu = json.load(f)
        for i in contenu:
            contenu[i] = [contenu[i]]
            