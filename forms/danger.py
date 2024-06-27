import psycopg2

# Establish a connection to the PostgreSQL server
conn = psycopg2.connect(
    host="127.0.0.1",
    database="fusion_dashboard",
    user="pi",
    password="fusion@123",
)

conn.autocommit = True

# Create a cursor object to interact with the database
cursor = conn.cursor()

# Execute the SQL query to drop the database
database_name = "fusion_dashboard"
query = f"DROP DATABASE IF EXISTS {database_name};"
cursor.execute(query)

# Commit the changes to the database
conn.commit()

# Close the cursor and connection
cursor.close()
conn.close()

'''

DROP

DROP DATABASE IF EXISTS fusion_dashboard;

RE-CREATE

sudo -u postgres psql

CREATE DATABASE fusion_dashboard;
CREATE USER pi WITH PASSWORD 'fusion@123';
ALTER ROLE pi SET client_encoding TO 'utf8';
ALTER ROLE pi SET default_transaction_isolation TO 'read committed';
ALTER ROLE pi SET timezone TO 'Europe/Berlin';
GRANT ALL PRIVILEGES ON DATABASE fusion_dashboard TO pi;

'''
