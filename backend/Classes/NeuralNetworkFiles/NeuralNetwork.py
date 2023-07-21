import os
import sys
import io
import base64

import pandas as pd
import numpy as np
from pathlib import Path

import matplotlib.pyplot as plt

from backend.Classes.NeuralNetworkFiles import Core

class Layer_Category:
    def __init__(self, name, display_name, definition):
        self.name = name
        self.display_name = display_name
        self.definition = definition
    
    def getName(self):
        return self.name

    def getDisplayName(self):
        return self.display_name

    def getDefinition(self):
        return self.definition

# Create a list of possible categories to sect from.
list_Layer_Categories = []

def getLayer_Categories():
    return list_Layer_Categories

# Layer options are located at https://keras.io/api/layers/

## Core
Name = "Core"
Display_Name = "Core"
Definition = ["Core layers that most Neural Networks require."]

list_Layer_Categories.append(Layer_Category(Name, Display_Name, Definition))

## Convolution layers
Name = "Convolution"
Display_Name = "Convolution"
Definition = ["Convolution layers."]

list_Layer_Categories.append(Layer_Category(Name, Display_Name, Definition))

# obtain the list of Layers from all categories via their separate python files
list_Core = Core.getCore()

# Methods to process the Neural Network options.

# Returns all layers from a Category
def getCategoryPreopts(Category_Name):
    info = []
    if Category_Name == "Core":
        layers = list_Core

    for layer in layers:
        preopt_info = {"Name": layer.getName(), "Display_Name": layer.getDisplayName()}
        info.append(layer_info)

    return info

# Method to pull all parameters from a given layer option
def getParameters(Layer_Name):
    Parameters = {}
    
    for layer in list_Core:
        if layer.getName() == Layer_Name:
            Parameters = layer.getParameters()
            return Parameters


    return Parameters

# Method to check the chosen neural network and return a summary.
def perform_Preopt(data, i):
    result = ""
    return result