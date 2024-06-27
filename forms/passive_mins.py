import psycopg2

def get_total_time(number, start_time, end_time):
    try:
        
        connection = psycopg2.connect(
            database="fusionpbx", user='fusionpbx', password='SQeB0pRyzYpXexMDQYvsJOqOBP0', host='127.0.0.1', port= '5432'
        )
        
        cursor = connection.cursor()

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
                     
        cursor.close()
        connection.close()

        return [total_seconds, total_time]

    except psycopg2.Error as e:
        return f"Database error: {e}"

