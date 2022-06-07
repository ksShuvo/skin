import os
import numpy as np
from PIL import Image
import tensorflow as tf
from tensorflow import keras

interpreter = tf.lite.Interpreter(model_path='./model.tflite')
interpreter.allocate_tensors()

read = lambda imname: np.asarray(Image.open(imname).convert("RGB"))

print("\n\n\n","inside predict","\n\n\n")

def predict(imag_name):
    image = Image.open(imag_name)
    resized_im = image.resize((224,224))
    resized_im.save(imag_name)
    img = [read(imag_name)]
    #img=img.resize((224,224))

    img_1 = np.array(img, dtype='float32')

    img_2 = img_1/255

    #img = cv2.imread(r"{}".format(file.resolve()))
    #new_img = cv2.resize(img, (224, 224))
    #ans = model_1.predict(img_2)
    input_details = interpreter.get_input_details()
    # print(interpreter.get_input_details())
    output_details = interpreter.get_output_details()

    # Test the model on random input data.
    input_shape = input_details[0]['shape']
    input_data = np.array(np.random.random_sample(input_shape), dtype=np.float32)
    interpreter.set_tensor(input_details[0]['index'], img_2)

    interpreter.invoke()

    # The function `get_tensor()` returns a copy of the tensor data.
    # Use `tensor()` in order to get a pointer to the tensor.
    a = interpreter.get_tensor(output_details[0]['index'])

    a = np.argmax(a, axis = 1)[0]

    if a == 0:
        return "benign"
    else:
        return "malignant"


