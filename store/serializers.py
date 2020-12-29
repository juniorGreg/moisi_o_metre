from rest_framework import serializers
from .models import *

class VariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variant
        fields = "__all__"

class ProductSerializer(serializers.ModelSerializer):
    variant_set = VariantSerializer(many=True)

    class Meta:
        model = Product
        fields = "__all__"
