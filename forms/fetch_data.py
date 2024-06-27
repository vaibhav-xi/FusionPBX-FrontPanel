import psycopg2
import requests 

connection = psycopg2.connect(
            database="fusionpbx", user='fusionpbx', password='SQeB0pRyzYpXexMDQYvsJOqOBP0', host='127.0.0.1', port= '5432'
        )
        
cursor = connection.cursor()

def active_mins():
    data = ['agent_active_mins', "0511380777712", 
        "all", "06/01/2024", 
        "06/27/2024"]
    
    post_data = {'details': data}
    response = requests.post('http://138.201.188.127:8000/api_req/', data=post_data)
    content = response.content.decode("utf-8")
    
    print(content)

def fetch_agentstatus():
    

    sql_query = """SELECT * FROM v_agentstatus"""

    # Execute the query
    cursor.execute(sql_query)
    result = cursor.fetchall()
    
    print(result)

def get_total_active_time(number, start_time, end_time):
    try:
        # Query to fetch login and logout times for the given number
        cursor.execute("""
            SELECT login_time, logout_time
            FROM v_agentstatus
            WHERE number = %s AND logout_time IS NOT NULL
            AND login_time BETWEEN %s AND %s
        """, (number, start_time, end_time))
        
        records = cursor.fetchall()
        
        total_seconds = 0
        for login_time, logout_time in records:
            # Calculate the difference in seconds
            time_difference = (logout_time - login_time).total_seconds()
            total_seconds += time_difference
        
        # Convert total seconds to hours, minutes, and seconds
        total_time = str(int(total_seconds // 3600)).zfill(2) + ":" + \
                     str(int((total_seconds % 3600) // 60)).zfill(2) + ":" + \
                     str(int(total_seconds % 60)).zfill(2)

        return total_time

    except psycopg2.Error as e:
        print(f"Database error: {e}")
        return None

# total_time = get_total_active_time("0511380777712", "06/01/2024", "06/27/2024")
# print("Total active time:", total_time)

# fetch_agentstatus()

active_mins()

cursor.close()
connection.close()

