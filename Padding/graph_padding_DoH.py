import csv
import matplotlib.pyplot as plt
import re

# Initialisation des compteurs
edns0_padding_count = 0
other_padding_count = 0
no_padding_count = 0

# Lecture du fichier CSV
with open('../capture_doh_padding.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # Analyse du champ dns.opt.code
        if row['dns.opt.code'] == '12':
            if (bool(re.search(r'468$', row['http2.length']))|(row['http2.length']=='0')):
                edns0_padding_count += 1
            else:
                other_padding_count += 1
        else:
            no_padding_count += 1

# Création des données pour l'histogramme
labels = ['EDNS(0) Recommended Padding', 'Other Padding', 'No Padding']
counts = [edns0_padding_count, other_padding_count, no_padding_count]

total_resolvers = edns0_padding_count + other_padding_count + no_padding_count
percentage_ends0_padding = (edns0_padding_count / total_resolvers) * 100
percentage_other_padding = (other_padding_count / total_resolvers) * 100
percentage_no_padding = (no_padding_count / total_resolvers) * 100

# Création de l'histogramme
plt.figure(figsize=(9, 6))
colors = ['green', 'yellow', 'red']
plt.bar(labels, counts, color=colors)

# Ajout de titre et d'étiquettes
plt.title('Comparison of Resolver Padding Usage when requests are padded with DoH')
plt.xlabel('Padding Usage')
plt.ylabel('Number of Resolvers')

plt.text(labels[0], counts[0], f'{percentage_ends0_padding:.2f}%', ha='center', va='bottom')
plt.text(labels[1], counts[1], f'{percentage_other_padding:.2f}%', ha='center', va='bottom')
plt.text(labels[2], counts[2], f'{percentage_no_padding:.2f}%', ha='center', va='bottom')

# Affichage de l'histogramme
plt.show()
