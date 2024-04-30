import subprocess
import concurrent.futures
import matplotlib.pyplot as plt

MAX_THREADS = 100

def run_dig_command(ip_address, dot_ips, non_dot_ips):
    command = f"dig @{ip_address} +tls -p 853"
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=5) 
        print("Va tester :", ip_address)
        dot_ips.append(ip_address)
    except subprocess.TimeoutExpired:
        print("Timeout occurred while executing command for", ip_address)
        print("DoT non implémenté pour l'adresse IP:", ip_address)
        non_dot_ips.append(ip_address)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while executing command for {ip_address}: {e}")
        print("DoT non implémenté pour l'adresse IP:", ip_address)

def main():
    dot_ips = []
    non_dot_ips = []
    threads = []

    with open('../List/nameservers-all.txt', 'r') as file:
        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
            for line in file:
                ip_address = line.strip()
                if ip_address:
                    thread = executor.submit(run_dig_command, ip_address, dot_ips, non_dot_ips)
                    threads.append(thread)

            concurrent.futures.wait(threads)

    labels = ['DoT Implémenté', 'DoT Non Implémenté']
    sizes = [len(dot_ips), len(non_dot_ips)]
    colors = ['green', 'red']
    explode = (0.1, 0) 
    plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
    plt.axis('equal') 
    plt.title('Implémentation de DNS-over-TLS (DoT)')
    plt.show()

if __name__ == "__main__":
    print("Starting script")
    main()
