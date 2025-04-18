from django import forms
from dictionary.models import Word
from accounts.models import Preference
from commun.enums import LANGUAGE


class WordForm(forms.ModelForm):
    class Meta:
        model = Word
        fields = ['FR', 'KR', 'EN', 'word_class']

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.language_labels = dict(LANGUAGE.choices)

        if user:
            preference = Preference.objects.filter(user=user).first()
            if preference:
                keep_columns = [
                    preference.languageA,
                    preference.languageB,
                    'word_class'
                    ]

                columns = self.fields.copy().keys()

                for column in columns:
                    if column in keep_columns:
                        continue
                    else:
                        self.fields.pop(column, None)