import subprocess
import threading
import csv

import concurrent.futures
import matplotlib.pyplot as plt

MAX_THREADS = 100

def run_dig_command(ip_address, website, algo_id):
    command = f"dig +dnssec @{ip_address[:-1]} {website} SOA | grep RRSIG"
    try:
        result = subprocess.run(command, shell=True, capture_output=True, timeout = 10).stdout.decode()
        print(result)
        pass
        if result != "" :            
            print(result)
            id_algo = result.split()[5]
            if id_algo in algo_id:
                algo_id[id_algo] += 1
            elif id_algo == "(for":
                pass
            else:
                algo_id[id_algo] = 1

    except subprocess.TimeoutExpired:
        print("Timeout ocurred while executing command for", website)
        print("DNSSEC non implémenté pour le site web: ", website)
        

    except subprocess.CalledProcessError as e:
        print(f"Error occurred while executing command for {website}: {e}")
        print("DNSSEC non implémenté pour le site web: ", website)


def main():
    algo_id = {}
    threads = []
    with open('../List/updated_list/DNSSEC_IPs.txt', 'r') as file:
        with open("../List/websites.csv", "r", encoding='utf-8') as f :
            reader = csv.reader(f,delimiter = ',')
            with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
                for ip_address in file:
                    for ligne in reader:
                        website = ligne[0]
                        if website:
                            thread = executor.submit(run_dig_command, ip_address, website, algo_id)
                            threads.append(thread)
                    
                concurrent.futures.wait(threads)

    id_names = {"5": "RSA/SHA-1", "3": "DSA/SHA-1", "8": "RSA/SHA-256", "7": "RSASHA1-NSEC3-SHA1","13": "ECDSA/SHA-256", "10": "RSA/SHA-512", "14": "ECDSA/SHA-384", "15": "Ed25519", "16": "Ed448"}


    print("Algo_id : ", algo_id)

    labels = []
    sizes = []
    for key in algo_id.keys():
        labels.append(id_names[key])
        sizes.append(algo_id[key])
    
    total = sum(sizes)
    for i in range(len(sizes)):
        sizes[i] = sizes[i] / total * 100

    for i in range(len(labels)):
        if "SHA-1" in labels[i] or "SHA1" in labels[i]:
            plt.bar(labels[i], sizes[i], color='red')
        elif "SHA-256" in labels[i] or "SHA-512" in labels[i]:
            plt.bar(labels[i], sizes[i], color='green')
        else:
            plt.bar(labels[i], sizes[i], color='blue')
    plt.title('Pourcentages d\'utilisation des algorithmes de chiffrement rencontrés')
    for i in range(len(labels)):
        plt.text(i, sizes[i], str(round(sizes[i],2)), ha='center', va='bottom')
    plt.show()
    
if __name__ == "__main__":
    print("Starting script")
    main()