
import psycopg2

# Connection parameters
source_dbname = 'fusion_dashboard'
source_user = 'pi'
source_password = 'fusion@123'  # Replace with the actual password
source_host = '127.0.0.1'  # Change to your PostgreSQL server's host if necessary

target_dbname = 'fusionprod'
target_user = 'fusionuser'
target_password = 'fusion-prod'  # Replace with the actual password
target_host = '127.0.0.1'  # Change to your PostgreSQL server's host if necessary

backup_file = '/home/pi/custompbx/custompbx/database/backup.sql'  # Replace with the path to your backup file

try:
    # Establish connection to the source database
    source_connection = psycopg2.connect(dbname=source_dbname, user=source_user, password=source_password, host=source_host)
    source_cursor = source_connection.cursor()

    # Read the backup file
    with open(backup_file, 'r') as f:
        sql_commands = f.read()

    # Close the backup file
    f.close()

    # Execute the SQL commands from the backup file on the source database
    source_cursor.execute(sql_commands)

    # Commit the changes
    source_connection.commit()

    # Close the cursor and connection to the source database
    source_cursor.close()
    source_connection.close()

    # Establish connection to the target database
    target_connection = psycopg2.connect(dbname=target_dbname, user=target_user, password=target_password, host=target_host)
    target_cursor = target_connection.cursor()

    # Now you can execute SQL queries using the target cursor

    # Example: Query the tables from the target database
    target_cursor.execute("SELECT * FROM pg_catalog.pg_tables WHERE schemaname != 'pg_catalog' AND schemaname != 'information_schema';")

    # Fetch the result
    tables = target_cursor.fetchall()
    print("Tables in the target database:")
    for table in tables:
        print(table)

    # Close the cursor and connection to the target database
    target_cursor.close()
    target_connection.close()

except psycopg2.Error as e:
    print("Error:", e)
