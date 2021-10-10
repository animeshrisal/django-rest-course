import os
from celery import shared_task
import numpy as np
import pandas as pd
from sentiment import settings

@shared_task
def analyze(file):
    file_name = os.path.basename(file['file'])
    file_path = os.path.join(settings.MEDIA_ROOT + '/excel/' + file_name)
    df = pd.read_csv(file_path)
    
 