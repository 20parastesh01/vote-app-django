from rest_framework import serializers
from .models import Plan, Vote


class CreatePlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ['title', 'body']

    def create(self, validated_data):
        return super().create(validated_data)

class VoteSerializer(serializers.ModelSerializer):
    vote = serializers.ChoiceField(choices=[(i, i) for i in range(1, 6)], required=True)
    class Meta:
        model = Vote
        fields = ['vote']

    def validate_vote(self, value):
        if not isinstance(value, int) or value not in [1, 2, 3, 4, 5]:
            raise serializers.ValidationError("Vote value must be an integer between 1 and 5.")
        return value
