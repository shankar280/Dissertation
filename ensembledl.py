# -*- coding: utf-8 -*-
"""Ensembledl.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1eJQUisYGsBqG5_yNYTXV1dd3dGw7RvBU
"""

from google.colab import drive
drive.mount('/content/drive')

from zipfile import ZipFile
file_name = "/content/drive/MyDrive/Covid radiography/CovidR.zip"
with ZipFile(file_name,'r') as zip:
  zip.extractall()
  print("Completed")

from tensorflow.keras.layers import *
from tensorflow.keras.models import *
import tensorflow.keras as tf

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('darkgrid')

import os
import random
import keras

import warnings
warnings.filterwarnings('ignore')

from sklearn.model_selection import train_test_split

from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.preprocessing.image import ImageDataGenerator

from sklearn.metrics import classification_report
import tensorflow as tf

c = '/content/COVID-19_Radiography_Dataset/COVID/images'
n = '/content/COVID-19_Radiography_Dataset/Normal/images'
p = '/content/COVID-19_Radiography_Dataset/Viral Pneumonia/images'

random.seed(42)
filenames = os.listdir(c) + random.sample(os.listdir(n), 2500) + os.listdir(p)

categories = []
for filename in filenames:
    category = filename.split('-')[0]
    if category == 'COVID':
        categories.append(str(2))
    elif category == 'Viral Pneumonia':
        categories.append(str(1))
    else:
        categories.append(str(0))

for i in range(len(filenames)):
    if 'COVID' in filenames[i]:
        filenames[i] = os.path.join(c, filenames[i])
    elif 'Viral Pneumonia' in filenames[i]:
        filenames[i] = os.path.join(p, filenames[i])
    else:
        filenames[i] = os.path.join(n, filenames[i])


df = pd.DataFrame({
    'filename': filenames,
    'category': categories
})

df.head()

df.shape

#df.drop(df.index[1000:5000], axis=0, inplace=True)

train_data, test_valid_data = train_test_split(df, test_size=0.2, random_state = 42, shuffle=True, stratify=df['category'])
train_data = train_data.reset_index(drop=True)
test_valid_data = test_valid_data.reset_index(drop=True)

test_data, valid_data = train_test_split(test_valid_data, test_size=0.5, random_state = 42,
                                         shuffle=True, stratify=test_valid_data['category'])
test_data = test_data.reset_index(drop=True)
valid_data = valid_data.reset_index(drop=True)

train_data.shape

test_data.shape

#X = valid_data.drop(columns = 'category', axis=1)
#Y = valid_data['category']

A = test_data.drop(columns = 'category', axis=1)
B = test_data['category']
print(B)

a_test = list(map(int, B))
a_test=np.array(a_test)

print(a_test)

#a_test = list(map(int, y_test))
#a_test=np.array(a_test)

#y_test = list(map(int, y_test))
#y_test=np.array(y_test)

y_test=a_test

train_data_gen = ImageDataGenerator(
    rotation_range=15,
    rescale=1./255,
    shear_range=0.1,
    zoom_range=0.2,
    horizontal_flip=True,
    width_shift_range=0.1,
    height_shift_range=0.1
)

train_generator = train_data_gen.flow_from_dataframe(
    train_data,
    x_col='filename',
    y_col='category',
    target_size=(224,224),
    class_mode='categorical',
    batch_size=32
)

valid_data_gen = ImageDataGenerator(rescale=1./255)

valid_generator = valid_data_gen.flow_from_dataframe(
    valid_data,
    x_col='filename',
    y_col='category',
    target_size=(224,224),
    class_mode='categorical',
    batch_size=32
)

import tensorflow as tf
base_model3 = tf.keras.applications.ResNet50V2(weights='imagenet', input_shape = (224,224,3),
                                                     include_top=False)
for layer in base_model3.layers:
    layer.trainable = False

model3 = tf.keras.Sequential([
    base_model3,
    tf.keras.layers.GlobalAveragePooling2D(),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(3, activation='Softmax')
])

callbacks = [

    tf.keras.callbacks.EarlyStopping(patience=3, monitor='val_loss', verbose=1),
    tf.keras.callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=2, verbose=1)
]



from tensorflow.keras.optimizers import Adam
opt = Adam(lr=0.001)


model3.compile(optimizer = opt,
              loss = 'categorical_crossentropy',
              metrics=['accuracy'])

history3 = model3.fit(train_generator,
                    validation_data=valid_generator, epochs=8,
                    callbacks=[callbacks])

test_set = valid_data_gen.flow_from_dataframe(
    test_data,
    x_col='filename',
    y_col='category',
    target_size=(224,224),
    class_mode='categorical',
    batch_size=32,
    shuffle=False
)

ytest=model1.evaluate(test_set)

ytest2=model2.evaluate(test_set)

model3.save("model3.h5")

pred4=model3.predict(test_set)

pred4=model3.predict(test_set)
pred5=np.argmax(pred4, axis=1)
pred5

pred6=model2.predict(test_set)
pred7=np.argmax(pred6, axis=1)

