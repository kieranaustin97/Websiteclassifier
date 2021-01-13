from django.db import models
from django.db.models import CharField

# Create your models here.
class PredictedWebsites(models.Model):
    classification = CharField(max_length=50)
    url = CharField(max_length=200)
