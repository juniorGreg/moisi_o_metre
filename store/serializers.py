from rest_framework import serializers
from .models import *

class VariantImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = VariantImage
        fields = ["thumbnail", "resized_preview"]

class VariantSerializer(serializers.ModelSerializer):
    variant_image = VariantImageSerializer()
    class Meta:
        model = Variant
        fields = "__all__"

class ProductSerializer(serializers.ModelSerializer):
    variant_set = VariantSerializer(many=True)

    class Meta:
        model = Product
        fields = "__all__"
