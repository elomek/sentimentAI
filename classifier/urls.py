from django.urls import path,  include
from .import views
from rest_framework.routers import DefaultRouter
from .views import ReviewViewSet


router = DefaultRouter()
router.register(r'submit-comment', ReviewViewSet, basename='submit_comment')
# router.register(r'usersite', UserSiteViewSet, basename = 'usersite')

urlpatterns = [
    path('',views.home_page_view, name='home'), 
    path('api/', include(router.urls)),
   
]