""" 
ReXNet 
Copyright (c) 2020-present NAVER Corp. 
Reimplementation of ReXNet by Dongryeol Lee 2021-2-1 
MIT license 
""" 
 
import tensorflow as tf 
from tensorflow import keras 
from math import ceil 
# Memory-efficient Siwsh using torch.jit.script borrowed from the code in (https://twitter.com/jeremyphoward/status/1188251041835315200) 
# Currently use memory-efficient Swish as default: 
def ConvBNAct(inputs, filters, kernel_size=1, strides=(1,1), padding='valid', use_bias=False, num_group=1, relu6=False, active=False, weight_decay=0.00005): 
    if num_group == 1 : 
        outputs = (keras.layers.Conv2D(filters=filters, kernel_size=kernel_size, strides=strides,  
                                 padding=padding, use_bias=use_bias, kernel_regularizer=keras.regularizers.l2(weight_decay), kernel_initializer=keras.initializers.he_normal()))(inputs) 
    else : 
        outputs = (keras.layers.DepthwiseConv2D(kernel_size=kernel_size, strides=strides, 
                                padding=padding, use_bias=use_bias, kernel_regularizer=keras.regularizers.l2(weight_decay), kernel_initializer=keras.initializers.he_normal() ))(inputs) 
    outputs = (keras.layers.BatchNormalization(momentum=0.1,epsilon=1e-05))(outputs) 
    if active: 
        if relu6: 
            outputs = (keras.layers.ReLU(6.0))(outputs) 
        else: 
            outputs = (keras.layers.Activation('relu'))(outputs) 
    return outputs 
 
def ConvBNSwish(inputs, filters, kernel_size=1, strides=(1,1), padding='valid', use_bias=False, num_group=1, weight_decay=0.00005): 
    if num_group == 1: 
        outputs =   keras.layers.Conv2D(filters=filters, kernel_size=kernel_size, 
                                 strides=strides, padding=padding,use_bias=use_bias, kernel_regularizer=keras.regularizers.l2(weight_decay), kernel_initializer=keras.initializers.he_normal())(inputs) 
    else: 
        outputs =   keras.layers.DepthwiseConv2D(kernel_size=kernel_size, strides=strides, 
                                padding=padding, use_bias=use_bias, kernel_regularizer=keras.regularizers.l2(weight_decay), kernel_initializer=keras.initializers.he_normal())(inputs) 
    outputs =   keras.layers.BatchNormalization(momentum=0.1,epsilon=1e-05)(outputs) 
    outputs =   keras.layers.Activation(tf.nn.swish)(outputs) 
 
    return outputs 
 
 
