import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import cv2
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Model, Sequential
from tensorflow.keras.layers import Input, Dense, Conv2D, Dropout, Flatten, Activation, MaxPooling2D, GlobalAveragePooling2D, BatchNormalization
from tensorflow.keras.optimizers import Adam, RMSprop
from tensorflow.keras.callbacks import ReduceLROnPlateau, EarlyStopping, ModelCheckpoint, LearningRateScheduler
from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras.applications import ResNet50V2
from tensorflow.keras.applications import Xception
from sklearn.model_selection import train_test_split
#%matplotlib inline
import tensorflow as tf
gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
    try:
        # Currently, memory growth needs to be the same across GPUs
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
        logical_gpus = tf.config.experimental.list_logical_devices('GPU')
        print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
    except RuntimeError as e:
        # Memory growth must be set before GPUs have been initialized
        print(e)
        
paths=[]
dataset_gubuns = []
label_gubuns = []



for dirname, _, filenames in os.walk('./Members/'):
    for filename in filenames:
        if '.jpg' in filename:
            file_path = dirname+'/'+filename
            paths.append(file_path)
            
            if '/TrainDataSet\\TrainDataSet\\' in file_path:
                dataset_gubuns.append("train")
            elif '/TestDataSet\\TestDataSet\\' in file_path:
                dataset_gubuns.append("test")
            elif '/ValidDataSet\\ValidDataSet\\' in file_path:
                dataset_gubuns.append("valid")
            else: dataset_gubuns.append("N/A")
            
            
            if "SeoTaeWoong" in file_path:
                label_gubuns.append("SeoTaeWoong")
            elif "KimSungTan" in file_path:
                label_gubuns.append("KimSungTan")
            elif "JangYungDae" in file_path:
                label_gubuns.append("JangYungDae")
            else: label_gubuns.append("N/A")
            
        
pd.set_option("display.max_colwidth", 200)
data_df = pd.DataFrame({'path':paths, 'dataset': dataset_gubuns, 'label': label_gubuns})
#print("data.df shape", data_df.shape)
data_df.head(10)

#print(data_df['dataset'].value_counts())
#print(data_df['label'].value_counts())

def show_grid_images(image_path_list, ncols=8, augmentor=None, title=None):
    figure, axs = plt.subplots(figsize=(22,6), nrows=1, ncols=ncols)
    for i in range(ncols):
        image = cv2.cvtColor(cv2.imread(image_path_list[i]), cv2.COLOR_BGR2GRAY)
        axs[i].imshow(image)
        axs[i].set_title(title)

"""
seo_image_list = data_df[data_df['label']=='SeoTaeWoong']['path'].iloc[:6].tolist()
show_grid_images(seo_image_list, ncols=6, title="SeoTaeWoong")
kim_image_list = data_df[data_df['label']=='KimSungTan']['path'].iloc[:6].tolist()
show_grid_images(kim_image_list, ncols=6, title="KimSungTan")
jang_image_list = data_df[data_df['label']=='JangYungDae']['path'].iloc[:6].tolist()
show_grid_images(jang_image_list, ncols=6, title="JangYungDae")
"""

train_df = data_df[data_df['dataset']=='train']
test_df = data_df[data_df['dataset']=='test']
valid_df = data_df[data_df['dataset']=='valid']
print("train_df.shape:", train_df.shape, "test_df.shape:", test_df.shape)


#tr_df, val_df = train_test_split(train_df, test_size=0.15, stratify=train_df['label'], random_state=2021)
#print("tr_df shape:", tr_df.shape, "val_df.shape:", val_df.shape)
#print("tr_df label distribution:\n", tr_df['label'].value_counts())
#print("val_df label distribution:\m", val_df["label"].value_counts())


IMAGE_SIZE = 128
BATCH_SIZE = 16

train_generator = ImageDataGenerator(horizontal_flip=True, rescale=1/255.)

train_flow_gen = train_generator.flow_from_dataframe(dataframe=train_df
                                               ,x_col="path"
                                               ,y_col="label"
                                               ,target_size=(IMAGE_SIZE,IMAGE_SIZE)
                                               ,class_mode="categorical"
                                               ,batch_size=BATCH_SIZE
                                               ,shuffle=True)


test_generator = ImageDataGenerator(rescale=1/255.)
test_flow_gen = test_generator.flow_from_dataframe(dataframe=test_df 
                                                   ,x_col="path"
                                                   ,y_col="label" 
                                                   ,target_size=(IMAGE_SIZE,IMAGE_SIZE)
                                                   ,class_mode="categorical" 
                                                   ,batch_size=BATCH_SIZE ,shuffle=False)

val_generator = ImageDataGenerator(rescale=1/255.)
val_flow_gen = train_generator.flow_from_dataframe(dataframe=valid_df
                                               ,x_col="path"
                                               ,y_col="label"
                                               ,target_size=(IMAGE_SIZE,IMAGE_SIZE)
                                               ,class_mode="categorical"
                                               ,batch_size=BATCH_SIZE
                                               ,shuffle=False)



images_array, labels_array = next(train_flow_gen)
#print(images_array.shape, labels_array.shape)
#print(images_array[:1], labels_array[:1])


def create_model(model_name="resnet50", verbose=False):
    input_tensor = Input(shape=(IMAGE_SIZE, IMAGE_SIZE, 3))
    if model_name =="vgg16":
        
        base_model = VGG16(input_tensor=input_tensor, include_top=False, weights="facenet")
        #base_model = VGG16(input_tensor=input_tensor, include_top=False)
    elif model_name =="resnet50":
        base_model = ResNet50V2(input_tensor=input_tensor, include_top=False, weights=None)
        #base_model = ResNet50V2(input_tensor=input_tensor, include_top=False)
    elif model_name =="xception":
        #base_model = Xception(input_tensor=input_tensor, include_top=False, weights="imagenet")
        base_model = Xception(input_tensor=input_tensor, include_top=False)
    
    bm_output = base_model.output
    
    x = GlobalAveragePooling2D()(bm_output)
    if model_name != "vgg16":
        x = Dropout(rate=0.5)(x)
    x = Dense(50, activation="relu", name="fc1")(x)
    output = Dense(3, activation="softmax", name="output")(x)
    
    model = Model(inputs=input_tensor, outputs=output)
    
    if verbose:
        model.summary()
        
    return model

model = create_model(model_name="xception", verbose=True)
model.compile(optimizer=Adam(0.001), loss="categorical_crossentropy", metrics=["accuracy"])

rlr_cb = ReduceLROnPlateau(monitor="val_loss", factor=0.2, patience=3, mode="min", verbose=1)
ely_cb = EarlyStopping(monitor='val_loss', patience=5, mode="min", verbose=1)

train_image_cnt = train_flow_gen.samples
print(train_image_cnt)
model.fit(train_flow_gen, epochs=15,
          steps_per_epoch=int(np.ceil(train_df.shape[0]/BATCH_SIZE)),
          validation_data=val_flow_gen,
          validation_steps=int(np.ceil(valid_df.shape[0]/BATCH_SIZE)),
          callbacks=[rlr_cb, ely_cb])

#model.fit_generator(train_flow_gen, epochs=15, steps_per_epoch=int(np.ceil(train_image_cnt/BATCH_SIZE)))


model.save("model.h5")
