import sqlite3

def init_db():
    try:
        db = sqlite3.connect("dns.db")
        cursor = db.cursor()

    except:
        pass

    try:
        cursor.execute("CREATE TABLE servers(hostname, ipAddress, type)")
        cursor.execute("CREATE TABLE logs(hostnameBefore, hostnameAfter, ipAddressBefore, ipAdressAfter, time)")

        db.commit()

    except:
        pass
