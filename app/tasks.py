import os
from celery import shared_task
import numpy as np
import pandas as pd
from sentiment import settings

@shared_task
def analyze(file):

    #Get file name
    file_name = os.path.basename(file['file'])
    
    #Get file path
    file_path = os.path.join(settings.MEDIA_ROOT + '/excel/' + file_name)
    
    #Read the file in pandas
    df = pd.read_csv(file_path)
    print(df)
    
 