from keras import Sequential, Input, Model
from keras.layers import Dense, Flatten, Conv3D, Activation

from settings import length_cube_side, nb_channels

# Configurations of the shape of data
input_shape = (length_cube_side, length_cube_side, length_cube_side, nb_channels)
data_format = "channels_last"


def first_model():
    model = Sequential(name="first_simple_model")
    model.add(Conv3D(
        kernel_size=3,
        input_shape=input_shape,
        filters=32,
        data_format=data_format
    ))
    model.add(Flatten())
    model.add(Dense(3 * length_cube_side))
    model.add(Dense(2 * length_cube_side))
    model.add(Dense(1 * length_cube_side))
    model.add(Dense(1, activation='sigmoid'))
    model.build()

    return model


def pafnucy_like():
    kernel_size = 5
    inputs = Input(shape=input_shape)

    x = Conv3D(kernel_size=kernel_size, filters=64)(inputs)
    x = Conv3D(kernel_size=kernel_size, filters=128)(x)
    x = Conv3D(kernel_size=kernel_size, filters=256)(x)
    x = Conv3D(kernel_size=kernel_size, filters=512)(x)

    x = Flatten()(x)
    x = Dense(1000)(x)
    x = Dense(500)(x)
    x = Dense(200)(x)
    x = Dense(1)(x)
    outputs = Activation('relu')(x)

    model = Model(inputs=inputs, outputs=outputs, name="pafnucy_like")
    return model


def ProtNet():
    kernel_size = 5
    inputs = Input(shape=input_shape)

    x = Conv3D(kernel_size=kernel_size, filters=64)(inputs)
    x = Conv3D(kernel_size=kernel_size, filters=128)(x)
    x = Conv3D(kernel_size=kernel_size, filters=256)(x)
    x = Conv3D(kernel_size=kernel_size, filters=512)(x)

    x = Flatten()(x)
    x = Dense(1000)(x)
    x = Dense(500)(x)
    x = Dense(200)(x)
    x = Dense(1)(x)
    outputs = Activation('sigmoid')(x)

    model = Model(inputs=inputs, outputs=outputs, name="ProtNet")
    return model


models_available = [first_model(), ProtNet()]
models_available_names = list(map(lambda model: model.name, models_available))

if __name__ == "__main__":
    print(f"{len(models_available_names)} Models availables: \n\n")
    for i, model in enumerate(models_available):
        print(f"#{i}: {model.name}")
        model.summary()
