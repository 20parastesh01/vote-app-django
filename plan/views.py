from rest_framework import generics
from .serializers import CreatePlanSerializer, VoteSerializer
from rest_framework.response import Response
from django.db import transaction
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .selectors import get_plan_or_404, get_or_create_vote, update_votes_record
from . import exceptions
from rest_framework.exceptions import ValidationError
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
    except exceptions.FailedToVote as e:
        raise exceptions.FailedToVote(e)