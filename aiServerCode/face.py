from tensorflow.keras.datasets import fashion_mnist
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.losses import CategoricalCrossentropy
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.metrics import Accuracy
import matplotlib.pyplot as plt
import numpy as np
%matplotlib inline

(train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()

def get_preprocessed_data(images, labels):
    images = np.array(images/255.0, dtype=np.float32)
    labels = np.array(labels, dtype=np.float32)
    
    return images, labels

train_images, train_labels = get_preprocessed_data(train_images, train_labels)
test_images, test_labels = get_preprocessed_data(test_images, test_labels)

print("train dataset shape:", train_images.shape, train_labels.shape)
print("test dataset shape", test_images.shape, test_labels.shape)
plt.imshow(train_images[3], cmap="gray")
plt.title(train_labels[3])

INPUT_SIZE = 28
model = Sequential([
    Flatten(input_shape=(INPUT_SIZE, INPUT_SIZE)),
    Dense(100, activation="relu"),
    Dense(30, activation="relu"),
    Dense(10, activation="softmax")
])

model.summary()

model.compile(optimizer=Adam(0.001), loss="categorical_crossentropy", metrics=['accuracy'])
train_oh_labels = to_categorical(train_labels)
test_oh_labels = to_categorical(test_labels)

print(train_oh_labels.shape, test_oh_labels.shape)

history = model.fit(x=train_images, y=train_oh_labels, batch_size=32, epochs=20, verbose=1)
print(history.history['loss'])
print(history.history['accuracy'])

pred_proba = model.predict(test_images)
print(pred_proba.shape)
pred_proba = model.predict(np.expand_dims(test_imaages[0], axis=0))
print("softmax output:", pred_proba)
pred = np.argmax(np.squeeze(pred_proba))
print("predicted class value:", pred)