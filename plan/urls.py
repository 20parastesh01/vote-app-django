from django.urls import path
from . import views


urlpatterns = [
    path('create-plan/', views.CreatePlan.as_view(), name='create_plan'),
    path('<int:plan_id>/vote/', views.vote_a_plan, name='vote_a_plan'),
]