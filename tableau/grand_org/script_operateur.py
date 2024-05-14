import subprocess
import json
import re
import plotly.graph_objects as go
import pandas as pd


nb_free_server = 0
nb_free_DoT = 0
nb_free_DoH = 0
nb_free_DoT_DoH = 0
nb_free_non = 0
nb_sfr_server = 0
nb_sfr_DoT = 0
nb_sfr_DoH = 0
nb_sfr_DoT_DoH = 0
nb_sfr_non = 0
nb_orange_server = 0
nb_orange_DoT = 0
nb_orange_DoH = 0
nb_orange_DoT_DoH = 0
nb_orange_non = 0

def get_tls_version(host, port):
    try : 
        command = f"echo | openssl s_client -connect {host}:{port}"
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT).decode("utf-8")
        matches = re.findall(r"New,\s*(TLSv\d\.\d)", output)
        return matches
    except :
        return "unknown"

if __name__ == "__main__":
    with open('donnees.json', 'r') as f:
        contenu = json.load(f)
        for i in contenu:
            for j in contenu[i]:
                if j['orgName'] == "Societe Francaise Du Radiotelephone - SFR SA":
                    nb_sfr_server += 1
                    nb_sfr_DoT += 1 if j['DoT'] == "Yes" and j['DoH'] == "No" else 0
                    nb_sfr_DoH += 1 if j['DoH'] == "Yes" and j['DoT'] == "No" else 0
                    nb_sfr_DoT_DoH += 1 if j['DoT'] == "Yes" and j['DoH'] == "Yes" else 0
                    nb_sfr_non += 1 if j['DoT'] == "No" and j['DoH'] == "No" else 0

                elif j['orgName'].startswith("Orange"):
                    nb_orange_server += 1
                    nb_orange_DoT += 1 if j['DoT'] == "Yes" and j['DoH'] == "No" else 0
                    nb_orange_DoH += 1 if j['DoH'] == "Yes" and j['DoT'] == "No" else 0
                    nb_orange_DoT_DoH += 1 if j['DoT'] == "Yes" and j['DoH'] == "Yes" else 0
                    nb_orange_non += 1 if j['DoT'] == "No" and j['DoH'] == "No" else 0

                elif j['orgName'] == "Free SAS":
                    nb_free_server += 1
                    nb_free_DoT += 1 if j['DoT'] == "Yes" and j['DoH'] == "No" else 0
                    nb_free_DoH += 1 if j['DoH'] == "Yes" and j['DoT'] == "No" else 0
                    nb_free_DoT_DoH += 1 if j['DoT'] == "Yes" and j['DoH'] == "Yes" else 0
                    nb_free_non += 1 if j['DoT'] == "No" and j['DoH'] == "No" else 0



data = {
    'Categories': ['Societe Francaise Du Radiotelephone - SFR', 'Orange', 'Free SAS'], 
    'Nombre_server': [nb_sfr_server,nb_orange_server,nb_free_server],
    'Percentages_DoT': [round(nb_sfr_DoT/nb_sfr_server*100,1),round(nb_orange_DoT/nb_orange_server*100,1),round(nb_free_DoT/nb_free_server*100,1)],
    'Percentages_DoH': [round(nb_sfr_DoH/nb_sfr_server*100,1),round(nb_orange_DoH/nb_orange_server*100,1),round(nb_free_DoH/nb_free_server*100,1)],
    'Percentages_DoT_DoH': [round(nb_sfr_DoT_DoH/nb_sfr_server*100,1),round(nb_orange_DoT_DoH/nb_orange_server*100,1),round(nb_free_DoT_DoH/nb_free_server*100,1)],
    'Percentages_non': [round(nb_sfr_non/nb_sfr_server*100,1),round(nb_orange_non/nb_orange_server*100,1),round(nb_free_non/nb_free_server*100,1)]
    }
df = pd.DataFrame(data)


fig = go.Figure(data=[go.Table(
    header=dict(values=['Organization name', 'Number of resolver', 'Percentage DoT', 'Percentage DoH', 'Percentage DoH and DoT', 'Not secure'],
                fill_color='lightcoral',
                align='left'),
    cells=dict(values=[df['Categories'], df['Nombre_server'], df['Percentages_DoT'], df['Percentages_DoH'], df['Percentages_DoT_DoH'], df['Percentages_non']],
               fill_color='lavender',
               align='left'))
])

# Affichage du tableau
fig.show()
