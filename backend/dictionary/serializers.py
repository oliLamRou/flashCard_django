from dictionary.models import Word
from rest_framework import serializers

class WordSerializer(serializers.ModelSerializer):
    user_score = serializers.SerializerMethodField()

    class Meta:
        model = Word
        fields = '__all__'

    def get_user_score(self, obj):
        score = getattr(obj, 'user_score', [])
        if score:
            return {
                'fail': score[0].fail,
                'success': score[0].success,
                'score': score[0].score,
                'last_try': score[0].last_try,
                'archive': score[0].archive,
            }
        return None
    
