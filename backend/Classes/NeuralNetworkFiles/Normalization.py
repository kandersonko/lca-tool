import base64

import pandas as pd
import numpy as np

from backend.Classes.NeuralNetworkFiles import Layer
from backend.Classes import HyperParameters

import matplotlib.pyplot as plt

from tensorflow import keras

# Create a list of core layers to select from.
list_Normalization = []

def getNormalization():
    return list_Normalization

## BatchNormalization
Name = "BatchNormalization"
Display_Name = "Batch Normalization"
Definition = ["Layer that normalizes its inputs.\n\nBatch normalization applies a transformation that maintains the mean output close to 0 and the output standard deviation close to 1.\n\nImportantly, batch normalization works differently during training and during inference."]
Parameter_0 = {"Name":"axis", "Type": ["int"], "Default_option":-1, "Default_value":-1, "Possible":["int"],
             "Definition":'Integer, the axis that should be normalized (typically the features axis). For instance, after a Conv2D layer with data_format="channels_first", set axis=1 in BatchNormalization.'}
Parameter_1 = {"Name":"momentum", "Type": ["float"], "Default_option":0.99, "Default_value":0.99, "Possible":["float"],
             "Definition":"Momentum for the moving average."}
Parameter_2 = {"Name":"epsilon", "Type": ["float"], "Default_option":0.001, "Default_value":0.001, "Possible":["float"],
             "Definition":"Small float added to variance to avoid dividing by zero."}
Parameter_3 = {"Name":"center", "Type": ["bool"], "Default_option":True, "Default_value":True, "Possible":[True,False],
             "Definition":"If True, add offset of beta to normalized tensor. If False, beta is ignored."}
Parameter_4 = {"Name":"scale", "Type": ["bool"], "Default_option":True, "Default_value":True, "Possible":[True,False],
             "Definition":"If True, multiply by gamma. If False, gamma is not used. When the next layer is linear (also e.g. nn.relu), this can be disabled since the scaling will be done by the next layer."}
Parameter_5 = {"Name":"beta_initializer", "Type": ["option"], "Default_option":"zeros", "Default_value":"zeros", "Possible":Layer.getInitializers(),
             "Definition":"Initializer for the beta weight."}
Parameter_6 = {"Name":"gamma_initializer", "Type": ["option"], "Default_option":"ones", "Default_value":"ones", "Possible":Layer.getInitializers(),
             "Definition":"Initializer for the gamma weight."}
Parameter_7 = {"Name":"moving_mean_initializer", "Type": ["option"], "Default_option":"zeros", "Default_value":"zeros", "Possible":Layer.getInitializers(),
             "Definition":"Initializer for the moving mean."}
Parameter_8 = {"Name":"moving_variance_initializer", "Type": ["option"], "Default_option":"ones", "Default_value":"ones", "Possible":Layer.getInitializers(),
             "Definition":"Initializer for the moving variance."}
Parameter_9 = {"Name":"beta_regularizer", "Type": ["option"], "Default_option":"None", "Default_value":"None", "Possible":Layer.getRegularizers(),
             "Definition":"Optional regularizer for the beta weight."}
Parameter_10 = {"Name":"gamma_regularizer", "Type": ["option"], "Default_option":"None", "Default_value":"None", "Possible":Layer.getRegularizers(),
             "Definition":"Optional regularizer for the gamma weight."}
#Parameter_12 = {"Name":"beta_constraint", "Type": ["option"], "Default_option":"None", "Default_value":"None", "Possible":Layer.getConstraints,
#             "Definition":"Optional constraint for the beta weight."}
#Parameter_12 = {"Name":"gamma_constraint", "Type": ["option"], "Default_option":"None", "Default_value":"None", "Possible":Layer.getConstraints,
#             "Definition":"Optional constraint for the gamma weight."}
## For some reason BatchNormalization doesnt recognize synchronized parameter.
#Parameter_11 = {"Name":"synchronized", "Type": ["bool"], "Default_option":False, "Default_value":False, "Possible":[True,False],
#             "Definition":"If True, synchronizes the global batch statistics (mean and variance) for the layer across all devices at each training step in a distributed training strategy. If False, each replica uses its own local batch statistics. Only relevant when used inside a tf.distribute strategy."}


Parameters = {"Parameter_0":Parameter_0, "Parameter_1":Parameter_1, "Parameter_2":Parameter_2, "Parameter_3":Parameter_3,
              "Parameter_4":Parameter_4, "Parameter_5":Parameter_5, "Parameter_6":Parameter_6, "Parameter_7":Parameter_7,
              "Parameter_8":Parameter_8, "Parameter_9":Parameter_9, "Parameter_10":Parameter_10}

list_Normalization.append(Layer.Layer(Name, Display_Name, Definition, Parameters))


