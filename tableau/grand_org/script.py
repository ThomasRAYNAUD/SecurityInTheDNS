import subprocess
import json
import re
import plotly.graph_objects as go
import pandas as pd



nb_Cloudflare_server = 0
nb_Cloudflare_DoT = 0
nb_Cloudflare_DoH = 0
nb_Cloudflare_DoT_DoH = 0
nb_Cloudflare_non = 0
nb_Google_server = 0
nb_Google_DoT = 0
nb_Google_DoH = 0
nb_Google_DoT_DoH = 0
nb_Google_non = 0
nb_atnt_server = 0
nb_atnt_DoT = 0
nb_atnt_DoH = 0
nb_atnt_DoT_DoH = 0
nb_atnt_non = 0
nb_amazon_server = 0
nb_amazon_DoT = 0
nb_amazon_DoH = 0
nb_amazon_DoT_DoH = 0
nb_amazon_non = 0
nb_level3_server = 0
nb_level3_DoT = 0
nb_level3_DoH = 0
nb_level3_DoT_DoH = 0
nb_level3_non = 0
nb_cisco_server = 0
nb_cisco_DoT = 0
nb_cisco_DoH = 0
nb_cisco_DoT_DoH = 0
nb_cisco_non = 0

def get_tls_version(host, port):
    try : 
        command = f"echo | openssl s_client -connect {host}:{port}"
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT).decode("utf-8")
        matches = re.findall(r"New,\s*(TLSv\d\.\d)", output)
        return matches
    except :
        return "unknown"

if __name__ == "__main__":
    nb_Cloudflare = 0
    with open('donnees.json', 'r') as f:
        contenu = json.load(f)
        for i in contenu:
            for j in contenu[i]:
                if j['orgName'] == "CLOUDFLARENET":
                    nb_Cloudflare_server += 1
                    nb_Cloudflare_DoT += 1 if j['DoT'] == "Yes" and j['DoH'] == "No" else 0
                    nb_Cloudflare_DoH += 1 if j['DoH'] == "Yes" and j['DoT'] == "No" else 0
                    nb_Cloudflare_DoT_DoH += 1 if j['DoT'] == "Yes" and j['DoH'] == "Yes" else 0
                    nb_Cloudflare_non += 1 if j['DoT'] == "No" and j['DoH'] == "No" else 0

                elif j['orgName'] == "GOOGLE":
                    nb_Google_server += 1
                    nb_Google_DoT += 1 if j['DoT'] == "Yes" and j['DoH'] == "No" else 0
                    nb_Google_DoH += 1 if j['DoH'] == "Yes" and j['DoT'] == "No" else 0
                    nb_Google_DoT_DoH += 1 if j['DoT'] == "Yes" and j['DoH'] == "Yes" else 0
                    nb_Google_non += 1 if j['DoT'] == "No" and j['DoH'] == "No" else 0
                
                elif j['orgName'] == "AT&T Corp.":
                    nb_atnt_server += 1
                    nb_atnt_DoT += 1 if j['DoT'] == "Yes" and j['DoH'] == "No" else 0
                    nb_atnt_DoH += 1 if j['DoH'] == "Yes" and j['DoT'] == "No" else 0
                    nb_atnt_DoT_DoH += 1 if j['DoT'] == "Yes" and j['DoH'] == "Yes" else 0
                    nb_atnt_non += 1 if j['DoT'] == "No" and j['DoH'] == "No" else 0
                    
                elif j['orgName'] == "Amazon Technologies Inc.":
                    nb_amazon_server += 1
                    nb_amazon_DoT += 1 if j['DoT'] == "Yes" and j['DoH'] == "No" else 0
                    nb_amazon_DoH += 1 if j['DoH'] == "Yes" and j['DoT'] == "No" else 0
                    nb_amazon_DoT_DoH += 1 if j['DoT'] == "Yes" and j['DoH'] == "Yes" else 0
                    nb_amazon_non += 1 if j['DoT'] == "No" and j['DoH'] == "No" else 0
                    
                elif j['orgName'] == "Level 3 Parent, LLC":
                    nb_level3_server += 1
                    nb_level3_DoT += 1 if j['DoT'] == "Yes" and j['DoH'] == "No" else 0
                    nb_level3_DoH += 1 if j['DoH'] == "Yes" and j['DoT'] == "No" else 0
                    nb_level3_DoT_DoH += 1 if j['DoT'] == "Yes" and j['DoH'] == "Yes" else 0
                    nb_level3_non += 1 if j['DoT'] == "No" and j['DoH'] == "No" else 0
                    
                elif j['orgName'] == "Cisco OpenDNS, LLC":
                    nb_cisco_server += 1
                    nb_cisco_DoT += 1 if j['DoT'] == "Yes" and j['DoH'] == "No" else 0
                    nb_cisco_DoH += 1 if j['DoH'] == "Yes" and j['DoT'] == "No" else 0
                    nb_cisco_DoT_DoH += 1 if j['DoT'] == "Yes" and j['DoH'] == "Yes" else 0
                    nb_cisco_non += 1 if j['DoT'] == "No" and j['DoH'] == "No" else 0



data = {
    'Categories': ['Cloudflare, Inc.', 'Google LLC', 'AT&T Corp.', 'Amazon Technologies Inc.', 'Level 3 Parent, LLC', 'Cisco OpenDNS, LLC'], 
    'Nombre_server': [nb_Cloudflare_server,nb_Google_server,nb_atnt_server,nb_amazon_server,nb_level3_server,nb_cisco_server],
    'Percentages_DoT': [round(nb_Cloudflare_DoT/nb_Cloudflare_server*100,1),round(nb_Google_DoT/nb_Google_server*100,1),round(nb_atnt_DoT/nb_atnt_server*100,1),round(nb_amazon_DoT/nb_amazon_server*100,1),round(nb_level3_DoT/nb_level3_server*100,1),round(nb_cisco_DoT/nb_cisco_server*100,1)],
    'Percentages_DoH': [round(nb_Cloudflare_DoH/nb_Cloudflare_server*100,1),round(nb_Google_DoH/nb_Google_server*100,1),round(nb_atnt_DoH/nb_atnt_server*100,1),round(nb_amazon_DoH/nb_amazon_server*100,1),round(nb_level3_DoH/nb_level3_server*100,1),round(nb_cisco_DoH/nb_cisco_server*100,1)],
    'Percentages_DoT_DoH': [round(nb_Cloudflare_DoT_DoH/nb_Cloudflare_server*100,1),round(nb_Google_DoT_DoH/nb_Google_server*100,1),round(nb_atnt_DoT_DoH/nb_atnt_server*100,1),round(nb_amazon_DoT_DoH/nb_amazon_server*100,1),round(nb_level3_DoT_DoH/nb_level3_server*100,1),round(nb_cisco_DoT_DoH/nb_cisco_server*100,1)],
    'Percentages_non': [round(nb_Cloudflare_non/nb_Cloudflare_server*100,1),round(nb_Google_non/nb_Google_server*100,1),round(nb_atnt_non/nb_atnt_server*100,1),round(nb_amazon_non/nb_amazon_server*100,1),round(nb_level3_non/nb_level3_server*100,1),round(nb_cisco_non/nb_cisco_server*100,1)]
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
