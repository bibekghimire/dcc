from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(f'service',views.ServiceViewSet)

app_name='services'
urlpatterns=[
    path('',views.home_view,name='home'),
    path('service/<int:pk>',views.service_view,name='service_view'),
    path('/api/',include(router.urls)),
] 