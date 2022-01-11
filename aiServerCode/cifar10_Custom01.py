import os
import numpy as np
import pandas as pd
from tensorflow.keras.datasets import cifar10
from tensorflow.keras.layers import Flatten ,Input, Dense, Conv2D, Dropout, Activation, MaxPooling2D, GlobalAveragePooling2D, BatchNormalization
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.optimizers import Adam, RMSprop
from tensorflow.keras.callbacks import ReduceLROnPlateau, EarlyStopping, ModelCheckpoint, LearningRateScheduler
import matplotlib.pyplot as plt

(train_images, train_labels), (test_images, test_labels) =  cifar10.load_data()
print("##Train dataset shape : ", train_images.shape, train_labels.shape)
print("##Test dataset shape : ", test_images.shape, test_labels.shape)

input_tensor = Input(shape=(32,32,3))
x = Conv2D(filters=32, kernel_size=(5,5), padding="valid", activation="relu")(input_tensor)
x = Conv2D(filters=32, kernel_size=(3,3), padding="same", activation="relu")(x)
x = MaxPooling2D( pool_size=(2,2))(x)

x = Conv2D(filters=64, kernel_size=(3,3), padding="same", activation="relu")(x)
x = Conv2D(filters=64, kernel_size=(3,3), padding="same", activation="relu")(x)
x = MaxPooling2D(pool_size=2)(x)

x = Conv2D(filters=128, kernel_size=(3,3), padding="same", activation="relu")(x)
x = Conv2D(filters=128, kernel_size=(3,3), padding="same", activation="relu")(x)
x = MaxPooling2D(pool_size=2)(x)

x = Flatten(name="flatten")(x)
x = Dropout(rate=(0.5))(x)
x = Dense(300, activation="relu", name="fc1")(x)
x = Dropout(rate=(0.3))(x)
output = Dense(10, activation="softmax", name="output")(x)

model = Model(inputs=input_tensor, outputs=output)
model.summary()

model.compile(optimizer=Adam(), loss="sparse_categorical_crossentropy", metrics=["accuracy"])

history = model.fit(x=train_images, y=train_labels, batch_size=64, epochs=30, validation_split=0.15)