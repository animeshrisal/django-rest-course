from rest_framework import serializers

from app.models import AnalyzedFile, ExcelFile

class ExcelFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExcelFile
        fields = ['id', 'file']

class AnalyzedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnalyzedFile
        fields = ['id', 'text', 'pos', 'neg', 'neu', 'compound']
        read_only_fields = ['pos', 'neg', 'neu', 'compound']