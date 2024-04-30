def get_orgname(ip_address):
    command = f"nslookup {ip_address} | grep 'name =' | awk '{{print $4}}'"
    try:
        result = subprocess.check_output(command, shell=True).decode().strip()
        domain_name = result if result else "Unknown"
        return domain_name
    except Exception as e:
        print(f"Error fetching WHOIS information for {ip_address}: {e}")
        return "Unknown"