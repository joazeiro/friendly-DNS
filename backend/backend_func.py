from backend_init import backend_client
import requests
from constants import Constants

# load average information
def load_average():

    load_command = "uptime"
    stdin, stdout, stderr = backend_client.client.exec_command(load_command)

    output = stdout.read().decode().strip()
    load_avg_str = output.split('load average:')[1].strip()
    load_averages = load_avg_str.split(',')

    # Format the load averages as a string without brackets
    formatted_load_averages = ' | '.join(load_averages).strip()
    return formatted_load_averages

# uptime info on pretty formatting
def uptime():
    uptime_command = "uptime -p"
    stdin, stdout, stderr = backend_client.client.exec_command(uptime_command)
    output = stdout.read().decode().strip()

    return output

def grab_system_info():
    
    commands = {
        'cpu': "cat /proc/cpuinfo | grep 'model name' | uniq | cut -d':' -f2",
        'ram': "free -g | awk '/Mem:/ {print $2 \" GB\"}'",  # Adjusted for GB
        'os': "lsb_release -d | cut -f2"  # Adjusted for simple OS version
    }
    output = {}

    for key, command in commands.items():
        stdin, stdout, stderr = backend_client.client.exec_command(command)
        output[key] = stdout.read().decode().strip()
    
    return output

def update_serial_number(file_path):
    # Define the path to the zone files
    forward_file_path = '/etc/bind/db.maria.local'
    reverse_file_path = '/etc/bind/db.100.168.192'

    # Define the commands for extracting, incrementing, and updating the serial number
    extract_serial_command = f"awk '/^@.*IN.*SOA.*ns1.maria.local.*root.maria.local/ {{ getline; print $1 }}' {file_path}"

    # Extract the current serial number
    stdin, stdout, stderr = backend_client.client.exec_command(extract_serial_command)
    current_serial = stdout.read().decode().strip()

    # Increment and update the serial number in the file
    new_serial = str(int(current_serial) + 1)

    increment_serial_command = (
        f"sudo sed -i -e '/^@\\s\\+IN\\s\\+SOA\\s\\+ns1.maria.local\\.\\s\\+root.maria.local\\.\\s\\+(/ "
        f"{{n; s/^[[:space:]]*[0-9]\\+/\t\t\t{new_serial}/}}' {file_path}"
    )

    backend_client.client.exec_command(increment_serial_command)


def add_local_dns(hostname, ip_address):

    # Split the IP address into its octets
    octets = ip_address.split('.')
    
    # Reverse the order of the octets
    reversed_octets = octets[::-1]
    
    # Join the reversed octets back into a string
    reversed_ip = '.'.join(reversed_octets)

    # Define file paths
    forward_file_path = "/etc/bind/db.maria.local"
    reverse_file_path = "/etc/bind/db.100.168.192"

    add_entry_command_forward = (
        f"sudo sed -i '/^@\tIN\tMX\t10\tmail/i {hostname}\tIN\tA\t{ip_address}' {forward_file_path}"
    )

    # Add PTR record to the reverse DNS file
    reverse_ip_last_octet = reversed_ip.split('.')[0]
    add_entry_command_reverse = (
        f"sudo sed -i '/^@\tIN\tNS\tns1.maria.local./a {reverse_ip_last_octet}\tIN\tPTR\t{hostname}.' {reverse_file_path}"
    )

    update_serial_number(forward_file_path)
    update_serial_number(reverse_file_path)
    backend_client.client.exec_command(add_entry_command_forward)
    backend_client.client.exec_command(add_entry_command_reverse)
    backend_client.client.exec_command("sudo rndc reload maria.local")

def remove_local_dns(ip_address):

    # Define file paths
    forward_file_path = "/etc/bind/db.maria.local"
    reverse_file_path = "/etc/bind/db.100.168.192"
    
    # Reverse the IP address to get the format for the PTR record
    reverse_ip = '.'.join(ip_address.split('.')[::-1])
    reverse_ip_last_octet = reverse_ip.split('.')[0]
    
    # Create the pattern to match in both files
    forward_pattern = f"{ip_address}"
    reverse_pattern = f"{reverse_ip_last_octet}"

    # Commands to remove entries
    remove_forward_command = (
        f"sed -i '/{forward_pattern}/d' {forward_file_path}"
    )

    remove_reverse_command = (
        f"sed -i '/{reverse_pattern}/d' {reverse_file_path}"
    )

    update_serial_number(forward_file_path)
    update_serial_number(reverse_file_path)
    backend_client.client.exec_command(remove_forward_command)
    backend_client.client.exec_command(remove_reverse_command)
    backend_client.client.exec_command("sudo rndc reload maria.local")

def get_zone_id(hostname):
        
    url = "https://api.cloudflare.com/client/v4/zones"
    headers = {
        "Authorization": f"Bearer {Constants.API_TOKEN}",
        "Content-Type": "application/json"
    }
    params = {
        "name": hostname
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    zones = response.json()["result"]
    if zones:
        return zones[0]["id"]
    else:
        raise ValueError("Zone not found")

def add_all_dns(hostname, ip_address):
    
    zone_id = get_zone_id(hostname)

    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records"
    headers = {
        "Authorization": f"Bearer {Constants.API_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "type": "A",
        "name": hostname,
        "content": ip_address,
        "ttl": 3600
    }
    
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    
    return response.json()

def get_record_id(hostname):

    zone_id = get_zone_id(hostname)

    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records"
    headers = {
        "Authorization": f"Bearer {Constants.API_TOKEN}",
        "Content-Type": "application/json"
    }
    params = {
        "name": hostname
    }
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    records = response.json()["result"]
    if records:
        return records[0]["id"]
    else:
        raise ValueError("Record not found")

def remove_all_dns(hostname):
    
    zone_id = get_zone_id(hostname)
    record_id = get_record_id(hostname)

    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record_id}"
    headers = {
        "Authorization": f"Bearer {Constants.API_TOKEN}",
        "Content-Type": "application/json"
    }
    response = requests.delete(url, headers=headers)
    if response.status_code == 200:
        print("Record deleted successfully")
    else:
        response.raise_for_status()


