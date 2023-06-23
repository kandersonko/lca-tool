import os
import sys
import io
import base64

import pandas as pd
import numpy as np

from backend.Classes.PreoptimizationFiles import Preoptimizer

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

Parameter_0 =  {"Name":"norm", "Type": ["option"], "Default":"l2", "Possible":["l1","l2","max"], 
               "Definition":"The norm to use to normalize each non zero sample (or each non-zero feature if axis is 0)."}
Parameter_1 =  {"Name":"axis", "Type": ["option"], "Default":1, "Possible":[0,1], 
               "Definition":"Define axis used to normalize the data along. If 1, independently normalize each sample, otherwise (if 0) normalize each feature."}
Parameter_2 =  {"Name":"copy", "Type": ["bool"], "Default":True, "Possible":[True, False], 
               "Definition":"Set to False to perform inplace transformation and avoid a copy (if the input is already a numpy array)."}
Parameter_3 =  {"Name":"return_norm", "Type": ["bool"], "Default":False, "Possible":[True,False], 
               "Definition":"Whether to return the computed norms."}

Parameters = {"Parameter_0":Parameter_0, "Parameter_1":Parameter_1,"Parameter_2":Parameter_2, "Parameter_3":Parameter_3}

list_Normalization.append(Preoptimizer.Preoptimizer(Name, Display_Name, Definition, Parameters))

# normalizer (same thing as normalize exept less customization. As such, is not implemented)

def perform_Preopt(data, i, df):
    # get method
    method = data["Preopt_" + str(i)]

    new_df = df.copy()

    ## normalizer
    if method == "normalizer":
        norm = data["Preopt_" + str(i) + "_norm_Input"]

        axis = data["Preopt_" + str(i) + "_axis_Input"]

        copy = True
        if data["Preopt_" + str(i) + "_copy_Input"] == "False":
            copy = False

        return_norm = False
        if data["Preopt_" + str(i) + "_return_norm_Input"] == "False":
            return_norm = True

        temp = df.copy()
        temp = temp.drop(columns=[data["class_col"]])

        X = temp

        new_df = preprocessing.normalize(X=X,
                                     norm=norm,
                                     axis=axis,
                                     copy=copy,
                                     return_norm=return_norm)

        new_df[data["class_col"]]=df[data["class_col"]]
        
    return new_df