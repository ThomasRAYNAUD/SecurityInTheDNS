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
               "lon": j['lon'],
               "DoT": j['DoT'],
               "DoH": j['DoH']
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

with open("../DoT.txt", "r") as dot_file:
        dot_ips = set(dot_file.read().splitlines())

with open("../DoH.txt", "r") as doh_file:
        doh_ips = set(doh_file.read().splitlines())


if __name__ == "__main__":
    with open('donnees.json', 'r') as f:
        contenu = json.load(f)
        for i in contenu:
            for j in contenu[i]:
                print(j['ip'])
                if j['ip'] in dot_ips :
                    DoT = "Yes"
                else:
                    DoT = "No"
                if j['ip'] in doh_ips :
                    DoH = "Yes"
                else: 
                    DoH = "No"
                donnees = {"ip": j['ip'],
                               "orgName": j['orgName'],
                               "lat": j['lat'],
                               "lon": j['lon'],
                               "DoT": DoT,
                               "DoH": DoH
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