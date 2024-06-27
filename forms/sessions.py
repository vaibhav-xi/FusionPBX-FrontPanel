from bs4 import BeautifulSoup

def queue_session(queueurl, session):
    response = session.get(queueurl, verify=False)
    
    SessionValue = ""
    SessionKey = ""
    
    if response.status_code == 200 or response.status_code == 201:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        title = soup.title
        
        print("TITLE: ", title)
        
        # Find the form with name "login"
        call_center_form = soup.find('form', attrs={'name': 'frm'})
        
        # Check if the login form exists
        if call_center_form:
            # Find all input fields within the form
            input_fields = call_center_form.find_all('input')
            
            # Print the input fields along with their names and values
            for input_field in input_fields:
                field_name = input_field.get('name')
                field_value = input_field.get('value')
                
                if field_name and field_value:
                    
                    # Update session_key and session_value
                    if len(field_name) > 10:
                        SessionKey = field_name
                    if len(field_value) > 10:
                        SessionValue = field_value
                        
            print("Queue: ", SessionKey, SessionValue)
                
            return SessionKey, SessionValue
    else:
        print("Failed to retrieve the web page. Status code:", response.status_code)
        return "Error"
    
def moh_session(url, session, form_name):
    response = session.get(url, verify=False)
    
    SessionValue = ""
    SessionKey = ""
    
    if response.status_code == 200 or response.status_code == 201:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        title = soup.title
        
        print("TITLE: ", title)
        
        # Find the form with name "login"
        moh_form = soup.find('form', attrs={'id': form_name})
        
        # Check if the login form exists
        if moh_form:
            # Find all input fields within the form
            input_fields = moh_form.find_all('input')
            
            # Print the input fields along with their names and values
            for input_field in input_fields:
                field_name = input_field.get('name')
                field_value = input_field.get('value')
                
                if field_name and field_value:
                    
                    # Update session_key and session_value
                    if len(field_name) > 10:
                        SessionKey = field_name
                    if len(field_value) > 10:
                        SessionValue = field_value
                        
            print("MOH Session: ", SessionKey, SessionValue)
                
            return SessionKey, SessionValue
    else:
        print("Failed to retrieve the web page. Status code:", response.status_code)
        return "Error"
    
def conference_session(url, session, form_name):
    response = session.get(url, verify=False)
    
    SessionValue = ""
    SessionKey = ""
    
    if response.status_code == 200 or response.status_code == 201:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        title = soup.title
        
        print("TITLE: ", title)
        
        # Find the form with name "login"
        conference_form = soup.find('form', attrs={'name': form_name})
        
        # Check if the login form exists
        if conference_form:
            # Find all input fields within the form
            input_fields = conference_form.find_all('input')
            
            # Print the input fields along with their names and values
            for input_field in input_fields:
                field_name = input_field.get('name')
                field_value = input_field.get('value')
                
                if field_name and field_value:
                    
                    # Update session_key and session_value
                    if len(field_name) > 10:
                        SessionKey = field_name
                    if len(field_value) > 10:
                        SessionValue = field_value
                        
            print("Conference Session: ", SessionKey, SessionValue)
                
            return SessionKey, SessionValue
    else:
        print("Failed to retrieve the web page. Status code:", response.status_code)
        return "Error"
    
def destination_session(desurl, session):
    response = session.get(desurl, verify=False)
    
    SessionValue = ""
    SessionKey = ""
    
    if response.status_code == 200 or response.status_code == 201:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        title = soup.title
        
        print("TITLE: ", title)
        
        # Find the form with name "login"
        call_center_form = soup.find('form', attrs={'name': 'frm'})
        
        # Check if the login form exists
        if call_center_form:
            # Find all input fields within the form
            input_fields = call_center_form.find_all('input')
            
            # Print the input fields along with their names and values
            for input_field in input_fields:
                field_name = input_field.get('name')
                field_value = input_field.get('value')
                
                if field_name and field_value:
                    
                    # Update session_key and session_value
                    if len(field_name) > 10:
                        SessionKey = field_name
                    if len(field_value) > 10:
                        SessionValue = field_value
                        
            print("Destination: ", SessionKey, SessionValue)
                
            return SessionKey, SessionValue
    else:
        print("Failed to retrieve the web page. Status code:", response.status_code)
        return "Error"