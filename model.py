from tensorflow import keras
from PIL import Image
import numpy as np

class Prediction:

    def __init__(self):
        self.model = keras.models.load_model('my_model3.h5')
        self.sopost = {2: 'Лебедь-шипун', 1: 'Лебедь-кликун', 0: 'Малый лебедь'}

    def predict(self, path):
        
        data_images = []   
        img = Image.open(path).resize((64, 64)) 
        img_np = np.array(img)
        data_images.append(img_np) 

        x_data = np.array(data_images)  

        x_data = x_data / 255.

        res = self.model.predict_step(x_data)
        classes_x=np.argmax(res,axis=1)

        self.res = self.sopost[classes_x[0]]
