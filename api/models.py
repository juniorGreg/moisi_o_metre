from django.db import models

# Create your models here.
class Language(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=10)

    def __str__(self):
        return self.name

class Sophism(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=400, null=True)
    language =  models.ForeignKey(Language, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.title

class Player(models.Model):
    username = models.CharField(max_length=200)
    points = models.IntegerField(default=0)

    def __str__(self):
        return self.username

class Sentence(models.Model):
    description = models.TextField(max_length=400)
    source = models.CharField(max_length=200)
    language = models.ForeignKey(Language, null=True, on_delete=models.SET_NULL)
    sophisms = models.ManyToManyField(Sophism)

    def __str__(self):
        if len(self.description) > 100:
            return self.description[:100] + " ..."
        else:
            return self.description
