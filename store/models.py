from django.db import models
import requests
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
import hashlib
import os
STORE_UPLOAD_FOLDER = "store/"

# Create your models here.
class Product(models.Model):
    id = models.CharField(max_length=12, primary_key=True)
    external_id = models.CharField(max_length=26)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name





class VariantImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    thumbnail = models.ImageField(upload_to=STORE_UPLOAD_FOLDER, blank=True)
    preview = models.ImageField(upload_to=STORE_UPLOAD_FOLDER)
    resized_preview = models.ImageField(upload_to=STORE_UPLOAD_FOLDER, blank=True)
    hash = models.CharField(max_length=100, unique=True, blank=True)

    def save(self, *args, **kwargs):
        super(VariantImage, self).save(*args, **kwargs)

        if "http" in self.preview.url:
            req_img = requests.get(self.preview.url, stream=True)
        else:
            req_img = requests.get("https://moisidev.xyz%s" % self.preview.url, stream=True)

        if req_img.status_code == 200:
            path = BytesIO(req_img.raw.read())
            img_preview = Image.open(path)

            md5hash = hashlib.md5(img_preview.tobytes()).hexdigest()

            if self.hash == md5hash:
                print("duplicate")
                return

            self.hash = md5hash


            img_resized_preview = img_preview.resize((450,450))
            img_thumbnail = img_preview.resize((60,60))

            def save_pil_img_to_imagefield(filename, pil_img, image_field):
                print(filename)
                buffer = BytesIO()

                pil_img.save(buffer, img_preview.format)

                image_field.save(filename,
                                 ContentFile(buffer.getvalue()),
                                 save=False)

            base_filename = os.path.basename(self.preview.url)
            save_pil_img_to_imagefield("preview_%s" % base_filename, img_resized_preview, self.resized_preview)
            save_pil_img_to_imagefield("thumb_%s" % base_filename, img_thumbnail, self.thumbnail)

            super(VariantImage, self).save(*args, **kwargs)

    def __str__(self):
        return self.hash



class Variant(models.Model):


    id = models.CharField(max_length=12, primary_key=True)
    variant_id = models.PositiveBigIntegerField(null=True)
    external_id = models.CharField(max_length=26)
    name = models.CharField(max_length=200)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    color = models.CharField(max_length=50)
    size = models.CharField(max_length=10)

    price = models.FloatField(default=0)

    variant_image = models.ForeignKey(VariantImage, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name



class Order(models.Model):
    STATUS_TYPE = (
        ('draft', 'draft'),
        ('pending', 'pending'),
        ('failed', 'failed'),
        ('canceled', 'canceled'),
        ('inprocess', 'inprocess'),
        ('onhold', 'onhold'),
        ('partial', 'partial'),
        ('fulfilled', 'fulfilled')
    )
    id = models.CharField(max_length=12, primary_key=True)
    paypal_id = models.CharField(max_length=20)
    external_id = models.CharField(max_length=26, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_TYPE)
    date_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)
    total_cost = models.FloatField(default=0)
    shipping_cost = models.FloatField(default=0)

class Customer(models.Model):
    fullname = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    country_code = models.CharField(max_length=3)
    state_code = models.CharField(max_length=3)
    zip_code = models.CharField(max_length=10)
    email = models.EmailField()

    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.fullname

class Shipment(models.Model):
    id = models.CharField(max_length=12, primary_key=True)
    carrier = models.CharField(max_length=100)
    service = models.CharField(max_length=100)
    tracking_number = models.CharField(max_length=100)
    tracking_url = models.URLField()
    date_created = models.DateTimeField(auto_now_add=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)






class OrderItem(models.Model):
    variant = models.ForeignKey(Variant, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1)
    quantity_shipped = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        if self.variant:
            return self.variant.name +":"+str(self.quantity)
        else:
            return str(self.quantity)
