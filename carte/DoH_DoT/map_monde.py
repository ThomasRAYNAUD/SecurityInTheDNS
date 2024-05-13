import requests
import folium
import json
import subprocess
import re
import time

def main():
    with open('../List/updated_list/nameservers_complet.txt', 'r') as file:
        i=0
        for ip in file:
            i+=1
            ip = ip.strip()
            who = whois(ip)
            traitement_whois(who,i,ip)

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

def traitement_whois(whois_output,i,ip):
    orgName_match = re.search(r'OrgName:\s+([^\n\r]+)', whois_output, re.IGNORECASE)
    orgName = orgName_match.group(1) if orgName_match else "unknown"
    org_match = re.search(r'org:\s+([^\n\r]+)', whois_output, re.IGNORECASE)
    org = org_match.group(1) if org_match else "unknown"

    time.sleep(0.5)  # import time

    api_url = f"http://ip-api.com/json/{ip}"
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        print(data)

        lat = data.get('lat', 'unknown')
        lon = data.get('lon', 'unknown')
        
    else:
        print(f"Failed to fetch IP information for {ip}")
        lat = 'unknown'
        lon = 'unknown'
    #si l'ip est dans le fichier dot.txt
    if ip in open('./DoT.txt').read() : 
        DoT = "Yes"
    else:
        DoT = "No"
    if ip in open('./DoH.txt').read() : 
        DoH = "Yes"
    else:
        DoH = "No"
    
    donnees = {"ip": ip,
               "orgName": orgName,
               "org": org,
               "lat": lat,
               "lon": lon,
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
    
    return "OK"

if __name__ == "__main__":
    main()
    ma_carte = folium.Map(location=[0, 0], zoom_start=2)
    # se balader dans le fichier json
    with open('donnees.json', 'r') as f:
        contenu = json.load(f)
        for i in contenu:
            for j in contenu[i]:
                if j['lat'] != 'unknown' or j['lon'] != 'unknown':
                    ip = j['ip']
                    orgName = j['orgName']
                    org = j['org']
                    lat = j['lat']
                    lon = j['lon']
                    if j['DoT'] == "Yes" and j['DoH'] == "Yes":
                        folium.Marker([lat, lon], popup=f"{ip}\n{orgName}\n{org}\nDoT: Yes\nDoH: Yes", icon=folium.Icon(color='green')).add_to(ma_carte)
                    elif j['DoT'] == "Yes" and j['DoH'] == "No":
                        folium.Marker([lat, lon], popup=f"{ip}\n{orgName}\n{org}\nDoT: Yes\nDoH: No", icon=folium.Icon(color='blue')).add_to(ma_carte)
                    elif j['DoT'] == "No" and j['DoH'] == "Yes":
                        folium.Marker([lat, lon], popup=f"{ip}\n{orgName}\n{org}\nDoT: No\nDoH: Yes", icon=folium.Icon(color='red')).add_to(ma_carte)
                    else:
                        folium.CircleMarker([lat, lon], radius=5, color='yellow', fill=True, fill_color='yellow').add_to(ma_carte)
    # ajouter une légende à ma carte
    legende = """
    <div style="position: fixed; bottom: 50px; left: 50px; width: 150px; height: 120px; background-color: white; border:2px solid grey; z-index:9999; font-size:14px;">
    <p style="margin: 5px">Green: DoT and DoH</p>
    <p style="margin: 5px">Blue: DoT only</p>
    <p style="margin: 5px">Red: DoH only</p>
    <p style="margin: 5px">Yellow: No DoT or DoH</p>
    </div>
    """
    ma_carte.get_root().html.add_child(folium.Element(legende))
    ma_carte.save('carte.html')