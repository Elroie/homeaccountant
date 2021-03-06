import threading, utils, os, uuid

import ntpath
from ML.FeedNoteManager import FeedNoteManager
from config import BASE_PATH, DB_NAME
from ImageRecognitionModel import ImageRecognitionModel
from Queue import Queue
from mongoengine import connect
from Entities.User import User
from Entities.UserImage  import UserImage
from OCR.ocr_service import OcrService

from ML import ClassificationResult


class ClassificationManager(threading.Thread):
    __metaclass__ = utils.Singleton

    def __init__(self):
        threading.Thread.__init__(self, name="Classification_Manager")
        self.feed_note_manager = FeedNoteManager()
        self.electricity = 'Electricity Bill'
        self.water = 'Water Bill'

        self._electricity_classifier = \
            ImageRecognitionModel(BASE_PATH + 'ML/images/electricity/train', self.electricity, 'elec')

        self._water_classifier = \
            ImageRecognitionModel(BASE_PATH +'/ML/images/water/train', self.water, 'wa')

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
            try:
                # take classification task, block if empty.
                classification_task = self._classification_queue.get(block=True, timeout=None)
                classification_result = self._electricity_classifier.classify(classification_task['image_path'])
                ocr_service = OcrService()
                image_path = classification_task['image_path']

                if classification_result.get_type() == self.electricity and classification_result.get_result() == True:
                    # save to db as electricity bill.
                    print 'save to db as electricity bill.'
                    user_image = self._save_classification_result(classification_task, classification_result)

                    file_name = image_path.split('.')[0]
                    ocr_service.enqueue_ocr_task(
                        classification_task['user_id'],
                        user_image.id,
                        image_path,
                        file_name + '_scanned.txt',
                        self.electricity,
                        unique_id=classification_task['unique_id']
                    )
                else:
                    classification_result = self._water_classifier.classify(classification_task['image_path'])
                    if classification_result.get_type() == self.water and classification_result.get_result() == True:
                        # save to db as water bill.
                        print "save to db as water bill."
                        user_image = self._save_classification_result(classification_task, classification_result)
                        file_name = image_path.split('.')[0]
                        ocr_service.enqueue_ocr_task(
                            classification_task['user_id'],
                            user_image.id,
                            image_path,
                            file_name,
                            self.water,
                            classification_task['unique_id']
                        )
                    else:
                        # we couldn't classify this image... no OCR required
                        print "we couldn't classify this image... no OCR required"
                        classification_result = ClassificationResult.ClassificationResult("General", False)
                        self._save_classification_result(classification_task, classification_result)
            except Exception as ex:
                # we should suppress and log the errors inside the threads since we don't want this manager to die.
                print ex.message

    def stop(self):
        self._should_stop = True

    def enqueue_classification_task(self, user_id, image_path, unique_id):
        self._classification_queue.put({'user_id': user_id, 'image_path': image_path, 'unique_id': unique_id})

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

    def _save_classification_result(self, classification_task, classification_result):
        connect(DB_NAME)
        user_image = UserImage(id=uuid.uuid4())
        user_image.classification_result = classification_result.get_type()
        # user_image.image.put(open(classification_task['image_path']))
        user_image.image = ntpath.basename(classification_task['image_path'])
        # user = User.objects(id=classification_task['user_id']).get()
        user_image.user_id = classification_task['user_id']
        user_image.user = classification_task['user_id']
        user_image.unique_id = classification_task['unique_id']
        user_image.save()
        self.feed_note_manager.add(classification_task['user_id'], classification_result.get_type() + " Report", "New report uploaded", "123", "Report")
        return user_image