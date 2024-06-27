import csv
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.core.files.storage import FileSystemStorage
from django.db.models.functions import ExtractYear, ExtractMonth
from django.contrib.auth.decorators import login_required
from django.db.models.functions import Now, TruncDate
from django.views.decorators.csrf import csrf_exempt
import psycopg2
from rest_framework.decorators import api_view
from email.mime.multipart import MIMEMultipart
from django.shortcuts import redirect, render
from django.http import FileResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from datetime import datetime, timedelta, date
from collections import defaultdict
from django.db.models import Count, Sum
from django.core.mail import send_mail
from django.http import JsonResponse
from .demopdf import gen_clientinvoice
from django.db.models import Max
from .client_invoice import client_pdf
from .create_pdf import generate_pdf
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from email.mime.text import MIMEText
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import render
from django.utils import timezone
from django.conf import settings
from bs4 import BeautifulSoup
from .api import create_queue, create_conference, upload_moh, moh_options, destination_options, create_destination, call_records
from .passive_mins import get_total_time
from .models import *
from .forms import *
import requests
import smtplib
import json
import pytz
import ast
import os
import re

def delete_info(destinations):
    entries = Disappearing_info.objects.filter(destination=destinations[0])

    current_time = datetime.now(pytz.timezone(settings.TIME_ZONE))
    
    # Iterate over the entries and compare the datetime field
    for entry in entries:
        entry_time = entry.disappearing_time.astimezone(pytz.timezone(settings.TIME_ZONE))
        
        if entry_time <= current_time:
            entry.delete()
        
def convert_min_og(input_value):
    if isinstance(input_value, str):
        try:
            seconds = float(input_value)
        except ValueError:
            return "Invalid input. Please provide a valid integer or a string that can be converted to an integer."
    else:
        seconds = round(float(input_value), 2)

    minutes = seconds / 60
    formatted_minutes = "{:.2f}".format(minutes)  # Format minutes with two decimal places
    return formatted_minutes
    
