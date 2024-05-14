import json
import matplotlib.pyplot as plt


if __name__ == "__main__":
    nb_Cloudflare = 0
    nb_high = 0
    nb_nucdn = 0
    nb_level3_server = 0
    nb_nextdns_server = 0
    nb_DNSSEC = 0
    nb_akamai = 0
    nb_comcast = 0

    with open("../remplirJSON/nellly/DNSSEC.json", 'r') as f:
        contenu = json.load(f)
        for i in contenu:
            for j in contenu[i]:
                if j['DNSSEC'] == "Yes":
                    nb_DNSSEC += 1
                    if j['orgName'] == "CLOUDFLARENET":
                        nb_Cloudflare += 1
                    elif j['orgName'] == "Hi-Tec Enterprise":
                        nb_high += 1
                    elif j['orgName'] == "NUCDN":
                        nb_nucdn+= 1
                    elif j['orgName'].startswith("Akamai"):
                        nb_akamai+= 1
                    elif j['orgName'] == "UUNET":
                        nb_level3_server += 1
                    elif j['orgName'] == "nextdns, Inc.":
                        nb_nextdns_server += 1
                    elif j['orgName'].startswith("COMCAST"):
                        nb_comcast += 1 
    
    labels = ["Cloudflare, Inc.", "nextdns","nucdn","Akamai", "COMCAST","Hi-Tec Enterprise","UUNET"]
    sizes = [nb_Cloudflare, nb_nextdns_server, nb_nucdn, nb_akamai, nb_comcast, nb_high, nb_level3_server]
    pourcentages = [nb_Cloudflare/nb_DNSSEC*100, nb_nextdns_server/nb_DNSSEC*100, nb_nucdn/nb_DNSSEC*100,nb_akamai/nb_DNSSEC*100, nb_comcast/nb_DNSSEC*100,nb_high/nb_DNSSEC*100,nb_level3_server/nb_DNSSEC*100]
    colors = ['cornflowerblue', 'cornflowerblue','cornflowerblue','cornflowerblue','cornflowerblue','cornflowerblue','cornflowerblue','cornflowerblue','cornflowerblue']

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
