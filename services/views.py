from django.shortcuts import render, get_object_or_404


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
