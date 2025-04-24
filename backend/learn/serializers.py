from learn.models import Score
from rest_framework import serializers

class ScoreSerializer(serializers.Serializer):
    class Meta:
        model = Score
        fields = '__all__'