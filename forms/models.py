from django.db import models
from django.contrib.auth.models import User

# Create your models here.
    
class Client(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, null=True, default="", blank=True, on_delete=models.CASCADE)
    # User Details
    name = models.CharField(max_length=200, null=True, default="")
    email = models.CharField(max_length=200, null=True, default="")
    invoice_email = models.CharField(max_length=200, null=True, default="")
    street = models.CharField(max_length=500, null=True, default="")
    country = models.CharField(max_length=200, null=True, default="")
    zip_code = models.CharField(max_length=200, null=True, default="")
    place = models.CharField(max_length=500, null=True, default="")
    company_name = models.CharField(max_length=200, null=True, default="")
    tax_num = models.CharField(max_length=200, null=True, default="")
    
    #Toggle Features
    daily_stats = models.BooleanField(default=False)
    weekly_stats = models.BooleanField(default=False)
    monthly_stats = models.BooleanField(default=False)
    imp_info = models.BooleanField(default=False)
    diss_info = models.BooleanField(default=False)
    sales = models.BooleanField(default=False)
    invoice_creation = models.BooleanField(default=False)
    form_fun = models.BooleanField(default=False)
    
    #Costs
    call_price = models.CharField(max_length=200, null=True, default="0")
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.name)
    
class Destinations(models.Model):
    user = models.ManyToManyField(Client, blank=True)
    name = models.CharField(max_length=200, null=True, default="")
    number = models.CharField(max_length=200, unique=True, default="")
    email = models.CharField(max_length=200, null=True, default="")
    
    call_price = models.CharField(max_length=200, null=True, default="0") #Price per_min
    price_percall = models.CharField(max_length=200, null=True, default="0")
    
    forward_destination = models.CharField(max_length=200, null=True, default="0")
    forward_seconds = models.CharField(max_length=200, null=True, default="0")
    
    fd_cost = models.CharField(max_length=200, null=True, default="0")
    forward_number = models.CharField(max_length=200, null=True, default="+916269106539")
    
    free_calls = models.IntegerField(null=True, default=0)
    free_mins = models.IntegerField(null=True, default=0)
    monthly_fees = models.IntegerField(null=True, default=0)
    
    monthly_fee = models.BooleanField(default=False)
    free_call = models.BooleanField(default=False)
    free_min = models.BooleanField(default=False)
    
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.number)
    
class Invoices(models.Model):
    user = models.ManyToManyField(Client, blank=True)
    invoice_number = models.CharField(max_length=200, null=True, default="0")
    destinations = models.ManyToManyField(Destinations, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.invoice_number)
    
class ForwardRoom(models.Model):
    room_number = models.CharField(max_length=200, null=True, default="0")
    time = models.CharField(max_length=200, null=True, default="0")
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.room_number) + str(self.date_created)
    
class Sip_trunks(models.Model):
    sip_provider = models.CharField(max_length=200, null=True, default="")
    start = models.CharField(max_length=200, null=True, default="0")
    end = models.CharField(max_length=200, null=True, default="0")
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.sip_provider)
    
class UserContact(models.Model):
    user = models.ManyToManyField(Client, blank=True)
    destination = models.ManyToManyField(Destinations, blank=True)
    name = models.CharField(max_length=200, null=True, default="")
    email = models.CharField(max_length=200, null=True, default="")
    phone = models.CharField(max_length=200, null=True, default="")
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.name)
    
class Agents(models.Model):
    name = models.CharField(max_length=200, null=True, default="")
    street = models.CharField(max_length=200, null=True, default="")
    zip_code = models.CharField(max_length=200, null=True, default="")
    city = models.CharField(max_length=200, null=True, default="")
    email = models.CharField(max_length=200, null=True, default="")
    tax_num = models.CharField(max_length=200, null=True, default="")
    sales_tax = models.CharField(max_length=200, null=True, default="19")
    account_name = models.CharField(max_length=200, null=True, default="")
    bank_name = models.CharField(max_length=200, null=True, default="")
    iban = models.CharField(max_length=200, null=True, default="")
    bic = models.CharField(max_length=200, null=True, default="")
    phone = models.CharField(max_length=200, null=True, default="")
    country_code = models.CharField(max_length=200, null=True, default="+49")
    pin = models.CharField(max_length=200, null=True, default="0")
    passive_mins = models.CharField(max_length=200, null=True, default="0")
    active_mins = models.CharField(max_length=200, null=True, default="0")
    status = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.name)
    
class UserProduct(models.Model):
    user = models.ManyToManyField(Client, blank=True)
    destination = models.ManyToManyField(Destinations, blank=True)
    name = models.CharField(max_length=200, null=True, default="")
    number = models.CharField(max_length=200, null=True, default="")
    shipping = models.CharField(max_length=200, null=True, default="")
    sales_price = models.CharField(max_length=200, null=True, default="")
    tax = models.CharField(max_length=200, null=True, default="")
    other = models.CharField(max_length=200, null=True, default="")
    status = models.BooleanField(default=False)
    purchase_price = models.CharField(max_length=200, null=True, default="")
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.name)
    
    
class UserOrder(models.Model):
    product = models.ManyToManyField(UserProduct, blank=True)
    user = models.ManyToManyField(Client, blank=True)
    order_id = models.CharField(max_length=200, null=True, default="")
    status = models.CharField(max_length=200, null=True, default="")
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.order_id)
    
class CallStat(models.Model):
    destination = models.ManyToManyField(Destinations, blank=True)
    number = models.CharField(max_length=200, null=True, default="")
    name = models.CharField(max_length=200, null=True, default="")
    total_time = models.CharField(max_length=200, null=True, default="")
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.name)
    
class Disappearing_info(models.Model):
    name = models.CharField(max_length=200, null=True, default="")
    destination = models.ManyToManyField(Destinations, blank=True)
    # info = models.CharField(max_length=200, null=True, default="")
    info = models.TextField(default='')
    disappearing_time = models.DateTimeField(null=False)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.name)
     
class Disappearing_record(models.Model):
    name = models.CharField(max_length=200, null=True, default="")
    destination = models.ManyToManyField(Destinations, blank=True)
    # info = models.CharField(max_length=200, null=True, default="")
    info = models.TextField(default='')
    disappearing_time = models.DateTimeField(null=False)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.name)
    
class User_forms(models.Model):
    name = models.CharField(max_length=200, null=True, default="")
    emails = models.JSONField(default=dict)
    form_client = models.ManyToManyField(Client, blank=True)
    cid = models.CharField(max_length=200, null=True, default="")
    destination = models.ManyToManyField(Destinations, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.name)
    
class General_info(models.Model):
    destination = models.ManyToManyField(Destinations, blank=True)
    # welcome_text = models.CharField(max_length=200, null=True, default="")
    # imp_info = models.CharField(max_length=200, null=True, default="")
    welcome_text = models.TextField(default='')
    imp_info = models.TextField(default='')
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return str(self.welcome_text)
    
class FormData(models.Model):
    form_name = models.CharField(max_length=200, null=True, default="")
    form_data = models.JSONField()
    
    def __str__(self):
        return str(self.form_name)