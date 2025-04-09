from django.contrib import admin
from .models import UserSite, Review, SentimentAnalysis



admin.site.register(UserSite)

admin.site.register(Review)

admin.site.register(SentimentAnalysis)


# Register your models here.
