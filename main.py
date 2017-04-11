#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ML.ClassificationManager import ClassificationManager
from REST.api import app
from OCR.ocr_service import OcrService
import config


def main(args=None):

    if config.SHOULD_USE_MACHINE_LEARNING:
        # start the classification thread.
        classification_manager = ClassificationManager()
        classification_manager.start()

    if config.SHOULD_USE_OCR:
        ocr_service = OcrService()
        image_path = config.BASE_PATH + 'ML/images/electricity/test/test1.jpg'
        # ocr_service.enqueue_ocr_task(image_path)

    # Start rest API.
    app.run()

if __name__ == "__main__":
    main()
