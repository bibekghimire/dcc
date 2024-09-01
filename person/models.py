
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.db import models
# from nepali_datetime_field.models import NepaliDateField
import nepali_datetime 
from datetime import date as dt


# Create your models here.
ward=11
WardStrings=('१','२','३','४','५','६','७','८','९','१०','११')

class Choices:
    @classmethod
    def IntegerChoices100(cls):
        return [(i,str(i)) for i in range(1,101)]
    @classmethod
    def StatusChoices(cls):
        return [(1,'वर्तमान'),(0,'पूर्व')]
    @classmethod
    def WardChoices(cls):
        return [(i,WardStrings[i-1]) for i in range(1,ward+1)]
    @classmethod
    def catagory(cls):
        return[(1,'कर्मचारी'),(2,'जनप्रतिनिधि')]
    
    @classmethod
    def services(cls):
        return [
            (1, 'विविध'),
            (2,'प्रशासन'),
            (3,'लेखा'),
            ]
    @classmethod
    def event_person_choices(cls):
        return[
            (1,'अध्यक्ष'),
            (2,'उपाध्यक्ष'),
            (3,'प्रमुख प्रसाशकीय अधिकृत')
        ]
    
    

class Post(models.Model):
    name=models.CharField(verbose_name='पदनाम',max_length=100)
    post_for=models.IntegerField(choices=Choices.catagory,default=1)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name='पद'
        verbose_name_plural='पदहरु'
    
class Section(models.Model):
    name = models.CharField(max_length=200, verbose_name='शाखा')
    head = models.OneToOneField('Employee', 
                                on_delete=models.SET_NULL, 
                                null=True,
                                blank=True, 
                                related_name='headed_section',
                                verbose_name='शाखा प्रमुख')
    def __str__(self):
        return self.name

    def clean(self):
        if self.head and self.head.section !=self:
            raise ValidationError('section head must be from same section')
    class Meta:
        verbose_name='शाखा'
        verbose_name_plural="शाखाहरु"

class PersonalInfo(models.Model):
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    mobile_number = models.CharField(
        max_length=10,verbose_name='सम्पर्क नं',
        validators=[
            RegexValidator(
                regex='^9[0-9]{9}$',
                message='मोबाइल नंबर १० अङ्कको हुनुपर्छ र ९ बाट सुरु भएको',
                code='invalid_mobile_number'
            ),
        ]
    )

    email=models.EmailField(default='hello@example.com',verbose_name='ईमेल')
    post=models.ForeignKey(Post,
                           on_delete=models.SET_DEFAULT,
                           default=1,
                           related_name='%(class)s_personalinfo')
    status=models.IntegerField(choices=Choices.StatusChoices, default=1)
    weight = models.IntegerField(choices=Choices.IntegerChoices100, default=1)
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    
    class Meta:
        abstract=True
        verbose_name='व्यक्तिगत विवरण'
  
class Employee(PersonalInfo):
    section=models.ForeignKey(Section,
                              on_delete=models.SET_NULL,
                              null=True, 
                              default=1,
                              related_name='employees',verbose_name='शाखा')
    #  service=models.CharField(
    #     verbose_name='सेवा',choices=
    # )
    # emp_id=models.IntegerField(verbose_name='Employee ID',)
    
    
    class Meta:
        ordering=["weight",]
        verbose_name='कर्मचारि'
        verbose_name_plural='कर्मचारिहरु'

class PublicRepresentative(PersonalInfo):
    ward=models.IntegerField(
        choices=Choices.WardChoices,default=1,verbose_name='वडा'
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    class Meta:
        ordering=["weight",]
        verbose_name='जनप्रतिनिधि'
        verbose_name_plural='जनप्रतिनिधिहरु'

class Event(models.Model):
    event_person=models.IntegerField(
        choices=Choices.event_person_choices,default=1, verbose_name='पदाधिकारी/कर्मचारी'
    )
    name=models.CharField(max_length=200)
    ev_date=models.DateField(verbose_name='Event_Date')
    str_date=models.CharField(verbose_name='कार्यक्रम मिति', max_length=15, null=True)
    event_time=models.TimeField(auto_now=False, auto_now_add=False,null=True)
    end_time=models.TimeField(auto_now=False, auto_now_add=False,null=True, blank=True)
    event_location=models.CharField(max_length=300,verbose_name='कार्यक्रम स्थान',null=True)
    def __str__(self):
        return self.name +':' + self.str_date + self.event_location
    
class subject_committee(models.Model):
    name=models.CharField(
        max_length=100, verbose_name='विषयगत समितिको नाम')
    coordinator=models.OneToOneField(
            PublicRepresentative,
            on_delete=models.SET_NULL,
            null=True,
            blank=True,
            related_name='coordinated_committee',
            verbose_name='समिति संयोजक'
        )
    members=models.ManyToManyField(PublicRepresentative,blank=True, verbose_name="सदस्य हरु")
    secretary=models.ForeignKey(Employee,
                                on_delete=models.SET_NULL,
                                null=True,
                                blank=True,
                                related_name='committes_secretary',
                                verbose_name="सदस्य सचिव"
                                )
    
# class Services(models.Model):
#     name=models.CharField(
#         max_length=200,
#         verbose_name="सेवा"
#     )
#     required_docs=models.TextField()
#     serv_fee=models.PositiveBigIntegerField(
#         verbose_name='लाग्ने शुल्क'
#     )
#     serv_time=models.CharField(
#         max_length=200,
#         verbose_name='लाग्ने समय'
#     )
#     section=models.ForeignKey(
#         Section,
#         verbose_name='सम्बन्धित शाखा',
#         on_delete=models.SET_NULL,
#         related_name='services',
#         null=True 
#     )
