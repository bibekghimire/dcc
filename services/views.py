from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from .serializers import ServiceSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser,AllowAny

from . models import Service
# Create your views here.

def home_view(request):
    services=Service.objects.all()
    context={'services':services}
    return render(request,'services/home_view.html',context)

def service_view(request, pk):
    services=Service.objects.all()
    active_service=get_object_or_404(services,id=pk)
    context={
        'services':services,
        'active_service':active_service,
        }
    return render(request,'services/serv_detail.html',context)

class ServiceViewSet(viewsets.ModelViewSet):
    queryset=Service.objects.all()
    serializer_class=ServiceSerializer
    def get_permissions(self):
        if self.action == 'create':
            # Only staff users can create
            permission_classes = [IsAuthenticated, IsAdminUser]
        elif self.action in ['update', 'partial_update', 'destroy']:
            # Only staff users can update or delete
            permission_classes = [IsAuthenticated, IsAdminUser]
        else:
            # Allow unauthenticated users to only view (GET)
            permission_classes = [AllowAny]  # Allow read-only for everyone (unauthenticated or authenticated)
        
        return [permission() for permission in permission_classes]
    



