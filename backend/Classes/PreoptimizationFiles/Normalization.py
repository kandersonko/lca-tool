import os
import sys
import io
import base64

import pandas as pd
import numpy as np

from backend.Classes.PreoptimizationFiles import Preoptimizer
from backend.Classes import HyperParameters

import matplotlib.pyplot as plt

from sklearn import preprocessing

# Create a list of standardization preoptimizations to select from.
list_Normalization = []

def getNormalization():
    return list_Normalization

# normalize
Name = "Normalize"
Display_Name = "Normalize"
Definition = ["Scale input vectors (all columns and rows execpt the y input e.i. class column) individually to unit norm (vector length)."]

Parameter_0 =  {"Name":"norm", "Type": ["option"], "Default_option":"l2", "Default_value":"l2", "Possible":["l1","l2","max"], 
               "Definition":"The norm to use to normalize each non zero sample (or each non-zero feature if axis is 0)."}
Parameter_1 =  {"Name":"axis", "Type": ["option_integer"], "Default_option":1, "Default_value":1, "Possible":[0,1], 
               "Definition":"Define axis used to normalize the data along. If 1, independently normalize each sample, otherwise (if 0) normalize each feature."}
Parameter_2 =  {"Name":"copy", "Type": ["bool"], "Default_option":True, "Default_value":True, "Possible":[True, False], 
               "Definition":"Set to False to perform inplace transformation and avoid a copy (if the input is already a numpy array)."}
## Does not work well with matrix data.
#Parameter_3 =  {"Name":"return_norm", "Type": ["bool"], "Default_option":False, "Default_value":"", "Possible":[True,False], 
#               "Definition":"Whether to return the computed norms."}

Parameters = {"Parameter_0":Parameter_0, "Parameter_1":Parameter_1,"Parameter_2":Parameter_2}

list_Normalization.append(Preoptimizer.Preoptimizer(Name, Display_Name, Definition, Parameters))

# normalizer (same thing as normalize exept less customization. As such, is not implemented)

def perform_Preopt(data, i, df):
    # get method
    method = data["Preopt_" + str(i)]

    new_df = df.copy()

    Parameters = HyperParameters.getParameters(data["Preopt_" + str(i)], list_Normalization)

    ## normalizer
    if method == "Normalize":
        
        settings = HyperParameters.getSettings(data, Parameters, i)

        new_df.loc[:, new_df.columns != data["class_col"]] = preprocessing.normalize(X=new_df.loc[:, new_df.columns != data["class_col"]],
                                        norm=settings["Parameter_0"],
                                        axis=settings["Parameter_1"],
                                        copy=settings["Parameter_2"])
        
    return new_df