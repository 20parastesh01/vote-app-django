from . import exceptions
from .models import Plan, Vote, VotesRecord
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError as DjangoValidationError


def get_plan_or_404(plan_id):
    try:
        return get_object_or_404(Plan, id=plan_id)
    except Exception as e:
        raise exceptions.FailedToGetPlan('Failed to get or plan.') from e

def get_or_create_vote(plan, user, vote_value):
    try:
        vote, created = Vote.objects.get_or_create(plan=plan, voted_by=user, defaults={'vote': vote_value})
        
        if not created:
            old_vote_value = vote.vote
            vote.vote = vote_value
            vote.save()
        else:
            old_vote_value = None
        
        return vote, created, old_vote_value
    except Exception as e:
        raise exceptions.FailedToCreateOrGetVote('Failed to get or create vote.') from e

def update_votes_record(plan, vote_value, old_vote_value=None):
    try:
        votes_record, record_created = VotesRecord.objects.get_or_create(plan=plan)
        
        if not record_created:
            if old_vote_value is not None:
                votes_record.votes_average = ((votes_record.votes_average * votes_record.total_voters) - old_vote_value + vote_value) / votes_record.total_voters
            else:
                votes_record.votes_average = ((votes_record.votes_average * votes_record.total_voters) + vote_value) / (votes_record.total_voters + 1)
                votes_record.total_voters += 1
        else:
            votes_record.total_voters = 1
            votes_record.votes_average = vote_value

        votes_record.save()
        return votes_record
    except DjangoValidationError as e:
        raise ValidationError({'error': e.messages})
    except Exception as e:
        raise exceptions.FailedToUpdateVoteRecords('Failed to update vote records.') from e
    
def get_plans():
    try:
        return Plan.objects.all()
    except Exception as e:
        raise exceptions.FailedToGetPlans('Failed to get plans.')
    
def get_votes_record_by_plan_id(plan):
    try:
        return VotesRecord.objects.filter(plan=plan).first()
    except Exception as e:
        raise exceptions.FailedToGetVotesRecord('Failed to get votes record for this plan.')
    
def get_vote_by_plan_and_user(plan, user):
    try:
        return Vote.objects.filter(plan=plan, voted_by=user).exists()
    except Exception as e:
        raise exceptions.FailedToGetVote('Failed to get vote.')