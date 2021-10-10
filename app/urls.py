from django.urls import path
from .views import FileUploadView, UpdateSentimentText

urlpatterns = [
    path('upload/', FileUploadView.as_view()),
    path('update_sentiment/<int:pk>/', UpdateSentimentText.as_view())
]
