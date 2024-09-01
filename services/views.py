from django.shortcuts import render

from . models import Service
# Create your views here.

def home_view(request):
    services=Service.objects.all()
    context={'services':services}
    return render(request,'services/home_view.html',context)

