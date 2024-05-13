import csv
import json

if __name__ == "__main__":
    with open('./donnees.json', 'r') as f:
        contenu = json.load(f)
    
    new_data = {}
    
    count = 1
    
    for i in contenu:
        for j in contenu[i]:
            ip = j['ip']
            with open('./as_orgname.csv', 'r') as fichier_csv:
                reader = csv.reader(fichier_csv)
                for row in reader:
                    if row[0] == ip:
                        data_item = {
                            "ip": j['ip'],
                            "orgName": row[1],
                            "lat": j['lat'],
                            "lon": j['lon'],
                            "DoT": j['DoT'],
                            "DoH": j['DoH']
                        }
                        
                        new_data[str(count)] = [data_item]
                        count += 1

    with open('good_orgName.json', 'w') as json_file:
        json.dump(new_data, json_file, indent=4)
