import sqlite3
from database_init import *

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

def add_local_server():
    cursor.execute()

def add_all_server():
    cursor.execute()

def remove_local_server():
    cursor.execute()

def remove_all_server():
    cursor.execute()

def new_log_entry():
    cursor.execute()

def get_all_servers():
    cursor.execute()

def get_local_servers():
    cursor.execute()

def get_logs():
    cursor.execute()