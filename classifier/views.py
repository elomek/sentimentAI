from django.shortcuts import render
from rest_framework import status
from transformers import pipeline
from .permissions import IsOwnerOrAdminForDelete
from rest_framework.viewsets import ModelViewSet
from .models import Review, SentimentAnalysis, UserSite
from .serializers import ReviewSerializer, SentimentAnalysisSerializer, FullReviewSerializer

# Create your views here.
def home_page_view(request):
    return render(request, 'home.html')

sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

class ReviewViewSet(ModelViewSet):
    serializer_class =  FullReviewSerializer 
    queryset = Review.objects.all()
    permission_classes = [IsOwnerOrAdminForDelete]
    
    def perform_create(self, serializer):
        review = serializer.save(user=self.request.user)

     
        prediction = sentiment_pipeline(review.review_text)[0]
        sentiment_label = prediction["label"].lower()  # POSITIVE / NEGATIVE → positive / negative
        confidence = prediction["score"]

        # ذخیره نتیجه در مدل SentimentAnalysis
        sentiment_analysis = SentimentAnalysis.objects.create(
            review=review,
            sentiment=sentiment_label,
            confidence=confidence
        )

        
 


'''class UserSiteViewSet(ModelViewSet):
    serializer_class = UserSiteSerializer
    queryset = UserSite.objects.all()'''