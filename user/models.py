from django.conf import settings
from django.db import models

# Creating the Address Model
class Address(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    province = models.CharField(max_length=250, null=True)
    district = models.CharField(max_length=250, null=True)
    sector = models.CharField(max_length=250, null=True)
    street_name = models.CharField(max_length=250, null=True)

    def __str__(self):
        return "{}@{}".format(self.sector, self.street_name)