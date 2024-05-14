import json
import matplotlib.pyplot as plt

nb_Cloudflare = 0
nb_Google_server = 0
nb_atnt_server = 0
nb_amazon_server = 0
nb_level3_server = 0
nb_cisco_server = 0
others = 0


if __name__ == "__main__":
    nb_DNSSEC = 0
    with open("../remplirJSON/nellly/DNSSEC.json", 'r') as f:
        contenu = json.load(f)
        for i in contenu:
            for j in contenu[i]:
                if j['DNSSEC'] == "Yes":
                    nb_DNSSEC += 1
                    if j['orgName'] == "Cloudflare, Inc.":
                        nb_Cloudflare += 1
                    elif j['orgName'] == "Google LLC":
                        nb_Google_server += 1
                    elif j['orgName'] == "AT&T Corp.":
                        nb_atnt_server += 1
                    elif j['orgName'] == "Amazon Technologies Inc.":
                        nb_amazon_server += 1
                    elif j['orgName'] == "Level 3 Parent, LLC":
                        nb_level3_server += 1
                    elif j['orgName'] == "Cisco OpenDNS, LLC":
                        nb_cisco_server += 1
                    else :
                        others += 1
    
    labels = ["Cloudflare, Inc.", "Google LLC", "AT&T Corp.", "Amazon Technologies Inc.", "Level 3 Parent, LLC", "Cisco OpenDNS, LLC"]
    sizes = [nb_Cloudflare, nb_Google_server, nb_atnt_server, nb_amazon_server, nb_level3_server, nb_cisco_server]
    pourcentages = [nb_Cloudflare/nb_DNSSEC*100, nb_Google_server/nb_DNSSEC*100, nb_atnt_server/nb_DNSSEC*100, nb_amazon_server/nb_DNSSEC*100, nb_level3_server/nb_DNSSEC*100, nb_cisco_server/nb_DNSSEC*100]
    colors = ['cornflowerblue', 'cornflowerblue','cornflowerblue','cornflowerblue','cornflowerblue','cornflowerblue']

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
