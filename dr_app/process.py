import tensorflow as tf
from PIL import Image, ImageOps
import numpy as np
import os

def process_img(image_path):
    np.set_printoptions(suppress=True)

    model_path = os.path.join(os.path.dirname(__file__), '..', 'dr_app', 'keras_model.h5')

    try:
        # Load model dari path ini
        model = tf.keras.models.load_model(model_path)
        print(f"Model berhasil dimuat dari {model_path}")
    except Exception as e:
        print(f"Gagal memuat model: {e}")
        return ["Failed to load model"]

    image = Image.open(image_path).convert('RGB')
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.LANCZOS)
    image_array = np.asarray(image)
    normalized_image_array = image_array.astype(np.float32) / 255.0

    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    data[0] = normalized_image_array

    # Prediksi menggunakan model
    prediction = model.predict(data)
    pred = max(prediction[0])
    index = np.argmax(prediction[0])
    class_names = ["DR", "No_DR"]

    result = class_names[index]
    return [result, "-", round(pred * 100, 2)]
