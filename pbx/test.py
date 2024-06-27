import psycopg2

connection = psycopg2.connect(
        database="fusionpbx", user='fusionpbx', password='zd9lEhV8hYQ8wl8tjWDJNIurSI', host='127.0.0.1', port= '5432'
    )
    
cursor = connection.cursor()    

query = f"SELECT * FROM v_destinations"

# query = f"DELETE FROM v_agents WHERE pin = '33152'"
    
cursor.execute(query)

result = cursor.fetchall()

# cursor.execute("""
#         SELECT EXISTS (
#             SELECT 1
#             FROM   information_schema.tables 
#             WHERE  table_name = 'v_agents'
#         );
#     """)
    
# table_exists = cursor.fetchone()[0]

# if not table_exists:

#     cursor.execute("""
#             CREATE TABLE v_agents (
#                 id SERIAL PRIMARY KEY,
#                 name VARCHAR(255),
#                 number VARCHAR(255),
#                 pin VARCHAR(255)
#             );
#         """)

#     connection.commit()
    
#     print("TABLE CREATED")
    
# else:
#     print("TABLE EXIST")

# print(table_exists)

print(result)
# connection.commit()

cursor.close()
connection.close()