"""scrumlab URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from jedzonko.views import IndexView, LandingPageView, \
    RecipeListView, DashboardView, AddRecipe, PlanListView, \
    AddPlan, PlanAddRecipe, RecipeDetailsView, SearchViewRecipes, SearchViewPlans, PlanDetailsView, RecipeModifyView, \
    DeleteRecipePlanView, EditScheduleView, DeleteRecipeView, DeletePlanView, PageView
from scrumlab import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', IndexView.as_view()),
    path('', LandingPageView.as_view(), name='index'),
    path('recipe/list/', RecipeListView.as_view(), name='recipe_list'),
    path('main/', DashboardView.as_view(), name='dashboard'),
    path('recipe/add/', AddRecipe.as_view(), name='add_recipe'),
    path('plan/list/', PlanListView.as_view(), name='plan_list'),
    path('plan/add/', AddPlan.as_view(), name='add_plan'),
    path('plan/add-recipe/', PlanAddRecipe.as_view(), name='plan_add_recipe'),
    path('plan/<int:us_id>/', PlanDetailsView.as_view(), name='plan_details'),
    path('recipe/<int:us_id>/', RecipeDetailsView.as_view(), name='recipe_details'),
    path('recipe/modify/<int:us_id>/', RecipeModifyView.as_view(), name='modify_recipe'),
    path('search-recipe/', SearchViewRecipes.as_view(), name='search_recipe'),
    path('search-plan/', SearchViewPlans.as_view(), name='search_plan'),
    path('plan/modify/<int:us_id>', EditScheduleView.as_view(), name='modify_plan'),
    path('plan/<int:us_id>/delete_recipe/', DeleteRecipePlanView.as_view(), name='delete_recipe_from_plan'),
    path('recipe/<int:us_id>/delete/', DeleteRecipeView.as_view(), name='delete_recipe'),
    path('plan/<int:us_id>/delete', DeletePlanView.as_view(), name='delete_plan'),
    path('<slug:slug>/', PageView.as_view(), name='page_views'),
]
