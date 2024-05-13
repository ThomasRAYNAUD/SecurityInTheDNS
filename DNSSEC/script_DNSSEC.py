import subprocess
import concurrent.futures
import matplotlib.pyplot as plt

MAX_THREADS = 100

def run_dig_command(ip_address, dnssec_ips, non_dnssec_ips):
    command = f"dig @{ip_address} dnssectest.sidn.nl"
    try:
        result = subprocess.run(command, shell=True, capture_output=True, timeout = 2)
        indice_début = result.stdout.decode().find("flags:") + len("flag:")
        indice_fin = result.stdout.decode().find(";", indice_début)
        portion = result.stdout.decode()[indice_début : indice_fin].strip()
        if "ad" in portion :
            print("DNSSEC implémenté pour l'adresse IP:", ip_address)
            dnssec_ips.append(ip_address)
            test +=1
        else :
            print("DNSSEC non implémenté pour l'adresse IP: ", ip_address)
            non_dnssec_ips.append(ip_address)

    except subprocess.TimeoutExpired:
        print("Timeout ocurred while executing command for", ip_address)
        print("DNSSEC non implémenté pour l'adresse IP: ", ip_address)
        non_dnssec_ips.append(ip_address)

    except subprocess.CalledProcessError as e:
        print(f"Error occurred while executing command for {ip_address}: {e}")
        print("DNSSEC non implémenté pour l'adresse IP: ", ip_address)


def main():
    dnssec_ips = []
    non_dnssec_ips = []
    threads = []

    with open('../List/updated_list/nameservers_complet.txt', 'r') as file:
        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
            for line in file:
                ip_address = line.strip()
                if ip_address:
                    thread = executor.submit(run_dig_command, ip_address, dnssec_ips, non_dnssec_ips)
                    threads.append(thread)
            
            concurrent.futures.wait(threads)

    labels = ['DNSSEC Implémenté', 'DNSSEC Non Implémenté']
    sizes = [len(dnssec_ips), len(non_dnssec_ips)]
    total = len(dnssec_ips) + len(non_dnssec_ips)
    pourcentages = [len(dnssec_ips)/total*100, len(non_dnssec_ips)/total*100]
    colors = ['green', 'red']
    rects = plt.bar(labels, sizes, color=colors)
    plt.ylabel('Nombre de résolveurs')
    plt.title('Implémentation de DNSSEC sur les différents résolveurs')
    i = 0
    for rect in rects:
        height = rect.get_height()
        plt.annotate(f'{pourcentages[i]:.1f}%',
            xy=(rect.get_x() + rect.get_width() / 2, height),
            xytext=(0, 3),  # Décalage de 3 points au-dessus de la barre
            textcoords="offset points",
            ha='center', va='bottom')
        i += 1
    plt.show()

if __name__ == "__main__":
    print("Starting script")
    main()