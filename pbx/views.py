import ast
import requests
import psycopg2
from subprocess import call
from django.conf import settings
from django.contrib import messages
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from forms.models import Destinations, ForwardRoom

@login_required(login_url='pbx_login')
def home(request):
    
    context = {}
    
    return render(request, 'pbx/home.html', context)

@login_required(login_url='pbx_login')
def agents(request):
    
    context = {}
    
    return render(request, 'pbx/agents.html', context)\
        
@login_required(login_url='pbx_login')
def records(request):
    
    context = {}
    
    return render(request, 'pbx/records.html', context)

@login_required(login_url='pbx_login')
def call_flow_records(request, pk):
    
    post_data = {'details': ['specific_call_flow', pk]}
    response = requests.post('http://138.201.188.127:8000/api_req/', data=post_data)
    content = response.content.decode('utf-8')
    
    flow_list = ast.literal_eval(content)
    
    context = {"flow_list": flow_list}
    
    return render(request, 'pbx/call_flow.html', context)

@login_required(login_url='pbx_login')
def agent_records(request):
    
    context = {}
    
    return render(request, 'pbx/agent_logs.html', context)

@login_required(login_url='pbx_login')
def forward_records(request):
    
    ForwardRooms = ForwardRoom.objects.all()
    
    context = {"rooms":ForwardRooms}
    
    return render(request, 'pbx/forward_records.html', context)

@login_required(login_url='pbx_login')
def admin_page(request):
    
    context = {}
    
    return render(request, 'pbx/admin.html', context)

def AdminPanel(request):
    
    context = {}
    
    return render(request, 'pbx/admin_panel.html', context)

def dashboard(request):
    
    context = {}
    
    return render(request, 'pbx/dashboard.html', context)

def Login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('pbx_home')
        else:
            messages.info(request, 'Username OR password is incorrect')

    context = {}
    
    return render(request, 'pbx/login.html', context)


def Register(request):
    
    context = {}
    
    return render(request, 'pbx/home.html', context)

@api_view(['POST'])
def Make_Call(request):
    
    details = request.data['details']
    
    print(details)
    
    number = details[1]
    
    # process = call(f'/root/call_center/python_scripts/call.sh {number}', shell=True)
    
    return Response("Hoi")

@api_view(['POST'])
def Test(request):
    
    details = request.data['details']
    
    print("RCS: ", details)
    
    # process = cashell=True)
    
    return Response("200")

@api_view(['POST'])
def fetch_data(request):
    
    data = request.data['details']
    
    # print("DATA: ", data, "TYPE: ", type(data))
    
    post_data = {'details': data}
    response = requests.post('http://138.201.188.127:8000/api_req/', data=post_data)
    content = response.content
    
    # options:
    # conferences
    # extensions
    # users
    
    # process = call(f'/root/call_center/python_scripts/call.sh {number}', shell=True)
    
    return Response(content)

@api_view(['POST'])
def uuid_kill(request):
    
    data = request.data['details']
    
    post_data = {'details': data}
    response = requests.post('http://138.201.188.127:8000/uuid_kill/', data=post_data)
    content = response.content
    
    return Response(content)

@api_view(['POST'])
def outbound_call(request):
    
    data = request.data['details']
    
    post_data = {'details': data}
    response = requests.post('http://138.201.188.127:8000/outbound_call/', data=post_data)
    content = response.content
    
    return Response(content)

@api_view(['POST'])
def send_admindata(request):
    
    data = request.data['details']
    
    post_data = {'details': data}
    response = requests.post('http://138.201.188.127:8000/admin_data/', data=post_data)
    content = response.content
    
    return Response(content)

@api_view(['POST'])
def ctransfer(request):
    
    data = request.data['details']
    
    post_data = {'details': data}
    response = requests.post('http://138.201.188.127:8000/uuid_tra/', data=post_data)
    content = response.content
    
    # options:
    # conferences
    # extensions
    # users
    
    # process = call(f'/root/call_center/python_scripts/call.sh {number}', shell=True)
    
    return Response(content)

@api_view(['POST'])
def dump_call(request):
    
    data = request.data['details']
        
    new_room = ForwardRoom(
        room_number = data[2],
        time = data[1]
    )
    
    new_room.save()
    
    post_data = {'details': data}
    response = requests.post('http://138.201.188.127:8000/dump_call/', data=post_data)
    content = response.content
    
    return Response(content)

