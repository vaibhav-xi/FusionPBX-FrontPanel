from django.contrib.auth import authenticate, login, logout, get_user_model
from django.db.models.functions import ExtractYear, ExtractMonth
from django.contrib.auth.decorators import login_required
from django.db.models.functions import Now, TruncDate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from email.mime.multipart import MIMEMultipart
from django.shortcuts import redirect, render
from django.http import FileResponse, HttpResponseRedirect
from rest_framework.response import Response
from datetime import datetime, timedelta, date
from django.db.models import Count, Sum
from django.core.mail import send_mail
from .create_pdf import generate_pdf
from email.mime.text import MIMEText
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import render
from django.utils import timezone
from django.conf import settings
from bs4 import BeautifulSoup
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
            return "Invalid input. Please provide a valid integer or a string that can be converted to an integer."
    else:
        seconds = round(float(input_value), 2)

    # Calculate minutes and seconds
    minutes = int(seconds // 60)
    remaining_seconds = seconds % 60

    # Format minutes and seconds with leading zeros
    formatted_time = "{:02d}:{:05.2f}".format(minutes, remaining_seconds)

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
   
   
@login_required(login_url=reverse_lazy('login'))
def login_asuser(request):
    
    user = request.user
    
    if user.is_staff:
        
        users = User.objects.all()
        
        context = {"users":users}
        
        return render(request, 'dashboard/login_asuser.html', context)
    
    else:
        
        return render(request, 'dashboard/error.html', context)

def login_as_user(request, user_id):
    User = get_user_model()
    try:
        user = User.objects.get(id=user_id)
        login(request, user)
        messages.success(request, f"Logged in as {user.username}")
    except User.DoesNotExist:
        messages.error(request, "User does not exist")
    
    return redirect('home') 

         
@login_required(login_url=reverse_lazy('login'))
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
    
    return render(request, 'dashboard/home.html', context)

@login_required(login_url=reverse_lazy('login'))
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
            des = Destinations.objects.filter(user=client)

            des_list = [
                
                {
                    "number": f"49{dess.number}",
                    "cost": dess.call_price
                }
                
                for dess in total_destinations
            ]
            
            print("TOTAL DES: ", des_list)
            
            # grand_min = 0
            # grand_calls = 0
            # grand_avg = 0
            # grand_total = 0
            
            for d in des_list:
    
                post_data = {'details': ['calculate_des', d["number"]]}
                response = requests.post('http://138.201.188.127:8000/api_req/', data=post_data)
                content = response.content.decode()
                decoded_list = ast.literal_eval(content)
            
                total_min = float(decoded_list[1])
                grand_min += total_min
                
                # Calculate total_cost
                total_cost = (float(d["cost"]) / 60) * total_min
                grand_total += total_cost
                
                grand_avg += float(decoded_list[2])
                grand_calls += float(decoded_list[0])
                
            # print(f"""
                  
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
               "orders":orders, "total_amount":total_cost, 
               "total_profit":round(profit, 2), "total_money":total_money, "pk":o,
                "welcome_text":wlc_text, "important_text":imp_text,
                "general_date":general_date, "form_fun":form_f,
                "overlap":overlap, "total_destinations":total_destinations,
                "gm":convert_min(grand_min).replace(".", ":"),
                "gc":str(grand_calls).replace(".", ","),
                "ga":str(convert_min(grand_avg)).replace(".", ":"),
                "gt":str(round(grand_total, 2)).replace(".", ","), "tdes":tdes}
    
    return render(request, 'dashboard/home.html', context)


@api_view(['POST'])
def destination_chart(request):
    
    data = request.data['details']
    
    post_data = {'details': data}
    response = requests.post('http://138.201.188.127:8000/api_req/', data=post_data)
    content = response.content
    
    return Response(content)

@api_view(['POST'])
@login_required(login_url=reverse_lazy('login'))
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
@login_required(login_url=reverse_lazy('login'))
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
        file_path = os.path.join('/home/pi/fusion_panel/fusion_dashboard/dashboard/templates/dashboard/', filename)  # Replace with your desired file path
        
        with open(file_path, 'w') as file:
            file.write(content)
        
        my_form = User_forms(name=mform_name)
        
        my_form.save()
        
        my_form.form_client.add(client_ins[0])
        
        # return render(request, "dashboard/dashboard.html")
    
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
        
        file_path = f"/home/pi/fusion_panel/fusion_dashboard/dashboard/templates/dashboard/{data[0]}.html"  # Replace with the actual path to your file

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
        
        return Response("Delete Successful")
    
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
    
    user_form = User_forms.objects.filter(name=fname, destination=my_des[0])
    
    gi = General_info.objects.filter(destination=my_des[0])
    
    important_info = gi[0].imp_info if gi else "Empty"
    
    welcome_text = gi[0].welcome_text if gi else "Empty"
    
    di = Disappearing_info.objects.filter(destination=my_des[0])
    
    disappearing_info = di[0].info if di else "Empty"
    
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
                for field, value in form_data.items():
                    # print("VALUES:", field, value)
                    if field not in check_list:
                        # print("INSIDE LOOP:", field, value)
                        table_body += f"""<tr><td>{field}</td><td>{'ja' if value == '1' else value}</td></tr>"""
                    elif field == "receiver_email":
                        receiver_email = extract_emails(value)
                        # receiver_email = ', '.join(receiver_emails)
                        
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
                
                    # print("EMAILS: ", mail, type(mail))
                    server.sendmail(from_email, mail, email.as_string())

                server.sendmail(from_email, bcc_email, email.as_string())

            print('Email sent successfully.')
            
            return render(request, f'dashboard/form_success.html')

        except Exception as e:
            print(f'An error occurred while sending the email: {str(e)}')
            
            return render(request, f'dashboard/form_error.html')
        
        # send_mail('Test Email', 'This is a test email.', settings.DEFAULT_FROM_EMAIL, ['vaibhav28890@gmail.com'],fail_silently=False,)
    
    if user_form:
        
        filename = user_form[0].name
        
        # path = f"/home/pi/fusion_panel/fusion_dashboard/static/user_forms/{filename}.html"
        
        # print("FILEPATH", path)
        
        # a = "home"
        
        emails = user_form[0].emails
        
        phone = '' if phone is None else phone
        
        context = {"phone_number":phone, "important_info":important_info,
                   "disappearing_info":disappearing_info, "data":emails,
                   "welcome_text":welcome_text}
    
        return render(request, f'dashboard/{filename}.html', context)

    else:
        
        context = {}
        
        return render(request, 'dashboard/home.html', context)

