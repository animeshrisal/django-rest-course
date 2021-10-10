from django.urls import path
from .views import FileUploadView, UpdateSentimentText
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('upload/', FileUploadView.as_view()),
    path('update_sentiment/<int:pk>/', UpdateSentimentText.as_view())
]
