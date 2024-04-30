import whois
import time
def get_orgname(ip_address):
    try:
        domain = whois.whois(ip_address)
        domain_name = domain.domain_name if domain.domain_name else "Unknown"
        return domain_name
    except Exception as e:
        #print(f"Error fetching WHOIS information for {ip_address}: {e}")
        return "Unknown"

with open('../IP_address/public_address.txt', 'r') as file:
    for ip in file:
        if ip == '\n':
            continue
        orgname = get_orgname(ip)
        print(f"OrgName: {orgname}")