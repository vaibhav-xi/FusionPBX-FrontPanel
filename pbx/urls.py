from django.contrib.auth.views import LogoutView
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name="pbx_home"),
    
    path('agents/', views.agents, name="agents"),
    path('records/', views.records, name="records"),
    path('admin_panel/', views.admin_page, name="adminpanel"),
    
    path('adminpanel/', views.AdminPanel, name="admin_panel"),
    path('dashboard/', views.dashboard, name="dashboard"),
    
    path('pbx_login/', views.Login, name="pbx_login"),
    path('pbx_register/', views.Register, name="pbx_register"),
    path('pbx_logout/', LogoutView.as_view(next_page="login"), name='pbx_logout'),
    
    path('make_call/', views.Make_Call, name="make_call"),
    
    path('get_data/', views.fetch_data, name="get_users"),
    
    path('uuid_transfer/', views.uuid_transfer, name="uuid_transfer"),
    path('uuid_transfer_fwd/', views.uuid_transfer_fwd, name="uuid_transfer_fwd"),
    path('cmd_transfer/', views.ctransfer, name="cmd_transfer"),
    path('forward_call/', views.forwardroom, name="forwardroom"),
    path('algo_m/', views.mute_fun, name="algo_m"),
    
    path('exin_transfer/', views.exin, name="cmd_transfer"),
    path('mod_conference/', views.conference, name="mod_conference"),
    path('activecalls/', views.active_calls, name="active_calls"),
    
    path('save_agent/', views.save_agent, name="save_agent"),
    
    path('fetch_agent/', views.fetch_agents, name="fetch_agent"),
    path('realtime_data/', views.realtime_data, name="realtime_data"),
    
    path('admin_data/', views.send_admindata, name="admin_data"),
    path('agents/', views.agents, name="agents"),
    
    path('rcs/', views.Test, name="rcs"),
    
    path('dump_call/', views.dump_call, name="dump_call"),
    path('outbound_call/', views.outbound_call, name="outbound_call"),
    
    path('forward_records/', views.forward_records, name="forward_records"),
    
    path('records/<str:pk>/', views.call_flow_records, name="call_flow_records"),
    path('agent_logs/', views.agent_records, name="agent_logs"),
    
    path('uuid_kill/', views.uuid_kill, name="uuid_kill"),
]

