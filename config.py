import os

basedir = os.path.abspath(os.path.dirname(__file__))

BASE_PATH = '/Users/elroie/Computer Science/Final Project/Project/homeaccountant/'

###### Machine Learning Configurations ######
SHOULD_USE_MACHINE_LEARNING = True
SHOULD_SAVE_MODEL = False
#############################################

###### OCR ######
SHOULD_USE_OCR = True
APPLICATION_ID = 'HomeAccountant'
APPLICATION_PASSWORD = 'TAlOOpwRaKq5V+jEgOW+MFXK'
#############################################


class Config(object):
    UPLOADS_PATH = os.path.join(basedir, 'media', 'upload')