import subprocess
import concurrent.futures
import matplotlib.pyplot as plt

MAX_THREADS = 50

def run_dig_command(ip_address, dot_ips, non_dot_ips):
    command = f"echo | openssl s_client -connect {ip_address}:443 | openssl x509 -noout -text"  # 2064       720      tls-probe 8.8.8.8 443           dig @8.8.8.8 +https
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=2) 
        if "Certificate" in result.stdout:
            print(result.stdout)
            dot_ips.append(ip_address)
    except subprocess.TimeoutExpired:
        non_dot_ips.append(ip_address)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while executing command for {ip_address}: {e}")

def main():
    dot_ips = []
    non_dot_ips = []
    threads = []

    with open('../../List/updated_list/nameservers_complet.txt', 'r') as file:
        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
            for line in file:
                ip_address = line.strip()
                if ip_address:
                    thread = executor.submit(run_dig_command, ip_address, dot_ips, non_dot_ips)
                    threads.append(thread)

            concurrent.futures.wait(threads)

    print(f"IP addresses with DoT: {len(dot_ips)}")
    print(dot_ips)
if __name__ == "__main__":
    main()