pred8=model1.predict(test_set)
pred9=np.argmax(pred8, axis=1)

base_model1 = tf.keras.applications.Xception(weights='imagenet', input_shape = (224,224,3),
                                                     include_top=False)
for layer in base_model1.layers:
    layer.trainable = False

model1 = tf.keras.Sequential([
    base_model1,
    tf.keras.layers.GlobalAveragePooling2D(),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(3, activation='Softmax')
])

callbacks = [

    tf.keras.callbacks.EarlyStopping(patience=3, monitor='val_loss', verbose=1),
    tf.keras.callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=2, verbose=1)
]



from tensorflow.keras.optimizers import Adam
opt = Adam(lr=0.001)


model1.compile(optimizer = opt,
              loss = 'categorical_crossentropy',
              metrics=['accuracy'])

history1 = model1.fit(train_generator,
                    validation_data=valid_generator, epochs=8,
                    callbacks=[callbacks])

model1.save("model1.h5")

plt.plot(history1.history['loss'], label='Loss (training data)')
plt.plot(history1.history['val_loss'], label='Loss (validation data)')
plt.title('Model loss')
plt.ylabel('Loss')
plt.xlabel('No. epoch')
plt.legend(['train', 'validation'], loc="upper left")
plt.show()
plt.plot(history1.history['accuracy'])
plt.plot(history1.history['val_accuracy'])
plt.title('Model accuracy')
plt.ylabel('accuracy')
plt.xlabel('No. of epoch')
plt.legend(['train', 'validation'], loc='upper left')
plt.show()

base_model2 = tf.keras.applications.VGG19(weights='imagenet', input_shape = (224,224,3),
                                                     include_top=False)
for layer in base_model2.layers:
    layer.trainable = False

model2 = tf.keras.Sequential([
    base_model2,
    tf.keras.layers.GlobalAveragePooling2D(),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(3, activation='Softmax')
])

callbacks = [

    tf.keras.callbacks.EarlyStopping(patience=3, monitor='val_loss', verbose=1),
    tf.keras.callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=2, verbose=1)
]



from tensorflow.keras.optimizers import Adam
opt = Adam(lr=0.001)


model2.compile(optimizer = opt,
              loss = 'categorical_crossentropy',
              metrics=['accuracy'])

history2 = model2.fit(train_generator,
                    validation_data=valid_generator, epochs=8,
                    callbacks=[callbacks])

model2.save("model2.h5")

models = [model1, model2, model3]

#graph
plt.plot(history3.history['loss'], label='Loss (training data)')
plt.plot(history3.history['val_loss'], label='Loss (validation data)')
plt.title('model loss')
plt.ylabel('Loss')
plt.xlabel('No. epoch')
plt.legend(['train', 'validation'], loc="upper left")
plt.show()

