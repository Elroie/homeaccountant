import threading, utils
from config import BASE_PATH
from ImageRecognitionModel import ImageRecognitionModel
from Queue import Queue


@utils.singleton
class ClassificationManager(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self, name="Classification_Manager")
        self._electricity_classifier = \
            ImageRecognitionModel(BASE_PATH + 'ML/images/electricity/train', 'Electricity Bill', 'elec')

        self._water_classifier = \
            ImageRecognitionModel(BASE_PATH +'/ML/images/water/train', 'Water Bill', 'wa')

        # we bound the queue to hold only max of 1000 classification tasks.
        self._classification_queue = Queue(1000)
        self._lock = threading.Lock()
        self._should_stop = False

    def run(self):
        """Start the classification thread"""
        try:
            self._train()
            self._test()
        except Exception as ex:
            print 'error ' + ex.message
            self.stop()

        while not self._should_stop:
            # take classification task, block if empty.
            classification_task = self._classification_queue.get(block=True, timeout=None)
            classification = self._electricity_classifier.classify(classification_task)
            if classification.get_result():
                # save to db as electricity bill.
                pass
            elif self._water_classifier.classify(classification_task).get_result():
                # save to db as water bill.
                pass
            else:
                # save to db as UNKNOWN RECEIPT
                pass

    def stop(self):
        self._should_stop = True

    def _train(self):
        """ Train all classification models """
        self._electricity_classifier.train()
        self._water_classifier.train()

    # elroie TODO: make this running in a loop.
    def _test(self):
        """ Test all classification models """
        classification = self._electricity_classifier.classify(
            BASE_PATH + 'ML/images/electricity/test/negative_test.jpeg')
        assert classification.get_result() is False

        classification = \
            self._electricity_classifier.classify(BASE_PATH + 'ML/images/electricity/test/test1.jpg')
        assert classification.get_result() is True

        classification = \
            self._electricity_classifier.classify(BASE_PATH + 'ML/images/electricity/test/negative_test1.jpg')
        assert classification.get_result() is False

        classification = self._electricity_classifier.classify(
            BASE_PATH + 'ML/images/electricity/test/negative_test2.jpg')
        assert classification.get_result() is False

        classification = self._water_classifier.classify(
            BASE_PATH + 'ML/images/water/test/negative_test2.jpg')
        assert classification.get_result() is False

        classification = self._water_classifier.classify(
            BASE_PATH + 'ML/images/water/test/negative_test2.jpg')
        assert classification.get_result() is False

        classification = self._water_classifier.classify(
            BASE_PATH + 'ML/images/water/test/negative_test12.jpg')
        assert classification.get_result() is False

        classification = self._water_classifier.classify(
            BASE_PATH + 'ML/images/water/test/test1.jpg')
        assert classification.get_result() is True

        classification = self._water_classifier.classify(
            BASE_PATH + 'ML/images/water/test/negative_test1.jpg')
        assert classification.get_result() is False

        print 'finish testing, sit back and enjoy :)'
