from django.db import models

# Create your models here.

from person.models import Employee,Section
def file_upload_to(instance,filename):
    return 'services/sample_documents/{0}'.format(filename)

class Service(models.Model):
    name=models.CharField(max_length=200,verbose_name='सेवाको नाम')
    required_docs=models.TextField(verbose_name='आवश्यक कागजातहरु',null=True )
    serv_fee=models.IntegerField(verbose_name="सेवा शुल्क")
    serv_fee2=models.CharField(verbose_name="सेवा शुल्क २", max_length=100,null=True)
    
    serv_time=models.CharField(verbose_name="लाग्ने समय", max_length=50)
    section=models.ForeignKey(Section,
                              verbose_name="सम्बन्धित शाखा",
                              on_delete=models.RESTRICT,
                              related_name='served_services',
                              null=True,
                              )
    sample_documents=models.FileField(verbose_name="नमुना कागजातहरु",
                                      upload_to=file_upload_to,
                                      null=True
                                      )

    def __str__(self):
        return self.name 