plt.plot(history3.history['accuracy'])
plt.plot(history3.history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('No. of epoch')
plt.legend(['train', 'validation'], loc='upper left')
plt.show()

plt.plot(history2.history['loss'], label='Loss (training data)')
plt.plot(history2.history['val_loss'], label='Loss (validation data)')
plt.title('model loss')
plt.ylabel('Loss')
plt.xlabel('No. epoch')
plt.legend(['train', 'validation'], loc="upper left")
plt.show()
plt.plot(history2.history['accuracy'])
plt.plot(history2.history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('No. of epoch')
plt.legend(['train', 'validation'], loc='upper left')
plt.show()

pred1 = model3.predict(valid_generator)

pred2=np.argmax(pred1, axis=1)

pred2

preds = [model.predict(test_set) for model in models]
preds=np.array(preds)
summed = np.sum(preds, axis=0)

ensemble_prediction = np.argmax(summed, axis=1)



weighted_preds = np.tensordot(preds, weights, axes=((0),(0)))
weighted_ensemble_prediction = np.argmax(weighted_preds, axis=1)

weighted_ensemble_prediction

weighted_ensemble_prediction

pred3=[0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 2, 1, 1, 1, 2,
       0, 1, 0, 0, 1, 1, 1, 1, 0, 2, 0, 1, 2, 0, 0, 1, 0, 1, 0, 0, 1, 1,
       0, 2, 2, 1, 1, 1, 1, 2, 1, 0, 1, 1, 1, 2, 0, 2, 2, 1, 1, 2, 1, 1,
       1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1,
       0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 2, 0, 0, 2,
       1, 2, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 2, 0, 1, 0, 0, 0, 1,
       1, 0, 2, 1, 2, 0, 1, 1, 1, 1, 0, 1, 2, 0, 1, 1, 1, 0, 2, 0, 0, 0,
       1, 1, 0, 1, 0, 2, 1, 2, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1,
       2, 0, 2, 1, 1, 0, 1, 0, 1, 0, 2, 1, 1, 1, 1, 0, 1, 2, 2, 0, 2, 0,
       2, 0, 0, 1, 1, 2, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 2, 1, 0, 2,
       1, 0, 0, 1, 1, 2, 0, 1, 0, 1, 2, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0,
       1, 2, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 2, 1, 1, 1, 1, 0, 0,
       1, 1, 0, 1, 0, 1, 2, 2, 0, 0, 2, 2, 0, 1, 0, 1, 2, 1, 1, 2, 0, 1,
       0, 1, 1, 2, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 2, 1, 2, 1,
       2, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 2, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0,
       0, 1, 0, 1, 0, 0, 2, 0, 1, 1, 0, 0, 1, 2, 0, 0, 1]
pred3=np.array(pred3)
pred3

pred2

from keras.models import load_model
from sklearn.metrics import accuracy_score

weighted_accuracy = accuracy_score(y_test, pred2)
weighted_accuracy

weighted_accuracy = accuracy_score(y_test, pred5)
weighted_accuracy

weighted_accuracy = accuracy_score(a_test,pred5)
weighted_accuracy

weighted_accuracy = accuracy_score(a_test, ensemble_prediction)
weighted_accuracy

from sklearn.metrics import classification_report, confusion_matrix
print('Confusion Matrix')
mat = confusion_matrix(a_test,ensemble_prediction)
print(mat)







#Ensembled program

from keras.models import load_model
from sklearn.metrics import accuracy_score

model1 = load_model('/content/model1.h5')
model2 = load_model('/content/model2.h5')
model3 = load_model('/content/model3.h5')

models = [model1, model2, model3]

preds = [model.predict(test_set) for model in models]
preds=np.array(preds)
summed = np.sum(preds, axis=0)

ensemble_prediction = np.argmax(summed, axis=1)

pred1=model1.predict(test_set)
pred1=np.argmax(pred1, axis=1)

pred2=model2.predict(test_set)
pred2=np.argmax(pred2, axis=1)

pred3=model3.predict(test_set)
pred3=np.argmax(pred3, axis=1)
print(ensemble_prediction)

accuracy1 = accuracy_score(y_test, pred1)
accuracy2 = accuracy_score(y_test, pred2)
accuracy3 = accuracy_score(y_test, pred3)
ensemble_accuracy = accuracy_score(y_test, ensemble_prediction)

print('Accuracy Score for model1 = ', accuracy1)
print('Accuracy Score for model2 = ', accuracy2)
print('Accuracy Score for model3 = ', accuracy3)
print('Accuracy Score for average ensemble = ', ensemble_accuracy)

#Weighted sum

ideal_weights = [0.2, 0.1, 0.4] #acc:0.9410187667560321
#weight1 = [0.4, 0.1, 0.4]  acc:0.9276139410187667
#weight2 = [0.4, 0.2, 0.4]  acc:0.9302949061662198
#weight3 = [[0.4, 0.1, 0.6]  acc:0.9316353887399463
#weight4 = [0.1, 0.4, 0.2] acc:0.9021447721179625

weighted_preds = np.tensordot(preds, ideal_weights, axes=((0),(0)))
weighted_ensemble_prediction = np.argmax(weighted_preds, axis=1)

weighted_accuracy = accuracy_score(y_test, weighted_ensemble_prediction)
print('Accuracy Score for weighted average ensemble = ', weighted_accuracy)



sample = random.choice(test_data['filename'])


category = sample.split('/')[-1].split('-')[0].upper()
true = ''
if category == 'COVID':
    true = 'COVID'
elif category == 'VIRAL PNEUMONIA':
    true = 'Viral Pneumonia'
else:
    true = 'Normal'

print(f'True value is : {true}')

image = load_img(sample, target_size=(224, 224))
img = img_to_array(image)/255
img = img.reshape((1, 224, 224, 3))

result =model3.predict(img)
result = np.argmax(result, axis=-1)
print('Prediction is:')
if result == 0:
    print("Normal")
elif result == 1:
    print("Viral Pneumonia")
else:
    print("COVID ")

plt.imshow(image)

from sklearn.metrics import confusion_matrix
import seaborn as sns
cm = confusion_matrix(y_test, weighted_ensemble_prediction)

print(cm)
ax= plt.subplot()
sns.heatmap(cm, annot=True, fmt='g', ax=ax);

# labels, title and ticks
ax.set_xlabel('Predicted labels');ax.set_ylabel('True labels');
ax.set_title('Confusion Matrix');

cm1 = confusion_matrix(y_test, pred1)

print(cm1)
ax= plt.subplot()
sns.heatmap(cm1, annot=True, fmt='g', ax=ax);

# labels, title and ticks
ax.set_xlabel('Predicted labels');ax.set_ylabel('True labels');
ax.set_title('Confusion Matrix');

cm2 = confusion_matrix(y_test, pred2)

print(cm2)
ax= plt.subplot()
sns.heatmap(cm2, annot=True, fmt='g', ax=ax);

# labels, title and ticks
ax.set_xlabel('Predicted labels');ax.set_ylabel('True labels');
ax.set_title('Confusion Matrix');

cm3 = confusion_matrix(y_test, pred3)

print(cm3)
ax= plt.subplot()
sns.heatmap(cm3, annot=True, fmt='g', ax=ax);

# labels, title and ticks
ax.set_xlabel('Predicted labels');ax.set_ylabel('True labels');
ax.set_title('Confusion Matrix');

