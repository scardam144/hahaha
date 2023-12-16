import sqlite3

conn = sqlite3.connect("car_data.db")
print("openedd database successfully")

conn.execute("INSERT INTO CAR_DETAILS (ID,NAME,COMPANY,CITY,PRICE) \
      VALUES (1, 'COLERA', 'CHEVORLET', 'Texas', 150000.00 )")

conn.execute("INSERT INTO CAR_DETAILS (ID,NAME,COMPANY,CITY,PRICE) \
      VALUES (2, 'NEXON', 'TATA', 'Mumbai', 250000.00 )")

conn.execute("INSERT INTO CAR_DETAILS (ID,NAME,COMPANY,CITY,PRICE) \
      VALUES (3, 'THAR', 'MAHINDRA', 'DELHI', 1500000.00 )")

conn.commit()
print("Records created successfully")
conn.close()