## LayerNormalization
Name = "LayerNormalization"
Display_Name = "Layer Normalization"
Definition = ["Layer that normalizes its inputs.\n\nBatch normalization applies a transformation that maintains the mean output close to 0 and the output standard deviation close to 1.\n\nImportantly, batch normalization works differently during training and during inference."]
Parameter_0 = {"Name":"axis", "Type": ["int"], "Default_option":-1, "Default_value":-1, "Possible":["int"],
             "Definition":'Integer, the axis that should be normalized (typically the features axis). For instance, after a Conv2D layer with data_format="channels_first", set axis=1 in BatchNormalization.'}
Parameter_1 = {"Name":"epsilon", "Type": ["float"], "Default_option":0.001, "Default_value":0.001, "Possible":["float"],
             "Definition":"Small float added to variance to avoid dividing by zero."}
Parameter_2 = {"Name":"center", "Type": ["bool"], "Default_option":True, "Default_value":True, "Possible":[True,False],
             "Definition":"If True, add offset of beta to normalized tensor. If False, beta is ignored."}
Parameter_3 = {"Name":"scale", "Type": ["bool"], "Default_option":True, "Default_value":True, "Possible":[True,False],
             "Definition":"If True, multiply by gamma. If False, gamma is not used. When the next layer is linear (also e.g. nn.relu), this can be disabled since the scaling will be done by the next layer."}
Parameter_4 = {"Name":"beta_initializer", "Type": ["option"], "Default_option":"zeros", "Default_value":"zeros", "Possible":Layer.getInitializers(),
             "Definition":"Initializer for the beta weight."}
Parameter_5 = {"Name":"gamma_initializer", "Type": ["option"], "Default_option":"ones", "Default_value":"ones", "Possible":Layer.getInitializers(),
             "Definition":"Initializer for the gamma weight."}
Parameter_6 = {"Name":"beta_regularizer", "Type": ["option"], "Default_option":"None", "Default_value":"None", "Possible":Layer.getRegularizers(),
             "Definition":"Optional regularizer for the beta weight."}
Parameter_7 = {"Name":"gamma_regularizer", "Type": ["option"], "Default_option":"None", "Default_value":"None", "Possible":Layer.getRegularizers(),
             "Definition":"Optional regularizer for the gamma weight."}
#Parameter_12 = {"Name":"beta_constraint", "Type": ["option"], "Default_option":"None", "Default_value":"None", "Possible":Layer.getConstraints,
#             "Definition":"Optional constraint for the beta weight."}
#Parameter_12 = {"Name":"gamma_constraint", "Type": ["option"], "Default_option":"None", "Default_value":"None", "Possible":Layer.getConstraints,
#             "Definition":"Optional constraint for the gamma weight."}

Parameters = {"Parameter_0":Parameter_0, "Parameter_1":Parameter_1, "Parameter_2":Parameter_2, "Parameter_3":Parameter_3,
              "Parameter_4":Parameter_4, "Parameter_5":Parameter_5, "Parameter_6":Parameter_6, "Parameter_7":Parameter_7}

list_Normalization.append(Layer.Layer(Name, Display_Name, Definition, Parameters))


