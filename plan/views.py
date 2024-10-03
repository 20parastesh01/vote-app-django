from rest_framework import generics
from .serializers import CreatePlanSerializer, VoteSerializer, PlanResultSerializer
from rest_framework.response import Response
from django.db import transaction
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .selectors import get_plan_or_404, get_or_create_vote, update_votes_record, get_plans, get_votes_record_by_plan_id, get_vote_by_plan_and_user
from . import exceptions
from rest_framework.exceptions import ValidationError, APIException
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from .throttles import HighVoteThrottle, LowVoteThrottle


class CreatePlan(generics.CreateAPIView):
    serializer_class = CreatePlanSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        plan = serializer.save()
        
        response_serializer = CreatePlanSerializer(plan)
        
        return Response({'data': [response_serializer.data], 'message': 'Plan created successfuly.', 'code': 201}, status=201)

@transaction.atomic
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@throttle_classes([UserRateThrottle, AnonRateThrottle, HighVoteThrottle, LowVoteThrottle])
def vote_a_plan(request, plan_id):
    try: 
        user = request.user

        serializer = VoteSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        vote_value = serializer.validated_data['vote']

        plan = get_plan_or_404(plan_id)

        vote, created, old_vote_value = get_or_create_vote(plan, user, vote_value)

        update_votes_record(plan, vote_value, old_vote_value)
        
        return Response({'data': [vote_value] ,'message': 'Vote successfully submitted.', 'code': 200}, status=status.HTTP_200_OK)

    except ValidationError as e:
        raise ValidationError({'error': e.messages})
    except Exception as e:
        if isinstance(e, APIException):
            raise exceptions.FailedToVote(e)
        else:
            raise exceptions.FailedToVote('Failed to submit vote.')

@transaction.atomic    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@throttle_classes([UserRateThrottle, AnonRateThrottle])
def get_results(request):
    try:
        user = request.user
        results = []
        
        plans = get_plans()
        
        for plan in plans:
            votes_record = get_votes_record_by_plan_id(plan)
            if votes_record:
                you_have_voted = get_vote_by_plan_and_user(plan, user)
                serializer = PlanResultSerializer(votes_record)
                result = serializer.data
                result["youHaveVoted"] = you_have_voted
            else:
                result = {
                    "title": plan.title,
                    "average": 0.0,
                    "total": 0,
                    "youHaveVoted": False,
                }
            results.append(result)

        return Response({'data': [results], 'message': 'Got results successfully.', 'code': 200}, status=status.HTTP_200_OK)

    except Exception as e:
        if isinstance(e, APIException):
            raise exceptions.FailedToGetResults(e)
        else:
            raise exceptions.FailedToGetResults('Failed to get results.')