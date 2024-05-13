import subprocess
import json
import re


def whois(ip_address):
    command = f"whois {ip_address}"
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=3)
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        print(f"Timeout expired while fetching WHOIS information for {ip_address}")
        return "Unknown"
    except Exception as e:
        print(f"Error fetching WHOIS information for {ip_address}: {e}")
        return "Unknown"

def traitement_whois(whois_output,i,j):
    orgName_match = re.search(r'org-name:\s+([^\n\r]+)', whois_output, re.IGNORECASE)
    orgName = orgName_match.group(1) if orgName_match else "unknown"
    
    donnees = {"ip": j['ip'],
               "orgName": j['orgName'],
               "lat": j['lat'],
               "lon": j['lon']
               }

    try:
        with open('./donnees.json', 'r') as f:
            contenu = json.load(f)
    except FileNotFoundError:
        contenu = {}
    except json.decoder.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        contenu = {}
    contenu[str(i)] = [donnees]

    with open('./donnees.json', 'w') as f:
        json.dump(contenu, f, indent=4)
    
    return "OK"

with open("../List/updated_list/DNSSEC_RESOLVERS1.txt", 'r') as dnssec_file:
        dnssec_ips = set(dnssec_file.read().splitlines())


if __name__ == "__main__":
    with open('donnees_dnssec.json', 'r') as f:
        contenu = json.load(f)
        for i in contenu:
            for j in contenu[i]:
                print(j['ip'])
                donnees = {"ip": j['ip'],
                               "orgName": j['orgName'],
                               "lat": j['lat'],
                               "lon": j['lon']
                               }
                try:
                    with open('./donnees.json', 'r') as f:
                        contenu = json.load(f)
                except FileNotFoundError:
                    contenu = {}
                except json.decoder.JSONDecodeError as e:
                    print(f"Error decoding JSON: {e}")
                    contenu = {}
                contenu[str(i)] = [donnees]

                with open('./donnees.json', 'w') as f:
                    json.dump(contenu, f, indent=4)