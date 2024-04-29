import subprocess
import threading

import concurrent.futures
import matplotlib.pyplot as plt

MAX_THREADS = 32

def run_dig_command(ip_address, doh_ips, non_doh_ips):
    command = f"dig @{ip_address} +https"
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=5)
        print("DoH implémenté pour l'adresse IP:", ip_address)
        doh_ips.append(ip_address)
    except subprocess.TimeoutExpired:
        print("Timeout occurred while executing command for", ip_address)
        print("DoH non implémenté pour l'adresse IP:", ip_address)
        non_doh_ips.append(ip_address)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while executing command for {ip_address}: {e}")
        print("DoH non implémenté pour l'adresse IP:", ip_address)

def main():
    doh_ips = []
    non_doh_ips = []
    threads = []

    with open('../List/nameservers-all.txt', 'r') as file:
        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
            for line in file:
                ip_address = line.strip()
                if ip_address:
                    thread = executor.submit(run_dig_command, ip_address, doh_ips, non_doh_ips)
                    threads.append(thread)

            concurrent.futures.wait(threads)

    labels = ['DoH Implémenté', 'DoH Non Implémenté']
    sizes = [len(doh_ips), len(non_doh_ips)]
    colors = ['green', 'red']
    explode = (0.1, 0) 
    plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
    plt.axis('equal') 
    plt.title('Implémentation de DNS-over-HTTPS (DoH)')
    plt.show()

if __name__ == "__main__":
    print("Starting script")
    main()
