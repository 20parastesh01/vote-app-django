from rest_framework.generics import CreateAPIView
from .serializers import CreatePlanSerializer
from rest_framework.response import Response
from django.db import transaction


@transaction.atomic
class CreatePlan(CreateAPIView):
    serializer_class = CreatePlanSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        plan = serializer.save()
        
        response_serializer = CreatePlanSerializer(plan)
        
        return Response(response_serializer.data, status=201)