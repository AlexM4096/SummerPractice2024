import pandas
from keras.applications import InceptionV3
from keras import regularizers
from keras.preprocessing.image import ImageDataGenerator
from tensorflow.python.keras import Model
from tensorflow.python.keras.callbacks import ModelCheckpoint
from tensorflow.python.keras.layers import GlobalAveragePooling2D, Dense

import data

image_size = (224, 244)
x_col = 'filepaths'
y_col = 'labels'
target_size = (100, 100)
batch_size = 8
seed = 21


class ModelInfo:
    classes = None
    classes_amount: int

    train_generator = None
    valid_generator = None
    test_generator = None

    train_steps: int
    valid_steps: int

    model = None
    checkpoint = None


def generate_dataset(info: ModelInfo):
    data_frame = pandas.read_csv(data.kaggle_dataset_cvs_path)

    train_data_frame = data_frame.loc[data_frame['data set'] == 'train']
    valid_data_frame = data_frame.loc[data_frame['data set'] == 'valid']
    test_data_frame = data_frame.loc[data_frame['data set'] == 'test']

    info.classes = data_frame["labels"].unique()
    info.classes_amount = len(info.classes)

    data_generator = ImageDataGenerator(
        rescale=1/255.0,
        rotation_range=20,
        zoom_range=0.05,
        width_shift_range=0.05,
        height_shift_range=0.05,
        shear_range=0.05,
        horizontal_flip=True,
        fill_mode="nearest",
        validation_split=0.20
    )

    info.train_generator = data_generator.flow_from_dataframe(
        dataframe=train_data_frame,
        directory=data.kaggle_dataset_directory,
        x_col=x_col,
        y_col=y_col,
        target_size=target_size,
        batch_size=batch_size,
        class_mode="categorical",
        subset='training',
        shuffle=True,
        seed=seed
    )

    info.valid_generator = data_generator.flow_from_dataframe(
        dataframe=valid_data_frame,
        directory=data.kaggle_dataset_directory,
        x_col=x_col,
        y_col=y_col,
        target_size=target_size,
        batch_size=batch_size,
        class_mode="categorical",
        subset='training',
        shuffle=True,
        seed=seed
    )

    info.test_generator = data_generator.flow_from_dataframe(
        dataframe=test_data_frame,
        directory=data.kaggle_dataset_directory,
        x_col=x_col,
        target_size=target_size,
        batch_size=1,
        class_mode=None,
        shuffle=False
    )

    info.train_steps = len(info.train_generator) // batch_size
    info.valid_steps = len(info.valid_generator) // batch_size


def create_model(info: ModelInfo):
    bottom_model = InceptionV3(weights='imagenet', include_top=False)
    top_model = bottom_model.output
    top_model = GlobalAveragePooling2D()(top_model)
    top_model = Dense(1024, activation='relu')(top_model)
    top_model = Dense(info.classes_amount, activation='softmax')(top_model)

    info.model = Model(inputs=bottom_model.inputs, outputs=top_model)
    info.checkpoint = ModelCheckpoint('the_best_model.keras', save_best_only=True, monitor='val_loss', mode='min')


def compile_model(info: ModelInfo):
    info.model.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])


def learn(info: ModelInfo):
    history = info.model.fit(
        info.train_generator,
        steps_per_epoch=info.train_steps,
        epochs=20,
        validation_data=info.valid_generator,
        validation_steps=info.valid_steps,
        callbacks=[info.checkpoint]
    )


def unfreeze():
    print()


def recompile_model(info: ModelInfo):
    info.model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])


def train():
    info = ModelInfo()
    generate_dataset(info)
    create_model(info)
    compile_model(info)
    learn(info)
    unfreeze()
    recompile_model(info)
    learn(info)
