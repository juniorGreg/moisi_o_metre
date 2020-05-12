from django.db import models

# Create your models here.
class Post(models.Model):
    POST_TYPE = (
        ('CRITIC', 'Critic'),
        ('ARTICLE', 'Article'),
        ('BD', 'BD')
    )
    post_type = models.CharField(max_length=10, choices=POST_TYPE, default='CRITIC')
    title = models.CharField(max_length=200)
    content = models.TextField(max_length=2000)
    date_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)
    source = models.CharField(max_length=200, null=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.title


class RottenPoint(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=2000)
    source = models.CharField(max_length=200, null=True, blank=True)
    rotten_source = models.CharField(max_length=200, null=True, blank=True)
    order = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.title

class Reference(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=400)
    source = models.CharField(max_length=200)

    def __str__(self):
        return self.title

class About(models.Model):
    text = models.TextField(max_length=2000)

    def __str__(self):
        return "about"
