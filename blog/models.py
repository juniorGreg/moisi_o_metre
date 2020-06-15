from django.db import models
from django.urls import reverse

# Create your models here.
class Reference(models.Model):
    title = models.CharField(max_length=400, null=True)
    description = models.TextField(max_length=800, null=True)
    source = models.CharField(max_length=400)
    is_global = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Post(models.Model):
    POST_TYPE = (
        ('CRITIC', 'Critic'),
        ('ARTICLE', 'Article'),
        ('BD', 'BD')
    )
    post_type = models.CharField(max_length=10, choices=POST_TYPE, default='CRITIC')
    title = models.CharField(max_length=400)
    content = models.TextField(max_length=8000)
    date_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(null=True, blank=True)
    sources = models.ManyToManyField(Reference)
    rotten_score = models.PositiveSmallIntegerField(default=4)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post", kwargs={"id": str(self.id)})


class RottenPoint(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    title = models.CharField(max_length=400)
    description = models.TextField(max_length=8000)
    order = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.title



class About(models.Model):
    text = models.TextField(max_length=4000)

    def __str__(self):
        return "about"
