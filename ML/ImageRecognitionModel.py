from ClassificationResult import ClassificationResult 
from sklearn.neighbors import KNeighborsClassifier
from PIL import Image
import numpy as np
import os
import cPickle
import config


class ImageRecognitionModel(object):
    
    def __init__(self, training_directory, type, prefix):
        self.training_directory = training_directory
        self.default_image_size = (600, 600)
        self.type = type
        self.prefix = prefix

    def train(self):
        # look for existing model.
        self._load_model()

        # if we load the model from a file we don't need to train a new model.
        if getattr(self, 'knn', None) is not None:
            return

        images = list(img for img in os.listdir(self.training_directory) if img.endswith('.jpg'))
        results = []

        # creates the results vector.
        for img in images:
            # train photos start with prefix are true positive
            if img.startswith(self.prefix):
                results.append(1)
            else: # else are false positive.
                results.append(0)

        matrix = self._prepare_data(images)
        # pca = RandomizedPCA(n_components=5)

        is_train = np.random.uniform(0, 1, len(matrix)) <= 0.7
        y = np.array(results)
        train_x, train_y = matrix[is_train], y[is_train]
        # test_x, test_y = matrix[is_train==False], y[is_train==False]

        # choose the result among k nearest neighbors.
        self.knn = KNeighborsClassifier(n_neighbors=2)
        self.knn.fit(train_x, train_y)
        print('learning ended succefully.\n')
        self._save_model()

    def classify(self, imagePath):
        image_matrix = self._image_to_matrix(imagePath)
        image_vector = self._flatten_image(image_matrix)
        preds = self.knn.predict(image_vector)
        return ClassificationResult(self.type, bool(preds[0]))

    def _image_to_matrix(self, image_file_name):
        image = Image.open(os.path.join(self.training_directory, image_file_name))
        image = image.resize(self.default_image_size)
        image = list(image.getdata())
        image = map(list, image)
        image = np.array(image) 
        return image
    
    def _prepare_data(self, images):
        images = images
        data = []
        for image_path in images:
            image = self._image_to_matrix(image_path)
            image = self._flatten_image(image)
            print 'finish processing ' + image_path
            print image_path, image.size

            # append each vector to the images matrix
            data.append(image)

        data = np.array(data)
        return data

    # converts an (m, n) matrix and flattens it into an array of shape (1, m * n)
    def _flatten_image(self, img):

        # This is a shity hack, we want that images will be in the same size of our trained images.
        # elroie:todo what if the image is less than 1080000
        if img.shape[0] * img.shape[1] > 1080000:
            img = np.delete(img, 0, 1)

        s = img.shape[0] * img.shape[1]
        img_wide = img.reshape(1, s)
        return img_wide[0]

    def _save_model(self):
        if config.SHOULD_SAVE_MODEL:
            print "save model"
            model_name = self.type + '.pkl'
            with open(model_name, 'wb') as fid:
                cPickle.dump(self.knn, fid)

    def _load_model(self):
        if config.SHOULD_SAVE_MODEL:
            model_name = self.type + '.pkl'

            try:
                with open(model_name, 'rb') as fid:
                    self.knn = cPickle.load(fid)
            except IOError:
                print 'No model found for ' + model_name

