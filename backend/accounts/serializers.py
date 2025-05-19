from rest_framework import serializers

from accounts.models import Preference

class PreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Preference
        fields = [
            'languageA', 
            'languageB', 
            'learnMode',
            'learnDeck',
        ]