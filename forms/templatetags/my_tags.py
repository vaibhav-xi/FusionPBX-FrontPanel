from django import template
from datetime import datetime

register = template.Library()

def format_date(my_date):
    # Parse ISO 8601 datetime string
    dt = datetime.fromisoformat(my_date)
    
    # Format datetime as desired, e.g., "Jun 22, 2024 13:21:21"
    formatted_datetime = dt.strftime('%b %d, %Y %H:%M:%S')
    
    return formatted_datetime

def subtract_dates(endtime, starttime):
    # Parse the date strings into datetime objects
    date_format = "%b %d, %Y %H:%M:%S"
    date2 = datetime.strptime(endtime, date_format)
    date1 = datetime.strptime(starttime, date_format)
    
    # Calculate the difference
    difference = date2 - date1
    
    # Format the timedelta object as HH:MM:SS
    seconds = difference.total_seconds()
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    
    return f"{hours:02}:{minutes:02}:{seconds:02}"

country_list = ['+49']

@register.filter
def get_item(list, index):
    return list[index]

@register.filter
def check_agent(country_code, number):
    if str(country_code) in country_list:
        return number
    else:
        return f"{country_code}{number}"

@register.filter
def replace_plus(my_str):
    return str(my_str).replace("+", "")
    
@register.filter
def calc_time_difference(main_list):
    return subtract_dates(format_date(main_list[11]), format_date(main_list[10]))

@register.filter
def format_datetime(list, index):
    # Parse ISO 8601 datetime string
    dt = datetime.fromisoformat(list[index])
    
    # Format datetime as desired, e.g., "Jun 22, 2024 13:21:21"
    formatted_datetime = dt.strftime('%b %d, %Y %H:%M:%S')
    
    return formatted_datetime