import csv

def read_padding_file(file_path):
    padding_data = {}
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            ip_address = row[0]
            padding_type = row[1]
            padding_data[ip_address] = padding_type
    return padding_data

def read_info_file(file_path):
    info_data = {}
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            ip_address = row[0]
            name = row[1]
            as_org = row[3]
            country_code = row[4]
            info_data[ip_address] = {'name': name, 'as_org': as_org, 'country_code': country_code}
    return info_data

def compare_and_write_result(padding_file_path, info_file_path, output_file_path):
    padding_data = read_padding_file(padding_file_path)
    info_data = read_info_file(info_file_path)

    with open(output_file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['IP Address', 'Padding Type', 'Name', 'AS Org', 'Country Code'])
        
        for ip_address, padding_type in padding_data.items():
            if ip_address in info_data:
                info = info_data[ip_address]
                writer.writerow([ip_address, padding_type, info['name'], info['as_org'], info['country_code']])

if __name__ == "__main__":
    padding_file_path = '../export_ip_doh.csv'
    info_file_path = '../nameservers.csv'
    output_file_path = 'location_doh.csv'
    compare_and_write_result(padding_file_path, info_file_path, output_file_path)
    print("Comparison and writing completed.")
