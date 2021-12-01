from django.db import models


# Create your models here.
class Banks(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        db_table = 'banks'

    def __str__(self):
        return self.name


class Branches(models.Model):
    ifsc = models.CharField(max_length=50, unique=True, blank=True, null=True)
    bank = models.ForeignKey(Banks, on_delete=models.CASCADE, null=True)
    branch_name = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    district = models.CharField(max_length=50, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        db_table = 'branches'

    def __str__(self):
        return self.branch_name
