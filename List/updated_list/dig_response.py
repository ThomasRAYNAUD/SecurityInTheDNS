import subprocess
from concurrent.futures import ThreadPoolExecutor

MAX_THREADS = 200

def reponse(ip):
    command = f"dig @{ip}"
    print(f"Checking {ip}")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=4)
        return False
    except subprocess.TimeoutExpired:
        return True
    except subprocess.CalledProcessError as e:
        return True

def filter_private_ips(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    filtered_ips = []
    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        futures = [executor.submit(reponse, line.strip()) for line in lines]
        for future, line in zip(futures, lines):
            if not future.result():
                filtered_ips.append(line.strip())

    return filtered_ips

file_path = "./nameservers.txt"
filtered_ips = filter_private_ips(file_path)
i=0
with open("./nameservers_complet.txt", 'w') as file:
    for ip in filtered_ips:
        i+=1
        file.write(ip + "\n")