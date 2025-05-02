import conncli

host='localhost'
user='root'
password='stock'
database='TWSE'

conn = conncli.connect_db(host, user, password, database)
with open('twse.sql', 'r') as file:
    sql_commands = file.read()

cursor = conn.cursor()
for command in sql_commands.split(';'):
    if command.strip():
        cursor.execute(command)
conn.commit()
cursor.close()
conn.close()