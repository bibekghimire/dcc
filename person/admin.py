from django import forms
from django.contrib import admin
from .models import Post, Section, Employee, PublicRepresentative, Choices, Event, SubjectCommittee
# app_models = models.__dict__

# for model_name in app_models:
#     model = app_models[model_name] 
#     if isinstance(model, type) and issubclass(model, Model):
#         admin.site.register(model)
from .forms import EmployeeAdminForm, PublicRepresentativeAdminForm,EventAdminForm


class EmployeeAdmin(admin.ModelAdmin):
    form = EmployeeAdminForm

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['post'].queryset = Post.objects.filter(post_for=1)
        return form

class PublicRepresentativeAdmin(admin.ModelAdmin):
    form = PublicRepresentativeAdminForm

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        print(Post.objects.filter(post_for=2))
        form.base_fields['post'].queryset = Post.objects.filter(post_for=2)
        return form

class EventAdmin(admin.ModelAdmin):
    form=EventAdminForm
    



admin.site.register(Post)
admin.site.register(SubjectCommittee)
admin.site.register(Section)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(PublicRepresentative, PublicRepresentativeAdmin)
admin.site.register(Event,EventAdmin)