from tensorflow.keras import Model
from tensorflow.keras.layers import Input, Conv2D, ReLU, BatchNormalization, Flatten, Dense
from tensorflow.keras import backend as K

class Autoencoder:

    """
    Autoencoder represents a Deep Concolutional autoencoder architeture with mirrored encoder and decoder components.
    """

    def __init__(self,
                input_shape,
                conv_filters,
                conv_kernels,
                conv_strides,
                latent_space_dim):
        
        self.input_shape = input_shape # [28, 28, 1]
        self.conv_filters = conv_filters # [2, 4, 8]
        self.conv_kernels = conv_kernels # [3, 5, 3]
        self.conv_strides = conv_strides # [1, 2, 2]
        self.latent_space_dim = latent_space_dim # 2

        self.encoder = None
        self.decoder = None
        self.model = None

        self._num_conv_layers = len(conv_filters)

        self._build()

    def summary(self):
        self.encoder.summary()

    def _build(self):
        self._build_encoder()
        #self._build_decoder()
        #self._build_autoencoder()

    def _build_encoder(self):
        encoder_input = self._add_encoder_input()
        conv_layers = self._add_conv_layers(encoder_input)
        bottleneck = self._add_bottleneck(conv_layers)
        self.encoder = Model(encoder_input, bottleneck, name="encoder") # pra isso, ele importou a funcao Model do keras

    def _add_encoder_input(self): # pra isso ele importou a funcao Input do keras
        return Input(shape=self.input_shape, name="encoder_input") # parametro que está sendo passado no init

    # ele vai chamar o que vem abaixo de method, provavelmente outras coisas tb, mas isso me chamou a atencao 

    def _add_conv_layers(self, encoder_input):
        """Creates all convolutional blocks in encoder."""
        x = encoder_input
        for layer_index in range(self._num_conv_layers):
            x = self._add_conv_layer(layer_index, x)
        return x 

    def _add_conv_layer(self, layer_index, x): # essa funcao nao tem s no nome, coisa de corno
        """
        Adds a convolutional block to a graph of layers, cosisting of conv 2d + ReLU + batch normalization
        """
        layer_number = layer_index + 1
        conv_layer = Conv2D(     # esta importado la em cima
            filters = self.conv_filters[layer_index],
            kernel_size = self.conv_kernels[layer_index],
            strides = self.conv_strides[layer_index],
            padding = "same",
            name = f"encoder_conv_layer_{layer_number}"
        )
        x = conv_layer(x)
        x = ReLU(name=f"encoder_relu_{layer_number}")(x)
        x = BatchNormalization(name=f"encoder_bn_{layer_number}")(x)
        return(x)

    def _add_bottleneck(self, x):
        """Flatten data and add bottleneck (Dense layer)."""
        self._shape_before_bottleneck = K.int_shape(x)[1:] # ele recebe 4 valores [2, 7, 7, 28], sendo que o primeiro é o batch size
        # como a gente não ta interessado no batch size, ele colocou o slice pra receber apenas [7, 7, 28]
        x = Flatten()(x)
        x = Dense(self.latent_space_dim, name= "encoder_output")(x)
        return x

if __name__ == "__main__":
    autoencoder = Autoencoder(
        input_shape = (28, 28, 1),
        conv_filters = (32, 64, 64, 64),
        conv_kernels = (3, 3, 3, 3),
        conv_strides = (1, 2, 2, 1),
        latent_space_dim = 2 
    )
    autoencoder.summary()