def convert_min(input_value):
    if isinstance(input_value, str):
        try:
            seconds = float(input_value)
        except ValueError:
            return "Invalid input"
    else:
        seconds = round(float(input_value), 2)

    # Calculate minutes and seconds
    minutes = int(seconds // 60)
    remaining_seconds = int(seconds % 60)  # Convert to an integer

    # Format minutes and seconds with leading zeros
    formatted_time = "{:02d}:{:02d}".format(minutes, remaining_seconds)

    return formatted_time

def get_records(url_para):
    
    post_data = {'details': url_para}
    response = requests.post('http://138.201.188.127:8000/api_req/', data=post_data)
    content = response.content
    
    # content = response.content.decode('utf-8')  # Decode the bytes into a string
    # content_list = content.splitlines()
    content = content.decode('utf-8')  # Decode the bytes into a string
    content_list = json.loads(content)
    
    return content_list
   
   
@login_required(login_url=reverse_lazy('form_login'))
def login_asuser(request):
    
    user = request.user
    
    if user.is_staff:
        
        users = User.objects.all()
        
        context = {"users":users}
        
        return render(request, 'forms/login_asuser.html', context)
    
    else:
        
        return render(request, 'forms/error.html', context)
    
def fusion_login(request):
    
    return render(request, 'forms/fusion.html')

def login_as_user(request, user_id):
    User = get_user_model()
    try:
        user = User.objects.get(id=user_id)
        login(request, user)
        # messages.success(request, f"Logged in as {user.username}")
    except User.DoesNotExist:
        messages.error(request, "User does not exist")
    
    return redirect('home') 

         
@login_required(login_url=reverse_lazy('form_login'))
def home(request):
    
    overlap = "yea"
    
    pk  = "disable"
    
    user = request.user
    
    client = Client.objects.get(user=user)
    
    contacts = "nothing"
    
    messages = "nothing"
    
    cc = Client.objects.get(user=user)
    
    destinations = Destinations.objects.filter(user=cc)
    
    total_destinations = Destinations.objects.filter(user=cc)
    
    destinations = destinations if destinations else "nothing"
            
    context = {'messages':messages, 'contacts':contacts,
               "destinations":destinations, "client": client,
               "pk":pk, "overlap":overlap, 
               "total_destinations":total_destinations}
    
    return render(request, 'forms/home.html', context)

@login_required(login_url=reverse_lazy('form_login'))
def home_sorted(request, pk):
    
    overlap = "none"
    
    total_cost = 0
    total_money = 0
    profit = 0
    
    grand_min = 0
    grand_calls = 0
    grand_avg = 0
    grand_total = 0
    
    user = request.user
    
    # if user.is_staff:
    #     client = Client.objects.get(name=uname)
    # else:
    client = Client.objects.get(user=user)
    
    form_f = client.form_fun
    
    Destination = Destinations.objects.filter(user=client, name=pk)
    
    total_destinations = Destinations.objects.filter(user=client)
    
    if Destination:
        # o = "destination found"
        o = pk
        
        messages = Disappearing_info.objects.filter(destination=Destination[0])
        contacts = UserContact.objects.filter(destination=Destination[0])
        
        g_info = General_info.objects.filter(destination=Destination[0])
        
        # imp_text = g_info.imp_info
        # wlc_text = g_info.welcome_text
        
        des_list = [
                
            {
                "number": f"49{dess.number}",
                "cost": dess.call_price
            }
            
            for dess in Destination
        ]
            
        # grand_min = 0
        # grand_calls = 0
        # grand_avg = 0
        # grand_total = 0
            
        for d in des_list:

            post_data = {'details': ['calculate_des_og', d["number"]]}
            response = requests.post('http://138.201.188.127:8000/api_req/', data=post_data)
            content = response.content.decode()
            
            # print("CONTENT: ", content, "DESTINATION: ", d["number"])
            
            content = content.replace('null', '0')
            
            decoded_list = ast.literal_eval(content)
        
            total_min = float(decoded_list[1])
            grand_min += total_min
            
            # Calculate total_cost
            total_cost = (float(d["cost"].replace(".","").replace(",", ".")) / 60) * total_min
            grand_total += total_cost
            
            grand_avg += float(decoded_list[2])
            grand_calls += float(decoded_list[0])
            
        # print(f"""
                  
        #        MINUTES: {convert_min(grand_min)}
                  
        #        CALLS: {grand_calls}
                  
        #        AVERAGE: {convert_min(grand_avg)}
                  
        #        TOTAL: {grand_total}
                  
        #           """)
        
        if g_info:
        
            imp_text = g_info[0].imp_info
            wlc_text = g_info[0].welcome_text
            general_date = g_info[0].date_created
        else:
            imp_text = ""
            wlc_text = ""
            general_date = ""
        
        delete_info(Destination)
        # contacts = "nothing"
    else:
        o = pk
        messages = "nothing"
        contacts = "nothing"
        Destination = "nothing"
        imp_text = ""
        wlc_text = ""
        general_date = ""
    
    if pk == "all_destinations":
        # o  = "disable"
        
        if client:
            # des = Destinations.objects.filter(user=client)

            des_list = [
                
                {
                    "number": f"49{dess.number}",
                    "cost": dess.call_price
                }
                
                for dess in total_destinations
            ]
            
            # print("TOTAL DES: ", des_list)
            
            # grand_min = 0
            # grand_calls = 0
            # grand_avg = 0
            # grand_total = 0
            
            for d in des_list:
    
                post_data = {'details': ['calculate_des_og', d["number"]]}
                
                # print("POST DETAILS: ", post_data)
                
                response = requests.post('http://138.201.188.127:8000/api_req/', data=post_data)
                
                # print("RESPONSE: ", response.content)
                
                content = response.content.decode().replace("null", "0")
                 
                decoded_list = ast.literal_eval(content)
            
                total_min = float(decoded_list[1])
                grand_min += total_min
                
                # Calculate total_cost
                total_cost = (float(d["cost"].replace(",", ".")) / 60) * total_min
                grand_total += total_cost
                
                grand_avg += float(decoded_list[2])
                grand_calls += float(decoded_list[0])
                
            # print(f"""
            #       ALL DESTINATIONS
                  
            #       MINUTES: {convert_min(grand_min)}
                  
            #       CALLS: {grand_calls}
                  
            #       AVERAGE: {convert_min(grand_avg)}
                  
            #       TOTAL: {grand_total}
                  
            #       """)
            
            tdes = [f"49{single.number}" for single in total_destinations]
        else:
            tdes = []
            
    elif pk == "Products":
        o = "disable"
    else:
        tdes = []
    
    orders = UserOrder.objects.filter(user=client)
    
    # for user_order in orders:
    #     products = user_order.product.all()
    #     for user_product in products:
    #         shipping = user_product.shipping
    #         sales_price = user_product.sales_price
    #         # total_tax = user_product.tax
    #         other = user_product.other
    #         purchase_price = user_product.purchase_price

    #         total_cost += int(shipping) + int(other) + int(purchase_price)
    #         total_money += int(sales_price)
    #         gross_profit = total_money - total_cost
    #         profit += gross_profit - (gross_profit * 0.19)
    
    # cc = Client.objects.get(user=user)
            
    context = {'messages':messages, 'contacts':contacts,
               "destinations":Destination, "client": client,
               "orders":orders, "total_amount":"{:.2f}".format(total_cost), 
               "total_profit":round(profit, 2), "total_money":total_money, "pk":o,
                "welcome_text":wlc_text, "important_text":imp_text,
                "general_date":general_date, "form_fun":form_f,
                "overlap":overlap, "total_destinations":total_destinations,
                "gm":convert_min(grand_min).replace(".", ":"),
                "gc":"{:.2f}".format(grand_calls).replace(".", ","),
                "ga":str(convert_min(grand_avg)).replace(".", ":"),
                "gt":str(round(grand_total, 2)).replace(".", ","), "tdes":tdes}
    
    return render(request, 'forms/home.html', context)


@api_view(['POST'])
def destination_chart(request):
    
    data = request.data['details']
    
    post_data = {'details': data}
    response = requests.post('http://138.201.188.127:8000/api_req/', data=post_data)
    content = response.content
    
    return Response(content)

@api_view(['POST'])
@login_required(login_url=reverse_lazy('form_login'))
def chart_data(request):
    data = request.data['details']
    user = request.user
    
    client_ins = Client.objects.filter(user=user)
    my_des = Destinations.objects.filter(name=data[1])
    
    # currentDay = datetime.now(pytz.timezone(settings.TIME_ZONE)).day
    # currentMonth = datetime.now(pytz.timezone(settings.TIME_ZONE)).month
    # currentYear = datetime.now(pytz.timezone(settings.TIME_ZONE)).year
    
    dates = []
    
    total_cost = 0
    total_money = 0
    profit = 0
    
    profit_list = []        
        
    # if data[0] == 'today' and client_ins and my_des:
    #     user_orders = UserOrder.objects.filter(date_created__date=date.today(),user=client_ins[0])

    # elif data[0] == 'monthly' and client_ins and my_des:
    #     user_orders = UserOrder.objects.annotate(month=TruncDate('date_created'),user=client_ins[0]).order_by('month')

    # elif data[0] == 'yearly' and client_ins and my_des:
    #     user_orders = UserOrder.objects.annotate(year=TruncDate('date_created'),user=client_ins[0]).order_by('year')
        
    if data[0] == 'today' and client_ins and my_des:
        today = date.today()

        user_orders = UserOrder.objects.filter(
            date_created__date=today
        ).order_by('-date_created')

    elif data[0] == 'monthly' and client_ins and my_des:
        today = date.today()
        month_start = today.replace(day=1)
        month_end = month_start + timedelta(days=30)

        user_orders = UserOrder.objects.filter(
            date_created__range=(month_start, month_end)
        ).order_by('-date_created')

    elif data[0] == 'yearly' and client_ins and my_des:
        today = date.today()
        year_start = today.replace(month=1, day=1)
        year_end = year_start + timedelta(days=365)

        user_orders = UserOrder.objects.filter(
            date_created__range=(year_start, year_end)
        ).order_by('-date_created')

    else:
        # last_90_days = date.today() - timedelta(days=90)
        # user_orders = UserOrder.objects.filter(date_created__date__gte=last_90_days, user__in=client_ins, product__destination__in=my_des)
        
        today = date.today()
        ninety_days_ago = today - timedelta(days=90)

        user_orders = UserOrder.objects.filter(
            date_created__date__gte=ninety_days_ago
        ).order_by('-date_created')
        
    for user_order in user_orders:
        products = user_order.product.all()
        for user_product in products:
            shipping = user_product.shipping
            sales_price = user_product.sales_price
            # total_tax = user_product.tax
            other = user_product.other
            purchase_price = user_product.purchase_price
            
            date_created = user_order.date_created

            total_cost += int(shipping) + int(other) + int(purchase_price)
            total_money += int(sales_price)
            gross_profit = total_money - total_cost
            profit += gross_profit - (gross_profit * 0.19)
            profit_list.append(round(profit, 2))
            dates.append(date_created.strftime('%Y-%m-%dT%H:%M.000Z'))
        
    return_data = [profit_list, dates]
    
    return Response(return_data)

@csrf_exempt
@login_required(login_url=reverse_lazy('form_login'))
def save_html(request):
    if request.method == 'POST':
        user = request.user
        
        content = request.POST.get('mform_content')
        # client_name = request.POST.get('mform_client')
        mform_name = request.POST.get('mform_name').replace(' ', '_')
        
        client_ins = Client.objects.filter(user=user)
        
        # soup = BeautifulSoup(content, 'html.parser')
        
        # body_tag = soup.find('body')
        # body_tag.append('<h2>Welcome to my website!</h2>')
        
        # updated_content = str(soup)
        
        if not client_ins:
            return Response({'message': 'Invalid User Name.'})
        
        # Generate a unique filename
        filename = f'{mform_name}.html'  # Replace with your desired filename logic
        
        # Write the content to a new HTML file
        file_path = os.path.join('/home/pi/custompbx/custompbx/forms/templates/forms', filename)  # Replace with your desired file path
        
        with open(file_path, 'w') as file:
            file.write(content)
        
        my_form = User_forms(name=mform_name)
        
        my_form.save()
        
        my_form.form_client.add(client_ins[0])
    
        return HttpResponseRedirect('/settings/')
    
    # return Response({'message': 'Invalid request method.'})

@api_view(['POST'])
def assign_form(request):
    data = request.data['details']
    
    my_des = Destinations.objects.filter(name=data[1])
    
    my_f = User_forms.objects.filter(name = data[0])
    
    if my_f and my_des:
        my_f[0].destination.add(my_des[0])
    else:
        return Response("DATA MISSING")
    
    return Response("Form Assigned")

@api_view(['POST'])
def delete_form(request):
    data = request.data['details']
    
    my_f = User_forms.objects.filter(name = data[0])
    
    if my_f :
        
        my_f[0].delete()
        
        file_path = f"/home/pi/custompbx/custompbx/forms/templates/forms/{data[0]}.html"  # Replace with the actual path to your file

        # Check if the file exists before attempting to delete it
        if os.path.exists(file_path):
            try:
                # Use os.remove() to delete the file
                os.remove(file_path)
                return Response(f"Form '{data[0]}' has been deleted successfully.")
            except OSError as e:
                return Response(f"Error deleting file: {e}")
        else:
            return Response("FORM MISSING")
    
    else:
        return Response("DATA MISSING")
    
@api_view(['POST'])
def delete_email(request):
    data = request.data['details']
    
    my_f = User_forms.objects.filter(name = data[1])
    
    if my_f :
        
        emails_dict = my_f[0].emails
        
        if data[0] in emails_dict.values():
            # Find the key associated with the "user1" value and delete the pair
            for key, value in list(emails_dict.items()):
                if value == data[0]:
                    del emails_dict[key]

            # Save the updated emails dictionary
            my_f[0].emails = emails_dict
            my_f[0].save()
        
        return Response("Delete Successful")
    
    else:
        return Response("DATA MISSING")

@api_view(['POST'])
def add_emails(request):
    data = request.data['details']
    
    my_form = User_forms.objects.filter(name=data[0])
    
    print("DETAILS: ", data[0], data[1], data[2])
    
    if my_form:
        my_form[0].emails[data[2]] = data[1]
        
        my_form[0].save()
        
        return Response("Successfull")
    
    else:
        
        return Response("No_form")
    
@api_view(['POST'])
def getuserdetails(request):
    data = request.data['username']
    
    my_user = Client.objects.filter(name=data)
    
    if my_user:
        return_data = [my_user[0].name, my_user[0].email, 
         my_user[0].invoice_email, my_user[0].street,
         my_user[0].zip_code, my_user[0].place,
         my_user[0].company_name, my_user[0].tax_num]
        
        return Response(return_data)
    
    else:
        
        return Response("No_form")
    
@api_view(['POST'])
def update_client(request):
    data = request.data['edit_client']
    
    my_user = Client.objects.filter(name=data[0])
    
    if my_user:
        my_user[0].name = data[0]
        my_user[0].email = data[1]
        my_user[0].invoice_email = data[2]
        my_user[0].street = data[3]
        my_user[0].zip_code = data[4]
        my_user[0].place = data[5]
        my_user[0].company_name = data[6]
        my_user[0].tax_num = data[7]
        
        my_user[0].save()
        
        return Response("Done")
    
    else:
        
        return Response("No_form")
    
@api_view(['POST'])
def create_agent(request):
    data = request.data['agent_data']

    new_agent = Agents(
    name = data[0],
    street = data[1],
    zip_code = data[2],
    city = data[3],
    email = data[4],
    tax_num = data[5],
    sales_tax = data[6],
    account_name = data[7],
    bank_name = data[8],
    iban = data[9],
    bic = data[10],
    phone = data[11],
    pin = data[12],
    country_code = data[13],
    )
    
    new_agent.save()
        
    return Response("Done")

@api_view(['POST'])
def create_gateway(request):
    data = request.data['gateway_data']

    new_gateway = Sip_trunks(
    sip_provider = data[0],
    start = data[1],
    end = data[2],
    )
    
    new_gateway.save()
        
    return Response("Done")

@api_view(['POST'])
def get_agent(request):
    data = request.data['agent_data']

    agent = Agents.objects.filter(name=data[0])
    
    if not agent:
        return Response("NO DATA")
        
    return Response([agent[0].street, agent[0].zip_code, agent[0].city, 
                     agent[0].email, agent[0].tax_num, agent[0].sales_tax,
                     agent[0].account_name, agent[0].bank_name, agent[0].iban, 
                     agent[0].bic, agent[0].phone, agent[0].name, agent[0].pin,
                     agent[0].country_code])
    
@api_view(['POST'])
def edit_agent(request):
    data = request.data['agent_data']
    
    agent = Agents.objects.filter(name=data[12])
    
    if not agent:
        return Response("NO DATA")
    
    # agent[0].name = data[0]
    agent[0].street = data[0]
    agent[0].zip_code = data[1]
    agent[0].city = data[2]
    agent[0].email = data[3]
    agent[0].tax_num = data[4]
    agent[0].sales_tax = data[5]
    agent[0].account_name = data[6]
    agent[0].bank_name = data[7]
    agent[0].iban = data[8]
    agent[0].bic = data[9]
    agent[0].phone = data[10]
    agent[0].name = data[11]
    agent[0].pin = data[13]
    agent[0].country_code = data[14]
    
    
    agent[0].save()
        
    return Response("Done")

@api_view(['POST'])
def delete_agent(request):
    data = request.data['agent_data']
    
    agent = Agents.objects.filter(name=data[0])
    
    if not agent:
        return Response("NO DATA")
    
    agent[0].delete()
        
    return Response("Done")

def change_agent_status(name, number, country_code, last_status):
    connection = psycopg2.connect(
        database="fusionpbx", user='fusionpbx', password='SQeB0pRyzYpXexMDQYvsJOqOBP0', host='127.0.0.1', port= '5432'
    )
    
    cursor = connection.cursor()
    
    cursor.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'v_agentstatus')")
    table_exists = cursor.fetchone()[0]
    
    if not table_exists:
        
        # create table if it doesn't exist
        cursor.execute("""
            CREATE TABLE v_agentstatus (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255),
                number VARCHAR(100),
                country_code VARCHAR(100),
                login_time TIMESTAMP,
                logout_time TIMESTAMP
            )
        """)
        connection.commit()
        
    if last_status == "inactive":
        
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
        cursor.execute("""
            INSERT INTO v_agentstatus (
                name, number, country_code, login_time, logout_time
            ) VALUES (%s, %s, %s, %s, NULL)
        """, (name, number, country_code, current_time))
        
        connection.commit()
        
    elif last_status == "active":
        
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        cursor.execute("""
            UPDATE v_agentstatus
            SET logout_time = %s
            WHERE name = %s AND number = %s AND logout_time is NULL
        """, (current_time, name, number))
            
        connection.commit()
    
    cursor.close()
    connection.close()

