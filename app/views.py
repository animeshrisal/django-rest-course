from django.http.response import Http404
from django.shortcuts import render
from django.views import generic
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework import status
from rest_framework.response import Response
from app.models import AnalyzedFile

from app.serializers import AnalyzedFileSerializer, ExcelFileSerializer
from app.services import get_sentiment_scores
from .tasks import analyze

# Create your views here.
class FileUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):

        context = {'request': request }
        serializer = ExcelFileSerializer(data=request.data, context=context)

        # Serializer checks if all the data is validated or not
        # If it is valid then the data is saved
        # If not then error is sent to the frontend

        if serializer.is_valid():
            serializer.save(user_id=request.user)
            analyze.delay(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdateSentimentText(APIView):
    serializer_class = AnalyzedFileSerializer
    queryset = AnalyzedFile.objects.all()

    def get_object(self, pk):
        try:
            return AnalyzedFile.objects.get(pk=pk)
        except AnalyzedFile.DoesNotExist:
            raise Http404

    def put(self, request, pk):
        snippet = self.get_object(pk)
        serializer = AnalyzedFileSerializer(snippet, data=request.data)

        if serializer.is_valid():
            score = get_sentiment_scores(request.data['text'])
            serializer.save(
                pos = score['pos'],
                neg = score['neg'],
                neu = score['neu'],
                compound = score['compound']
            )
            return Response(serializer.data)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)