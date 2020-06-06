from rest_framework import serializers
from .models import *

class ReferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reference
        fields = ["title", "source"]

class RottenPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = RottenPoint
        fields = "__all__"


class PostSerializer(serializers.ModelSerializer):

    rottenpoint_set = RottenPointSerializer(many=True, read_only=True)
    sources = ReferenceSerializer(many=True)

    class Meta:
        model = Post
        fields = '__all__'
