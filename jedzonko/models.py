from django.db import models


# Create your models here.
from jedzonko.enums import Days


class Recipe(models.Model):
    name = models.CharField(max_length=255)
    ingredients = models.TextField()
    description = models.TextField()
    prep_instructions = models.TextField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    preparation_time = models.IntegerField()
    votes = models.IntegerField(default=0)


class Plan(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    recipes = models.ManyToManyField('Recipe', through='RecipePlan')


class DayName(models.Model):
    day_name = models.SmallIntegerField(choices=Days.CHOICES)
    order = models.IntegerField(unique=True)

    def __str__(self):
        return self.get_day_name_display()


class RecipePlan(models.Model):
    meal_name = models.CharField(max_length=255)
    order = models.IntegerField()
    recipe = models.ForeignKey('Recipe', on_delete=models.PROTECT)
    plan = models.ForeignKey('Plan', on_delete=models.PROTECT)
    day_name = models.ForeignKey('DayName', on_delete=models.PROTECT)




