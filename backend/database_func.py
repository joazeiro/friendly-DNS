import sqlite3
from database_init import db_client
import datetime

'''def what_action(action, hostname, ip_address, type):
    if action == "add":
        if type == "local":
            add_local_server(hostname, ip_address)
        elif type == "all":
            add_all_server(hostname, ip_address)
        else:
            return "Type not specified"
    elif action == "delete":
        if type == "local":
            remove_local_server(hostname, ip_address)
        elif type == "all":
            remove_all_server(hostname, ip_address)
        else:
            return "Type not specified"
    else:
        return "Invalid Action" '''

def add_local_server(hostname, ip_address):
    sql_command = "INSERT INTO servers (hostname, ipAddress, type) VALUES (?, ?, ?)"
    type = "local" 
    db_client.cursor.execute(sql_command, (hostname, ip_address, type))

    current_time = datetime.datetime.now()
    date = current_time.strftime("%Y-%m-%d %H:%M:%S")
    new_log_entry(hostname, ip_address, "Added", date)

    db_client.db.commit()
    

def add_all_server(hostname, ip_address):
    sql_command = "INSERT INTO servers (hostname, ipAddress, type) VALUES (?, ?, ?)"
    type = "all" 
    db_client.cursor.execute(sql_command, (hostname, ip_address, type))

    current_time = datetime.datetime.now()
    date = current_time.strftime("%Y-%m-%d %H:%M:%S")
    new_log_entry(hostname, ip_address, "Added", date)

    db_client.db.commit()

def remove_local_server(ip_address):
    '''sql_command = "DELETE FROM servers WHERE ipAddress = ? AND type = ?"
    type = "local"
    db_client.cursor.execute(sql_command, (ip_address, type))
    db_client.db.commit()'''

    type = "local"
    sql_hostname = "SELECT hostname from servers WHERE ipAddress = ? AND type = ?"
    grab_hostname = db_client.cursor.execute(sql_hostname, (ip_address, type))

    result = db_client.cursor.fetchone()

    if result:
        grab_hostname = result[0]  # This extracts the hostname from the tuple
    else:
        grab_hostname = "Unknown"  # Default or error handling if no hostname is found

    sql_command = "DELETE FROM servers WHERE ipAddress = ? AND type = ?"
    db_client.cursor.execute(sql_command, (ip_address, type))

    sql_command = "DELETE FROM servers WHERE ipAddress = ? AND type = ?"
    db_client.cursor.execute(sql_command, (ip_address, type))

    current_time = datetime.datetime.now()
    date = current_time.strftime("%Y-%m-%d %H:%M:%S")
    new_log_entry(grab_hostname, ip_address, "Deleted", date)

    db_client.db.commit()

def remove_all_server(ip_address):
    
    type = "all"
    sql_hostname = "SELECT hostname from servers WHERE ipAddress = ? AND type = ?"
    grab_hostname = db_client.cursor.execute(sql_hostname, (ip_address, type))
    result = db_client.cursor.fetchone()

    if result:
        grab_hostname = result[0]  # This extracts the hostname from the tuple
    else:
        grab_hostname = "Unknown"  # Default or error handling if no hostname is found

    sql_command = "DELETE FROM servers WHERE ipAddress = ? AND type = ?"
    db_client.cursor.execute(sql_command, (ip_address, type))

    current_time = datetime.datetime.now()
    date = current_time.strftime("%Y-%m-%d %H:%M:%S")
    new_log_entry(grab_hostname, ip_address, "Deleted", date)

    db_client.db.commit()

def new_log_entry(hostname, ip_address, action, time):

    '''print("Logging new entry:")
    print(f"Hostname: {hostname}, Type: {type(hostname)}")
    print(f"IP Address: {ip_address}, Type: {type(ip_address)}")
    print(f"Action: {action}, Type: {type(action)}")
    print(f"Time: {time}, Type: {type(time)}")'''

    sql_command = "INSERT INTO logs (hostname, ipAddress, action, time) VALUES (?, ?, ?, ?)"
    db_client.cursor.execute(sql_command, (hostname, ip_address, action, time))

    db_client.db.commit()

def get_all_servers():
    return db_client.cursor.execute("SELECT * FROM servers WHERE type = 'all'")

def get_local_servers():
    return db_client.cursor.execute("SELECT * FROM servers WHERE type = 'local'")

def get_logs():
    # sql_command = "INSERT INTO logs (hostname, ipAddress, action, time) VALUES (?, ?, ?, ?)"
    # db_client.cursor.execute(sql_command, ("test", "alex", "Added", "today"))

    # db_client.db.commit()

    return db_client.cursor.execute("SELECT * FROM logs")