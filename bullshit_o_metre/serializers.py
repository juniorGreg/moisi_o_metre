from rest_framework import serializers
from .models import *

class LabeledWebSiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabeledWebSite
        fields = "__all__"

class WebSiteSerializer(serializers.Serializer):
    url = serializers.URLField()
    is_bullshit = serializers.BooleanField()
