from learn.models import Score
from rest_framework import serializers

class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = [
            'fail', 
            'success',
            'score', 
            'last_try', 
            'archive'
        ]