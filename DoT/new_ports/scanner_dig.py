import subprocess
import json
import concurrent.futures

MAX_THREADS = 40
PORTS_PER_THREAD = 257  # Diviser le nombre total de ports par le nombre de threads

def run_dig_command(ip_address, port_range):
    result = []
    for port in port_range:
        command = f"dig @{ip_address} +tls -p {port}"
        print(f"Port: {port}")
        try:
            output = subprocess.check_output(command, shell=True, text=True, timeout=1)
            if "->>HEADER<<-" in output:
                result.append(port)
        except subprocess.TimeoutExpired:
            continue
        except subprocess.CalledProcessError as e:
            continue
    return ip_address, result

def main(ip_address):
    dot_ips = {}
    non_dot_ips = []
    port_ranges = [(start_port, start_port + PORTS_PER_THREAD) for start_port in range(1, 65536, PORTS_PER_THREAD)]
    futures = [executor.submit(run_dig_command, ip_address, range(start, end)) for start, end in port_ranges] # Créer une liste de futures pour chaque plage de ports
    for future in concurrent.futures.as_completed(futures): # Parcourir les futures dès qu'ils sont terminés
        ip_address, result = future.result()
        if result:
            with open('output.json', 'w') as json_file:
                json.dump({"dot_ips": dot_ips, "non_dot_ips": non_dot_ips}, json_file, indent=4)
            return ip_address, result
    return ip_address, None


if __name__ == "__main__":
    with open('./address.txt', 'r') as file:
        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as executor: 
            for line in file:
                ip_address = line.strip()
                test1, test2 = main(ip_address)
                print(test1, test2)
                

    