@api_view(['POST'])
def agent_status(request):
    agent_phone = request.data['agent_data']
    agent_pin = request.data['agent_pin']
    
    agent = Agents.objects.filter(phone=agent_phone)
    
    if not agent:
        return Response("No Agent Found")
    
    if agent_pin == agent[0].pin:
        
        if agent[0].status:
            a_status = "active"
        else:
            a_status = "inactive"
        
        change_agent_status(agent[0].name, agent[0].phone, agent[0].country_code, a_status)
    
        agent[0].status = not agent[0].status
        
        agent[0].save()
    else:
        return Response("Wrong Pin")
        
    return Response("Done")

@api_view(['POST'])
def change_agent_status_admin(request):
    agent_phone = request.data['details'][0]
    
    agent = Agents.objects.filter(name=agent_phone)
    
    if not agent:
        return Response(f"No Agent Found {agent_phone}")
        
    if agent[0].status:
        a_status = "active"
    else:
        a_status = "inactive"
    
    change_agent_status(agent[0].name, agent[0].phone, agent[0].country_code, a_status)

    agent[0].status = not agent[0].status
    
    agent[0].save()
        
    return Response("Done")

@api_view(['POST'])
def agents(request):
    
    agents = Agents.objects.all()
    
    total_agents = {}
    
    for agent in agents:
        colour = "green" if agent.status else "red"
        total_agents[agent.name] = [agent.phone, colour]
        
    return Response(total_agents)

@api_view(['POST'])
def send_emails(request):
    data = request.data['details']
    
    my_form = User_forms.objects.filter(name=data[0])
    
    if my_form:
        form_emails = my_form[0].emails
        
        if form_emails:
            
            # form_emails.append(data[0])
    
            return Response(form_emails)
        
        else:
            
            return Response({"Message":"No Emails"})
    else:
        return Response({"Message":"No Emails"})
    
@api_view(['POST'])
def edit_formdetails(request):
    data = request.data['details']
    
    my_form = User_forms.objects.filter(name=data[0])
    
    if my_form:
        
        my_form[0].emails[data[1]] = data[2]
        
        my_form[0].save()
    
        return Response({"Message":"Changed!"})
        
    else:
        return Response({"Message":"Not found"})
    
def extract_emails(email_string):
    # Match emails separated by commas
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    emails = re.findall(pattern, email_string)

    if len(emails) == 1:
        return emails
    else:
        return emails

