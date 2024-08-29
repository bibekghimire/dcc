from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from django.utils import timezone
# Create your views here.
from . import forms
from . import models

form_classes={
    'post':(forms.PostForm,models.Post),
    'section':(forms.SectionForm, models.Section),
    'employee':(forms.EmployeeForm, models.Employee),
    'public_representative':(forms.PublicRepresentativeForm,models.PublicRepresentative),
    'event':(forms.EventForm,models.Event),

}

def HomeView(request):
    public_representative=models.PublicRepresentative.objects.all().order_by('weight')[:5]
    employees=models.Employee.objects.all().order_by('weight')[:5]
    sections=models.Section.objects.all()[:5]
    return render(request,'person/home.html',{
        'public_representative':public_representative,
        'employees':employees,
        'sections':sections,
        })
def AddNew(request, form_type):
    if form_type not in form_classes:
        return redirect('person:home')
    form_class, model_class=form_classes[form_type]
    if request.method == 'POST':
        form=form_class(request.POST)
        if form.is_valid():
            model_class.objects.create(**form.cleaned_data)
            messages.success(
                request,
                f'{form.FormName} : सफलतापूर्वक थपिएको छ।'
                )
            if 'save_add_another' in request.POST:
    
                return redirect('person:addnew',form_type=form_type)
            return redirect('person:home')
        else:
            return HttpResponse(request,'form invalid')
    else:
        form=form_class()
    
    return render(request,'person/addnew_form.html',{'form':form})


def all_models(request):
    all_models=[
            {'model':models.Post,'verbose_name_plural': models.Post._meta.verbose_name_plural},
            {'model':models.Section,'verbose_name_plural': models.Section._meta.verbose_name_plural},
            {'model':models.PublicRepresentative,'verbose_name_plural': models.PublicRepresentative._meta.verbose_name_plural},
            {'model':models.Employee,'verbose_name_plural': models.Employee._meta.verbose_name_plural},
        ]
    return render(request,'person/all_models.html',{'all_models':all_models})

def all_view(request,model_type):
    model_class=form_classes[model_type]
    
def public_representative_view(request):
    person=models.PublicRepresentative.objects.filter(post__name="अध्यक्ष") 
    context={
        'name':person._get_full_name,
        'address':f"अन्नपूर्ण {person.ward}",
        'email':person.email,
        'phone_number':person.mobile_number,

    }


def event_view(request,person=1):
    
    now=timezone.localtime()
    person_obj=models.PublicRepresentative.objects.filter(post__name=models.Choices.event_person_choices()[person-1][1]).first()
    events=models.Event.objects.filter(event_person=person).order_by('ev_date','event_time').reverse()
    current_event=events.filter(
        ev_date=now.date(),
        event_time__lte=now.time()
    ).filter(end_time__gte=now.time()).first()
    context={
        'person':person_obj,
        'events':events,
        'current_event':current_event,
    }
    return render(request,'person/person_event.html',context)

def profile_view(request,pub_emp,pk):
    pub_reps=models.PublicRepresentative.objects.all()
    employee=models.Employee.objects.all()
    model=[None,models.Employee, models.PublicRepresentative,][pub_emp]
    try:
        person_object=model.objects.get(id=pk)
        # exclude_fields = ['id', 'weight', 'status','first_name', 'last_name']
        # fields=[field for field in person_object._meta.fields if field.name not in exclude_fields]
    except:
        return render(request, 'person/404.html', status=404)
    context={
        'pub_reps':pub_reps,
        'employee':employee,
        'person_object':person_object,
        # 'fields':fields,
    }
    return render(request,'person/person_profile.html',context)

def service_view(request,serv):
    return None