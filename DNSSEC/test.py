import json
import subprocess

if __name__ =="__main__":
    dico = {}
    with open("../remplirJSON/nellly/DNSSEC.json", 'r') as f:
        contenu = json.load(f)
        for i in contenu:
            for j in contenu[i]:
                if j['DNSSEC'] == "Yes":
                    if j['orgName'] not in dico :
                        dico[j['orgName']] = 1
                    elif j['orgName'] in dico :
                        dico[j['orgName']] += 1
        print(dico)