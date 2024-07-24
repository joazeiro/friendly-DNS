import sqlite3

db = sqlite3.connect("dns.db")
cursor = db.cursor()

# WE NEED A COUPLE OF TABLES HERE 
# 1. LOCAL SERVERS
# 2. ALL SERVERS
# 3. LOGS (RECENT CHANGES)
# EVERYTHING ELSE WILL BE GRABBED DIRECTLY FROM THE "API" CALLS

cursor.execute("CREATE TABLE servers(hostname, ipAddress, type)")
cursor.execute("CREATE TABLE logs(hostnameBefore, hostnameAfter, ipAddressBefore, ipAdressAfter, time)")

db.commit()