from django.db.models.query import QuerySet
from django.http.response import Http404
from django.shortcuts import render
from django.views import generic
from rest_framework import serializers
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.views import APIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework import status
from rest_framework.response import Response
from app.helpers import StandardResultsSetPagination
from app.models import AnalyzedFile, ExcelFile

from app.serializers import AnalyzedFileSerializer, ExcelFileSerializer
from app.services import get_sentiment_scores
from .tasks import analyze, export_data



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

        excel_file = ExcelFile.objects.get(id=snippet.file_id)

        #Check if the excel file belongs to the user
        if(excel_file.user_id == request.user.id):
            return Response({'error': 'You are not authorized to change this'}, status=status.HTTP_403_FORBIDDEN)

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

class ExportData(APIView):
    serializer_class = ExcelFileSerializer
    queryset = ExcelFile.objects.all()

    def does_file_exist(self, pk):
        try:
            value = ExcelFile.objects.get(pk=pk)
            return True
        except ExcelFile.DoesNotExist:
            return False

    def get(self, request, pk):
        if self.does_file_exist(pk):
            export_data.delay(pk, request.user.email)
            return Response({'message': 'Your file is being prepared. An excel file will be emailed to you shortly'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Could not find file'}, status=status.HTTP_404_NOT_FOUND)

class ViewSentimentScoresView(ListAPIView):
    serializer_class = AnalyzedFileSerializer
    queryset = AnalyzedFile.objects.all()
    pagination_class = StandardResultsSetPagination

    def get(self, request, excel_id):
        queryset = self.queryset.filter(file_id=excel_id)
        page = self.paginate_queryset(queryset)

        serializer = AnalyzedFileSerializer(page, many=True)
        result = self.get_paginated_response(serializer.data)

        return result