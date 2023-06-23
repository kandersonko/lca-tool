import os
import sys
import io
import base64

import pandas as pd
import numpy as np

from backend.Classes.PreoptimizationFiles import Preoptimizer

import matplotlib.pyplot as plt

from sklearn import preprocessing

from sklearn.feature_selection import VarianceThreshold

# Create a list of standardization preoptimizations to select from.
list_RemoveData = []

def getRemoveData():
    return list_RemoveData

## Drop Columns:
Name = "RemoveColumn"
Display_Name = "Remove Column"
Definition = ["Remove column from the dataset."]
Parameter_0 = {"Name":"column", "Type": ["select"], "Default":"", "Possible":["col_names"],
             "Definition":"The column name to remove from the dataset."}

Parameters = {"Parameter_0":Parameter_0}

list_RemoveData.append(Preoptimizer.Preoptimizer(Name, Display_Name, Definition, Parameters))

## Drop Rows:
Name = "RemoveRow"
Display_Name = "Remove Row"
Definition = ["Remove row from the dataset."]
Parameter_0 = {"Name":"row", "Type": ["int"], "Default":"", "Possible":["int"],
             "Definition":"The index number of the row to remove."}

Parameters = {"Parameter_0":Parameter_0}

list_RemoveData.append(Preoptimizer.Preoptimizer(Name, Display_Name, Definition, Parameters))

## Drop null values Removal:
Name = "DropRowsContainingNullValues"
Display_Name = "Drop Rows Containing Null Values"
Definition = ["Removes the rows that contain null value entires in any of the columns."]

Parameters = {}

list_RemoveData.append(Preoptimizer.Preoptimizer(Name, Display_Name, Definition, Parameters))

# VarianceThreshold
Name = "VarianceThreshold"
Display_Name = "Variance Threshold"
Definition = ["Feature selector that removes all low-variance features.\n\nThis feature selection algorithm looks only at the features (X), not the desired outputs (y), and can thus be used for unsupervised learning."]

Parameter_0 = {"Name":"threshold", "Type": ["float"], "Default":0.0, "Possible":["float"],
             "Definition":"Features with a training-set variance lower than this threshold will be removed. The default is to keep all features with non-zero variance, i.e. remove the features that have the same value in all samples."}

Parameters = {"Parameter_0":Parameter_0}

list_RemoveData.append(Preoptimizer.Preoptimizer(Name, Display_Name, Definition, Parameters))

def perform_Preopt(data, i, df):
    # get method
    method = data["Preopt_" + str(i)]

    new_df = df.copy()

    ## Removal
    if method == "RemoveColumn":
        new_df = df.drop(columns=[data["Preopt_" + str(i) + "_column_Input"]])

    if method == "RemoveRow":
        new_df = df.drop([int(data["Preopt_" + str(i) + "_row_Input"])])

    ## Null instances
    ### Remove all
    if method == "DropRowsContainingNullValues":
        new_df = df.dropna(axis=0)

    if method == "VarianceThreshold":
        threshold = float(data["Preopt_" + str(i) + "_threshold_Input"])

        enc = VarianceThreshold(threshold=threshold)

        new_df[data["Preopt_" + str(i) + "_column_Input"]] = enc.fit_transform(df[[data["Preopt_" + str(i) + "_column_Input"]]])

    return new_df
