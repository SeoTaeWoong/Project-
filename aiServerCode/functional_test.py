# -*- coding: utf-8 -*-
"""
Created on Fri Dec 31 10:40:09 2021

@author: USER
"""

from tensorflow.keras.layers import Input, Dense, Flatten
from tensorflow.keras.models import Model

INPUT_SIZE = 28
input_tensor = Input(shape=(INPUT_SIZE, INPUT_SIZE))
x = Flatten()(input_tensor)
x = Dense(100, activation = "relu")(x)
x = Dense(30, activation="relu")(x)
output = Dense(10,activation="softmax")(x)
model = Model(inputs=input_tensor,outputs=output)

model.summary()