###The following is only supported with tensorflow 2.13 and up. As we are using 2.11, these are not used.
'''
## UnitNormalization
Name = "UnitNormalization"
Display_Name = "Unit Normalization"
Definition = ["Unit normalization layer.\n\nNormalize a batch of inputs so that each input in the batch has a L2 norm equal to 1 (across the axes specified in axis)."]
Parameter_0 = {"Name":"axis", "Type": ["int"], "Default_option":-1, "Default_value":-1, "Possible":["int"],
             "Definition":'Integer or list/tuple. The axis or axes to normalize across. Typically this is the features axis or axes. The left-out axes are typically the batch axis or axes. Defaults to -1, the last dimension in the input.'}

Parameters = {"Parameter_0":Parameter_0 }

list_Normalization.append(Layer.Layer(Name, Display_Name, Definition, Parameters))


## GroupNormalization
Name = "GroupNormalization"
Display_Name = "Group Normalization"
Definition = ["Group normalization layer.\n\nGroup Normalization divides the channels into groups and computes within each group the mean and variance for normalization. Empirically, its accuracy is more stable than batch norm in a wide range of small batch sizes, if learning rate is adjusted linearly with batch sizes.\n\nRelation to Layer Normalization: If the number of groups is set to 1, then this operation becomes nearly identical to Layer Normalization (see Layer Normalization docs for details).\n\nRelation to Instance Normalization: If the number of groups is set to the input dimension (number of groups is equal to number of channels), then this operation becomes identical to Instance Normalization."]
Parameter_0 = {"Name":"groups", "Type": ["int"], "Default_option":32, "Default_value":32, "Possible":["int"],
             "Definition":'Integer, the number of groups for Group Normalization. Can be in the range [1, N] where N is the input dimension. The input dimension must be divisible by the number of groups. Defaults to 32.'}
Parameter_0 = {"Name":"axis", "Type": ["int"], "Default_option":-1, "Default_value":-1, "Possible":["int"],
             "Definition":'Integer or List/Tuple. The axis or axes to normalize across. Typically this is the features axis/axes. The left-out axes are typically the batch axis/axes. This argument defaults to -1, the last dimension in the input.'}
Parameter_1 = {"Name":"epsilon", "Type": ["float"], "Default_option":0.001, "Default_value":0.001, "Possible":["float"],
             "Definition":"Small float added to variance to avoid dividing by zero."}
Parameter_2 = {"Name":"center", "Type": ["bool"], "Default_option":True, "Default_value":True, "Possible":[True,False],
             "Definition":"If True, add offset of beta to normalized tensor. If False, beta is ignored."}
Parameter_3 = {"Name":"scale", "Type": ["bool"], "Default_option":True, "Default_value":True, "Possible":[True,False],
             "Definition":"If True, multiply by gamma. If False, gamma is not used. When the next layer is linear (also e.g. nn.relu), this can be disabled since the scaling will be done by the next layer."}
Parameter_4 = {"Name":"beta_initializer", "Type": ["option"], "Default_option":"zeros", "Default_value":"zeros", "Possible":Layer.getInitializers(),
             "Definition":"Initializer for the beta weight."}
Parameter_5 = {"Name":"gamma_initializer", "Type": ["option"], "Default_option":"ones", "Default_value":"ones", "Possible":Layer.getInitializers(),
             "Definition":"Initializer for the gamma weight."}
Parameter_6 = {"Name":"beta_regularizer", "Type": ["option"], "Default_option":"None", "Default_value":"None", "Possible":Layer.getRegularizers(),
             "Definition":"Optional regularizer for the beta weight."}
Parameter_7 = {"Name":"gamma_regularizer", "Type": ["option"], "Default_option":"None", "Default_value":"None", "Possible":Layer.getRegularizers(),
             "Definition":"Optional regularizer for the gamma weight."}
#Parameter_12 = {"Name":"beta_constraint", "Type": ["option"], "Default_option":"None", "Default_value":"None", "Possible":Layer.getConstraints,
#             "Definition":"Optional constraint for the beta weight."}
#Parameter_12 = {"Name":"gamma_constraint", "Type": ["option"], "Default_option":"None", "Default_value":"None", "Possible":Layer.getConstraints,
#             "Definition":"Optional constraint for the gamma weight."}

Parameters = {"Parameter_0":Parameter_0, "Parameter_1":Parameter_1, "Parameter_2":Parameter_2, "Parameter_3":Parameter_3,
              "Parameter_4":Parameter_4, "Parameter_5":Parameter_5, "Parameter_6":Parameter_6, "Parameter_7":Parameter_7}

list_Normalization.append(Layer.Layer(Name, Display_Name, Definition, Parameters))
'''

def create_Layer(data, i):
    # get layer name
    layer = data["Layer_" + str(i)]

    # get the chosen settings for the layer
    Parameters = HyperParameters.getParameters(data["Layer_" + str(i)], list_Normalization)
    settings = HyperParameters.getSettings(data, Parameters, i, Layer.getName())

    new_layer = ""

    ## BatchNormalization
    if layer == "BatchNormalization":

        # Create the layer
        new_layer = keras.layers.BatchNormalization(axis=settings["Parameter_0"], momentum=settings["Parameter_1"], epsilon=settings["Parameter_2"],
                                                    center=settings["Parameter_3"], scale=settings["Parameter_4"], beta_initializer=settings["Parameter_5"],
                                                    gamma_initializer=settings["Parameter_6"], moving_mean_initializer=settings["Parameter_7"], moving_variance_initializer=settings["Parameter_8"],
                                                    beta_regularizer=settings["Parameter_9"], gamma_regularizer=settings["Parameter_10"])
    
    ## LayerNormalization
    if layer == "LayerNormalization":

        new_layer = keras.layers.LayerNormalization(axis=settings["Parameter_0"], epsilon=settings["Parameter_1"], center=settings["Parameter_2"],
                                                    scale=settings["Parameter_3"], beta_initializer=settings["Parameter_4"], gamma_initializer=settings["Parameter_5"],
                                                    beta_regularizer=settings["Parameter_6"], gamma_regularizer=settings["Parameter_7"])
     
    '''
    ## UnitNormalization
    if layer == "UnitNormalization":

        new_layer = keras.layers.UnitNormalization(axis=settings["Parameter_0"])

    ## GroupNormalization
    if layer == "GroupNormalization":

        new_layer = keras.layers.GroupNormalization(groups=settings["Parameter_0"], axis=settings["Parameter_1"], epsilon=settings["Parameter_2"], center=settings["Parameter_3"],
                                                    scale=settings["Parameter_4"], beta_initializer=settings["Parameter_5"], gamma_initializer=settings["Parameter_6"],
                                                    beta_regularizer=settings["Parameter_7"], gamma_regularizer=settings["Parameter_8"])
    '''

        
    return new_layer