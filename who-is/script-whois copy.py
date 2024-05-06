import subprocess
import re

i=0

def get_orgname(ip_address):
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

def get_netname(whois_output):
    netname_match = re.search(r'OrgName:\s+([^\n\r]+)', whois_output, re.IGNORECASE)
    if netname_match:
        return netname_match.group(1)
    else:
        return "NetName non trouvé"

with open('../IP_address/trier_adresses/public_address.txt', 'r') as file:
    for ip in file:
        ip = ip.strip()
        orgname = get_orgname(ip)
        netname = get_netname(orgname)
        if netname != "NetName non trouvé":
            i+=1
            print(f"IP: {ip} - NetName: {netname}")
            
print(f"Nombre d'IP avec NetName trouvé: {i}")