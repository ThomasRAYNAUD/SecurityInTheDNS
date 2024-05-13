import csv
import json

if __name__ == "__main__":
    with open('../donnees.json', 'r') as f:
        contenu = json.load(f)
    
    new_data = {}
    
    count = 1
    
    for i in contenu:
        for j in contenu[i]:
            ip = j['ip']
            with open('export_ip_doh.csv', 'r') as fichier_csv:
                reader = csv.reader(fichier_csv)
                for row in reader:
                    if row[0] == ip:
                        if row[1] == "EDNS0":
                            eDNS = "eDNS0"
                        elif row[1] == "no padding":
                            eDNS = "No padding"
                        elif row[1] == "other padding":
                            eDNS = "Other padding"
                        
                        # Créer un dictionnaire pour chaque entrée avec les données formatées
                        data_item = {
                            "ip": j['ip'],
                            "orgName": j['orgName'],
                            "lat": j['lat'],
                            "lon": j['lon'],
                            "DoT": j['DoT'],
                            "DoH": j['DoH'],
                            "eDNS": eDNS
                        }
                        
                        # Ajouter le dictionnaire à la clé appropriée dans le nouveau JSON
                        new_data[str(count)] = [data_item]
                        
                        # Incrémenter le compteur
                        count += 1

    # Écrire le nouveau JSON dans un fichier
    with open('nouveau_fichier_json.json', 'w') as json_file:
        json.dump(new_data, json_file, indent=4)
