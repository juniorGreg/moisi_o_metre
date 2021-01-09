from django.db import models

STORE_UPLOAD_FOLDER = "store/"

# Create your models here.
class Product(models.Model):
    id = models.CharField(max_length=12, primary_key=True)
    external_id = models.CharField(max_length=26)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Variant(models.Model):


    id = models.CharField(max_length=12, primary_key=True)
    variant_id = models.PositiveBigIntegerField(null=True)
    external_id = models.CharField(max_length=26)
    name = models.CharField(max_length=200)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    color = models.CharField(max_length=50)
    size = models.CharField(max_length=10)
    thumbnail = models.ImageField(upload_to=STORE_UPLOAD_FOLDER, blank=True)
    preview = models.ImageField(upload_to=STORE_UPLOAD_FOLDER, blank=True)
    price = models.FloatField(null=True)

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
    carrier = models.CharField(max_length=20)
    service = models.CharField(max_length=20)
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
        return self.variant.name +":"+str(self.quantity)
