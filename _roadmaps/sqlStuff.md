Great! You're working with Django models. Based on what you described, let's assume we have models like:

```python
class Word(models.Model):
    french = models.CharField(max_length=100)
    korean = models.CharField(max_length=100)

class Score(models.Model):
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    good = models.IntegerField(default=0)
    bad = models.IntegerField(default=0)
    last_try = models.DateTimeField(null=True, blank=True)
```

Now, let's address your queries one by one:

---

### ✅ 1. Get all `Word` with or without a `Score`

This is a **left outer join**:
```python
from django.db.models import OuterRef, Subquery

words_with_scores = Word.objects.all().annotate(
    score_id=Subquery(Score.objects.filter(word=OuterRef('pk')).values('id')[:1])
)
```

Or more simply:
```python
from django.db.models import Q

# Words that have a Score
words_with_score = Word.objects.filter(score__isnull=False)

# Words that don't have a Score
words_without_score = Word.objects.filter(score__isnull=True)

# All words, regardless of Score
all_words = Word.objects.all()
```

---

### ✅ 2. Get all `Word` that have a score where `good > bad`

```python
words = Word.objects.filter(score__good__gt=F('score__bad'))
```

---

### ✅ 3. Get all `Word` that have not been tried in a month

```python
from django.utils import timezone
from datetime import timedelta

one_month_ago = timezone.now() - timedelta(days=30)

words = Word.objects.filter(
    Q(score__last_try__lt=one_month_ago) | Q(score__last_try__isnull=True)
)
```

---

### ✅ 4. Get 10% of words where `good > bad`

```python
from math import ceil

words_with_positive_score = Word.objects.filter(score__good__gt=F('score__bad'))
count = words_with_positive_score.count()
ten_percent = ceil(count * 0.1)

sample = words_with_positive_score.order_by("?")[:ten_percent]
```

---

Let me know if you're using `related_name` on your ForeignKey or if you want to filter using Score directly (like `Score.objects.filter(...)` returning `Word` objects). I can adapt it!