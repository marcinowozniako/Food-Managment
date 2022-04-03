import random
from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import ProtectedError
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View

from jedzonko.custom_functions import PaginatorClass, get_pagination_range
from jedzonko.models import Recipe, Plan, RecipePlan, DayName, Page
from jedzonko.enums import Days


class IndexView(View):

    def get(self, request):
        ctx = {"actual_date": datetime.now()}
        return render(request, "test.html", ctx)


class LandingPageView(View):
    def get(self, request):
        recipes = list(Recipe.objects.all())
        if len(recipes) >= 3:
            random.shuffle(recipes)
            context = {
                'recipe1': recipes[0],
                'recipe2': recipes[1],
                'recipe3': recipes[2],
            }
            return render(request, 'index.html', context=context)
        return render(request, 'index.html')


class RecipeListView(View):
    def get(self, request):
        recipes_sorted = Recipe.objects.all().order_by('-votes', 'created')
        records_on_list = request.COOKIES.get('records_on_list_recipe')
        choice_rec_on_list = [50, 25, 10, 5]
        paginator_dict = PaginatorClass(
            request, recipes_sorted, int(records_on_list) if records_on_list is not None else 50).prepare_paginator()
        context = {
            'recipes_on_page': paginator_dict['on_page'],
            'range': range(2, 5),
            'pages_range': get_pagination_range(paginator_dict),
            'page_nr': paginator_dict['page'],
            'pag': paginator_dict['paginator'],
            'page_obj': paginator_dict['paginator'].page(paginator_dict['page']),
            'choice_rec_on_list': choice_rec_on_list,
        }
        return render(request, 'app-recipes.html', context=context)

    def post(self, request):
        records_on_list = request.POST.get('records')
        response = redirect(reverse('recipe_list'))
        response.set_cookie('records_on_list_recipe', records_on_list)
        return response


