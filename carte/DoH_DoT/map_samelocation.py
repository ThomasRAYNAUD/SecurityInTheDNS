import folium
from folium.plugins import MarkerCluster
import json

v = 0

if __name__ == "__main__":
    ma_carte = folium.Map(location=[0, 0], zoom_start=2)
    
    # Création d'un groupe de clusters de marqueurs
    marker_cluster = MarkerCluster().add_to(ma_carte)
    
    with open('donnees.json', 'r') as f:
        contenu = json.load(f)
        for i in contenu:
            for j in contenu[i]:
                if j['lat'] != 'unknown' or j['lon'] != 'unknown':
                    ip = j['ip']
                    orgName = j['orgName']
                    lat = j['lat']
                    lon = j['lon']
                    if j['DoT'] == "Yes" and j['DoH'] == "Yes":
                        folium.Marker([lat, lon], popup=f"{ip}\n{orgName}\nDoT: Yes\nDoH: Yes", icon=folium.Icon(color='green')).add_to(marker_cluster)
                    elif j['DoT'] == "Yes" and j['DoH'] == "No":
                        folium.Marker([lat, lon], popup=f"{ip}\n{orgName}\nDoT: Yes\nDoH: No", icon=folium.Icon(color='blue')).add_to(marker_cluster)
                    elif j['DoT'] == "No" and j['DoH'] == "Yes":
                        folium.Marker([lat, lon], popup=f"{ip}\n{orgName}\nDoT: No\nDoH: Yes", icon=folium.Icon(color='red')).add_to(marker_cluster)
                    else:
                        folium.CircleMarker([lat, lon], radius=5, color='yellow', fill=True,popup=f"{ip}\n{orgName}\nDoT: No\nDoH: No", fill_color='yellow').add_to(marker_cluster)
                else:
                    v += 1

                    
    legende = f"""
    <div style="position: fixed; bottom: 50px; left: 50px; width: 200px; background-color: rgba(255, 255, 255, 0.8); border-radius: 10px; box-shadow: 0px 0px 5px 0px rgba(0,0,0,0.75); z-index: 9999; font-family: Arial, sans-serif; font-size: 14px; padding: 10px;">
        <h3 style="margin-bottom: 10px; color: #333;">Legend</h3>
        <div style="margin-bottom: 5px;">
            <span style="display: inline-block; width: 12px; height: 12px; background-color: rgb(112, 173, 37) ; border-radius: 50%; margin-right: 5px;"></span> DoT and DoH
        </div>
        <div style="margin-bottom: 5px;">
            <span style="display: inline-block; width: 12px; height: 12px; background-color: rgb(54, 161, 208); border-radius: 50%; margin-right: 5px;"></span> DoT only
        </div>
        <div style="margin-bottom: 5px;">
            <span style="display: inline-block; width: 12px; height: 12px; background-color: rgb(204, 62, 42); border-radius: 50%; margin-right: 5px;"></span> DoH only
        </div>
        <div>
            <span style="display: inline-block; width: 12px; height: 12px; background-color: rgb(248, 248, 0); border-radius: 50%; margin-right: 5px;"></span> No DoT or DoH
        </div>
        <div style="margin-top: 10px; color: #888;">Number of resolvers without coordinates: {v}</div>
        <div style="margin-top: 10px; color: #888;">Total number of resolvers: 9696</div>
    </div>
    """
    ma_carte.get_root().html.add_child(folium.Element(legende))
    ma_carte.save('map_samelocationDoHDoT.html')
