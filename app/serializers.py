from rest_framework import serializers

from app.models import AnalyzedFile, ExcelFile

class ExcelFileSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        file = ExcelFile.objects.create(
            file = validated_data['file'],
            user=self.context['request'].user
        )

        return file
        
    class Meta:
        model = ExcelFile
        fields = ['id', 'file']

class AnalyzedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnalyzedFile
        fields = ['id', 'text', 'pos', 'neg', 'neu', 'compound']
        read_only_fields = ['pos', 'neg', 'neu', 'compound']