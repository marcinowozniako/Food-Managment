import random
from datetime import datetime

from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.core.paginator import Paginator

from jedzonko.models import Recipe, Plan, RecipePlan, DayName

from jedzonko.custom_functions import PaginatorClass
from jedzonko.models import Recipe, Plan, RecipePlan, DayName
from jedzonko.enums import Days


class IndexView(View):

    def get(self, request):
        ctx = {"actual_date": datetime.now()}
        return render(request, "test.html", ctx)


class LandingPageView(View):
    def get(self, request):
        recipes = list(Recipe.objects.all())
        random.shuffle(recipes)
        context = {
            'recipe1': recipes[0],
            'recipe2': recipes[1],
            'recipe3': recipes[2],
        }
        return render(request, 'index.html', context=context)


class RecipeListView(View):
    def get(self, request):
        recipes_sorted = Recipe.objects.all().order_by('-votes', 'created')
        paginator_dict = PaginatorClass(request, recipes_sorted, 50).prepare_paginator()
        context = {
            'recipes_on_page': paginator_dict['on_page'],
            'range': range(2, 5),
            'page_2less': paginator_dict['page'] - 2,
            'page_2more': paginator_dict['page'] + 2,
            'pag': paginator_dict['paginator'],
            'page_obj': paginator_dict['paginator'].page(paginator_dict['page']),
        }
        return render(request, 'app-recipes.html', context=context)


class DashboardView(View):
    def get(self, request):
        recipes = Recipe.objects.all()
        recipes_length = recipes.count()
        context = {
            'recipes_length': recipes_length
        }

        return render(request, 'dashboard.html', context=context)


class AddRecipe(View):
    def get(self, request):
        return render(request, 'app-add-recipe.html')

    def post(self, request):
        recipe_name = request.POST['recipe_name']
        ingredients = request.POST['ingredients']
        description = request.POST['recipe_description']
        time = request.POST['time']
        preparation = request.POST['preparation']
        if recipe_name and ingredients and description and time and preparation:
            data = {
                'name': recipe_name,
                'ingredients': ingredients,
                'description': description,
                'prep_instructions': preparation,
                'preparation_time': time,
            }
            Recipe.objects.create(**data)
            return redirect(reverse('recipe_list'))
        else:
            return render(request, 'app-add-recipe.html', context={'Error': 'Musisz wypełnić wszystkie pola!!'})


class PlanListView(View):
    def get(self, request):
        plans_sorted = Plan.objects.all().order_by('name')
        print(plans_sorted)
        paginator_dict = PaginatorClass(request, plans_sorted, 50).prepare_paginator()
        context = {
            'plans_on_page': paginator_dict['on_page'],
            'page_2less': paginator_dict['page'] - 2,
            'page_2more': paginator_dict['page'] + 2,
            'pag': paginator_dict['paginator'],
            'page_obj': paginator_dict['paginator'].page(paginator_dict['page']),
        }
        return render(request, 'app-schedules.html', context=context)


class AddPlan(View):
    def get(self, request):
        return render(request, 'app-add-schedules.html')

    def post(self, request):
        plan_name = request.POST['plan_name']
        description = request.POST['description']
        if plan_name and description:
            data = {
                'name': plan_name,
                'description': description,
            }
            Plan.objects.create(**data)
            return redirect(reverse('plan_details'))
            # return redirect(reverse('To be Done'))
        else:
            return render(request, 'app-add-schedules.html', context={'Error': 'Musisz wypełnić wszystkie pola!!'})


class PlanAddRecipe(View):
    def get(self, request):
        plan_names_list = Plan.objects.all().order_by('name')
        recipe_names_list = Recipe.objects.all()
        for day in Days.CHOICES:
            print(f'value={day[0]}, day={day[1]}')
        context = {
            'plan_names_list': plan_names_list,
            'recipe_names_list': recipe_names_list,
            'days': Days.CHOICES,
        }
        return render(request, 'app-schedules-meal-recipe.html', context=context)

    def post(self, request):
        plan_id = int(request.POST.get('plan'))
        meal_name = request.POST.get('meal_name')
        order = int(request.POST.get('meal_number'))
        recipe_id = int(request.POST.get('recipe'))
        day_of_week = int(request.POST.get('day_of_week')) + 1

        RecipePlan.objects.create(meal_name=meal_name, order=order, day_name_id=day_of_week, plan_id=plan_id,
                                  recipe_id=recipe_id)

        return render(request, 'app-schedules-meal-recipe.html')


class PlanDetailsView(View):
    def get(self, request, us_id):
        plan = RecipePlan.objects.filter(plan=us_id).first()
        days = RecipePlan.objects.filter(plan=us_id).order_by('day_name__order', 'order')
        context = {
            'name': plan,
            'days': days,
        }
        return render(request, 'app-details-schedules.html', context=context)


class RecipeDetailsView(View):
    def get(self, request, us_id):
        recipe = Recipe.objects.get(pk=us_id)
        return render(request, 'app-recipe-details.html', context={'recipe': recipe})

# TODO: brakuje odpowiedniego przekierowania do widoku /plan/<id>/ ponieważ jeszcze nie istnieje
# return redirect(reverse(f'plan_id_view ')) - cos takiego, gdzie id to id planu konkretnego
