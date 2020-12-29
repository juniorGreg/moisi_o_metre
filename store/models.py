from django.db import models

STORE_UPLOAD_FOLDER = "store/"

# Create your models here.
class Product(models.Model):
    id = models.PositiveBigIntegerField(primary_key=True)
    external_id = models.CharField(max_length=26)
    name = models.CharField(max_length=200)
    thumbnail = models.ImageField(upload_to=STORE_UPLOAD_FOLDER, blank=True)

    def __str__(self):
        return self.name


class Variant(models.Model):
    SIZE_TYPE = (
        ('N', 'None'),
        ('XS', 'X Small'),
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'X Large'),
        ('2XL', 'XX Large'),
        ('3XL', '3X Large'),
        ('4XL', '4X Large'),
        ('5XL', '5X Large')
    )
    id = models.PositiveBigIntegerField(primary_key=True)
    variant_id = models.PositiveBigIntegerField()
    external_id = models.CharField(max_length=26)
    name = models.CharField(max_length=200)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = models.CharField(max_length=50)
    size = models.CharField(max_length=3, choices=SIZE_TYPE)
    thumbnail = models.ImageField(upload_to=STORE_UPLOAD_FOLDER, blank=True)
    preview = models.ImageField(upload_to=STORE_UPLOAD_FOLDER, blank=True)
    price = models.FloatField()


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
    id = models.PositiveIntegerField(primary_key=True)
    external_id = models.CharField(max_length=26, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_TYPE)
    email = models.EmailField()


class OrderItem(models.Model):
    variant = models.ForeignKey(Variant, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1)
