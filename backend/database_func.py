import sqlite3
from database_init import db_client

def what_action(action, hostname, ip_address, type):
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
        return "Invalid Action"

def add_local_server(hostname, ip_address):
    sql_command = "INSERT INTO servers (hostname, ipAddress, type) VALUES (?, ?, ?)"
    type = "local" 
    db_client.cursor.execute(sql_command, (hostname, ip_address, type))

    db_client.db.commit()

def add_all_server(hostname, ip_address):
    sql_command = "INSERT INTO servers (hostname, ipAddress, type) VALUES (?, ?, ?)"
    type = "all" 
    db_client.cursor.execute(sql_command, (hostname, ip_address, type))

    db_client.db.commit()

def remove_local_server(hostname, ip_address):
    sql_command = "DELETE FROM servers (hostname, ipAddress, type) VALUES (?, ?, ?)"
    type = "local" 
    db_client.cursor.execute(sql_command, (hostname, ip_address, type))

    db_client.db.commit()

def remove_all_server(hostname, ip_address):
    sql_command = "DELETE FROM servers (hostname, ipAddress, type) VALUES (?, ?, ?)"
    type = "all" 
    db_client.cursor.execute(sql_command, (hostname, ip_address, type))

    db_client.db.commit()

def new_log_entry(hostname_before, hostname_after, ip_before, ip_after, time):
    sql_command = "INSERT INTO logs (hostnameBefore, hostnameAfter, ipAddressBefore, ipAddressAfter, time) VALUES (?, ?, ?, ?, ?)"
    db_client.cursor.execute(sql_command, (hostname_before, hostname_after, ip_before, ip_after, time))

    db_client.db.commit()

def get_all_servers():
    return db_client.cursor.execute("SELECT * FROM servers WHERE type = 'all'")

def get_local_servers():
    return db_client.cursor.execute("SELECT * FROM servers WHERE type = 'local'")

def get_logs():
    sql_command = "INSERT INTO logs (hostnameBefore, hostnameAfter, ipAddressBefore, ipAddressAfter, time) VALUES (?, ?, ?, ?, ?)"
    db_client.cursor.execute(sql_command, ("test", "test2", "alex1", "alex2", "today"))

    db_client.db.commit()

    return db_client.cursor.execute("SELECT * FROM logs")