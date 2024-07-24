from backend_init import backend_client

# load average information
def load_average():
    load_command = "uptime"
    stdin, stdout, stderr = backend_client.client.exec_command(load_command)

    output = stdout.read().decode().strip()
    load_avg_str = output.split('load average:')[1].strip()
    load_averages = load_avg_str.split(',')

    return load_averages

# uptime info on pretty formatting
def uptime():
    uptime_command = "uptime -p"
    stdin, stdout, stderr = backend_client.client.exec_command(uptime_command)
    output = stdout.read().decode().strip()

    return output
