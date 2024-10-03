from rest_framework import serializers
from .models import Plan

class CreatePlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ['title', 'body']

    def create(self, validated_data):
        return super().create(validated_data)
