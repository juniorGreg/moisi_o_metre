from rest_framework import serializers
from .models import *

class RottenPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = RottenPoint
        fields = "__all__"


class PostSerializer(serializers.ModelSerializer):

    rottenpoint_set = RottenPointSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = '__all__'
