from django.db import models
from django.db.models import CharField, DateTimeField

# Create your models here.
class PredictedWebsites(models.Model):
    url = CharField(max_length=200)
    classification = CharField(max_length=50)
    datestamp = DateTimeField(blank=True, null=True)   
    
