import random
from datetime import datetime

from django.shortcuts import render
from django.views import View

from jedzonko.models import Recipe


class IndexView(View):

    def get(self, request):
        ctx = {"actual_date": datetime.now()}
        return render(request, "test.html", ctx)


class LandingPageView(View):
    def get(self, request):
        recipes = list(Recipe.objects.all())
        random.shuffle(recipes)
        context = {
            'recipe1':  recipes[0],
            'recipe2': recipes[1],
            'recipe3': recipes[2],
        }
        return render(request, 'index.html', context=context)


class RecipeListView(View):
    def get(self, request):
        return render(request, 'app-recipes.html')