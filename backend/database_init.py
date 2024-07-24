import sqlite3

'''def init_db():
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
        pass'''

class DatabaseInitiator:
    def __init__(self):
        try:
            self.db = sqlite3.connect("dns.db")
            self.cursor = self.db.cursor()

        except:
            pass

        try:
            self.cursor.execute("CREATE TABLE servers(hostname, ipAddress, type)")
            self.cursor.execute("CREATE TABLE logs(hostnameBefore, hostnameAfter, ipAddressBefore, ipAddressAfter, time)")

            self.db.commit()

        except:
            pass

db_client = DatabaseInitiator()
