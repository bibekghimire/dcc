from django.urls import path
from . import views

app_name='services'
urlpatterns=[
    path('',views.home_view,name='home'),
    path('service/<int:pk>',views.service_view,name='service_view')
]