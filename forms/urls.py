from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views

urlpatterns = [
    
    path('form-builder/', views.index, name="create_form"),
    path('save_html/', views.save_html, name='save_html'),
    path('assign_form/', views.assign_form, name='assign_form'),
    path('delete_form/', views.delete_form, name='delete_form'),
    path('add_emails/', views.add_emails, name='add_emails'),
    path('edit_formdetails/', views.edit_formdetails, name='edit_formdetails'),
    path('send_emails/', views.send_emails, name='send_emails'),
    path('delete_email/', views.delete_email, name='delete_email'),
    path('forms/<str:fname>/<str:dname>/<str:phone>/', views.render_form, name='forms'),
    path('forms/<str:fname>/<str:dname>/', views.render_form, name='default_forms'),
    
    path('admin_dashboard/', views.admin_dash, name="admin_dash"),
    
    path('create_invoice/', views.create_invoice, name="create_invoice"),
    path('client_invoice/', views.client_invoice, name="client_invoice"),
    path('download_invoice/<str:filename>/', views.download_pdf, name='download_pdf'),
    
    path('getuserdetails/', views.getuserdetails, name="getuserdetails"),
    path('update_client/', views.update_client, name="update_client"),
    
    path('', views.home, name="home"),
    path('home/<str:pk>/', views.home_sorted, name="home_sorted"),
    
    path('settings/', views.dashboard, name="settings"),
    path('dashboard/<str:pk>/', views.dashboard_sorted, name="dashboard_sorted"),
    
    path('form_login/', views.loginPage, name="form_login"),  
    path('form_register/', views.registerPage, name="form_register"),
    path('form_logout/', LogoutView.as_view(next_page="form_login"), name='form_logout'),

    path('create_diss/', views.createDissinfo, name="create_diss"),
    path('edit_diss/', views.EditDissinfo, name="edit_diss"),
    path('delete_diss/', views.delete_diss, name="delete_diss"),
    path('fetch_diss/', views.fetchDissinfo, name="fetch_diss"),
    path('assign_diss/', views.assign_diss, name="assign_diss"),
    
    path('create_contact/', views.create_contact, name="create_contact"),
    
    path('create_product/', views.create_product, name="create_product"),
    path('change_pstatus/', views.change_pstatus, name="change_pstatus"),
    
    path('get_settings/', views.get_settings, name="get_settings"),
    
    path('update_settings/', views.update_settings, name="update_settings"),
    
    path('get_destinations/', views.get_destinations, name="get_destinations"),
    path('get_destination/', views.get_destination, name="get_destination"),
    
    path('destination_data/', views.destination_data, name="destination_data"),
    path('destination_sorted/', views.destination_sorted, name="destination_sorted"),
    
    path('update_des_price/', views.update_des_price, name="update_des_price"),
    path('fetch_des_settings/', views.fetch_des_settings, name="fetch_des_settings"),
    
    path('chart_data/', views.chart_data, name="chart_data"),
    path('destination_chart/', views.destination_chart, name="destination_chart"),
    
    path('diss_info/', views.diss_info, name="diss_info"),
    
    path('general_info/', views.general_info, name="general_info"),
    
    path('login_asuser/', views.login_asuser, name="login_asuser"),
    path('login_as_user/<int:user_id>/', views.login_as_user, name='login_as_user'),
    
    path('fusion_login/', views.fusion_login, name="fusion_login"),
    
    path('create_agent/', views.create_agent, name="create_agent"),
    path('get_agent/', views.get_agent, name="get_agent"),
    path('edit_agent/', views.edit_agent, name="edit_agent"),
    path('delete_agent/', views.delete_agent, name="delete_agent"),
    path('agent_status/', views.agent_status, name="agent_status"),
    path('change_agent_status_admin/', views.change_agent_status_admin, name="change_agent_status_admin"),
    path('agents/', views.agents, name="agents"),
    
    path('convert_csv/', views.convert_csv, name="convert_csv"),
    path('download_csv/<str:filename>/', views.download_csv, name='download_csv'),
    
    path('csv_upload/', views.csv_upload, name='csv_upload'),
    path('csv_viewer/', views.csv_viewer, name="csv_viewer"),
    path('csv_viewer/<str:pk>/', views.specific_csv, name='specific_csv'),
    path('del_csv/', views.del_csv, name='del_csv'),
    path('down_csv/<str:filename>/', views.down_csv, name='down_csv'),
    path('down_pdf/<str:filename>/', views.down_pdf, name='down_pdf'),
    
    path('setup_wizard/', views.setup_wizard, name="setup_wizard"),
    path('create_gateway/', views.create_gateway, name="create_gateway"),
    
    path('create_client/', views.create_client, name="create_client"),
    path('get_numbers/', views.get_numbers, name="get_numbers"),
    
    path('upload_music/', views.upload_music, name="upload_music"),
    path('get_mohsounds/', views.get_mohsounds, name="get_mohsounds"),
    
    path('create_queue/', views.createqueue, name="create_queue"),
    path('create_conference/', views.createconference, name="create_conference"),
    
    path('get_destination_data/', views.fetchdestination_data, name="get_destination_data"),
    path('create_destination/', views.createdestination, name="create_destination"),
    
    path('exin_transfer/', views.exin, name="exin_transfer"),
    
    path('call_stats/', views.call_stats, name="call_stats"),
    
    path('search_agent/', views.search_agent, name="search_agent"),
    
    path('ivr_records/', views.ivr_records, name="ivr_records"),
]