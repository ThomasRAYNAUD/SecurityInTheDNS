import subprocess
import threading

import concurrent.futures
import matplotlib.pyplot as plt

MAX_THREADS = 100

def run_dig_command(ip_address, dnssec_ips, non_dnssec_ips, test):
    command = f"dig @{ip_address} dnssectest.sidn.nl"
    try:
        result = subprocess.run(command, shell=True, capture_output=True, timeout = 5)
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

    with open('../IP_address/public_address_v2.txt', 'r') as file:
        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
            for line in file:
                ip_address = line.strip()
                if ip_address:
                    thread = executor.submit(run_dig_command, ip_address, dnssec_ips, non_dnssec_ips)
                    threads.append(thread)
            
            concurrent.futures.wait(threads)

    labels = ['DNSSEC Implémenté', 'DNSSEC Non Implémenté']
    sizes = [len(dnssec_ips), len(non_dnssec_ips)]
    colors = ['green', 'red']
    explode = (0.1, 0) 
    plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
    plt.axis('equal') 
    plt.title('Implémentation de DNSSEC')
    plt.show()

if __name__ == "__main__":
    print("Starting script")
    main()