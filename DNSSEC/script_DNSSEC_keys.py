import subprocess
import threading
import csv

import concurrent.futures
import matplotlib.pyplot as plt

MAX_THREADS = 100

def run_dig_command(ip_address, website, algo_id):
    command = f"dig +dnssec @{ip_address[:-1]} {website} | grep RRSIG"
    try:
        result = subprocess.run(command, shell=True, capture_output=True, timeout = 2)
        if result.stdout.decode() == "" :
            print(f"DNSSEC non implémenté pour le site web: {website}")
        else :
            print(f"DNSSEC implémenté pour le site web: {website}")
            print(f"resultat : {result.stdout.decode()}")
            id_algo = result.stdout.decode().split()[5]
            print(f"id du chiffrement utilisé : {id_algo}")
            algo_id[id_algo] += 1

    except subprocess.TimeoutExpired:
        print("Timeout ocurred while executing command for", website)
        print("DNSSEC non implémenté pour le site web: ", website)
        

    except subprocess.CalledProcessError as e:
        print(f"Error occurred while executing command for {website}: {e}")
        print("DNSSEC non implémenté pour le site web: ", website)


def main():
    algo_id = {"5": 0, "3": 0, "8": 0, "13": 0, "10": 0, "14": 0, "15": 0, "16": 0}
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
          
    labels = ["RSA/SHA-1", "DSA/SHA-1", "RSA/SHA-256", "ECDSA/SHA-256", "RSA/SHA-512", "ECDSA/SHA-384", "Ed25519", "Ed448"]
    sizes = [algo_id["5"], algo_id["3"], algo_id["8"], algo_id["13"], algo_id["10"], algo_id["14"], algo_id["15"], algo_id["16"]]
    colors = ['green', 'red', 'blue', 'yellow', 'purple', 'orange', 'pink', 'brown']
    
    plt.bar(labels, sizes, color=colors)
    plt.title('Parts des algorithmes de chiffrement utilisés pour DNSSEC')
    plt.show()
    
if __name__ == "__main__":
    print("Starting script")
    main()