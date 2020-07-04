from django.db.models.signals import post_save
from datetime import datetime

from .models import *

def on_post_save(sender, instance, **kwargs):
    instance.calculate_statistics()

def on_rottent_point_save(sender, instance, **kwargs):
    instance.post.date_modified = datetime.now()
    instance.post.save()
    instance.post.calculate_statistics()

post_save.connect(on_rottent_point_save, sender=RottenPoint)
post_save.connect(on_post_save, sender=Post)
