from django.urls import path
from .views import ExportData, FileUploadView, UpdateSentimentText, ViewSentimentScoresView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('upload/', FileUploadView.as_view()),
    path('update_sentiment/<int:pk>/', UpdateSentimentText.as_view()),
    path('export_data/<int:pk>/', ExportData.as_view()),
    path('view_sentiment_scores/<int:excel_id>/', ViewSentimentScoresView.as_view())
]
