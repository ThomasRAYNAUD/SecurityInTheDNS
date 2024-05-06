import subprocess
import concurrent.futures
import matplotlib.pyplot as plt

MAX_THREADS = 100

def verifDNSover(ip_address, doh_ips, dot_ips):
    runDoH(ip_address, doh_ips)
    runDoT(ip_address, dot_ips)


def runDoH(ip_address, doh_ips):
    command = f"dig @{ip_address} +https -p 443" # obligé de forcer le port ? J'ai peur que tls peut intérroger https, à voir
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=3)
        if "->>HEADER<<-" in result.stdout:
            print("DoH implémenté pour l'adresse IP:", ip_address)
            doh_ips.append(ip_address)
    except subprocess.TimeoutExpired:
        print("DoH non implémenté pour l'adresse IP:", ip_address)
    except subprocess.CalledProcessError as e:
        print(f"Une erreur est apparue lors de l'exécution de la commande pour {ip_address}: {e}")

def runDoT(ip_address, dot_ips):
    command = f"dig @{ip_address} +tls -p 853"
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=3) 
        if "->>HEADER<<-" in result.stdout:
            print("DoT implémenté pour l'adresse IP:", ip_address)
            dot_ips.append(ip_address)
    except subprocess.TimeoutExpired:
        print("DoT non implémenté pour l'adresse IP:", ip_address)
    except subprocess.CalledProcessError as e:
        print(f"Une erreur est apparue lors de l'exécution de la commande pour {ip_address}: {e}")

def main():
    doh_ips = []
    dot_ips = []
    threads = []

    with open('../List/updated_list/nameservers_complet.txt', 'r') as file:
        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
            for line in file:
                ip_address = line.strip()
                if ip_address:
                    thread = executor.submit(verifDNSover, ip_address, doh_ips, dot_ips)
                    threads.append(thread)

            concurrent.futures.wait(threads)
    return doh_ips, dot_ips

if __name__ == "__main__":
    print("Starting script")
    doh_ips, dot_ips = main()
    with open("./DoH.txt", 'w') as file:
        for ip in doh_ips:
            file.write(ip + "\n")
    with open("./DoT.txt", 'w') as file:
        for ip in dot_ips:
            file.write(ip + "\n")

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
uniquement_C = list_all - list_DoH - list_DoT

# Adresses présentes à la fois dans A et B
list_DoT_DoH = list_DoH.intersection(list_DoT)

# Définition des données
categories = ['Serveurs mettant uniquement en place DoH', 
              'Serveurs mettant uniquement en place DoT', 
              'Serveurs mettant en place DoT et DoH',
              'Serveurs qui ne mettent pas en place DoT et DoH']
counts = [len(only_DoH), len(only_DoT), len(list_DoT_DoH), len(uniquement_C)]

# Création de l'histogramme
plt.figure(figsize=(10, 6))
bars = plt.bar(categories, counts, color=['lightcoral', 'lightskyblue', 'lightgreen', 'gold'])

# Ajout des chiffres exacts au-dessus des barres sinon ne pas mettre pour avoir des % ages
for bar, count in zip(bars, counts):
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), str(count), 
             ha='center', va='bottom', fontsize=10)

plt.xlabel('Présences ou pas de DoT et DoH')
plt.ylabel('Nombre d\'adresses IP')
plt.title('Répartition des adresses IP')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()





























