import random

# Chemin vers votre fichier contenant les adresses IP
input_file = "../../List/updated_list/nameservers_complet.txt"

# Chemin vers le nouveau fichier où vous voulez écrire les adresses IP sélectionnées
output_file = "./address.txt"

# Nombre d'adresses IP à sélectionner
num_addresses_to_select = 100

# Lire les adresses IP à partir du fichier
with open(input_file, "r") as file:
    all_addresses = file.readlines()

# Sélectionner 100 adresses IP aléatoires
selected_addresses = random.sample(all_addresses, num_addresses_to_select)

# Écrire les adresses IP sélectionnées dans le nouveau fichier
with open(output_file, "w") as file:
    file.writelines(selected_addresses)
