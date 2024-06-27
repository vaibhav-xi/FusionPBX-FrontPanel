import requests

class FusionPBXAPI:
    def __init__(self, server_url, username, password):
        self.server_url = server_url
        self.username = username
        self.password = password
        self.session = requests.Session()

    def authenticate(self):
        login_url = f"{self.server_url}/login.php"
        response = self.session.get(login_url)

        # Extract CSRF token from the response
        csrf_token = response.text.split('name="csrf_token1" value="')[1].split('"')[0]

        print(csrf_token)
        
        # Authenticate with FusionPBX
        auth_data = {
            'username': self.username,
            'password': self.password,
            'csrf_token1': csrf_token,
            'submit': 'Login'
        }
        auth_url = f"{self.server_url}/core/dashboard/"
        auth_response = self.session.post(auth_url, data=auth_data)

        # Check if authentication was successful
        return 'Invalid Username or Password' not in auth_response.text

    def create_destination(self, destination_data):
        # Adjust the URL and payload based on your FusionPBX setup
        destination_url = f"{self.server_url}/app/destinations/destination_edit.php"
        response = self.session.post(destination_url, data=destination_data)

        # Process the response as needed
        return response.text
