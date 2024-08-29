from django.urls import path
from . import views

app_name='person'
urlpatterns=[
    path('add/<str:form_type>/', views.AddNew, name='addnew'),
    path('',views.HomeView, name='home'),
    path('all_models',views.all_models, name='allmodels'),
    
    path('events/<int:person>/', views.event_view,name='event_view'),
    path('profile/<int:pub_emp>/<int:pk>',views.profile_view,name='personal_profile')
    
]

