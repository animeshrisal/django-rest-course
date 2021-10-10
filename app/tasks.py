import os
from celery import shared_task
import numpy as np
import pandas as pd
from sentiment import settings
from .models import AnalyzedFile

from nltk.sentiment.vader import SentimentIntensityAnalyzer

from django.db import transaction

@shared_task
def analyze(file):
    #Get file name
    file_name = os.path.basename(file['file'])
    
    #Get file path
    file_path = os.path.join(settings.MEDIA_ROOT + '/excel/' + file_name)
    
    #Read the file in pandas
    df = pd.read_csv(file_path)   

    sid = SentimentIntensityAnalyzer()
    

    #Atomic transactions will either save all entries or none if an error occurs
    with transaction.atomic():
        for index, row in df.iterrows():

            #Get sentiment scores
            sentiment_scores = sid.polarity_scores(row['text'])
            
            AnalyzedFile.objects.create(
                text = row['text'],
                pos = sentiment_scores['pos'],
                neg = sentiment_scores['neg'],
                neu = sentiment_scores['neu'],
                compound = sentiment_scores['compound'],
                file_id = file['id']
            )


    
    
 