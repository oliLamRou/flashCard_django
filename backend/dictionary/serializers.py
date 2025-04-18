from dictionary.models import Word
from rest_framework import serializers

from learn.serializers import ScoreSerializer

class WordSerializer(serializers.ModelSerializer):
    user_score = serializers.SerializerMethodField()

    class Meta:
        model = Word
        fields = '__all__'

    def get_user_score(self, obj):
        score = getattr(obj, 'user_scores', [])
        if score:
            return {
                'fail': score[0].fail,
                'success': score[0].success,
                'last_try': score[0].last_try,
            }
        return None