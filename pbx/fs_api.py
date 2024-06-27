import requests
from bs4 import BeautifulSoup

# URL of the website
url = 'https://138.201.188.127'

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find the form with name "login"
    login_form = soup.find('form', attrs={'name': 'login'})
    
    # Check if the login form exists
    if login_form:
        # Find all input fields within the form
        input_fields = login_form.find_all('input')
        
        # Print the input fields along with their names and values
        for input_field in input_fields:
            field_name = input_field.get('name')
            field_value = input_field.get('value')
            print(f"Input Field Name: {field_name}, Value: {field_value}")
    else:
        print("No login form found on the page.")
else:
    print("Failed to retrieve the web page. Status code:", response.status_code)
