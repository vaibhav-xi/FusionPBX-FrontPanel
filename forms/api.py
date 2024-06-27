import requests
from bs4 import BeautifulSoup
from .queue_data import CallCenterData
from .sessions import *
from .destination_data import DestinationPostData

# URL of the website
url = 'https://138.201.188.127/'
login_url = url + "core/dashboard/"
destination_url = url + "app/destinations/destination_edit.php?type=inbound"
queue_url = url + "app/call_centers/call_center_queue_edit.php"
moh_url = url + "app/music_on_hold/music_on_hold.php"
conference_url = url + "app/conferences/conference_edit.php"
records_url = url + "app/xml_cdr/fetch_xml_cdr.php"

session_key = ""
session_value = ""

QueueSessionValue = ""
QueueSessionKey = ""

session = requests.Session()

login_username = "admin@138.201.188.127"
login_password = "4P8yQxYxK6XbqSk0D3rkWWjds9E"

def get_token():
    response = session.get(url, verify=False)
    
    if response.status_code == 200 or response.status_code == 201:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        title = soup.title
        
        if "Login" not in title.text:
            return "LoggedIn"
        
        # Find the form with name "login"
        login_form = soup.find('form', attrs={'name': 'frm'})
        
        # Check if the login form exists
        if login_form:
            # Find all input fields within the form
            input_fields = login_form.find_all('input')
            
            # Print the input fields along with their names and values
            for input_field in input_fields:
                field_name = input_field.get('name')
                field_value = input_field.get('value')
                
                if field_name and field_value:
                    print(f"Input Field Name: {field_name}, Value: {field_value}")
                    
                    # Update session_key and session_value
                    if len(field_name) > 10:
                        global session_key
                        session_key = field_name
                    if len(field_value) > 10:
                        global session_value
                        session_value = field_value
                        
                    return "session_var"
        else:
            print("No login form found on the page.")
            return "Error"
    else:
        print("Failed to retrieve the web page. Status code:", response.status_code)
        return "Error"
        
def apilogin():
    # if session_key and session_value:
        # Make a POST request with the specified key-value pairs
        post_data = {
            session_key: session_value,
            'username': login_username,
            'password': login_password
        }
        post_response = session.post(login_url, data=post_data, verify=False)
        
        # Check if the POST request was successful
        if post_response.status_code == 200 or post_response.status_code == 201:
            # Parse the HTML content of the response
            post_soup = BeautifulSoup(post_response.content, 'html.parser')
            
            # Find and print the title of the HTML page
            title = post_soup.title
            if "Dashboard" in title.text:
                print("Logged In Successfully")
            else:
                print("Title not found in the HTML page.")
        else:
            print("Failed to make POST request. Status code:", post_response.status_code)
    # else:
    #     print("Session Variables Empty")
    
def call_records():
    
    get_token()
    apilogin()
    
    response = session.get(records_url, verify=False)
    
    if response.status_code == 200 or response.status_code == 201:
        return response.content
    else:
        print("Failed to retrieve records. Status code:", response.status_code)
        return "Error"
    
def create_queue(queue_name, queue_extension, queue_cid_prefix,
                queue_description, moh_sounds):
    get_token()
    apilogin()
    
    session_data = queue_session(queue_url, session)
    
    global QueueSessionKey
    global QueueSessionValue
    
    QueueSessionKey = session_data[0]
    QueueSessionValue = session_data[1]
    
    queue_data = {
        "queue_name": queue_name,
        "queue_extension": queue_extension,
        "queue_cid_prefix": queue_cid_prefix,
        "queue_description": queue_description,
        "queue_moh_sound": moh_sounds
    }
    
    post_data = CallCenterData(QueueSessionKey, QueueSessionValue, queue_data)
    
    # print("POST DATA: ", post_data)
    
    response = session.post(queue_url, data=post_data, verify=False)
    
    with open("response.html", "w") as html_file:
        html_file.write(response.content.decode('utf-8'))
    
    if response.status_code == 200 or response.status_code == 201:
        print("Queue Created successfully.")
    else:
        print("Failed to create queue, Check response. Status code:", response.status_code)
        
def upload_moh(file_path, name):
    
    get_token()
    apilogin()
    
    url = moh_url
    
    form_name = 'form_upload'
    
    session_data = moh_session(url, session, form_name)
    
    SessionKey = session_data[0]
    SessionValue = session_data[1]
    
    # Open the .wav file in binary mode
    try:
        with open(file_path, 'rb') as file:
            files = {'file': file}

            # Additional form data
            data = {
                'action': 'upload',
                SessionKey: SessionValue,
                'name_new': name,
                'rate': ""
            }

            response = session.post(url, files=files, data=data, verify=False)
            
            if response.status_code == 200 or response.status_code == 201:
                return "MOH uploaded successfully."
            else:
                return f"Failed to upload file. Status code: {response.status_code}"  
    except FileNotFoundError:
        return "File not found."     
        