@api_view(['POST'])
def uuid_transfer_fwd(request):
    
    post_data = request.data['details']
    
    sdata = post_data.split(".")
    
    froom = sdata[0]
    uuid = sdata[1]
    caller_num = sdata[2].replace("49", "")
    
    destination = get_object_or_404(Destinations, number__startswith=caller_num + '/')
    
    forward_des = destination.forward_destination
    
    data = [uuid, forward_des, froom]
    
    post_data = {'details': data}
    response = requests.post('http://138.201.188.127:8000/uuid_transfer/', data=post_data)
    forward_des = response.content
    
    return Response(forward_des)

@api_view(['POST'])
def forwardroom(request):
    
    post_data = request.data['details']
    
    sdata = post_data.split(".")
    
    # froom = sdata[0]
    # uuid = sdata[1]
    caller_num = sdata[2].replace("49", "")
    
    destination = get_object_or_404(Destinations, number__startswith=caller_num + '/')
    
    forward_des = destination.forward_destination
    number = destination.forward_number
    
    res = requests.post('http://138.201.188.127:8000/outbound_call/', data={'details': [forward_des, number]})
    outbound_res = res.content
    
    # data = [uuid, forward_des, froom]
    
    # post_data = {'details': data}
    # response = requests.post('http://138.201.188.127:8000/uuid_transfer/', data=post_data)
    # forward_des = response.content
    
    return Response({"outbound_res":outbound_res})

@api_view(['POST'])
def uuid_transfer(request):
    
    post_data = request.data['details']
    
    uuid = post_data[0]
    froom = post_data[1]
    troom = post_data[2]
    call_application = post_data[3]
    
    data = [uuid, troom, froom, call_application]
    
    print("UUID TRANSFER DATA: ", data)
    
    post_data = {'details': data}
    response = requests.post('http://138.201.188.127:8000/uuid_transfer/', data=post_data)
    forward_des = response.content
    
    return Response(forward_des)

@api_view(['POST'])
def realtime_data(request):
    
    data = request.data['details']
    
    post_data = {'details': data}
    response = requests.post('http://138.201.188.127:8000/realtime_data/', data=post_data)
    content = response.content
    
    return Response(content)

@api_view(['POST'])
def mute_fun(request):
    
    data = request.data['details']
    
    post_data = {'details': data}
    response = requests.post('http://138.201.188.127:8000/mute_fun/', data=post_data)
    content = response.content
    
    return Response(content)

@api_view(['POST'])
def save_agent(request):
    data = request.data['details']
    
    print('DATA RECEIVED: ', data)
    
    post_data = {'details': data}
    response = requests.post('http://138.201.188.127:8000/save_agent/', data=post_data)
    content = response.content
    
    return Response(content)
    
    return Response({'success':'data'})

@api_view(['POST'])
def fetch_agents(request):
    
    data = request.data['details']
    
    # connection = psycopg2.connect(
    #     database="fusionpbx", user='fusionpbx', password='zd9lEhV8hYQ8wl8tjWDJNIurSI', host='127.0.0.1', port= '5432'
    # )
    
    # cursor = connection.cursor()    

    # query = f"SELECT * FROM v_agents"
        
    # cursor.execute(query)

    # result = cursor.fetchall()

    # cursor.close()
    # connection.close()
    
    # return Response({'agents':result})

    post_data = {'details': data}
    response = requests.post('http://138.201.188.127:8000/fetch_agent/', data=post_data)
    content = response.content
    
    return Response(content)

@api_view(['POST'])
def exin(request):
    
    data = request.data['details']
    
    post_data = {'details': data}
    response = requests.post('http://138.201.188.127:8000/exin/', data=post_data)
    content = response.content
    
    return Response(content)

@api_view(['POST'])
def agents(request):
    post_data = {'HOI': "HOI"}
    response = requests.post('http://94.237.84.206/agents/', data=post_data)
    content = response.content.decode()
    
    return Response(content)
    
@api_view(['POST'])
def active_calls(request):
    
    # data = request.data['details']
    
    response = requests.post('http://138.201.188.127:8000/api_activeCalls/')
    
    content = response.content
    
    print(content)
    
    return Response(content)

@api_view(['POST'])
def conference(request):
    
    data = request.data['details']
    
    post_data = {'details': data}
    response = requests.post('http://138.201.188.127:8000/api_conf/', data=post_data)
    content = response.content
    
    # options:
    # conferences
    # extensions
    # users
    
    # process = call(f'/root/call_center/python_scripts/call.sh {number}', shell=True)
    
    return Response(content)