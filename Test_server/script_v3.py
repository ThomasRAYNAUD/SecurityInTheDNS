import os
import socket
import dns.resolver
import threading
import matplotlib.pyplot as plt
import requests
import subprocess
import re

def check_server_accessibility(server):
    """
    Vérifie l'accessibilité d'un serveur DNS en effectuant une requête DNS de test.
    """
    try:
        # Configure le résolveur DNS pour une courte durée de timeout
        resolver = dns.resolver.Resolver()
        resolver.timeout = 1
        resolver.lifetime = 1
        resolver.query(server, 'A')  # Effectue une requête DNS de test
        return True  # Le serveur est accessible
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.resolver.NoNameservers):
        # Le serveur ne répond pas ou ne renvoie pas de réponse valide
        return False
    except dns.exception.Timeout:
        # Timeout de la requête DNS
        return False
    except Exception as e:
        # Autres erreurs inattendues
        print(f"Erreur lors de la vérification de l'accessibilité du serveur {server}: {e}")
        return False

def get_dns_server_type(server, server_types):
    """
    Obtient le type de serveur DNS en interrogeant le serveur pour les enregistrements SOA.
    """
    try:
        resolver = dns.resolver.Resolver()
        resolver.timeout = 1
        resolver.lifetime = 1
        response = resolver.query(server, 'SOA')  # Interroge le serveur DNS pour les enregistrements SOA
        
        # Si une réponse est reçue, le serveur est un serveur d'autorité
        if response:
            server_types["Serveur d'autorité"] += 1
        else:
            server_types["Serveur récursif"] += 1  # Sinon, le serveur est probablement récursif
    
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
        server_types["Serveur récursif"] += 1
    except dns.exception.Timeout:
        server_types["Serveur DNS non disponible"] += 1
    except dns.resolver.NoNameservers:
        server_types["Serveur de noms non trouvé"] += 1
    except dns.resolver.NoRootSOA:
        server_types["Serveur racine"] += 1
    except Exception as e:
        print(f"Erreur lors de l'analyse du serveur {server}: {e}")

def process_servers(servers, server_types):
    """
    Traite chaque serveur DNS dans la liste et détermine son type.
    """
    for server in servers:
        server = server.strip()  # Supprime les espaces et les sauts de ligne
        if check_server_accessibility(server):
            get_dns_server_type(server, server_types)
        else:
            server_types["Serveur inaccessible"] += 1  # Incrémente le compteur des serveurs inaccessibles

def use_third_party_services():
    """
    Utilise des services tiers ou des API pour obtenir des informations sur les serveurs DNS.
    """
    # Exemple : Utilisation de l'API DNSViz
    url = "https://dnsviz.net/d/api.sk/dnssec/"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            print("Résultat de l'API DNSViz:")
            print(response.json())  # Affiche la réponse JSON de l'API
        else:
            print("Erreur lors de la requête à l'API DNSViz:", response.status_code)
    except Exception as e:
        print("Erreur lors de l'utilisation de l'API DNSViz:", e)

def analyze_dns_traffic():
    """
    Analyse le trafic DNS en utilisant l'outil Wireshark.
    """
    try:
        subprocess.run(["wireshark"])  # Ouvre l'application Wireshark
    except Exception as e:
        print("Erreur lors de l'ouverture de Wireshark:", e)

def query_dns_servers_directly():
    """
    Interroge directement les serveurs DNS pour obtenir des informations sur leur propriétaire.
    """
    try:
        subprocess.run(["python3", "../who-is/script-whois.py"])  # Exécute le script-whois.py
    except Exception as e:
        print("Erreur lors de l'exécution du script-whois.py:", e)

def analyze_dns_metadata():
    """
    Analyse les options EDNS dans les réponses DNS pour obtenir des informations sur les capacités du serveur DNS.
    """
    print("Analyse des métadonnées DNS")

def analyze_dns_response_content():
    """
    Analyse le contenu des réponses DNS pour identifier des indices sur le type de serveur DNS.
    """
    print("Analyse du contenu des réponses DNS")

def main():
    # Chemin vers le fichier contenant la liste des serveurs DNS
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_name = os.path.join(script_dir, "../List/updated_list/nameservers.txt")
    
    try:
        # Ouvre le fichier contenant les serveurs DNS
        with open(file_name, "r") as file:
            servers = file.readlines()
            
            # Initialise un dictionnaire pour stocker les types de serveurs DNS
            server_types = {
                "Serveur récursif": 0,
                "Serveur racine": 0,
                "Serveur TLD": 0,
                "Serveur d'autorité": 0,
                "Serveur DNS non disponible": 0,
                "Serveur de noms non trouvé": 0,
                "Serveur inaccessible": 0
            }
            
            # Traite chaque serveur DNS dans la liste
            process_servers(servers, server_types)
    
    except FileNotFoundError:
        print(f"Erreur: Le fichier {file_name} n'existe pas")

    # Affiche un histogramme des types de serveurs DNS
    labels = list(server_types.keys())
    values = list(server_types.values())
    plt.bar(labels, values)
    plt.xlabel('Types de serveurs DNS')
    plt.ylabel('Nombre de serveurs')
    plt.title('Répartition des types de serveurs DNSv3')
    plt.show()

    # Utilisation de services tiers
    use_third_party_services()

    # Analyse du trafic DNS
    analyze_dns_traffic()

    # Interrogation directe des serveurs DNS
    query_dns_servers_directly()

    # Analyse des métadonnées DNS
    analyze_dns_metadata()

    # Analyse du contenu des réponses DNS
    analyze_dns_response_content()

if __name__ == "__main__":
    print("Starting script")
    main()
