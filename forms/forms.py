from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# form-control

# class CreateUserForm(UserCreationForm):
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password1', 'password2']

class CreateUserForm(UserCreationForm):
    
    COUNTRY_CHOICES = (
        ('Select Country', 'Select Country'),
        ('Germany', 'Germany'),
        ('Switzerland', 'Switzerland'),
        ('Austria', 'Austria'),
    )
    
    username = forms.CharField(label='Name', required=True)
    email_address = forms.CharField(label='Email Address', required=True)
    street = forms.CharField(label='Street', required=True)
    zip_code = forms.CharField(label='ZIP Code', required=True)
    city = forms.CharField(label='City', required=True)
    tax_number = forms.CharField(label='Tax Number', required=False)
    company_name = forms.CharField(label='Company Name', required=True)
    country = forms.ChoiceField(choices=COUNTRY_CHOICES, widget=forms.Select(attrs={'class': 'form-selectnew'}))
    invoice_email_address = forms.CharField(label='Invoice Email Address', required=False)

    class Meta:
        model = User
        fields = ['username', 'email_address', 'password1', 'password2', 'street', 'zip_code', 'city', 'tax_number', 'invoice_email_address', 'company_name', 'country']