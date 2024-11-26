from rest_framework import serializers
from .models import Service



class ServiceSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()
    class Meta:
        model=Service
        fields='__all__'

    def get_file_url(self, obj):
        print(obj.get_sample_document_url())
        return obj.get_sample_document_url()