@csrf_exempt
def render_form(request, fname, dname, phone=None):
    
    my_des = Destinations.objects.filter(name=dname)
    
    users = my_des[0].user.all()
    for user in users:
        user_name = user.name
        
    form_name = phone if phone is not None else user_name
    
    user_form = User_forms.objects.filter(name=fname, destination=my_des[0])
    
    gi = General_info.objects.filter(destination=my_des[0])
    
    important_info = gi[0].imp_info if gi else "Empty"
    
    welcome_text = gi[0].welcome_text if gi else "Empty"
    
    di = Disappearing_info.objects.filter(destination=my_des[0])
    
    disappearing_info = di[0].info if di else "Empty"
    
    my_form = FormData.objects.filter(form_name = form_name)
    
    if request.method == 'POST':
        # Extract form data from the POST request
        form_data = request.POST

        # Build the email content using the form data
        subject = 'Anrufnotiz - Teleoffice24'
        body = "\n".join([f"{field}: {value}" for field, value in form_data.items()])
        from_email = settings.DEFAULT_FROM_EMAIL
        # receiver_email = 'vaibhav28890@gmail.com'  # Replace with your recipient email(s)
        
        try:
            # Create a secure SSL/TLS connection
            with smtplib.SMTP_SSL(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
                # Login to the SMTP server
                server.login(from_email, settings.EMAIL_HOST_PASSWORD)
                
                check_list = ["receiver_email", "send_email", "disappearing_info", "important_info", "welcome_text"]
                
                table_body = ""
                formdata = {}
                # fname = phone if phone is not None else user_name
                
                for field, value in form_data.items():
                    # print("VALUES:", field, value)
                    formdata[field] = value
                    if field not in check_list:
                        # print("INSIDE LOOP:", field, value)
                        table_body += f"""<tr><td>{field}</td><td>{'ja' if value == '1' else value}</td></tr>"""
                    elif field == "receiver_email":
                        receiver_email = extract_emails(value)
                        # receiver_email = ', '.join(receiver_emails)
                        
                #################### EDITED BLOCK ####################
                
                if my_form:
                    my_form[0].form_data = formdata
                    my_form[0].save()
                else:
                    mform = FormData.objects.create(form_name = form_name, form_data=formdata)
                    mform.save()
                    
                #################### EDITED BLOCK ####################
                        
                # print("RECEIVER EMAIL:", receiver_email, value)

                # Create the HTML table with invisible table lines
                html_table = f"""
                    <html>
                        <head>
                        <meta content="text/html; charset=utf-8" http-equiv="content-type"/>
                        </head>
                            <body>
                                <p><br/></p>
                                <div class="moz-forward-container">
                                    <br/>
                                    <meta charset="utf-8" content="text/html; charset=UTF-8" http-equiv="content-type"/>
                                    <div id="_content">
                                        <table border="0" cellpadding="0" cellspacing="0" style="font-size: 11pt; font-family: verdana,arial; width: 100%;">
                                            <tbody>
                                            {table_body}
                                            </tbody>
                                        </table>
                                    </div>
                                    <br/>
                                    <div id="_sig">
                                        <br/>
                                        <div style="font-size:10pt; font-family:Tahoma; color:#999999;">
                                            <b>Innovicom GmbH</b>
                                        </div>
                                        <div style="font-size:9pt; font-family:Arial; color:#999999;">
                                            Kampsriede 6a
                                        </div>
                                        <div style="font-size:9pt; font-family:Arial; color:#999999;">
                                            30659 Hannover
                                        </div>
                                        <br/>
                                        <div style="font-size:9pt; font-family:Arial; color:#999999;">
                                            <a href="http://www.teleoffice24.com/" moz-do-not-send="true">www.teleoffice24.com</a>
                                        </div>
                                        <div style="font-size:9pt; font-family:Arial; color:#999999;">
                                            <a class="moz-txt-link-freetext" href="mailto:info@innovicom.de" moz-do-not-send="true">info@innovicom.de</a>
                                        </div>
                                        <br/>
                                        <div style="font-size:8pt; font-family:Arial; color:#999999;">
                                            Vertretungsberechtigter Geschäftsführer: Marcel Soleinsky<br/>
                                            Registergericht: Amtsgericht Hannover<br/>
                                            Registernummer: HRB 208225<br/>
                                        </div>
                                    </div>
                                </div>
                            </body>
                    </html>
                """
                
                for mail in receiver_email:
                    # Create the email message
                    email = MIMEMultipart()
                    email['From'] = from_email
                    email['To'] = mail
                    email['Subject'] = subject
                    # email.attach(MIMEText(body, 'html'))
                    
                    # Add BCC email
                    bcc_email = 'service@innovicom.de'
                    # bcc_email = 'vaibhav0249@gmail.com'
                    # email['Bcc'] = bcc_email
                    
                    email.attach(MIMEText(html_table, 'html'))

                    # Send the email
                    
                    server.sendmail(from_email, mail, email.as_string())

                server.sendmail(from_email, bcc_email, email.as_string())

            print('Email sent successfully.')
            
            return render(request, f'forms/form_success.html')

        except Exception as e:
            print(f'An error occurred while sending the email: {str(e)}')
            
            return render(request, f'forms/form_error.html', context={"error":str(e)})
        
        # send_mail('Test Email', 'This is a test email.', settings.DEFAULT_FROM_EMAIL, ['vaibhav28890@gmail.com'],fail_silently=False,)
    
    if user_form:
        
        filename = user_form[0].name
        
        # path = f"/home/pi/fusion_panel/fusion_dashboard/static/user_forms/{filename}.html"
        
        # print("FILEPATH", path)
        
        # a = "home"
        
        emails = user_form[0].emails
        
        phone = '' if phone is None else phone
        
        if my_form:
            form_obj = my_form[0].form_data
        else:
            form_obj = {}
        
        context = {"phone_number":phone, "important_info":important_info,
                   "disappearing_info":disappearing_info, "data":emails,
                   "welcome_text":welcome_text, "form_obj":form_obj}
    
        return render(request, f'forms/{filename}.html', context)

    else:
        
        context = {}
        
        return render(request, 'forms/home.html', context)

@login_required(login_url=reverse_lazy('form_login'))
def index(request):
    
    user = request.user
    
    client_instance = Client.objects.get(user=user)
    
    return render(request, 'forms/index.html', {"client_name":client_instance.name})

def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # return redirect('settings')
        
            if user.is_staff:
                return redirect('admin_dash')  # Redirect to the staff dashboard page
            else:
                return redirect('home')  # Redirect to the regular user settings page
        else:
            messages.info(request, 'Username OR password is incorrect')

    context = {}
    return render(request, 'forms/login.html', context)

def registerPage(request):

    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            name = form.cleaned_data.get('username')
            email_address = form.cleaned_data.get('email_address')
            invoice_email = form.cleaned_data.get('invoice_email_address')
            street = form.cleaned_data.get('street')
            zipcode = form.cleaned_data.get('zip_code')
            place = form.cleaned_data.get('city')
            country = form.cleaned_data.get('country')
            tax_num = form.cleaned_data.get('tax_number')
            company_name = form.cleaned_data.get('company_name')
            
            Client.objects.create(user=user,name=name, email=email_address,
                                  invoice_email=invoice_email, street=street,
                                  zip_code=zipcode, place=place, tax_num=tax_num,
                                  company_name=company_name, country=country)

            # messages.success(request, 'Account was created for ' + name)

            return HttpResponseRedirect('/login/')
        else:
            # If the form is not valid, display an error message
            error_message = "Registration failed. Please correct the errors below."
            form_errors = form.errors.as_text()
            messages.error(request, error_message + "\n" + form_errors)
            # messages.error(request, error_message)
        
    context = {'form':form}
    
    return render(request, 'forms/register.html', context)

def create_client(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            name = form.cleaned_data.get('username')
            email_address = form.cleaned_data.get('email_address')
            invoice_email = form.cleaned_data.get('invoice_email_address')
            street = form.cleaned_data.get('street')
            zipcode = form.cleaned_data.get('zip_code')
            place = form.cleaned_data.get('city')
            country = form.cleaned_data.get('country')
            tax_num = form.cleaned_data.get('tax_number')
            company_name = form.cleaned_data.get('company_name')
            
            Client.objects.create(user=user,name=name, email=email_address,
                                  invoice_email=invoice_email, street=street,
                                  zip_code=zipcode, place=place, tax_num=tax_num,
                                  company_name=company_name, country=country)

            return JsonResponse({"message": "Client Created"}, status=201)
        else:
            # If the form is not valid, return form errors as JSON response
            form_errors = form.errors
            return JsonResponse({"errors": form_errors}, status=400)

    # This part will not be executed in your case as you are not rendering any template
    context = {'form': form}
    return render(request, 'forms/register.html', context)

@login_required(login_url=reverse_lazy('form_login'))
def dashboard(request):
    
    overlap = "yea"
    
    user = request.user
    
    client = Client.objects.get(user=user)
    
    contacts = "nothing"
    
    messages = "nothing"
    
    pk = "none"
    
    # cc = Client.objects.get(user=user)
    
    destinations = Destinations.objects.filter(user=client)
    
    destinations = destinations if destinations else "nothing"
    
    total_destinations = Destinations.objects.filter(user=client)
    
    current_time = datetime.now(pytz.timezone(settings.TIME_ZONE))
    
    # entries = Disappearing_info.objects.filter(user=user)

    # # Iterate over the entries and compare the datetime field
    # for entry in entries:
    #     entry_time = entry.disappearing_time.astimezone(pytz.timezone(settings.TIME_ZONE))
        
    #     # print("ENTRY", entry)
    #     # print("CURRENT TIME:", current_time.astimezone(pytz.timezone(settings.TIME_ZONE)))
    #     # print("DISS TIME:", entry_time)
    #     # print(entry_time <= current_time)
        
    #     if entry_time <= current_time:
    #         entry.delete()
            
    entries = "nothing"
            
    context = {'messages':messages, 'contacts':contacts,
               "destinations":destinations, "client": client,
               "pk":pk, "overlap":overlap, "total_destinations":total_destinations}
    
    return render(request, 'forms/dashboard.html', context)

@login_required(login_url=reverse_lazy('form_login'))
def admin_dash(request):
    
    customers = Client.objects.all()
    
    destinations = Destinations.objects.all()
    
    orders = UserOrder.objects.all()
    
    records = Disappearing_record.objects.all()
    
    agents = Agents.objects.all()
    
    gateways = Sip_trunks.objects.all()
    
    forms_data = FormData.objects.all()
    
    post_data = {'details': ['conferences']}
    response = requests.post('http://138.201.188.127:8000/api_req/', data=post_data)
    content = response.content.decode('utf-8').replace("null", "1")
    
    rooms = ast.literal_eval(content)
            
    context = {"destinations":destinations, 'customers':customers,
               "orders":orders, "records":records, "agents":agents,
               "forms_data":forms_data,"gateways":gateways, 'rooms':rooms}
    
    return render(request, 'forms/admin.html', context)

def down_csv(request, filename):
    csv_path = os.path.join(f"/home/pi/custompbx/custompbx/forms/csv_file/{filename}")
    response = FileResponse(open(csv_path, 'rb'))
    response['Content-Type'] = 'text/csv'
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response

def remove_duplicates(rows):
    unique_rows = []
    seen_rows = set()

    for row in rows:
        # Convert each row to a tuple to make it hashable
        row_tuple = tuple(row.values())

        # Check if the row is not a duplicate
        if row_tuple not in seen_rows:
            seen_rows.add(row_tuple)
            unique_rows.append(row)

    return unique_rows

def sortcsv_og(data):
    combined_data = defaultdict(lambda: defaultdict(list))

    for row in data:
        first_name = row.get('First Name (Shipping)')
        last_name = row.get('Last Name (Shipping)')
        category = row.get('Category')
        
        key = (first_name, last_name)
        combined_data[key]['Order Subtotal Amount'].append(row.get('Order Subtotal Amount'))
        combined_data[key]['Order Shipping Amount'].append(row.get('Order Shipping Amount'))
        combined_data[key]['Order Total Amount'].append(row.get('Order Total Amount'))
        combined_data[key]['Order Total Tax Amount'].append(row.get('Order Total Tax Amount'))
        combined_data[key]['Category'].append(category)

    result_data = []
    
    for key, values in combined_data.items():
        combined_row = {
            'First Name (Shipping)': key[0],
            'Last Name (Shipping)': key[1],
            'Order Subtotal Amount': int(values['Order Subtotal Amount']),
            'Order Shipping Amount': int(values['Order Shipping Amount']),
            'Order Total Amount': int(values['Order Total Amount']),
            'Order Total Tax Amount': int(values['Order Total Tax Amount']),
            'Category': ', '.join(values['Category']),
        }
        result_data.append(combined_row)

    return result_data

def sortcsv(data):
    combined_data = defaultdict(lambda: defaultdict(list))

    for row in data:
        first_name = row.get('First Name (Shipping)')
        last_name = row.get('Last Name (Shipping)')
        name = row.get('Full Name (Shipping)')
        category = row.get('Category')
        
        filed1 = row.get('Phone (Billing)')
        filed2 = row.get('Address 1 (Shipping)')
        filed3 = row.get('City (Shipping)')
        # filed4 = row.get('State Code (Shipping)')
        # filed5 = row.get('Postcode (Shipping)')
        filed6 = row.get('Country Code (Shipping)')
        filed7 = row.get('Address')
        
        filter_phone = row.get('lphone')
        filter_city = row.get('lcity')
        
        filter_a = row.get('City, State, Zip (Shipping)')
        
        # print("FILTER PHONE: ", filter_phone)
        # print("FILTER CITY: ", filter_city)
        
        # key = (first_name, last_name)
        key = (name)
        combined_data[key]['Order Subtotal Amount'].append(float(row.get('Order Subtotal Amount', 0)))
        combined_data[key]['Order Shipping Amount'].append(float(row.get('Order Shipping Amount', 0)))
        combined_data[key]['Order Total Amount'].append(float(row.get('Order Total Amount', 0)))
        combined_data[key]['Order Total Tax Amount'].append(float(row.get('Order Total Tax Amount', 0)))
        combined_data[key]['Category'].append(category)
        
        combined_data[key]['Phone (Billing)'].append(filed1)
        combined_data[key]['Address 1 (Shipping)'].append(filed2)
        combined_data[key]['City (Shipping)'].append(filed3)
        # combined_data[key]['State Code (Shipping)'].append(filed4)
        # combined_data[key]['Postcode (Shipping)'].append(filed5)
        combined_data[key]['Country Code (Shipping)'].append(filed6)
        combined_data[key]['Address'].append(filed7)
        
        combined_data[key]['lphone'].append(filter_phone)
        combined_data[key]['lcity'].append(filter_city)
        
        combined_data[key]['City, State, Zip (Shipping)'].append(filter_a)

    result_data = []
    for key, values in combined_data.items():
        unique_categories = set(values['Category'])
        
        f1 = values['Phone (Billing)'][0]
        f2 = set(values['Address 1 (Shipping)'])
        f3 = values['City (Shipping)'][0]
        # f4 = set(values['State Code (Shipping)'])
        # f5 = set(values['Postcode (Shipping)'])
        f6 = set(values['Country Code (Shipping)'])
        f7 = values['Address'][0]
        
        f8 = values['City, State, Zip (Shipping)'][0]
        
        f_phone = values['lphone'][0]
        f_city = values['lcity'][0]
        
        # print("ADDRESS: ", f7)
        
        # combined_row = {
        #     'First Name (Shipping)': key[0],
        #     'Last Name (Shipping)': key[1],
        #     'Order Subtotal Amount': round(sum(values['Order Subtotal Amount']), 2),
        #     'Order Shipping Amount': round(sum(values['Order Shipping Amount']), 2),
        #     'Order Total Amount': round(sum(values['Order Total Amount']), 2),
        #     'Order Total Tax Amount': round(sum(values['Order Total Tax Amount']), 2),
        #     'Category': ', '.join(unique_categories),
            
        #     "Phone (Billing)": ', '.join(f1),
        #     "Address 1 (Shipping)": f7,
        #     "City (Shipping)": ', '.join(f3),
        #     "State Code (Shipping)": ', '.join(f4),
        #     "Postcode (Shipping)": ', '.join(f5),
        #     "Country Code (Shipping)": ', '.join(f6),
        # }
        
        combined_row = {
            'Full Name (Shipping)': key,
            'Order Subtotal Amount': round(sum(values['Order Subtotal Amount']), 2),
            'Order Shipping Amount': round(sum(values['Order Shipping Amount']), 2),
            'Order Total Amount': round(sum(values['Order Total Amount']), 2),
            'Order Total Tax Amount': round(sum(values['Order Total Tax Amount']), 2),
            'Category': ', '.join(unique_categories),
            
            "Phone (Billing)": f1,
            "Address 1 (Shipping)": f7,
            "City (Shipping)": f3,
            # "State Code (Shipping)": ', '.join(f4),
            # "Postcode (Shipping)": ', '.join(f5),
            "Country Code (Shipping)": ', '.join(f6),
            
            "City, State, Zip (Shipping)": f8,
        }
        
        result_data.append(combined_row)

    return result_data

@csrf_exempt
def csv_upload(request):
    if request.method == 'POST' and request.FILES['file']:
        uploaded_file = request.FILES['file']
        
        # print('Uploaded file:', uploaded_file.name)
        
        with open(f"/home/pi/custompbx/custompbx/forms/csv_file/{uploaded_file.name}", "wb+") as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)

        return JsonResponse({'message': 'File uploaded successfully!'})

    return JsonResponse({'error': 'Invalid request.'}, status=400)

def csv_viewer(request):
    
    files_path = "/home/pi/custompbx/custompbx/forms/csv_file"
    
    csv_files = [f for f in os.listdir(files_path) if f.endswith('.csv')]
            
    context = {"files":csv_files}
    
    return render(request, 'forms/csv_viewer.html', context)

def filter_csv_og(data):
    unique_order_numbers = set()
    filtered_data = []

    for row in data:
        order_number = row.get('Order Number')

        # Check if Order Number is already encountered
        if order_number not in unique_order_numbers:
            unique_order_numbers.add(order_number)
            filtered_data.append(row)

    return filtered_data

def filter_csv(data):
    unique_order_numbers = set()
    filtered_data = []

    # Sort data by 'Order Date' in descending order
    data.sort(key=lambda row: datetime.strptime(row['Order Date'], '%d/%m/%Y %H:%M'), reverse=True)

    for row in data:
        order_number = row.get('Order Number')

        # Check if Order Number is already encountered
        if order_number not in unique_order_numbers:
            unique_order_numbers.add(order_number)

            # Include 'Address' field as the latest 'Address 1 (Shipping)' value
            latest_address = row.get('Address 1 (Shipping)')
            latest_phone = row.get('Phone (Billing)')
            latest_city = row.get('City (Shipping)')
            
            filtered_data.append({**row, 'Address': latest_address})
            filtered_data.append({**row, 'lphone': latest_phone})
            filtered_data.append({**row, 'lcity': latest_city})
            # print("LATEST CITY: ", latest_city)
            # print("LATEST PHONE: ", latest_phone)
            
    # print("FILTERED DATA: ", filtered_data)

    return filtered_data


def createpdf(sorted_headers, sorted_data, output_file, printing_list):
    pdf_path = f"/home/pi/custompbx/custompbx/forms/csv_file/{output_file}.pdf"  # Replace with your desired output path

    # Set up the PDF canvas
    c = canvas.Canvas(pdf_path, pagesize=A4)
    width, height = A4

    # Calculate the column width for equally spaced columns
    col_width = width / len(sorted_headers) + 70

    # print("DIMENSIONS: ", width, height, col_width, y_pos)
    
    ######################### HEADERS #########################
    
    # y_pos = height - 50
    
    # for i, header in enumerate(sorted_headers):
    #     y_pos -= 20
    #     # print("Y-AXIS: ", y_pos, "HEADER: ", header)
    #     c.drawString(col_width, y_pos, header)
    
    ######################### HEADERS #########################
    
    my_data = {}
    
    r  = 1
    
    for row in sorted_data:
        m = {}
        for i, header in enumerate(sorted_headers):
            value = row.get(header, '')
            
            header = str(header).replace(" ", "").lower()
            
            # print("HEADER: ", header, "VALUE: ", value)
            
            # if "firstname" in header:
            #     m['first'] = value
                
            # elif "lastname" in header:
            #     m['last'] = value
                
            if "name" in header:
                m['name'] = value
                
            elif "address1" in header:
                m['address'] = value
                
            elif "city,state,zip" in header:
                # print("COMBINED DATA: ", str(value).strip(","))
                ci = str(value).split(",")[0].replace(" ", "")
                z = str(value).split(",")[2].replace(" ", "")
                m['a2'] = f"{z} {ci}"
                
            # elif "city" in header:
            #     m['city'] = value
                
            elif "countrycode" in header:
                m['countrycode'] = value
                
            else:
                pass
        my_data[r] = m
        r += 1
                
    # print("USEFUL DATA: ", my_data)

    y_pos = height - 130

    # Write data to subsequent pages
    for key in my_data:
        # name = f"{my_data[key]['first']}{my_data[key]['last']}"
        name = f"{my_data[key]['name']}"
        # print("NAME: ", name)
        if name in printing_list:
            # c.showPage()  # Start a new page for each row
            my_i = 0
            for keyn in my_data[key].values():
                
                print("VALUE: ", keyn)
                
                if "," in keyn:
                    # print("VALUE WITH COMMA: ", keyn)
                    p1 = keyn.split(",")[0]
                    p2 = keyn.split(",")[1]
                    
                    # print("Part1: ", p1, len(p1), p1.isdigit())
                    # print("Part2: ", p2, len(p2), p2.isdigit())
                    
                    if p1.isdigit() and len(p1) > 4:
                        
                        # print("PART1 is integer")
                        
                        keyn = p2.replace(" ", "")
                        
                        # print("AFTER REPLACING: ", keyn)
                        
                    if p2.isdigit() and len(p2) > 4:
                        
                        # print("PART2 is integer")
                        
                        keyn = p1.replace(" ", "")
                        
                        # print("AFTER REPLACING: ", keyn)
                
                y_pos -= 20
                      
                c.drawString(col_width, y_pos, f"{keyn}")
                my_i += 1

            y_pos = height - 130
            c.showPage() 

    c.save()
    
# @api_view(['POST'])
# def down_pdf(request):
#     data = request.data['details']
    
#     file_path = f"/home/pi/custompbx/custompbx/forms/csv_file/{data[0]}.pdf"
    
#     if os.path.exists(file_path):
    
#         os.remove(file_path)
        
#         return Response("File Removed")
    
#     return Response("File Does Not Exist")
        
def down_pdf(request, filename):
    pdf_path = os.path.join(f"/home/pi/custompbx/custompbx/forms/csv_file/{filename}.pdf")
    response = FileResponse(open(pdf_path, 'rb'))
    response['Content-Type'] = 'application/pdf'
    response['Content-Disposition'] = f'attachment; filename="{filename}.pdf"'
    return response

@csrf_exempt
def specific_csv(request, pk):
    
    file_path = f"/home/pi/custompbx/custompbx/forms/csv_file"
    
    csv_files = [f for f in os.listdir(file_path) if f.endswith('.csv')]
    
    file_path += f"/{pk}.csv"
    
    remove_headers = ["Item Name", "SKU", "State Code (Shipping)", "Customer Note", "Order Date", "Order Number"]
    
    # Read the CSV file
    with open(file_path, 'r') as file:
        csv_reader = csv.DictReader(file)
        headers = csv_reader.fieldnames
        sorted_headers = [header for header in csv_reader.fieldnames if header not in remove_headers]
        data = list(csv_reader)
        
    data_without_duplicates = remove_duplicates(data)
    
    sorted_data = sortcsv(filter_csv(data))
    
    # sorted_data = data
    
    sorted_headers.append("Address")
    
    # createpdf(sorted_headers, sorted_data, pk)
    
    if request.method == "POST":
        # Get raw JSON data from the request body
        data_received = json.loads(request.body)['details']
        
        print(data_received)

        # Access the elements in the array
        file_name = data_received[0]
        printing_list = data_received[1]

        # print(file_name, type(file_name))
        # print(printing_list, type(printing_list))

        # Handle the data accordingly
        createpdf(sorted_headers, sorted_data, file_name, printing_list)

        # Return a JSON response
        return JsonResponse({'status': 'success'})

    context = {
        'headers': headers,
        'sorted_headers':sorted_headers,
        'data': data_without_duplicates,
        "files":csv_files,
        "sorted_data":sorted_data,
        "pk":pk,
    }
    
    return render(request, 'forms/csv_viewer.html', context)

@api_view(['POST'])
def del_csv(request):
    data = request.data['details']
    
    file_path = f"/home/pi/custompbx/custompbx/forms/csv_file/{data[0]}.csv"
    
    if os.path.exists(file_path):
    
        os.remove(file_path)
        
        return Response("File Removed")
    
    return Response("File Does Not Exist")

@login_required(login_url=reverse_lazy('form_login'))
def dashboard_sorted(request, pk):
    user = request.user
    
    overlap = "none"
    
    client_ins = Client.objects.get(user=user)
    
    destinations = Destinations.objects.filter(user=client_ins, name=pk)
    
    total_destinations = Destinations.objects.filter(user=client_ins)
    
    passed_url = "https://telefonzentrale.digital/forms"
    
    if destinations:
        
        my_destinations = Destinations.objects.filter(user=client_ins)
        
        u_forms = User_forms.objects.filter(form_client=client_ins)
        
        contacts = UserContact.objects.filter(destination=destinations[0])
    
        messages = Disappearing_info.objects.filter(destination=destinations[0])
    
        products = UserProduct.objects.filter(user=client_ins, destination=destinations[0])
        
        g_info = General_info.objects.filter(destination=destinations[0])
        
        records = Disappearing_record.objects.filter(destination=destinations[0])
        
        delete_info(destinations)
        
        if g_info:
        
            imp_text = g_info[0].imp_info
            wlc_text = g_info[0].welcome_text
        
        else:
            
            imp_text = ""
            wlc_text = ""

    else:
        destinations = "nothing"
        my_destinations = "nothing"
        contacts = "nothing"
        messages = "nothing"
        records = "nothing"
        u_forms = "nothing"
        products = "nothing"
        imp_text = ""
        wlc_text = ""
            
    context = {'messages':messages, 'contacts':contacts,
               "destinations":destinations, "products": products, 
               "pk":pk, "welcome_text":wlc_text, "important_text":imp_text,
               "records":records, "my_forms":u_forms, "passed_url":passed_url,
               "my_destinations":my_destinations, "overlap":overlap,
               "total_destinations":total_destinations}
    
    return render(request, 'forms/dashboard.html', context)

@api_view(['POST'])
def general_info(request):
    data = request.data['details']
    
    my_des = Destinations.objects.filter(name=data[2])
    
    GI  = General_info.objects.filter(destination=my_des[0])
    
    if GI:
        
        GI[0].welcome_text =  data[0]
        
        GI[0].imp_info =  data[1]
        
        GI[0].save()
        
    else:
    
        I = General_info(welcome_text = data[0], imp_info = data[1])
        
        I.save()
        
        I.destination.add(my_des[0])
    
    return Response("Created")

@api_view(['POST'])
def createDissinfo(request):
    data = request.data['details']
    
    datetime_object = datetime.strptime(data[2], "%d/%m/%Y %H:%M")
    
    # cc_ins = Client.objects.get(name=data[3])
    
    my_des = Destinations.objects.filter(name=data[3])
    
    S = Disappearing_info(name = data[0], info = data[1], disappearing_time = datetime_object)
    
    S.save()
    
    S.destination.add(my_des[0])
    
    S_record = Disappearing_record(name = data[0], info = data[1], disappearing_time = datetime_object)
    
    S_record.save()
    
    S_record.destination.add(my_des[0])
    
    return Response("Created")

@api_view(['POST'])
def EditDissinfo(request):
    data = request.data['details']
    
    datetime_object = datetime.strptime(data[2], "%d/%m/%Y %H:%M")
    
    diss_obj = Disappearing_info.objects.filter(id=data[4])
    
    if diss_obj:
        
        record_obj = Disappearing_record.objects.filter(name=diss_obj[0].name)
        
        diss_obj[0].name = data[0]
        diss_obj[0].info = data[1]
        diss_obj[0].disappearing_time = datetime_object
        diss_obj[0].save()
        
        record_obj[0].name = data[0]
        record_obj[0].info = data[1]
        record_obj[0].disappearing_time = datetime_object
        record_obj[0].save()
        
        return Response("Created")
    else:
        return Response(f"Not Found {data[4]}")

@api_view(['POST'])
def diss_info(request):
    data = request.data['details']
    
    md = Disappearing_info.objects.filter(name=data[0])
    
    if md:
        return_data = [md[0].name, md[0].disappearing_time.strftime("%B %d, %Y, %I:%M %p"), md[0].info, md[0].id]
    else:
        return_data = ["NO RECORD"]
    
    return Response(return_data)

@api_view(['POST'])
def delete_diss(request):
    data = request.data['details']
    
    md = Disappearing_info.objects.filter(id=data[0])
    
    if md:
        md[0].delete()
        return_data = ["Deleted"]
    else:
        return_data = ["No Record Found"]
    
    return Response(return_data)

@api_view(['POST'])
def get_settings(request):
    my_user = request.data['user_name']
    
    settings = Client.objects.get(name=my_user)
    
    datar = {"daily_stats":settings.daily_stats, "weekly_stats":settings.weekly_stats,
             "monthly_stats":settings.monthly_stats,
             "invoice_creation":settings.invoice_creation,
             "form_function":settings.form_fun,
             "call_price":settings.call_price,
             "imp_sw":settings.imp_info,
             "diss_sw":settings.diss_info,
             "sales_sw":settings.sales,}
    
    return Response({"user_settings":datar})

@api_view(['POST'])
def update_settings(request):
    details = request.data['update_settings']
    
    settings = Client.objects.get(name=details[0])
    
    settings.daily_stats = details[1]
    settings.weekly_stats = details[2]
    settings.monthly_stats = details[3]
    settings.invoice_creation = details[4]
    settings.form_fun = details[5]
    settings.imp_info = details[6]
    settings.diss_info = details[7]
    settings.sales = details[8]
    
    settings.save()
    
    return Response("DONE!")

@api_view(['POST'])
def get_destinations(request):
    
    data = request.data['details']
    
    # print("DATA: ", data, "TYPE: ", type(data))
    
    post_data = {'details': data}
    response = requests.post('http://138.201.188.127:8000/api_req/', data=post_data)
    content = response.content
    
    return Response(content)

@api_view(['POST'])
def get_destination(request):
    
    post_data = request.data['details']
    
    sdata = post_data.split(".")
    
    froom = sdata[0]
    user_id = sdata[1]
    
    print("DATA RECEIVED: ", sdata[2])
    
    destination = get_object_or_404(Destinations, number__startswith=sdata[2] + '/')

    # Retrieve the forward_destination field
    forward_des = destination.forward_destination
    
    data = [user_id, froom, forward_des, False]
    
    post_data = {'details': data}
    response = requests.post('http://138.201.188.127:8000/uuid_tra/', data=post_data)
    content = response.content
    
    return Response({"content":content})

def replace_leading_zero(input_string, country_code):
    # Check if the string is of length 12
    if len(input_string) == 12:
        # Check if the string starts with '0'
        if input_string.startswith('0'):
            # Replace the leading '0' with '+49'
            return str(country_code) + input_string[1:]
    return input_string

@api_view(['POST'])
def exin(request):
    
    data = request.data['details']
    
    countrycode = Agents.objects.get(phone=data[1]).country_code
    
    if countrycode == "+49":
        final_number = data[1]
    else:
        final_number = countrycode + data[1]
    
    data = [data[0], final_number, 'external']
    
    post_data = {'details': data}
    response = requests.post('http://138.201.188.127:8000/exin/', data=post_data)
    content = response.content
    
    return Response(content)

@api_view(['POST'])
def call_stats(request):
    
    data = request.data['details']
    
    post_data = {'details': ['call_flow']}
    response = requests.post('http://138.201.188.127:8000/api_req/', data=post_data)
    content = response.content
    
    return Response(content)

@api_view(['POST'])
def ivr_records(request):
    
    data = request.data['details']
    
    post_data = {'details': data}
    response = requests.post('http://138.201.188.127:8000/api_req/', data=post_data)
    content = response.content
    
    return Response(content)

@api_view(['POST'])
def search_agent(request):
    
    data = request.data['details']
    
    agent_numbers = Agents.objects.values_list('number', flat=True)
    
    data = data.append(agent_numbers)

    passive_mins = get_total_time(data[1], data[3], data[4])
    
    post_data = {'details': data}
    response = requests.post('http://138.201.188.127:8000/api_req/', data=post_data)
    content = response.content.decode("utf-8")
    
    return Response([passive_mins[0], content])

@api_view(['POST'])
def update_des_price(request):
    
    data = request.data['save_price']
    
    my_destination = Destinations.objects.filter(name=data[0])
    
    des = int(Destinations.objects.order_by('-forward_destination').first().forward_destination)
    
    # forward = des + 1 if des == 0 else forward
    
    if int(my_destination[0].forward_destination) == 0:
        forward = des + 1
        
        create_conference(
            f"{data[0].strip()}_forward", forward,
            f"Forward Destination for {data[0]}")
    else:
        forward = my_destination[0].forward_destination
    
    if my_destination:
        
        my_destination[0].price_percall = data[1]
        my_destination[0].call_price  = data[2] #Price per_min
        my_destination[0].free_calls = data[3]
        my_destination[0].free_mins = data[4]
        
        my_destination[0].monthly_fees = data[5]
        my_destination[0].monthly_fee = data[6]
        my_destination[0].free_call = data[7]
        my_destination[0].free_min = data[8]
        
        my_destination[0].forward_destination = forward
        my_destination[0].fd_cost = data[10]
        my_destination[0].forward_number = data[11]
        
        my_destination[0].save()
        
        return Response("Updated")
    else:
        return Response("No records")
    
@api_view(['POST'])
def fetch_des_settings(request):
    
    data = request.data['data']
    
    my_destination = Destinations.objects.filter(name=data[0])
    
    if my_destination:
        
        return_data = {
            "ppc":my_destination[0].price_percall,
            "ppm":my_destination[0].call_price,
            "fc":my_destination[0].free_calls,
            "fm":my_destination[0].free_mins,
            "mf":my_destination[0].monthly_fees,
        
            "monthly_fee":my_destination[0].monthly_fee,
            "charge_pc":my_destination[0].free_call,
            "charge_pm":my_destination[0].free_min,
            
            "forward_des":my_destination[0].forward_destination,
            "forward_cost":my_destination[0].fd_cost,
            "forward_number":my_destination[0].forward_number,
            "forward_seconds":my_destination[0].forward_seconds,
            }
        
        return Response({"data": return_data})
    else:
        return Response("No records")

@api_view(['POST'])
def destination_data(request):
    
    data = request.data['details']
    
    post_data = {'details': ['calculate_des_og', data]}
    response = requests.post('http://138.201.188.127:8000/api_req/', data=post_data)
    content = response.content
    
    return Response(content)

@api_view(['POST'])
def destination_sorted(request):
    
    number = request.data['details']
    start = request.data['start']
    end = request.data['end']
    
    post_data = {'details': ['des_sorted', number, start, end]}
    response = requests.post('http://138.201.188.127:8000/api_req/', data=post_data)
    content = response.content
    
    return Response(content)

def download_pdf(request, filename):
    pdf_path = os.path.join(f"/home/pi/custompbx/custompbx/forms/invoices/{filename}.pdf")
    response = FileResponse(open(pdf_path, 'rb'))
    response['Content-Type'] = 'application/pdf'
    response['Content-Disposition'] = f'attachment; filename="{filename}.pdf"'
    return response

def download_csv(request, filename):
    csv_path = os.path.join(f"/home/pi/custompbx/custompbx/forms/forms_data/{filename}.csv")
    response = FileResponse(open(csv_path, 'rb'))
    response['Content-Type'] = 'text/csv'
    response['Content-Disposition'] = f'attachment; filename="{filename}.csv"'
    return response

@api_view(['POST'])
def client_invoice(request):
    
    data = request.data['details']
    
    # date_string = '12/13/2023'
    date_format = '%m/%d/%Y'
    current_date = datetime.today().strftime('%-d %b %Y').replace(" ", "")

    start_date = datetime.strptime(data[1], date_format) #datetime(2023, 12, 1)
    end_date = datetime.strptime(data[2], date_format) #datetime(2023, 12, 7) 
    
    if data[3] == "client":
        
        des_user = Client.objects.get(name=data[0])
        destinations = Destinations.objects.filter(user=des_user)
        
        client = des_user
        
    elif data[3] == "destintaion":
        destinations = Destinations.objects.filter(number=data[0][2:])
        
        clients = destinations[0].user.all()

        if clients.exists():
            client = clients.first()
            
        des_user = client
    
    total_destintaions = {}
    
    table_monthly = False
    table_freecalls = False
    table_freemins = False
    
    for destination in destinations:
        destination_data = {}
        
        print("Destination: ", f"49{destination.number}")
        
        post_data = {'details': ['calculate_des', f"49{destination.number}", start_date, end_date]}
        response = requests.post('http://138.201.188.127:8000/api_req/', data=post_data)
        content = response.content.decode()
        decoded_list = ast.literal_eval(content)
        
        total_min = float(decoded_list[1])
        
        total_calls = float(decoded_list[0])
        
        # og = float(destination.call_price.replace(".","").replace(",", "."))
        # print("PRICE OG: ", og)
        # print("MIN OG: ", total_min, "PRICE / 60: ", og/60)
        
        total_cost = (float(destination.call_price.replace(".","").replace(",", ".")) / 60) * total_min
        
        destination_data["min"] = convert_min(total_min)
        destination_data["total"] = total_cost
        
        destination_data["total_calls"] = total_calls
        # destination_data["min_og"] = int(total_min) // 60
        destination_data["min_og"] = total_min
        destination_data["des_name"] = destination.name
        destination_data["des_num"] = destination.number
        destination_data["price_min"] = destination.call_price
        destination_data["monthly_fee"] = destination.monthly_fees
        destination_data["t_freecalls"] = destination.free_calls
        destination_data["t_freemins"] = destination.free_mins
        destination_data["price_pc"] = destination.price_percall
        
        destination_data["monthly_bool"] = destination.monthly_fee
        destination_data["freecall_bool"] = destination.free_call
        destination_data["freemin_bool"] = destination.free_min
        
        if destination.monthly_fee:
            table_monthly = True
        if destination.free_call:
            table_freecalls = True
        if destination.free_min:
            table_freemins = True
        
        total_destintaions[f"49{destination.number}"] = destination_data
        
    # client_pdf(total_destintaions, des_user.company_name, des_user.street, des_user.place,
    #            des_user.country, f"{end_date.strftime('%d/%m/%Y')}",
    #            f"{start_date.strftime('%d/%m/%Y')} - {end_date.strftime('%d/%m/%Y')}",
    #            f"{des_user.name}_{current_date}")
    
    highest_id = Invoices.objects.all().aggregate(Max('invoice_number'))['invoice_number__max']
    
    if highest_id is not None:
        invoice_number = int(highest_id) + 1
    else:
        invoice_number = 10000
    
    new_invoice = Invoices(invoice_number = invoice_number)
    
    new_invoice.save()
    
    new_invoice.destinations.set(destinations)
    new_invoice.user.add(client)
    
    gen_clientinvoice(total_destintaions, des_user.company_name, des_user.street, des_user.place,
               des_user.country, f"{end_date.strftime('%d/%m/%Y')}",
               f"{start_date.strftime('%d/%m/%Y')} - {end_date.strftime('%d/%m/%Y')}",
               f"{des_user.name}_{current_date}", table_freemins, table_freecalls,
               table_monthly, invoice_number)
        
    # print("FINAL DATA: ", total_destintaions)
        
    return Response({"message":f"{des_user.name}_{current_date}"})


@api_view(['POST'])
def convert_csv(request):
    data = request.data['form_data']
    
    form_m = FormData.objects.filter(form_name=data[0])
    
    if not form_m:
        return Response({"message":"No Data"})
    
    mdict = form_m[0].form_data
    
    keys = list(mdict.keys())
    values = list(mdict.values())

    # Combine keys and values for writing to the CSV file
    rows = list(zip(keys, values))
    
    location = f"/home/pi/custompbx/custompbx/forms/forms_data/{form_m[0].form_name}.csv"
    
    with open(location, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        
        # Write headers
        csv_writer.writerow(['Field', 'Value'])
        
        # Write data rows
        csv_writer.writerows(rows)
    
    return Response({"message":f"{form_m[0].form_name}"})
    
    
    
@api_view(['POST'])
def create_invoice(request):
    
    data = request.data['details']
    
    # date_string = '12/13/2023'
    date_format = '%m/%d/%Y'

    start_date = datetime.strptime(data[1], date_format) #datetime(2023, 12, 1)
    end_date = datetime.strptime(data[2], date_format) #datetime(2023, 12, 7) 
    
    post_data = {'details': ['calculate_des', data[0], start_date, end_date]}
    response = requests.post('http://138.201.188.127:8000/api_req/', data=post_data)
    content = response.content.decode()
    decoded_list = ast.literal_eval(content)
    
    destination = Destinations.objects.filter(number=data[0][2:])
    
    if destination:
        
        current_user = destination[0].user.all()[0]
    
        total_min = float(decoded_list[1])
        
        total_calls = float(decoded_list[0])

        # print("PRICE LIST: ", decoded_list)
        
        # Calculate total_cost
        total_cost = (float(destination[0].call_price) / 60) * total_min

        current_date = datetime.today().strftime('%-d %b %Y').replace(" ", "")
        
        # print("DETAILS: ", current_user.company_name, current_user.street,
        #              current_user.place, current_user.country,
        #              destination[0].name, destination[0].number,
        #              destination[0].call_price, total_min, total_cost,
        #              f"{current_user.name} {current_date}", data)
        
        generate_pdf(company = current_user.company_name, street = current_user.street,
                    plz = current_user.place, city = current_user.country,
                     
                    min = convert_min(total_min),total = total_cost, 
                    output =  f"{current_user.name}_{current_date}",
                     
                    total_calls = total_calls, 
                    min_og = int(total_min) // 60,
                    des_name = destination[0].name, 
                    des_num = destination[0].number,
                    price_min = destination[0].call_price,
                    monthly_fee = destination[0].monthly_fees, 
                    t_freecalls = destination[0].free_calls,
                    t_freemins = destination[0].free_mins,
                    price_pc = destination[0].price_percall, 
                    monthly_bool = destination[0].monthly_fee,
                    freecall_bool = destination[0].free_call,
                    freemin_bool = destination[0].free_min,
                    
                    service_period = f"{start_date.strftime('%d/%m/%Y')} - {end_date.strftime('%d/%m/%Y')}",
                    invoice_date = f"{end_date.strftime('%d/%m/%Y')}")
        
        # filename = f"{current_user.name}_{current_date}"
        
        return Response({"message":f"{current_user.name}_{current_date}"})
    
    else:
    
        return Response({"message":"Destination not found"})

@api_view(['POST'])
def assign_diss(request):
    
    data = request.data['details']
    
    # print("DATA: ", data, "TYPE: ", type(data))
    
    cc = Client.objects.get(name=data[0])
    
    D_new = Destinations(number=data[1], name=data[2])
    
    # D_new = Destinations(user=cc, number=data[1], name=data[2])
    
    D_new.save()
    
    D_new.user.add(cc)
    
    return Response("DONE !")

@api_view(['POST'])
def create_contact(request):
    data = request.data['details']
    
    user = request.user
    
    client_ins = Client.objects.get(user=user)
    
    destination = Destinations.objects.filter(user=client_ins,name=data[3])
    
    if not destination:
    
        return Response("NO DESTINATION")
    
    else:
    
        D = UserContact(name=data[0],email=data[1],phone=data[2])
        
        # D = UserContact(user=client_ins, destination=destination[0],name=data[0],email=data[1],phone=data[2])
        
        D.save()
        
        D.user.add(client_ins)
        D.destination.add(destination[0])
        
        return Response("Created")

@api_view(['POST'])
def create_product(request):
    data = request.data['details']
    
    user = request.user
    
    client_ins = Client.objects.get(user=user)
    
    destination = Destinations.objects.filter(user=client_ins,name=data[4])
    
    # P = UserProduct(user=client_ins, destination=destination,name=data[0],number=data[1],sales_price=data[2],purchase_price=data[3])
    
    P = UserProduct(name=data[0],
                    number=data[1],sales_price=data[2],
                    purchase_price=data[3], tax=data[5], 
                    shipping=data[6], other=data[7])
    
    P.save()
    
    P.user.add(client_ins)
    P.destination.add(destination[0])
    
    return Response("Created")

@api_view(['POST'])
def change_pstatus(request):
    data = request.data['details']
    
    user = request.user
    
    client_ins = Client.objects.get(user=user)
    
    my_product = UserProduct.objects.filter(user=client_ins,number=data)
    
    if my_product:
        
        my_p = my_product[0]
    
        if my_p.status:
            my_p.status = False
            my_p.save()
        else:
            my_p.status = True
            my_p.save()
            
        return Response("Status Updated")
        
    else:
    
        return Response("No Product")

@api_view(['POST'])
def fetchDissinfo(request):
    data = request.data['details']
    
    d_message = Disappearing_info.objects.get(name=data)
    
    return Response([d_message.name, d_message.disappearing_time.strftime('%d/%m/%Y %H:%M'), d_message.info])


@login_required(login_url=reverse_lazy('form_login'))
def setup_wizard(request):
    
    gateways = Sip_trunks.objects.all()
            
    context = {"gateways":gateways}
    
    return render(request, 'forms/easyform.html', context)

def createqueue(request):
    if request.method == 'POST':
        queue_name = request.POST.get('queue_name')
        queue_ext = request.POST.get('queue_ext')
        moh_sounds = request.POST.get('moh_sounds')
        queue_desc = request.POST.get('queue_desc')
        
        
        create_queue(queue_name, queue_ext, 
                    queue_name, queue_desc, moh_sounds)

        # Return a JSON response indicating success
        return JsonResponse({'message': 'Queue created successfully'})

    # Return a 404 error if the request method is not POST
    return JsonResponse({'error': 'Method not allowed'}, status=404)

def createconference(request):
    if request.method == 'POST':
        conf_name = request.POST.get('conf_name')
        conf_ext = request.POST.get('conf_ext')
        conf_desc = request.POST.get('conf_desc')
        
        
        create_conference(conf_name, conf_ext, conf_desc)

        # Return a JSON response indicating success
        return JsonResponse({'message': 'Conference created successfully'})

    # Return a 404 error if the request method is not POST
    return JsonResponse({'error': 'Method not allowed'}, status=404)

def createdestination(request):
    if request.method == 'POST':
        des_number = request.POST.get('destination_number')
        des_action = request.POST.get('des_action')
        des_domain = request.POST.get('des_domain')
        banner_color = request.POST.get('banner_color')
        font_color = request.POST.get('font_color')
        destination_url = request.POST.get('destination_url')
        destination_desc = request.POST.get('destination_desc')
        
        description = f"{destination_desc},{font_color},{banner_color},{destination_url}"
        
        create_destination(des_number, des_action, description, des_domain)

        # Return a JSON response indicating success
        return JsonResponse({'message': 'Destination created successfully'})

    # Return a 404 error if the request method is not POST
    return JsonResponse({'error': 'Method not allowed'}, status=404)

@api_view(['POST'])
def get_mohsounds(request):
    data = request.data['details']
    
    options = moh_options()
    
    return Response(options)

@api_view(['POST'])
def fetchdestination_data(request):
    data = request.data['details']
    
    options = destination_options()
    
    return Response(options)

@api_view(['POST'])
def get_numbers(request):
    
    data = request.data['details']
    
    # print("DATA: ", data, "TYPE: ", type(data))
    
    post_data = {'details': data}
    response = requests.post('http://138.201.188.127:8000/api_req/', data=post_data)
    content = response.content
    
    return Response(content)

def upload_music(request):
    path = "/home/pi/custompbx/forms/music_on_hold/"
    if request.method == 'POST':
        music_name = request.POST.get('music_name')
        music_file = request.FILES.get('music_file')

        # Get the file extension from the filename
        file_extension = music_file.name.split('.')[-1]

        # Create a new filename with the extension
        filename = f"{music_name}.{file_extension}"

        # Save the file to the filesystem
        fs = FileSystemStorage(location=path)
        with fs.open(filename, 'wb+') as destination:
            for chunk in music_file.chunks():
                destination.write(chunk)

        # Return the URL of the uploaded file
        uploaded_file_url = fs.url(filename)
        
        retruned_msg = upload_moh(f"{path}{filename}", music_name)

        return JsonResponse({'status': 'success', 'api_response': retruned_msg})

    return render(request, 'upload_music.html')