from rest_framework import serializers
from .models import *


class SentenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sentence
        field = '__all__'