@login_required(login_url=reverse_lazy('login'))
def index(request):
    
    user = request.user
    
    client_instance = Client.objects.get(user=user)
    
    return render(request, 'dashboard/index.html', {"client_name":client_instance.name})

def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password =request.POST.get('password')

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
    return render(request, 'dashboard/login.html', context)

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

            messages.success(request, 'Account was created for ' + name)

            return HttpResponseRedirect('/login/')
        else:
            # If the form is not valid, display an error message
            error_message = "Registration failed. Please correct the errors below."
            form_errors = form.errors.as_text()
            messages.error(request, error_message + "\n" + form_errors)
            # messages.error(request, error_message)
        
    context = {'form':form}
    
    return render(request, 'dashboard/register.html', context)

@login_required(login_url=reverse_lazy('login'))
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
    
    return render(request, 'dashboard/dashboard.html', context)

@login_required(login_url=reverse_lazy('login'))
def admin_dash(request):
    
    customers = Client.objects.all()
    
    destinations = Destinations.objects.all()
    
    orders = UserOrder.objects.all()
    
    records = Disappearing_record.objects.all()
            
    context = {"destinations":destinations, 'customers':customers,
               "orders":orders, "records":records}
    
    return render(request, 'dashboard/admin.html', context)

@login_required(login_url=reverse_lazy('login'))
def dashboard_sorted(request, pk):
    user = request.user
    
    overlap = "none"
    
    client_ins = Client.objects.get(user=user)
    
    destinations = Destinations.objects.filter(user=client_ins, name=pk)
    
    total_destinations = Destinations.objects.filter(user=client_ins)
    
    passed_url = "http://94.237.84.206/forms"
    
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
    
    return render(request, 'dashboard/dashboard.html', context)

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
             "sales_sw":settings.sales}
    
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
    settings.call_price = details[6]
    settings.imp_info = details[7]
    settings.diss_info = details[8]
    settings.sales = details[9]
    
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
def update_des_price(request):
    
    data = request.data['save_price']
    
    my_destination = Destinations.objects.filter(name=data[0])
    
    if my_destination:
        my_destination[0].call_price = data[1]
        my_destination[0].save()
        
        return Response("Updated")
    else:
        return Response("No records")

@api_view(['POST'])
def destination_data(request):
    
    data = request.data['details']
    
    post_data = {'details': ['calculate_des', data]}
    response = requests.post('http://138.201.188.127:8000/api_req/', data=post_data)
    content = response.content
    
    return Response(content)

def download_pdf(request, filename):
    pdf_path = os.path.join(f"/home/pi/fusion_panel/fusion_dashboard/dashboard/invoices/{filename}.pdf")
    response = FileResponse(open(pdf_path, 'rb'))
    response['Content-Type'] = 'application/pdf'
    response['Content-Disposition'] = f'attachment; filename="{filename}.pdf"'
    return response

@api_view(['POST'])
def create_invoice(request):
    
    data = request.data['details']
    
    post_data = {'details': ['calculate_des', data]}
    response = requests.post('http://138.201.188.127:8000/api_req/', data=post_data)
    content = response.content.decode()
    decoded_list = ast.literal_eval(content)
    
    destination = Destinations.objects.filter(number=data[2:])
    
    if destination:
        
        current_user = destination[0].user.all()[0]
    
        total_min = float(decoded_list[1])

        # Calculate total_cost
        total_cost = (float(destination[0].call_price) / 60) * total_min

        current_date = datetime.today().strftime('%-d %b %Y').replace(" ", "")
        
        # print("DETAILS: ", current_user.company_name, current_user.street,
        #              current_user.place, current_user.country,
        #              destination[0].name, destination[0].number,
        #              destination[0].call_price, total_min, total_cost,
        #              f"{current_user.name} {current_date}", data)
        
        generate_pdf(current_user.company_name, current_user.street,
                     current_user.place, current_user.country,
                     destination[0].name, destination[0].number,
                     destination[0].call_price, convert_min(total_min), total_cost,
                     f"{current_user.name}_{current_date}")
        
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

