import os
from celery import shared_task
import numpy as np
import pandas as pd
from app.services import get_sentiment_scores
from sentiment import settings
from .models import AnalyzedFile, ExcelFile

from django.core.mail import EmailMessage

from django.db import transaction

import uuid

@shared_task
def analyze(file):
    #Get file name
    file_name = os.path.basename(file['file'])
    
    #Get file path
    file_path = os.path.join(settings.MEDIA_ROOT + '/excel/' + file_name)
    
    #Read the file in pandas
    df = pd.read_csv(file_path)   


    #Atomic transactions will either save all entries or none if an error occurs
    with transaction.atomic():
        for index, row in df.iterrows():

            #Get sentiment scores
            sentiment_scores = get_sentiment_scores(row['text'])
            
            AnalyzedFile.objects.create(
                text = row['text'],
                pos = sentiment_scores['pos'],
                neg = sentiment_scores['neg'],
                neu = sentiment_scores['neu'],
                compound = sentiment_scores['compound'],
                file_id = file['id']
            )


@shared_task
def export_data(excel_file_id, user):
    
    #Reads from database and makes a dataframe
    df = pd.DataFrame.from_records(AnalyzedFile.objects.filter(file_id=excel_file_id).values())
    
    #Removes last column
    df = df.iloc[:, :-1]

    try:
        email = EmailMessage(
            'Your excel file is ready',
            '',
            settings.EMAIL_HOST_USER,
            [user]
        )

        #Generate file name
        name = uuid.uuid4()

        file_path = 'media/excel/' + str(name) + '.csv'
        
        #Create CSV FIle
        df.to_csv(file_path, index=False)

        #Sends email
        email.attach_file(file_path)
        email.send()

        os.remove(file_path) 

    except Exception as e:
        print(e)
