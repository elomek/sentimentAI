from django.db import models
from django.conf import settings

# Modèle des informations complémentaires des utilisateurs
class UserSite(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

# Modèle des avis des utilisateurs
class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    review_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Review by {self.user.username} - {self.review_text[:50]}..."

# Modèle d'analyse des sentiments des avis
class SentimentAnalysis(models.Model):
    SENTIMENT_CHOICES = [
        ("positive", "Positive"),
        ("negative", "Negative"),
    ]

    review = models.OneToOneField(Review, on_delete=models.CASCADE, related_name='sentiment_analysis')
    sentiment = models.CharField(max_length=10, choices=SENTIMENT_CHOICES)
    confidence = models.FloatField()

    def __str__(self):
        return f"Sentiment for Review {self.review.id}: {self.sentiment}"

