from tensorflow.keras.models import load_model
import numpy as np
import cv2
import tensorflow as tf
import io
from PIL import Image

model = load_model('models/image_segmentation_classifier.h5')

def predict_emotion(image_bytes):
    img = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    img = img.resize((256, 256))
    img_array = np.array(img) / 255.0
    pred = model.predict(np.expand_dims(img_array, axis=0))[0][0]
    return "Sad 😢" if pred > 0.5 else "Happy 😊"
