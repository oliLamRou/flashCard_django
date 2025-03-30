from django import forms
from dictionary.models import Word

class WordForm(forms.ModelForm):
    class Meta:
        model = Word
        fields = ['french', 'korean']