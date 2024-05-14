import json
import matplotlib.pyplot as plt
import concurrent.futures


MAX_THREADS = 100

def find_org_resolver(resolver, nb_Cloudflare, nb_Google_server, nb_atnt_server, nb_amazon_server, nb_level3_server, nb_cisco_server, others):
    if resolver["DNSSEc"] :
        if resolver['DNSSEC'] == "Yes":
            if resolver['orgName'] == "Cloudflare, Inc.":
                nb_Cloudflare.append(resolver['ip'])
            elif resolver['orgName'] == "Google LLC":
                nb_Google_server.append(resolver['ip'])
            elif resolver['orgName'] == "AT&T Corp.":
                nb_atnt_server.append(resolver['ip'])
            elif resolver['orgName'] == "Amazon Technologies Inc.":
                nb_amazon_server.append(resolver['ip'])
            elif resolver['orgName'] == "Level 3 Parent, LLC":
                nb_level3_server.append(resolver['ip'])
            elif resolver['orgName'] == "Cisco OpenDNS, LLC":
                nb_cisco_server.append(resolver['ip'])
            else :
                others.append(resolver['ip'])
def main():
    threads = []
    nb_Cloudflare = []
    nb_Google_server = []
    nb_atnt_server = []
    nb_amazon_server = []
    nb_level3_server = []
    nb_cisco_server = []
    others = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        with open("../remplirJSON/nellly/DNSSEC.json", 'r') as f:
            contenu = json.load(f)
            for i in contenu:
                thread = executor.submit(find_org_resolver, i, nb_Cloudflare, nb_Google_server, nb_atnt_server, nb_amazon_server, nb_level3_server, nb_cisco_server, others)
                threads.append(thread)
        concurrent.futures.wait(threads)

    labels = ["Cloudflare, Inc.", "Google LLC", "AT&T Corp.", "Amazon Technologies Inc.", "Level 3 Parent, LLC", "Cisco OpenDNS, LLC", "Others"]
    sizes = [len(nb_Cloudflare), len(nb_Google_server), len(nb_atnt_server), len(nb_amazon_server), len(nb_level3_server), len(nb_cisco_server), len(others)]
    total = len(nb_Cloudflare) + len(nb_amazon_server) + len(nb_atnt_server) + len(others) + len(nb_cisco_server) + len(nb_Google_server) + len(nb_level3_server)
    pourcentages = [len(nb_Cloudflare)/total*100, len(nb_Google_server)/total*100, len(nb_atnt_server)/total*100, len(nb_amazon_server)/total*100, len(nb_level3_server)/total*100, len(nb_cisco_server)/total*100, len(others)/total*100]
    colors = ['cornflowerblue', 'cornflowerblue','cornflowerblue','cornflowerblue','cornflowerblue','cornflowerblue', 'cornflowerblue']

    rects = plt.bar(labels, sizes, color=colors)
    plt.ylabel('Nombre de résolveurs')
    plt.title('Organismes des différents résolveurs implémentant DNSSEC')
    i = 0
    for rect in rects:
        height = rect.get_height()
        plt.annotate(f'{pourcentages[i]:.1f}%',
            xy=(rect.get_x() + rect.get_width() / 2, height),
            xytext=(0, 3),  # Décalage de 3 points au-dessus de la barre
            textcoords="offset points",
            ha='center', va='bottom')
        i += 1

    plt.show()

if __name__ == "__main__":
    print("Starting script")
    main()