def create_conference(name, extension, description):
    url = conference_url
    
    get_token()
    apilogin()
    
    form_name = 'frm'
    
    session_data = conference_session(url, session, form_name)
    
    SessionKey = session_data[0]
    SessionValue = session_data[1]
    
    data = {
        'conference_name': name,
        'conference_extension': extension,
        'conference_pin_number': "",
        'conference_profile': "default",
        'conference_flags': "",
        'conference_account_code': "",
        'conference_order': "000",
        'conference_context':"138.201.188.127",
        'conference_enabled': "true",
        'conference_description': description,
        SessionKey: SessionValue
    }

    response = session.post(url, data=data, verify=False)
    
    if response.status_code == 200 or response.status_code == 201:
        print("Conference Room Created.")
    else:
        print("Failed to create Conference. Status code:", response.status_code)    

def create_destination(destination_number, destination_action, destination_description, domain_uuid):
    
    get_token()
    apilogin()
    
    session_data = destination_session(destination_url, session)
    
    SessionKey = session_data[0]
    SessionValue = session_data[1]
    
    conf_data = {
        "destination_number": destination_number,
        "destination_action": destination_action,
        "domain_uuid": domain_uuid,
        "destination_description": destination_description
    }
    
    post_data = CallCenterData(SessionKey, SessionValue, conf_data)
    
    print("POST DATA: ", post_data)
    
    response = session.post(destination_url, data=post_data, verify=False)
    
    with open("response.html", "w") as html_file:
        html_file.write(response.content.decode('utf-8'))
    
    if response.status_code == 200 or response.status_code == 201:
        print("Destination Created successfully.")
    else:
        print("Failed to create Destination, Check response. Status code:", response.status_code)
                        
def moh_options():
    get_token()
    apilogin()
    
    url = queue_url
    moh_options = []
    
    response = session.get(url, verify=False)
    
    if response.status_code == 200 or response.status_code == 201:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
    
        # Find the select element with id "queue_moh_sound"
        select_element = soup.find('select', id='queue_moh_sound')
        
        # Check if the select element exists
        if select_element:
            # Find the optgroup element with label "Music on Hold"
            optgroup_moh = select_element.find('optgroup', label='Music on Hold')
            
            # Check if the optgroup element exists
            if optgroup_moh:
                # Find all option elements within the optgroup
                options = optgroup_moh.find_all('option')
                
                # Iterate over each option
                for option in options:
                    # Get the value and text of the option
                    option_value = option.get('value')
                    option_text = option.text
                    
                    # Append the value and text to the moh_options list
                    moh_options.append({
                        'option_value': option_value,
                        'option_text': option_text
                })
    return moh_options

def destination_options():
    
    get_token()
    apilogin()
    
    url = destination_url
    destianation_options = []
    domain_options = []
    
    response = session.get(url, verify=False)
    
    if response.status_code == 200 or response.status_code == 201:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the select element with id "queue_moh_sound"
        select_element = soup.find('select', id='destination_actions_0')
        
        domain_element = soup.find('select', id='destination_domain')
        
        if domain_element:
            
            # Find all option elements within the optgroup
            options = domain_element.find_all('option')
            
            # Iterate over each option
            for option in options:
                # Get the value and text of the option
                option_value = option.get('value')
                option_text = option.text

                domain_options.append({
                    'option_value': option_value,
                    'option_text': option_text
                })
        
        # Check if the select element exists
        if select_element:
            # Find all optgroup elements within the select element
            optgroups = select_element.find_all('optgroup')
            
            # Iterate over each optgroup
            for optgroup in optgroups:
                # Get the label of the optgroup
                optgroup_label = optgroup.get('label')
                
                # Find all option elements within the optgroup
                options = optgroup.find_all('option')
                
                # Iterate over each option
                for option in options:
                    # Get the value and text of the option
                    option_value = option.get('value')
                    option_text = option.text
                    
                    # Append the label, value, and text to the moh_options list
                    destianation_options.append({
                        'optgroup_label': optgroup_label,
                        'option_value': option_value,
                        'option_text': option_text
                    })
                    
        final_data = {
            "domains" : domain_options,
            "destination_options": destianation_options
        }
        
    return final_data

# def create_destination(destination_number, destination_action, destination_description, domain_uuid):
#     session_data = destination_session(destination_url, session)
    
#     SessionKey = session_data[0]
#     SessionValue = session_data[1]
    
#     conf_data = {
#         "destination_number": destination_number,
#         "destination_action": destination_action,
#         "domain_uuid": domain_uuid,
#         "destination_description": destination_description
#     }
    
#     post_data = DestinationPostData(SessionKey, SessionValue, conf_data)
    
#     print("POST DATA: ", post_data)
    
#     response = session.post(destination_url, data=post_data, verify=False)
    
#     with open("response.html", "w") as html_file:
#         html_file.write(response.content.decode('utf-8'))
    
#     if response.status_code == 200 or response.status_code == 201:
#         print("Destination Created successfully.")
#     else:
#         print("Failed to create Destination, Check response. Status code:", response.status_code)

# create_queue("TestQueue999", "9124", "TestQueue999", "Api Test Queue 1", "Music on Hold")
# upload_moh('/home/pi/custompbx/forms/music_on_hold/moh_new.wav', 'test')
# create_conference('TestConf 9.04', '12121', "NewTestConf 9.04")