class DashboardView(View):
    def get(self, request):
        recipes = Recipe.objects.all()
        recipes_length = recipes.count()
        plans = Plan.objects.all()
        plans_length = plans.count()
        sorted_plans = Plan.objects.all().order_by('-created')
        context = {
            'recipes_length': recipes_length,
            'plans_length': plans_length,
            'last_added_plan': sorted_plans[0],
            'meals_from_last_added_plan': sorted_plans[0].recipeplan_set.all().order_by('day_name_id', 'order'),
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
        records_on_list = request.COOKIES.get('records_on_list_plan')
        choice_rec_on_list = [50, 25, 10, 5]
        paginator_dict = PaginatorClass(
            request, plans_sorted, int(records_on_list) if records_on_list is not None else 50).prepare_paginator()
        context = {
            'plans_on_page': paginator_dict['on_page'],
            'pages_range': get_pagination_range(paginator_dict),
            'pag': paginator_dict['paginator'],
            'page_nr': paginator_dict['page'],
            'page_obj': paginator_dict['paginator'].page(paginator_dict['page']),
            'choice_rec_on_list': choice_rec_on_list,
        }
        return render(request, 'app-schedules.html', context=context)

    def post(self, request):
        records_on_list = request.POST.get('records')
        response = redirect(reverse('plan_list'))
        response.set_cookie('records_on_list_plan', records_on_list)
        return response


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
            us_id = Plan.objects.latest('id').id
            return redirect(reverse('plan_details', args=(us_id,)))
        else:
            return render(request, 'app-add-schedules.html', context={'Error': 'Musisz wypełnić wszystkie pola!!'})


class PlanAddRecipe(View):
    plan_names_list = Plan.objects.all().order_by('name')
    recipe_names_list = Recipe.objects.all()

    def get(self, request):
        context = {
            'plan_names_list': self.plan_names_list,
            'recipe_names_list': self.recipe_names_list,
            'days': Days.CHOICES,
        }
        return render(request, 'app-schedules-meal-recipe.html', context=context)

    def post(self, request):
        plan_id = int(request.POST.get('plan'))
        order = int(request.POST.get('meal_number'))
        recipe_id = int(request.POST.get('recipe'))
        day_of_week = int(request.POST.get('day_of_week')) + 1
        meal_name = request.POST.get('meal_name')
        if not meal_name:
            context = {
                'Error': 'Nazwa posiłku nie może być pusta!',
                'plan_names_list': self.plan_names_list,
                'recipe_names_list': self.recipe_names_list,
                'days': Days.CHOICES,
            }
            return render(request, 'app-schedules-meal-recipe.html', context=context)

        RecipePlan.objects.create(meal_name=meal_name, order=order, day_name_id=day_of_week, plan_id=plan_id,
                                  recipe_id=recipe_id)

        return redirect('plan_details', us_id=plan_id)


class PlanDetailsView(View):
    def get(self, request, us_id):
        plan = Plan.objects.get(pk=us_id)
        days = RecipePlan.objects.filter(plan=us_id).order_by('day_name__order', 'order')
        context = {
            'id': us_id,
            'name': plan,
            'days': days,
        }
        return render(request, 'app-details-schedules.html', context=context)


class RecipeDetailsView(View):
    def get(self, request, us_id):
        recipe = Recipe.objects.get(pk=us_id)
        recipe_plan = RecipePlan.objects.filter(recipe_id=us_id).order_by('plan__name')
        return render(request, 'app-recipe-details.html', context={'recipe': recipe, 'recipe_plan': recipe_plan})

    def post(self, request, us_id):
        recipe_object = Recipe.objects.get(pk=us_id)
        if request.POST.get('likeButton') == 'like':
            recipe_object.votes += 1
            recipe_object.save()
        elif request.POST.get('unlikeButton') == 'unlike' and recipe_object.votes > 0:
            recipe_object.votes -= 1
            recipe_object.save()

        return redirect('recipe_details', us_id=us_id)


class RecipeModifyView(View):
    def get(self, request, us_id):
        recipe = get_object_or_404(Recipe, pk=us_id)
        return render(request, 'app-edit-recipe.html', context={'recipe': recipe})

    def post(self, request, us_id):
        name = request.POST['name']
        ingredients = request.POST['ingredients']
        description = request.POST['description']
        preparation_time = request.POST['time']
        prep_instructions = request.POST['instructions']
        if name and ingredients and description and prep_instructions and preparation_time:
            data = {
                'name': name,
                'ingredients': ingredients,
                'description': description,
                'preparation_time': int(preparation_time),
                'prep_instructions': prep_instructions,
            }
            if Recipe.objects.filter(name=name).exists():
                recipe = get_object_or_404(Recipe, pk=us_id)
                context = {
                    'error1': 'Taki przepis w bazie danych już istnieje!',
                    'recipe': recipe,
                }
                return render(request, 'app-edit-recipe.html', context=context)
            else:
                Recipe.objects.create(**data)
                return redirect('recipe_list')
        else:
            recipe = get_object_or_404(Recipe, pk=us_id)
            context = {
                'error': 'Musisz wypełnić wszystkie Pola!',
                'recipe': recipe,
            }
            return render(request, 'app-edit-recipe.html', context=context)


class SearchViewRecipes(View):
    def get(self, request):
        return render(request, 'app-search-recipe.html')

    def post(self, request):
        searching_value = request.POST.get('search_bar')
        recipes = Recipe.objects.filter(name__icontains=searching_value)
        no_results = True if len(recipes) == 0 else False
        context = {
            'searching_value': searching_value,
            'searched_value_from_data_base': recipes,
            'no_results': no_results,
        }
        return render(request, 'app-search-recipe.html', context=context)


class SearchViewPlans(View):
    def get(self, request):
        return render(request, 'app-search-plan.html')

    def post(self, request):
        searching_value = request.POST.get('search_bar')
        plans = Plan.objects.filter(name__icontains=searching_value)
        no_results = True if len(plans) == 0 else False
        context = {
            'searching_value': searching_value,
            'searched_value_from_data_base': plans,
            'no_results': no_results,
        }
        return render(request, 'app-search-plan.html', context=context)

      
class DeleteRecipePlanView(View):
    def get(self, request, us_id):
        return render(request, 'app-delete-confirmation.html', context={'id': request.META['HTTP_REFERER']})

    def post(self, request, us_id):
        RecipePlan.objects.get(pk=us_id).delete()
        previous = request.POST.get('next')
        return redirect(previous)


class EditScheduleView(View):
    def get(self, request, us_id):
        plan = Plan.objects.get(pk=us_id)
        return render(request, 'app-edit-schedules.html', context={'plan': plan})

    def post(self, request, us_id):
        plan = Plan.objects.get(pk=us_id)
        plan.name = request.POST['name']
        plan.description = request.POST['description']
        plan.save()
        return redirect('plan_list')


class DeleteRecipeView(View):
    def get(self, request, us_id):
        return render(request, 'app-delete-confirmation.html')

    def post(self, request, us_id):
        try:
            Recipe.objects.get(pk=us_id).delete()
        except ProtectedError:
            return render(request, 'app-recipes.html',
                          context={'error': 'Nie możesz usunąć przepisu który znajduje się w Planie!'})
        return redirect(reverse('recipe_list'))


class DeletePlanView(View):
    def get(self, request, us_id):
        return render(request, 'app-delete-confirmation.html')

    def post(self, request, us_id):
        try:
            Plan.objects.get(pk=us_id).delete()
        except ProtectedError:
            return render(request, 'app-schedules.html',
                          context={'error': 'Nie możesz usunąć planu w którym znajdują się przepisy!'})
        return redirect(reverse('plan_list'))


class PageView(View):
    def get(self, request, slug):
        if Page.objects.filter(slug=slug):
            page_details = Page.objects.get(slug=slug)
            context = {
                'page_details': page_details,
            }
            return render(request, page_details.slug + '.html', context)
        return redirect(reverse('index') + '#' + slug)
