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
                        j["DNSSEC"] = "Yes"
                    else:
                        j["DNSSEC"] = "No"
                try:
                    with open('./DNSSEC.json', 'r') as f:
                        contenu_json = json.load(f)
                except FileNotFoundError:
                    contenu_json = {}
                except json.decoder.JSONDecodeError as e:
                    print(f"Error decoding JSON: {e}")
                    contenu_json = {}
                contenu_json[cle] = j

                with open('./DNSSEC.json', 'w') as f:
                    json.dump(contenu_json, f, indent=4)


"""
if __name__ == "__main__":
    with open('donnees.json', 'r') as f:
        contenu = json.load(f)
        for i in contenu:
            for j in contenu[i]:
                print(j['ip'])
                file = open("DNSSEC_RESOLVERS.txt", "r")
                content = file.read()
                if j['ip'] in file :
                    donnees = {"ip": j['ip'],
                               "orgName": j['orgName'],
                               "lat": j['lat'],
                               "lon": j['lon'],
                               "DoT": j['DoT'],
                               "DoH": j['DoH'],
                               "DNSSEC": "Yes",
                               }
                else:
                    donnees = {"ip": j['ip'],
                               "orgName": j['orgName'],
                               "lat": j['lat'],
                               "lon": j['lon'],
                               "DoT": j['DoT'],
                               "DoH": j['DoH'],
                               "DNSSEC": "No",
                               }
                try:
                    with open('./DNSSEC.json', 'r') as f:
                        contenu = json.load(f)
                except FileNotFoundError:
                    contenu = {}
                except json.decoder.JSONDecodeError as e:
                    print(f"Error decoding JSON: {e}")
                    contenu = {}
                contenu[str(i)] = [donnees]

                with open('./DNSSEC.json', 'w') as f:
                    json.dump(contenu, f, indent=4)
"""