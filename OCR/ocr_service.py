import config
from threading import Thread
from AbbyyOnlineSdk import *
from Queue import Queue
import utils


@utils.singleton
class OcrService(Thread):
    """This is a wrapper for abbyy OCR"""

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

    def run(self):
        while not self.should_stop:
            ocr_task = self.ocr_queue.get(block=True, timeout=None)

            print "Uploading.."
            settings = ProcessingSettings()
            settings.Language = ocr_task.language
            settings.OutputFormat = ocr_task.outputFormat
            task = self.processor.ProcessImage(ocr_task.filePath, settings)
            if task == None:
                print "Error"
                return
            if task.Status == "NotEnoughCredits":
                print "Not enough credits to process the document. Please add more pages to your application's account."
                return

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
                    self.processor.DownloadResult(task, ocr_task.resultFilePath)
                    print "Result was written to %s" % ocr_task.resultFilePath
            else:
                print "Error processing task"

    def enqueue_ocr_task(self, filePath, resultFilePath, language, outputFormat):
        ocr_task = {
            'filePath': filePath,
            'resultFilePath': resultFilePath,
            'language': language,
            'outputFormat': outputFormat
        }

        self.ocr_queue.put(ocr_task)

    def stop(self):
        self.should_stop = True
