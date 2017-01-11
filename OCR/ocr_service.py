import config
import requests
from base64 import b64encode


class OcrService(object):
    """This is a wrapper for abbyy OCR"""

    def __init__(self):
        self.processing_url = 'https://cloud.ocrsdk.com/processImage'
        self.authentication_token = b64encode('{0}:{1}'.format(config.APPLICATION_ID, config.APPLICATION_PASSWORD))

    def process_image(self, image_path):

        headers = {'Authorization': 'Basic ' + self.authentication_token}
        payload = {
            'file': open(image_path)
        }
        url = '{0}?{1}&{2}&{3}'.format(self.processing_url, 'language=Hebrew', 'profile=documentConversion', 'exportFormat=docx')
        response = requests.post(url, headers=headers, data=payload)
        print response.status_code, response.text

    def _enqueue_processing_task(self, user_id, image):
        pass
