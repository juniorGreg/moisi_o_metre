from django.db import models

# Create your models here.
class TaintedLemma(models.Model):
    TYPE = (
        ('NEG', 'Negative'),
        ('NEU', 'Neutral'),
        ('POS', 'Positive'),
        ('SUP', 'Superlative')
    )

    LANG = (
        ('FR', 'Français'),
        ('EN', 'English')
    )

    type = models.CharField(max_length=3, choices=TYPE, default='NEU')
    lang = models.CharField(max_length=2, choices=LANG, default='FR')
    name = models.CharField(max_length=400)
    is_evaluated = models.BooleanField(default=False)

class RecordedWebSite(models.Model):
    title = models.CharField(max_length=400)
    url = models.URLField(max_length=400)
    meaningful_lemmas = models.ManyToManyField(TaintedLemma)
    lemmas_count = models.PositiveIntegerField()

    score = models.FloatField()
