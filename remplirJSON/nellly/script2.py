import subprocess
import json

if __name__ == "__main__":
    with open('donnees.json', 'r') as f:
        contenu = json.load(f)
        for cle in contenu:
            for j in contenu[cle]:
                print(j['ip'])
                with open("DNSSEC_RESOLVERS.txt", "r") as file:
                    content = file.read()
                    if j['ip'] in content:
                        DNSSEC = "Yes"
                    else:
                        DNSSEC = "No"
                try:
                    with open('./DNSSEC.json', 'r') as f:
                        contenu_json = json.load(f)
                except FileNotFoundError:
                    contenu_json = {}
                except json.decoder.JSONDecodeError as e:
                    print(f"Error decoding JSON: {e}")
                    contenu_json = {}
                j['DNSSEC'] = DNSSEC
                contenu_json[cle] = [j]

                with open('./DNSSEC.json', 'w') as f:
                    json.dump(contenu_json, f, indent=4)