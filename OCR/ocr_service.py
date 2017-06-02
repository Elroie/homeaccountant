import config, utils
from threading import Thread
from AbbyyOnlineSdk import *
from Queue import Queue
from mongoengine import connect
from Entities.UserImage import UserImage
from Entities.ScannedImage import ScannedImage
from OCR.TextExtractor import TextExtractorBase


class OcrService(Thread):
    """This is a wrapper for abbyy OCR123"""

    __metaclass__ = utils.Singleton

    def __init__(self):
        Thread.__init__(self, name="OCR_Service")
        self.processor = AbbyyOnlineSdk()
        self.ocr_queue = Queue()
        self.should_stop = False
        if "ABBYY_APPID" in os.environ:
            self.processor.ApplicationId = os.environ["ABBYY_APPID"]

        if "ABBYY_PWD" in os.environ:
            self.processor.Password = os.environ["ABBYY_PWD"]

        # Proxy settings
        if "http_proxy" in os.environ:
            proxyString = os.environ["http_proxy"]
            print "Using proxy at %s" % proxyString
            self.processor.Proxy = urllib2.ProxyHandler({"http": proxyString})

        return

    def run(self):
        try:
            while not self.should_stop:
                ocr_task = self.ocr_queue.get(block=True, timeout=None)

                print "Uploading.."
                settings = ProcessingSettings()
                settings.Language = ocr_task['language']
                settings.OutputFormat = ocr_task['outputFormat']
                task = self.processor.ProcessImage(ocr_task['filePath'], settings)
                if task == None:
                    print "Error"
                if task.Status == "NotEnoughCredits":
                    print "Not enough credits to process the document. Please add more pages to your application's account."

                print "Id = %s" % task.Id
                print "Status = %s" % task.Status

                # Wait for the task to be completed
                sys.stdout.write("Waiting..")

                while task.IsActive() == True:
                    time.sleep(5)
                    sys.stdout.write(".")
                    task = self.processor.GetTaskStatus(task)

                print "Status = %s" % task.Status

                if task.Status == "Completed":
                    if task.DownloadUrl != None:
                        self.processor.DownloadResult(task, ocr_task['resultFilePath'])
                        print "Result was written to %s" % ocr_task['resultFilePath']

                        connect(config.DB_NAME)
                        user_image = UserImage.objects(id=ocr_task['image_id']).first()
                        scanned_image = ScannedImage(user_id=ocr_task['user_id'])
                        scanned_image.status = 'pending'
                        scanned_image.original_image = user_image
                        scanned_image.unique_id = ocr_task['unique_id']

                        with open(ocr_task['resultFilePath']) as f:
                            scanned_image.text = f.read()

                        # try extract data from ocr.... in any case save the ocr result
                        try:
                            text_extractor = TextExtractorBase.create(ocr_task['classification_type'])
                            scanned_image.to_date = text_extractor.get_date(ocr_task['resultFilePath'])
                            scanned_image.price = text_extractor.get_price(ocr_task['resultFilePath'])
                            # scanned_image.to_date = '14/5/2017'
                            # scanned_image.price = 590
                        except Exception as e:
                            print e

                        scanned_image.save()
                else:
                    print "Error processing task"
        except Exception as ex:
            # we should suppress and log the errors inside the threads since we don't want this manager to die.
            print ex.message

    def enqueue_ocr_task(self, user_id, image_id, filePath, resultFilePath, classification_type,language='Hebrew', outputFormat='txt', unique_id=None):
        ocr_task = {
            'user_id': user_id,
            'image_id': image_id,
            'filePath': filePath,
            'resultFilePath': resultFilePath,
            'classification_type': classification_type,
            'language': language,
            'outputFormat': outputFormat,
            'unique_id': unique_id
        }

        self.ocr_queue.put(ocr_task)

    def stop(self):
        self.should_stop = True
