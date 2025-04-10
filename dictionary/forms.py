from django import forms
from dictionary.models import Word
from accounts.models import Preference


class WordForm(forms.ModelForm):
    class Meta:
        model = Word
        fields = ['french', 'korean', 'english', 'word_class']

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            preference = Preference.objects.filter(user=user).first()
            if preference:
                langA = preference.languageA
                langB = preference.languageB

                # Keep only languageA and word_class in the form
                lang_fields = {
                    'FR': 'french',
                    'EN': 'english',
                    'KR': 'korean'
                }
                keep_fieldA = lang_fields.get(langA)
                keep_fieldB = lang_fields.get(langB)

                # Hide the others
                for lang_code, field_name in lang_fields.items():
                    if field_name == keep_fieldA:
                        continue
                    elif field_name == keep_fieldB:
                        continue
                    elif field_name == 'word_class':
                        continue
                    else:
                        self.fields.pop(field_name, None)