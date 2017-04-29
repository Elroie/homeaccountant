class ClassificationResult:
    def __init__(self, type, result):
        self.type = type
        self.result = result
    
    def get_result(self):
        return self.result
    
    def get_type(self):
        return self.type

    def get_classification_result(self):
        if self.result == True:
            return self.type
        else:
            return 'Not a ' + self.type
