import dns.query
import dns.message

list_ip = []
with open('../List/nameservers-all.txt', 'r') as file:
    for line in file:
        list_ip.append(line.strip())


i=0
for ip in list_ip:
    try:
        request = dns.message.make_query('google.com', dns.rdatatype.ANY)
        response = dns.query.tls(request, ip)
        print(response)
        i+=1
        if i == 5:
            break
    except:
        print("IPv6")
        i+=1
        if i == 5:
            break



# débugger l'IPv6 qui ne fonctionne pas
# faire un whois pour récupérer qui c'est l'adresse IP