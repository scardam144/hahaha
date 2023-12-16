import psycopg2
conn = psycopg2.connect(database="car_data",
                        user="root",
                        host='localhost',
                        password="123456",
                        port=5432)
# Open a cursor to perform database operations
cur = conn.cursor()
# Execute a command: create datacamp_courses table
cur.execute("""CREATE TABLE car_details(
            car_id SERIAL PRIMARY KEY,
            car_name VARCHAR (50) UNIQUE NOT NULL,
            car_company VARCHAR (100) NOT NULL,
            car_prize VARCHAR (20) NOT NULL);
            """)
# Make the changes to the database persistent
conn.commit()
# Close cursor and communication with the database
cur.close()
conn.close()
