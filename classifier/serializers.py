from rest_framework import serializers
from .models import Review, SentimentAnalysis


'''class UserSiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSite
        fields =['id', 'first_name', 'last_name']'''


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields =['id', 'review_text', 'created_at']




class SentimentAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = SentimentAnalysis
        fields = ['sentiment', 'confidence']


class FullReviewSerializer(serializers.ModelSerializer):        #ترکیب Review با SentimentAnalysis برای نمایش یکجا
    sentiment_analysis = SentimentAnalysisSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'review_text', 'created_at', 'sentiment_analysis']