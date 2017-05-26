import os

basedir = os.path.abspath(os.path.dirname(__file__))

BASE_PATH = basedir + '/'

###### Machine Learning Configurations ######
SHOULD_USE_MACHINE_LEARNING = True
SHOULD_SAVE_MODEL = False
#############################################

###### OCR ######
SHOULD_USE_OCR = False
# APPLICATION_ID = 'HomeAccountant'
# APPLICATION_PASSWORD = 'TAlOOpwRaKq5V+jEgOW+MFXK'
APPLICATION_ID = 'home_bills'
APPLICATION_PASSWORD = 'fo39+Fy0MPEleDRQ4OyAj0yz'
#############################################

###### DB ######
DB_NAME = 'homeaccountant'
#############################################


class Config(object):
    DEBUG = True
    UPLOADS_PATH = os.path.join(basedir, 'media', 'upload')
    SECRET_KEY = 'HRHIHHNJANU='