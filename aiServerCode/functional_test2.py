# -*- coding: utf-8 -*-
"""
Created on Fri Dec 31 11:12:51 2021

@author: USER
"""
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.layers import Layer, Input, Dense, Flatten
from tensorflow.keras.models import Model, Sequential
from tensorflow.keras.losses import CategoricalCrossentropy
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.datasets import fashion_mnist
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
from sklearn.model_selection import train_test_split



INPUT_SIZE = 28

def create_model():
    
    
    input_tensor = Input(shape=(INPUT_SIZE, INPUT_SIZE))
    x = Flatten()(input_tensor)
    x = Dense(100, activation="relu")(x)
    x = Dense(30, activation="relu")(x)
    output = Dense(10, activation="softmax")(x)
    
    model = Model(inputs=input_tensor, outputs=output)
    return model
    

def get_preprocessed_data(images, labels):
    images = np.array(images/255.0, dtype=np.float32)
    labels = np.array(labels, dtype=np.float32)
    return images, labels

def get_preprocessed_ohe(images, labels):
    images, labels = get_preprocessed_data(images, labels)
    oh_labels = to_categorical(labels)
    return images, oh_labels

def get_train_valid_test_set(train_images, train_labels, test_images, test_labels, valid_size=0.15, random_state=2021):
    train_images, train_oh_labels = get_preprocessed_ohe(train_images, train_labels)
    test_images, test_oh_labels = get_preprocessed_ohe(test_images, test_labels)
    
    tr_images, val_images, tr_oh_labels, val_oh_labels = train_test_split(train_images, train_oh_labels, test_size=valid_size, random_state=random_state)
    return (tr_images, tr_oh_labels), (val_images, val_oh_labels), (test_images, test_oh_labels)
    

(train_images, train_labels), (test_images, test_labels) =fashion_mnist.load_data()
print(train_images.shape, train_labels.shape, test_images.shape, test_labels.shape)
(tr_images, tr_oh_labels), (val_images, val_oh_labels), (test_images, test_oh_labels) = \
    get_train_valid_test_set(train_images, train_labels, test_images, test_labels)

print(tr_images.shape, tr_oh_labels.shape, val_images.shape, val_oh_labels.shape, test_images.shape, test_labels.shape)

model = create_model()
model.compile(optimizer=Adam(0.001), loss="categorical_crossentropy", metrics=["accuracy"])
filePath = "./working/weights.{epoch:02d}--{val_loss:.2f}.hdf5"
mcp_cb = ModelCheckpoint(filepath = filePath, monitor="val_loss", save_best_only=True, save_weights_only=True, mode="min", period=1, verbose=1)
rlr_cb = ReduceLROnPlateau(monitor="val_loss", factor=0.3, patience=3, mode="min", verbose=1)
ely_cb = EarlyStopping(monitor = "val_loss", patience=7, mode="min", verbose=1)
history = model.fit(x=tr_images, y=tr_oh_labels, batch_size=32, epochs=30, validation_data=(val_images, val_oh_labels), callbacks=[mcp_cb, rlr_cb, ely_cb])



def show_history(history):
    plt.plot(history.history['accuracy'], label="train")
    plt.plot(history.history['val_accuracy'], label="valid")
    plt.legend()

show_history(history)

model.evaluate(test_images, test_oh_labels, batch_size=256, verbose=1)