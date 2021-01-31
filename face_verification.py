import base64
import io
from PIL import Image
import numpy as np
import cv2 as cv
from keras import backend as K
import tensorflow as tf
import keras

class FaceVerification():
    def __init__(self, l1, model = "facenet.h5"):
        self.l1 = l1
        self.model_add = model
        self.model = None
    def load_model(self):
		self.model = tf.keras.models.load_model(self.model_add, custom_objects={'tf': tf})
    def baseToArray(self,base64_code):
		base64_decoded = base64.b64decode(base64_code)
		image = Image.open(io.BytesIO(base64_decoded))
		image_np = np.array(image)
		image_np = image_np[:,:,:3]
		image_resize = cv.resize(image_np, dsize=(96,96), interpolation=cv.INTER_LINEAR)
		crop_rgb = cv.cvtColor(image_resize, cv.COLOR_BGR2RGB)
		crop_array = np.array(crop_rgb, dtype=K.floatx()) / 255.0
		img = np.array([crop_array])
		predictions = self.model.predict(img)
		return list(predictions.squeeze())
    def main(self):
        load_model()
        final= [baseToArray(i) for i in self.l1]
        return final
        
