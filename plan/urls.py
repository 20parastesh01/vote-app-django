from . import views
from django.urls import path


urlpatterns = [
    path('create-plan/', views.CreatePlan.as_view(), name='create_plan'),
    path('<int:plan_id>/vote/', views.vote_a_plan, name='vote_a_plan'),
    path('results/', views.get_results, name='get_results'),
]