import ast
import requests

def make_call():
    
    data = [8084, "+916269106539", 'external']
    
    post_data = {'details': data}
    response = requests.post('http://138.201.188.127:8000/exin/', data=post_data)
    content = response.content
    
    print(content)
    
def call_flow():
    post_data = {'details': ['call_flow']}
    response = requests.post('http://138.201.188.127:8000/api_req/', data=post_data)
    content = response.content.decode("utf-8")
    
    flow_list = ast.literal_eval(content)
    
    print(flow_list)
    
def conferences():
    post_data = {'details': ['conferences']}
    response = requests.post('http://138.201.188.127:8000/api_req/', data=post_data)
    content = response.content.decode('utf-8').replace("null", "1")
    
    rooms = ast.literal_eval(content)
    
    print(rooms)
    
conferences()    
# make_call()
# call_flow()