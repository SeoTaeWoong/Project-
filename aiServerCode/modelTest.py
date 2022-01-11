import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import cv2
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Model, Sequential, load_model
from tensorflow.keras.layers import Input, Dense, Conv2D, Dropout, Flatten, Activation, MaxPooling2D, GlobalAveragePooling2D, BatchNormalization
from tensorflow.keras.optimizers import Adam, RMSprop
from tensorflow.keras.callbacks import ReduceLROnPlateau, EarlyStopping, ModelCheckpoint, LearningRateScheduler
from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras.applications import ResNet50V2
from tensorflow.keras.applications import Xception
from sklearn.model_selection import train_test_split



paths=[]
dataset_gubuns = []
label_gubuns = []

for dirname, _, filenames in os.walk('./Members/'):
    for filename in filenames:
        if '.jpg' in filename:
            file_path = dirname+'/'+filename
            
            
            if '/TestDataSet\\TestDataSet\\' in file_path:
                paths.append(file_path)
                dataset_gubuns.append("test")
                if "SeoTaeWoong" in file_path:
                    label_gubuns.append("SeoTaeWoong")
                elif "KimSungTan" in file_path:
                    label_gubuns.append("KimSungTan")
                elif "JangYungDae" in file_path:
                    label_gubuns.append("JangYungDae")
                else: label_gubuns.append("N/A")

            

pd.set_option("display.max_colwidth", 200)

data_df = pd.DataFrame({'path':paths, 'dataset': dataset_gubuns, 'label': label_gubuns})

print("data.df shape", data_df.shape)
data_df.head(10)

test_df = data_df[data_df['dataset']=='test']

IMAGE_SIZE = 224
BATCH_SIZE = 16

test_generator = ImageDataGenerator(rescale=1/255.)
test_flow_gen = test_generator.flow_from_dataframe(dataframe=test_df 
                                                   ,x_col="path"
                                                   ,y_col="label" 
                                                   ,target_size=(IMAGE_SIZE,IMAGE_SIZE)
                                                   ,class_mode="categorical" 
                                                   ,batch_size=BATCH_SIZE ,shuffle=False)

model = load_model("mnist_member_model.h5")
model.summary()

prediction = model.predict(test_flow_gen)
#np.set_printoptions(formatter={'float': lambda x:"{0:0.3f}".format(x)})
