from django.urls import path
from . import views


urlpatterns = [
    path('create-plan/', views.CreatePlan.as_view(), name='create_plan'),
]