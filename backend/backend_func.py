from backend_init import backend_client

# load average information
def load_average():
    '''load_command = "uptime"
    stdin, stdout, stderr = backend_client.client.exec_command(load_command)

    output = stdout.read().decode().strip()
    load_avg_str = output.split('load average:')[1].strip()
    load_averages = load_avg_str.split(',')

    return load_averages'''

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
