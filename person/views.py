from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test

from django.contrib import messages
from django.http import HttpResponse
from django.utils import timezone
# Create your views here.
from . import forms
from . import models

def is_admin(user):
    return user.is_superuser

def is_staff(user):
    return user.is_staff


form_classes={
    'post':(forms.PostForm,models.Post),
    'section':(forms.SectionForm, models.Section),
    'employee':(forms.EmployeeForm, models.Employee),
    'public_representative':(forms.PublicRepresentativeForm,
                             models.PublicRepresentative
                             ),
    'event':(forms.EventForm,models.Event),

}

def  UserHomeView(request):
    user=request.user
    now=timezone.localtime()
    if user.groups.filter(name='cao_group').exists():
        person_obj=models.Employee.objects.filter(
            post__name='प्रमुख प्रशासकीय अधिकृत'
            ).first()
        print(person_obj)
        events=models.Event.objects.filter(event_person=3).order_by(
            'ev_date','event_time').reverse()
        current_event=events.filter(
        ev_date=now.date(),
        event_time__lte=now.time()).filter(end_time__gte=now.time()).first()
    elif user.groups.filter(name="chairman_group").exists():
        person_obj=models.PublicRepresentative.objects.filter(
            post__name='अध्यक्ष'
        ).first()
        events=models.Event.objects.filter(event_person=1).order_by(
            'ev_date','event_time').reverse()
        current_event=events.filter(
        ev_date=now.date(),
        event_time__lte=now.time()).filter(end_time__gte=now.time()).first()
    else:
        return render(request, 'home.html')
    context={
        'person':person_obj,
        'events':events,
        'current_event':current_event,
    }
    return render(request,'person/user_home.html',context)   

@login_required
def HomeView(request):
    public_representative=models.PublicRepresentative.objects.all().order_by('weight')[:5]
    employees=models.Employee.objects.all().order_by('weight')[:5]
    sections=models.Section.objects.all()[:5]
    return render(request,'person/home.html',{
        'public_representative':public_representative,
        'employees':employees,
        'sections':sections,
        })

@login_required
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

@login_required
def all_models(request):
    all_models=[
            {'model':models.Post,'verbose_name_plural': models.Post._meta.verbose_name_plural},
            {'model':models.Section,'verbose_name_plural': models.Section._meta.verbose_name_plural},
            {'model':models.PublicRepresentative,'verbose_name_plural': models.PublicRepresentative._meta.verbose_name_plural},
            {'model':models.Employee,'verbose_name_plural': models.Employee._meta.verbose_name_plural},
        ]
    return render(request,'person/all_models.html',{'all_models':all_models})

@login_required
def all_view(request,model_type):
    model_class=form_classes[model_type]

#@login_required  
def public_representative_view(request):
    person=models.PublicRepresentative.objects.filter(post__name="अध्यक्ष") 
    context={
        'name':person._get_full_name,
        'address':f"अन्नपूर्ण {person.ward}",
        'email':person.email,
        'phone_number':person.mobile_number,

    }

@login_required
def event_view(request,person=1):
    now=timezone.localtime()
    model=[None,models.PublicRepresentative,models.PublicRepresentative,models.Employee][person]
    person_obj=model.objects.filter(
        post__name=models.Choices.event_person_choices()[person-1][1]
        ).first()
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


#@login_required
def profile_view(request,pub_emp,pk):
    pub_reps=models.PublicRepresentative.objects.all().order_by('weight')
    employees=models.Employee.objects.all().order_by('weight')
    model=[None,models.Employee, models.PublicRepresentative,][pub_emp]
    post=[None,'प्रमुख प्रशासकीय अधिकृत','अध्यक्ष'][pub_emp]
    
    try:
        if pk==0:
            person_object=model.objects.all().filter(post__name=post).first()
            title=model._meta.verbose_name
        else:
            person_object=model.objects.get(id=pk)
            title=model._meta.verbose_name
    except:
        return render(request, 'person/404.html', status=404)
    context={
        'pub_reps':pub_reps,
        'employees':employees,
        'person_object':person_object,
        'title':title
        # 'fields':fields,
    }
    return render(request,'person/pr_emp_view.html',context)

#@login_required
def more_view(request):
    return render(request,'person/more_view.html')


#@login_required
def section_committee_view(request,type=0,pk=0):
    # this view is to display section list and subject committtee in left and right side
    # while displaying the detail for selected 
    sections=models.Section.objects.all()
    committees=models.SubjectCommittee.objects.all()
    cabinet=models.PublicRepresentative.objects.filter(cabinet_member=True)
    if type==0:
        active_committee=cabinet
    elif type==1:
        active_committee=committees.filter(id=pk).first()
    elif type==2:
        active_committee=sections.filter(id=pk).first()
        print(active_committee)

    context={'sections':sections,
             'committees':committees,
             'cabinet':cabinet,
             'active_committee':active_committee,
             'type':type
             }
    return render(request,'person/section_committee.html',context)
    