def SE(inputs, filters, kernel_size=1, strides=(1,1), padding='valid',use_bias=True, se_ratio=12, weight_decay=0.00005): 
     
    outputs = keras.layers.GlobalAveragePooling2D()(inputs) 
    outputs = keras.layers.Reshape((1,1,filters))(outputs) 
    outputs = keras.layers.Conv2D(filters=filters // se_ratio, kernel_size=kernel_size, padding=padding, kernel_regularizer=keras.regularizers.l2(weight_decay), kernel_initializer=keras.initializers.he_normal())(outputs) 
    outputs = keras.layers.BatchNormalization(momentum=0.1,epsilon=1e-05)(outputs) 
    outputs = keras.layers.Activation(tf.nn.relu)(outputs) 
    outputs = keras.layers.Conv2D(filters=filters, kernel_size=kernel_size, padding=padding, kernel_regularizer=keras.regularizers.l2(weight_decay), kernel_initializer=keras.initializers.he_normal())(outputs) 
    outputs = keras.layers.Activation(tf.nn.sigmoid)(outputs) 
 
    return outputs * inputs 
 
 
def LinearBottleneck(inputs, in_channels, filters, t, strides=(1,1), padding='valid',use_se=True, se_ratio=12): 
    use_shortcut = strides[0] ==1 and in_channels <= filters 
    # outputs = None 
    if t != 1: 
        dw_channels = in_channels * t 
        outputs = ConvBNSwish(inputs, filters=dw_channels, kernel_size=1, padding='same') 
        outputs = ConvBNAct(outputs, filters=dw_channels, kernel_size=3, strides=strides, padding='same', 
                    num_group=dw_channels,active=False) 
 
    else: 
        dw_channels = in_channels 
        outputs = ConvBNAct(inputs, filters=dw_channels, kernel_size=3, strides=strides, padding='same', 
                    num_group=dw_channels,active=False) 
    if use_se: 
        outputs = SE(outputs, filters=dw_channels, kernel_size=1, padding=padding, se_ratio=se_ratio) 
    outputs = (keras.layers.ReLU(6.0))(outputs) 
    outputs = ConvBNAct(outputs, filters=filters, relu6=True) 
    if use_shortcut: 
        shortcut = keras.layers.Lambda(lambda inputs: inputs[:, :, :, 0:in_channels])(outputs)  
        outputs_sc = tf.keras.layers.Add()([shortcut,inputs]) 
        x_in = keras.layers.Lambda(lambda inputs: inputs[:, :, :, in_channels:])(outputs)  
        outputs = tf.keras.layers.Concatenate(axis=-1)([x_in,outputs_sc]) 
     
    return outputs 
 
 
def ReXNetV1(input_shape, input_ch=16, final_ch=180, width_mult=1.0, depth_mult=1.0, classes=1000, 
                 use_se=True, 
                 se_ratio=12, 
                 dropout_ratio=0.2, 
                 bn_momentum=0.9): 
 
    input = keras.layers.Input(shape=input_shape) 
    layers = [1, 2, 2, 3, 3, 5] 
    strides = [1, 2, 2, 2, 1, 2] 
    use_ses = [False, False, True, True, True, True] 
 
    layers = [ceil(element * depth_mult) for element in layers] 
    strides = sum([[element] + [1] * (layers[idx] - 1) 
                    for idx, element in enumerate(strides)], []) 
    if use_se: 
        use_ses = sum([[element] * layers[idx] for idx, element in enumerate(use_ses)], []) 
         
    else: 
        use_ses = [False] * sum(layers[:]) 
    ts = [1] * layers[0] + [6] * sum(layers[1:]) 
 
    depth = sum(layers[:]) * 3 
    stem_channel = 32 / width_mult if width_mult < 1.0 else 32 
    inplanes = input_ch / width_mult if width_mult < 1.0 else input_ch 
 
    in_channels_group = [] 
    channels_group = [] 
 
    for i in range(int(depth // 3)): 
        if i == 0: 
            in_channels_group.append(int(round(stem_channel * width_mult))) 
            channels_group.append(int(round(inplanes * width_mult))) 
        else: 
            in_channels_group.append(int(round(inplanes * width_mult))) 
            inplanes += final_ch / (depth // 3 * 1.0) 
            channels_group.append(int(round(inplanes * width_mult))) 
 
    features = ConvBNSwish(input, int(round(stem_channel * width_mult)), kernel_size=3, strides=(2,2), padding='same') 
 
    for block_idx, (in_c, c, t, s, se) in enumerate(zip(in_channels_group, channels_group, ts, strides, use_ses)): 
        features = LinearBottleneck(features, in_channels=in_c, filters=c, 
                                             t=t, 
                                             strides=(s,s), 
                                             use_se=se, se_ratio=se_ratio) 
     
    pen_channels = int(1280 * width_mult) 
    features = ConvBNSwish(features, pen_channels) 
    features = keras.layers.GlobalAveragePooling2D()(features)
    features = keras.layers.Reshape((1,1,pen_channels))(features)
    output = pretrainedClassifier(features, dropout_ratio, classes)

    model = keras.models.Model(input, output)
    return model

def pretrainedClassifier(input, dropout_ratio, classes, weight_decay=0.00005):
    output = keras.layers.Dropout(dropout_ratio)(input)
    output = keras.layers.Conv2D(filters=classes, kernel_size=1, padding='same',bias_regularizer=keras.regularizers.l2(weight_decay),kernel_regularizer=keras.regularizers.l2(weight_decay), kernel_initializer=keras.initializers.he_normal())(output)
    output = keras.layers.Activation(tf.nn.softmax)(output)
    output = keras.layers.Flatten()(output)
    return output

if __name__=='__main__':
    rexnetv1 = ReXNetV1((224,224,3), classes=1000)
    rexnetv1.summary()