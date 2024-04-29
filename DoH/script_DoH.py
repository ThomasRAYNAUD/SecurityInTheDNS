import subprocess
import threading

import matplotlib.pyplot as plt

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

    with open('../List/nameservers.txt', 'r') as file:
        for line in file:
            ip_address = line.strip()
            if ip_address:
                thread = threading.Thread(target=run_dig_command, args=(ip_address, doh_ips, non_doh_ips))
                thread.start()
                threads.append(thread)

    for thread in threads:
        thread.join()

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
