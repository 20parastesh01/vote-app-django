from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class Plan(models.Model):
    title = models.CharField('title', max_length=100, null= False, blank= False)
    body = models.CharField('body', max_length=1000, null= False, blank= False)

class Vote(models.Model):
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT)
    voted_by = models.ForeignKey(User, on_delete=models.PROTECT) 
    vote_value_choices = [
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    ]
    vote = models.IntegerField('vote', null=False, choices=vote_value_choices)
    created_at = models.DateTimeField('createdAt', auto_now_add=True)
    updated_at = models.DateTimeField('updatedAt', auto_now=True)
    
class VotesRecord(models.Model):
    plan = models.ForeignKey(Plan, null=False, on_delete=models.CASCADE)
    total_voters = models.IntegerField('totalVoters', null=False, default=0)
    votes_average = models.FloatField('votesAverage', null=False, default=0)