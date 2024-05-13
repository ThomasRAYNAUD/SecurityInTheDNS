

import plotly.graph_objects as go
import pandas as pd


# Création d'un DataFrame avec les données
data = {
    'Categories': ['Resolvers implementing DoH', 'Resolvers implementing DoT', 'Resolvers implementing DoH and DoT'], 
    'Percentages': ["4.4", "53.7", "41.9"],
    'Number': ["67", "811", "633"]
}
df = pd.DataFrame(data)

# Création du tableau à l'aide de Plotly
fig = go.Figure(data=[go.Table(
    header=dict(values=['Resolver type', 'Percentage (%)', 'Number of resolvers'],
                fill_color='lightcoral',
                align='left'),
    cells=dict(values=[df['Categories'], df['Percentages'], df['Number']],
               fill_color='lavender',
               align='left'))
])

# Affichage du tableau
fig.show()
