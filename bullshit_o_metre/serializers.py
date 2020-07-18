from rest_framework import serializers
from .models import *

class RecordedWebSiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecordedWebSite
        fields = "__all__"
