from django.db import models
from django.urls import reverse

# Create your models here.
class Reference(models.Model):
    title = models.CharField(max_length=400, null=True)
    description = models.TextField(max_length=800, null=True)
    source = models.CharField(max_length=400)
    is_global = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class PostStatistics(models.Model):
    word_count = models.PositiveIntegerField(default=0)
    avg_reading_time = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.word_count) + " " + str(self.avg_reading_time)


class Post(models.Model):
    POST_TYPE = (
        ('CRITIC', 'Critic'),
        ('ARTICLE', 'Article'),
        ('BD', 'BD')
    )

    post_type = models.CharField(max_length=10, choices=POST_TYPE, default='CRITIC')
    title = models.CharField(max_length=400)
    content = models.TextField(max_length=8000, blank=True)
    date_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(null=True, blank=True)
    hidden_image = models.ImageField(null=True, blank=True)
    sources = models.ManyToManyField(Reference, blank=True)
    rotten_score = models.PositiveSmallIntegerField(default=4)

    pub = models.TextField(max_length=8000, null=True, blank=True)

    admin_only = models.BooleanField(default=False)

    statistics = models.OneToOneField(PostStatistics, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post", kwargs={"id": str(self.id)})

    def calculate_statistics(self):
        text = self.content

        for rotten_point in self.rottenpoint_set.all():
            text += " "
            text += rotten_point.description

        text = text.replace("?", "").replace("!", "")
        words = text.split()
        word_count = len(words)
        avg_reading_time = int(round(float(word_count)/184.0))

        if self.statistics is None:
            statistics = PostStatistics(word_count=word_count, avg_reading_time=avg_reading_time)
            statistics.save()
            self.statistics = statistics
            self.save()
        else:
            self.statistics.word_count = word_count
            self.statistics.avg_reading_time = avg_reading_time
            self.statistics.save()


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
