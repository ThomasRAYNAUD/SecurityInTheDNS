import csv

def read_ip_file(file_path):
    ip_list = []
    with open(file_path, 'r') as file:
        for line in file:
            ip_address = line.strip()
            ip_list.append(ip_address)
    return ip_list

def read_csv_file(file_path):
    ip_org_map = {}
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            ip_address = row[0]
            org_name = row[3]
            ip_org_map[ip_address] = org_name
    return ip_org_map

def compare_and_write_result(ip_file_path, csv_file_path, output_file_path):
    ip_list = read_ip_file(ip_file_path)
    ip_org_map = read_csv_file(csv_file_path)

    with open(output_file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['IP Address', 'AS Organization'])
        
        for ip_address in ip_list:
            if ip_address in ip_org_map:
                org_name = ip_org_map[ip_address]
                writer.writerow([ip_address, org_name])

if __name__ == "__main__":
    ip_file_path = 'List/updated_list/nameservers_complet.txt'
    csv_file_path = '../nameservers.csv'
    output_file_path = '../as_orgname.csv'
    compare_and_write_result(ip_file_path, csv_file_path, output_file_path)
    print("Comparison and writing completed.")
