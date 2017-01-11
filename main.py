#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ML.ClassificationManager import ClassificationManager
from REST.AccountResource import app
from OCR.ocr_service import OcrService
import config


def main(args=None):

    if config.SHOULD_USE_MACHINE_LEARNING:
        # start the classification thread.
        classification_manager = ClassificationManager()
        classification_manager.start()

    if config.SHOULD_USE_OCR:
        ocr_service = OcrService()
        image_path = '/Users/elroie/Computer Science/Final Project/Project/ML/images/electricity/test/test1.jpg'
        ocr_service.process_image(image_path)

    # Start rest API.
    #app.run()

if __name__ == "__main__":
    main()
