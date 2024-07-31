from django.db import models

# Create your models here.
class Skill(models.Model):
    name = models.CharField(max_length=16, unique=True)

class Search(models.Model):
    vacancy = models.CharField(max_length=16)
    city = models.CharField(max_length=16)
    count = models.IntegerField()
    sal_from = models.CharField(max_length=14)
    sal_to = models.CharField(max_length=14)

class Requirements(models.Model):
    world_id = models.IntegerField()
    skill_id = models.IntegerField()
