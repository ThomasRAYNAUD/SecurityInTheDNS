import subprocess

def run_dig_command (ip_address):
    command = f"dig @{ip_address} dnssectest.sidn.nl"
    resultat = subprocess.run(command, shell=True, capture_output=True)
    print ("Sortie Standard :")
    print(resultat.stdout.decode())
    indice_début = resultat.stdout.decode().find("flags:") + len("flag:")
    indice_fin = resultat.stdout.decode().find(";", indice_début)
    portion = resultat.stdout.decode()[indice_début : indice_fin].strip()
    print(portion)
    if "ad" in portion :
        print("\n\n DNSSEC est bien implémenté")


ip_address = "1.1.1.1"
run_dig_command(ip_address)