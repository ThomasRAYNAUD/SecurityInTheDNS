

import plotly.graph_objects as go
import pandas as pd


# Création d'un DataFrame avec les données
data = {
    'Categories': ['Résolveurs sécurisés', 
                   'Résolveurs non sécurisés'],
    'Percentages': ["15.8", "84.2"]
}
df = pd.DataFrame(data)

# Création du tableau à l'aide de Plotly
fig = go.Figure(data=[go.Table(
    header=dict(values=['Type de résolveur', 'Pourcentage (%)'],
                fill_color='paleturquoise',
                align='left'),
    cells=dict(values=[df['Categories'], df['Percentages']],
               fill_color='lavender',
               align='left'))
])

# Affichage du tableau
fig.show()
