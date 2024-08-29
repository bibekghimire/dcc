from django import forms
from django.contrib import admin
from .models import Post, Section, Employee, PublicRepresentative, Choices, Event


import nepali_datetime
from datetime import date as dt

class EmployeeAdminForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'
        

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['post'].queryset = Post.objects.filter(post_for=1)

class PublicRepresentativeAdminForm(forms.ModelForm):
    class Meta:
        model = PublicRepresentative
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['post'].queryset = Post.objects.filter(post_for=2)

class EventAdminForm(forms.ModelForm):
    str_date= forms.CharField(label="कार्यक्रम मितिः", required=True)
    class Meta:
        model=Event
        fields=['name','str_date','event_time', 'event_location','end_time','event_person']


    def clean(self):
        cleaned_data = super().clean()
        date_str=self.cleaned_data.get('str_date')
        try:
            ev_date=nepali_datetime.datetime.strptime(date_str, '%Y-%m-%d')
            ev_date=ev_date.to_datetime_date()
        except ValueError :
            raise forms.ValidationError("Age must be a valid date.")
        
        cleaned_data['ev_date']= ev_date
        return cleaned_data
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.ev_date = self.cleaned_data['ev_date']
        if commit:
            instance.save()
        
        return instance

class PostForm(forms.Form):
    name=forms.CharField(
        max_length=100,
        label='पद',
        help_text='पद उल्लेख गर्नुहोस',
        error_messages={'required':'पद खालि राख्न मिल्दैन'},
        widget=forms.TextInput(attrs={
            'placeholder':'पद'
        })
    )

class SectionForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.FormName='शाखा थप्नुहोस'

    name=forms.CharField(
        max_length=100,
        label='शाखा',
        help_text="शाखाको नाम उल्लेख गर्नुहोस",
        error_messages={'required':'शाखा खालि नछोड्नुहोस'},
        widget=forms.TextInput(attrs={
            'placeholder':'शाखाको नाम'
        })
        )
    # head=forms.ModelChoiceField(queryset)

class EmployeeForm(forms.Form):
    def __init__(self, *args,**kwargs):
        self.FormName='नया कर्मचारी थप्नुहोस'
        super().__init__(*args,**kwargs)
        self.fields['post'].queryset=Post.objects.filter(post_for=1)
    
    first_name=forms.CharField(
        max_length=100,
        label='पहिलो नाम',
        help_text='आफ्नो नाम',
        error_messages={
            'required':'पहिलो नाम अनिबार्य छ।'
        },
        widget=forms.TextInput(
            attrs={
                'placeholder':'पहिलो नाम'
            }
        ),
    )
    last_name=forms.CharField(
        max_length=100,
        label='थर',
        help_text='थर',
        error_messages={
            'required':'थर अनिबार्य छ।'
        },
        widget=forms.TextInput(
            attrs={
                'placeholder':'थर'
            }
        ),
    )
    mobile_number=forms.CharField(
        max_length=10,
        label='सम्पर्क नं',
        help_text='सम्पर्क नं उल्लेख गर्नुहोस',
        widget=forms.TextInput(
            attrs={
                'placeholder':'xxxxxxxxxx'
            }
        ),
    )
    email=forms.EmailField(
        label='Enter Email',
    )
    post=forms.ModelChoiceField(
        queryset=Post.objects.filter(post_for=1),
        label='पद',
        help_text='पद छनौट गर्नुहोस',
    )
    section=forms.ModelChoiceField(
        queryset=Section.objects.all(),
    )
    status=forms.ChoiceField(choices=Choices.StatusChoices)
    weight=forms.ChoiceField(choices=Choices.IntegerChoices100)

class PublicRepresentativeForm(forms.Form):
    def __init__(self, *args,**kwargs):
        self.FormName='नया जनप्रतिनिधि '
        super().__init__(*args,**kwargs)
        self.fields['post'].queryset=Post.objects.filter(post_for=2)
    
    first_name=forms.CharField(
        max_length=100,
        label='पहिलो नाम',
        help_text='आफ्नो नाम',
        error_messages={
            'required':'पहिलो नाम अनिबार्य छ।'
        },
        widget=forms.TextInput(
            attrs={
                'placeholder':'पहिलो नाम'
            }
        ),
    )
    last_name=forms.CharField(
        max_length=100,
        label='थर',
        help_text='थर',
        error_messages={
            'required':'थर अनिबार्य छ।'
        },
        widget=forms.TextInput(
            attrs={
                'placeholder':'थर'
            }
        ),
    )
    mobile_number=forms.CharField(
        max_length=10,
        label='सम्पर्क नं',
        help_text='सम्पर्क नं उल्लेख गर्नुहोस',
        widget=forms.TextInput(
            attrs={
                'placeholder':'xxxxxxxxxx'
            }
        ),
    )
    email=forms.EmailField(
        label='Enter Email',
    )
    post=forms.ModelChoiceField(
        queryset=Post.objects.none(),
        label='पद',
        help_text='पद छनौट गर्नुहोस',
    )
    ward=forms.ChoiceField(choices=Choices.WardChoices)
    status=forms.ChoiceField(choices=Choices.StatusChoices)
    weight=forms.ChoiceField(choices=Choices.IntegerChoices100)

class EventForm(forms.Form):
    def __init__(self, *args,**kwargs):
        self.FormName='नया कार्यक्रम'
        super().__init__(*args,**kwargs)
    name=forms.CharField(
        max_length=300,
        label='कार्यक्रमको नाम',
        help_text="कार्यक्रमको नाम उल्लेख गर्नुहोस",
        error_messages={'required':'कार्यक्रम खालि नछोड्नुहोस'},
        widget=forms.TextInput(attrs={
            'placeholder':'कार्यक्रमको नाम'
        })
        )
    str_date=forms.CharField(
        max_length=15,label='कार्यक्रम मितिः', required=True,
        widget=forms.TextInput(attrs={
            'placeholder':'yyyy-m-d'
        })
        )
    event_time=forms.TimeField(
        widget=forms.TimeInput(format="%H:%M"),
        label="कार्यक्रमको समयः"
    )
    end_time=forms.TimeField(
        widget=forms.TimeInput(format="%H:%M"),
        label="कार्यक्रमको सकिने समयः"
    )

    event_location=forms.CharField(
        max_length=300,
        label='कार्यक्रम स्थान',
        help_text='कार्यक्रमको नाम उल्लेख गर्नुहोस',
        error_messages={'required':'कार्यक्रम स्थान खालि नछोड्नुहोस'},
        widget=forms.TextInput(attrs={
            'placeholder':'कार्यक्रमको स्थान'
        })
    )
    def clean(self):
        cleaned_data = super().clean()
        date_str=self.cleaned_data.get('str_date')
        try:
            ev_date=nepali_datetime.datetime.strptime(date_str, '%Y-%m-%d')
            ev_date=ev_date.to_datetime_date()
        except ValueError :
            raise forms.ValidationError("Age must be a valid date.")
        
        cleaned_data['ev_date']= ev_date
        return cleaned_data
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.ev_date = self.cleaned_data['ev_date']
        if commit:
            instance.save()
        
        return instance
    

