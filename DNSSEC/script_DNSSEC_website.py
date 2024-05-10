import subprocess
import csv
import concurrent.futures
import matplotlib.pyplot as plt

<<<<<<< HEAD
MAX_THREADS = 10
=======
MAX_THREADS = 100
>>>>>>> f6fecd55fd2b2e21c7fd53bf1040aaa9b0e841f2

def run_dig_command(website, dnssec_web, non_dnssec_web):
    command = f"dig @1.1.1.1 +dnssec {website}"
    try:
        result = subprocess.run(command, shell=True, capture_output=True, timeout = 5)
        indice_début = result.stdout.decode().find("flags:") + len("flag:")
        indice_fin = result.stdout.decode().find(";", indice_début)
        portion = result.stdout.decode()[indice_début : indice_fin].strip()
        if "ad" in portion :
            print("DNSSEC implémenté pour le site web:", website)
            dnssec_web.append(website)
<<<<<<< HEAD

=======
        else :
            print("DNSSEC non implémenté pour le site web: ", website)
            non_dnssec_web.append(website)
>>>>>>> f6fecd55fd2b2e21c7fd53bf1040aaa9b0e841f2

    except subprocess.TimeoutExpired:
        print("Timeout ocurred while executing command for", website)
        print("DNSSEC non implémenté pour le site web: ", website)
        non_dnssec_web.append(website)

    except subprocess.CalledProcessError as e:
        print(f"Error occurred while executing command for {website}: {e}")
        print("DNSSEC non implémenté pour le site web: ", website)


def main():
    dnssec_web = []
    non_dnssec_web = []
    threads = []

    with open("../List/websites.csv", "r", encoding='utf-8') as f :
        reader = csv.reader(f,delimiter = ',')
        with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
            for ligne in reader:
                website = ligne[0]
                if website:
                    thread = executor.submit(run_dig_command, website, dnssec_web, non_dnssec_web, test)
                    threads.append(thread)
            
            concurrent.futures.wait(threads)
            
    labels = ['DNSSEC Implémenté', 'DNSSEC Non Implémenté']
    sizes = [len(dnssec_web), len(non_dnssec_web)]
    colors = ['green', 'red']
    explode = (0.1, 0) 
    plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
    plt.axis('equal') 
    plt.title('Implémentation de DNSSEC')
    plt.show()

if __name__ == "__main__":
    print("Starting script")
    main()