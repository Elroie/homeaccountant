#!/usr/bin/env python
# -*- coding: utf-8 -*-

import abc
import re


class TextExtractorBase(object):
    '''Base class for extracting price & dates from bills'''
    __metaclass__ = abc.ABCMeta

    @classmethod
    def create(cls, bill_type):
        ''' Factory method for creating the appropriate extractor'''
        if bill_type == 'Electricity Bill':
            return ElectricityTextExtractor()
        elif bill_type == 'Water Bill':
            return WaterTextExtractor()
        else:
            raise ValueError('Text Extractor support only "Electricity Bill" or "Water Bill"')

    @abc.abstractmethod
    def get_price(self, image_path):
        """Extract the price from the bill"""

    @abc.abstractmethod
    def get_date(self, image_path):
        """Extract due date"""


class ElectricityTextExtractor(TextExtractorBase):

    def get_date(self, image_path):
        with open(image_path) as f:
            text = f.read()
            match = re.search(r'ל-(\d+/\d+/\d+)', text)
            if match is not None and match.lastindex == 1:
                to_date = match.group(1)
                print 'extracted: ' + to_date
                return to_date

    def get_price(self, image_path):
        with open(image_path) as f:
            lines = f.readlines()
            price = None
            for line in lines:
                if 'לתשלום בש״ח' in line:
                    print line

                    # remove whitespaces from both side of the line.
                    words = line.strip().split(' ')

                    # the proce would probably we at the end of the line
                    # so lets reverse the order of the words in this line
                    words.reverse()
                    for word in words:
                        try:
                            price = float(word)
                            print price
                            break
                        except ValueError as ex:
                            print 'invalid cast while trying to extract electricity price'
            return price


class WaterTextExtractor(TextExtractorBase):

    def get_date(self, image_path):
        with open(image_path) as f:
            text = f.read()
            match = re.search(r'לתשלום עד (\d+/\d+/\d+)', text)
            if match is not None and match.lastindex == 1:
                to_date = match.group(1)
                print 'extracted: ' + to_date
                return to_date

    def get_price(self, image_path):
        with open(image_path) as f:
            lines = f.readlines()
            price = None
            for line in lines:
                if ' חיוב תקופתי' in line:
                    words = line.strip().split(' ')
                    # words.reverse()

                    for word in words:
                        try:
                            price = float(word)
                            break
                        except ValueError as ex:
                            print 'invalid cast while trying to extract electricity price'

            return round(price + (price * 0.17), 2)
