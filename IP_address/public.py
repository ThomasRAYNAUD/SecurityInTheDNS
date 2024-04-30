import ipaddress

def is_private_ip(ip):
    try:
        ip_obj = ipaddress.ip_address(ip)
        return ip_obj.is_private # True si l'adresse IP est privée, False sinon
    except ValueError:
        return True

def filter_private_ips(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    filtered_ips = [line.strip() for line in lines if not is_private_ip(line.strip())] # On filtre les adresses privées (non routables) grâce à la fonction is_private_ip
    return filtered_ips

file_path = "../List/nameservers-all.txt"
filtered_ips = filter_private_ips(file_path)

with open("public_address.txt", 'w') as file:
    for ip in filtered_ips:
        file.write(ip + '\n')

#print("Adresses IP filtrées :")
#for ip in filtered_ips:
#    print(ip)
