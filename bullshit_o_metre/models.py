from django.db import models

# Create your models here.
class LabeledWebSite(models.Model):
    title = models.CharField(max_length=400)
    url = models.URLField(max_length=400, unique=True)
    is_bullshit = models.BooleanField()
    texts = models.TextField()
    lang = models.CharField(max_length=5)

    def __str__(self):
        return self.title
