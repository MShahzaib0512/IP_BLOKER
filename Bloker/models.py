from django.db import models

# Create your models here.
class IP_BLOCK(models.Model):
 name=models.GenericIPAddressField()
 reason = models.CharField(max_length=50)