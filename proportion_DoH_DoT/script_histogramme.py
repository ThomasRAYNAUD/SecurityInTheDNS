import subprocess
import concurrent.futures
import matplotlib.pyplot as plt


with open('DoH.txt', 'r') as file:
    list_DoH = set(file.read().splitlines())

with open('DoT.txt', 'r') as file:
    list_DoT = set(file.read().splitlines())

with open('../List/updated_list/nameservers_complet.txt', 'r') as file:
    list_all = set(file.read().splitlines())

# Adresses uniquement présentes dans la liste A
only_DoH = list_DoH - list_DoT

# Adresses uniquement présentes dans la liste B
only_DoT = list_DoT - list_DoH

# Adresses présentes dans C mais pas dans A ni B
non_securise = list_all - list_DoH - list_DoT

# Adresses présentes à la fois dans A et B
list_DoT_DoH = list_DoH.intersection(list_DoT)

# faire la somme des only_DoH, only_DoT et only_C pour vérifier que la somme est égale à list_all
somme = len(only_DoH) + len(only_DoT) + len(list_DoT_DoH)

# Définition des données
categories = ['Resolvers implementing DoH', 
              'Resolvers implementing DoT',
              'Resolvers implementing DoH and DoT',]
counts = [len(non_securise), len(only_DoT), len(list_DoT_DoH)]

# Calcul des pourcentages
total = sum(counts)
percentages = [count / total * 100 for count in counts]

# Création de l'histogramme
plt.figure(figsize=(10, 6))
bars = plt.bar(categories, percentages, color=['lightblue', 'lightcoral', 'lightgreen'])

# Ajout des pourcentages au-dessus des barres
for bar, percent in zip(bars, percentages):
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f"{percent:.1f}%", 
             ha='center', va='bottom', fontsize=10)


print("DoT :", len(only_DoT))
print("DoH :", len(only_DoH))
print("DoT et DoH :", len(list_DoT_DoH))
print("Non sécurisé :", len(non_securise))
print("Sécurisé :", somme)

plt.xlabel('DNS resolver security')
plt.ylabel('Percentage of DNS resolvers')
plt.title('Comparative analysis: DNS resolver security (DoT and DoH)')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()





























