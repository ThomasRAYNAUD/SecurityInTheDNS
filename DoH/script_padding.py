import subprocess
import concurrent.futures
import matplotlib.pyplot as plt
import re

MAX_THREADS = 100
count = 0

def run_dig_command(ip_address):
    global count
    command = f"export SSLKEYLOGFILE=/home/vincent/sslkeyfile && dig +tls @{ip_address} google.com"
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=5)
        print(f"Test :", ip_address)
        count+=1
        """if result.stderr:
            keys = re.findall(r"\s+(\w+)\s+(\w+)\s+(\w+)", result.stderr)
            formatted_keys = [' '.join(key) for key in keys]
            #print(formatted_keys)
            # Exporter les clés dans le fichier sslkeyfile
            with open('/home/vincent/sslkeyfile', 'a') as f:
                for key in formatted_keys:
                    f.write(key + '\n')"""
    except subprocess.TimeoutExpired:
        print("Timeout occurred while executing command for", ip_address)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while executing command for {ip_address}: {e}")


def main():
    threads = []
    with open('../List/updated_list/nameservers_complet.txt', 'r') as file:
        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
            for line in file:
                ip_address = line.strip()
                if ip_address:
                    thread = executor.submit(run_dig_command, ip_address)
                    threads.append(thread)

            concurrent.futures.wait(threads)

if __name__ == "__main__":
    print("Starting script")
    main()
    print("Capture DNS terminée")
    print(f"{count} résolveurs implémentent DoT")
