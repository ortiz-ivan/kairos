import sqlite3

conn = sqlite3.connect(r"C:\Users\ASUS\AppData\Roaming\Kairos\datos\kairos.db")
c = conn.cursor()
c.execute("SELECT username, nombre, rol FROM usuarios")
usuarios = c.fetchall()
print("Usuarios:")
for u in usuarios:
    print(f"  - {u[0]} ({u[1]}) - {u[2]}")
conn.close()
