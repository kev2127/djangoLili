from django.urls import path 
from . import views
urlpatterns = [ 
    path('', views.home, name = 'home'),
    path('login/', views.login_user, name = 'login'),
    path('logout/', views.logout_user, name = 'logout'),
    path('register/', views.register_user, name = 'register'),
    path('record/<int:pk>', views.customer_record, name= 'record'),
    path('delete_record/<int:pk>', views.delete_record, name = 'delete_record'),
    path('add_record/', views.add_record, name = 'add_record'),
    path('update_record/<int:pk>', views.update_record, name = 'update_record'),
    path('agenda/', views.agenda, name='agenda'),
    path('delete_appointment/<int:pk>', views.delete_appointment, name='delete_appointment'),
    path('update_appointment/<int:pk>', views.update_appointment, name= 'update_appointment'),
]