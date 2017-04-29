
class TextExtractor(object):
    '''Base class for extracting price & dates from bills'''
    pass

    @classmethod
    def create(cls, bill_type):
        ''' Factory method for creating the appropriate extractor'''
        pass

    def get_price(self, scanned_image):
        # abstract method
        pass

    def get_dates(self, scanned_image):
        # abstract method
        pass