import csv
import matplotlib.pyplot as plt

# Initialisation des compteurs
padding_count = 0
no_padding_count = 0

# Lecture du fichier CSV
with open('../capture_dot_filter.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # Analyse du champ dns.opt.code
        if row['dns.opt.code'] == '12':
            padding_count += 1
        else:
            no_padding_count += 1

# Création des données pour l'histogramme
labels = ['Padding', 'No Padding']
counts = [padding_count, no_padding_count]

total_resolvers = padding_count + no_padding_count
percentage_padding = (padding_count / total_resolvers) * 100
percentage_no_padding = (no_padding_count / total_resolvers) * 100

# Création de l'histogramme
colors = ['green', 'red']
plt.bar(labels, counts, color=colors)

# Ajout de titre et d'étiquettes
plt.title('Comparison of Resolver Padding Usage by default with DoT')
plt.xlabel('Padding Usage')
plt.ylabel('Number of Resolvers')

plt.text(labels[0], counts[0], f'{percentage_padding:.2f}%', ha='center', va='bottom')
plt.text(labels[1], counts[1], f'{percentage_no_padding:.2f}%', ha='center', va='bottom')

# Affichage de l'histogramme
plt.show()
