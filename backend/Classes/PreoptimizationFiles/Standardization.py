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
list_standardization = []

def getStandardization():
    return list_standardization

# Standard Scaling:
Name = "StandardScaler"
Display_Name = "Standard Scaler"
Definition = ["Standardize features by removing the mean and scaling to unit variance.\n\nThe standard score of a sample x is calculated as:\n\nz = (x - u) / s\n\nwhere u is the mean of the training samples or zero if with_mean=False, and s is the standard deviation of the training samples or one if with_std=False.\n\nCentering and scaling happen independently on each feature by computing the relevant statistics on the samples in the training set. Mean and standard deviation are then stored to be used on later data using transform.\n\nStandardization of a dataset is a common requirement for many machine learning estimators: they might behave badly if the individual features do not more or less look like standard normally distributed data (e.g. Gaussian with 0 mean and unit variance).\n\nFor instance many elements used in the objective function of a learning algorithm (such as the RBF kernel of Support Vector Machines or the L1 and L2 regularizers of linear models) assume that all features are centered around 0 and have variance in the same order. If a feature has a variance that is orders of magnitude larger than others, it might dominate the objective function and make the estimator unable to learn from other features correctly as expected.\n\nThis scaler can also be applied to sparse CSR or CSC matrices by passing with_mean=False to avoid breaking the sparsity structure of the data."]
Parameter_0 =  {"Name":"copy", "Type": ["bool"], "Default":True, "Possible":[True, False], 
               "Definition":"If False, try to avoid a copy and do inplace scaling instead. This is not guaranteed to always work inplace; e.g. if the data is not a NumPy array or scipy.sparse CSR matrix, a copy may still be returned."}
Parameter_1 =  {"Name":"with_mean", "Type": ["bool"], "Default":True, "Possible":[True, False], 
               "Definition":"If True, center the data before scaling. This does not work (and will raise an exception) when attempted on sparse matrices, because centering them entails building a dense matrix which in common use cases is likely to be too large to fit in memory."}
Parameter_2 =  {"Name":"with_std", "Type": ["bool"], "Default":True, "Possible":[True, False], 
               "Definition":"If True, scale the data to unit variance (or equivalently, unit standard deviation)."}
Parameter_3 = {"Name":"column", "Type": ["select"], "Default":"", "Possible":["col_names"],
               "Definition":"Column to perform the preoptimization on."}

Parameters = {"Parameter_0":Parameter_0, "Parameter_1":Parameter_1,"Parameter_2":Parameter_2, "Parameter_3":Parameter_3}

list_standardization.append(Preoptimizer.Preoptimizer(Name, Display_Name, Definition, Parameters))

# MinMaxScaler
Name = "MinMaxScaler"
Display_Name = "Min-Max Scaler"
Definition = ["Transform features by scaling each feature to a given range.\n\nThis estimator scales and translates each feature individually such that it is in the given range on the training set, e.g. between zero and one.\n\nThe transformation is given by:\n\nX_std = (X - X.min(axis=0)) / (X.max(axis=0)) - X.min(axis=0))\nX_scaled = X_std * (max - min) +min\n\nwhere min, max = feature_range.\n\nThis transformation is often used as an alternative to zero mean, unit variance scaling."]

Parameter_0 =  {"Name":"min", "Type": ["int"], "Default":0, "Possible":["int"], 
               "Definition":"Minimum range of the desired transformed data"}
Parameter_1 =  {"Name":"max", "Type": ["int"], "Default":1, "Possible":["int"], 
               "Definition":"Maxium range of the desired transformed data."}
Parameter_2 =  {"Name":"copy", "Type": ["bool"], "Default":True, "Possible":[True, False], 
               "Definition":"Set to False to perform inplace row normalization and avoid a copy (if the input is already a numpy array)."}
Parameter_3 = {"Name":"clip", "Type": ["bool"], "Default":False, "Possible":[True, False],
               "Definition":"Set to True to clip transformed values of held-out data to provided feature range."}
Parameter_4 = {"Name":"column", "Type": ["select"], "Default":"", "Possible":["col_names"],
               "Definition":"Column to perform the preoptimization on."}

Parameters = {"Parameter_0":Parameter_0, "Parameter_1":Parameter_1,"Parameter_2":Parameter_2, "Parameter_3":Parameter_3, "Parameter_4":Parameter_4}

list_standardization.append(Preoptimizer.Preoptimizer(Name, Display_Name, Definition, Parameters))

## MaxAbsScaler
Name = "MaxAbsScaler"
Display_Name = "Max Absolute Scaler"
Definition = ["Scale each feature by its maximum absolute value.\n\nThis estimator scales and translates each feature individually such that the maximal absolute value of each feature in the training set will be 1.0. It does not shift/center the data, and thus does not destroy any sparsity.\n\nThis scaler can also be applied to sparse CSR or CSC matrices."]

Parameter_0 =  {"Name":"copy", "Type": ["bool"], "Default":True, "Possible":[True, False], 
               "Definition":"Set to False to perform inplace row normalization and avoid a copy (if the input is already a numpy array)."}
Parameter_1 = {"Name":"column", "Type": ["select"], "Default":"", "Possible":["col_names"],
               "Definition":"Column to perform the preoptimization on."}

Parameters = {"Parameter_0":Parameter_0, "Parameter_1":Parameter_1}

list_standardization.append(Preoptimizer.Preoptimizer(Name, Display_Name, Definition, Parameters))

## RobustScaler
Name = "RobustScaler"
Display_Name = "Robust Scaler"
Definition = ["Scale features using statistics that are robust to outliers.\n\nThis Scaler removes the median and scales the data according to the quantile range (defaults to IQR: Interquartile Range). The IQR is the range between the 1st quartile (25th quantile) and the 3rd quartile (75th quantile).\n\nCentering and scaling happen independently on each feature by computing the relevant statistics on the samples in the training set. Median and interquartile range are then stored to be used on later data using the transform method.\n\nStandardization of a dataset is a common requirement for many machine learning estimators. Typically this is done by removing the mean and scaling to unit variance. However, outliers can often influence the sample mean / variance in a negative way. In such cases, the median and the interquartile range often give better results."]

Parameter_0 =  {"Name":"with_centering", "Type": ["bool"], "Default":True, "Possible":[True, False], 
               "Definition":"If True, center the data before scaling. This will cause transform to raise an exception when attempted on sparse matrices, because centering them entails building a dense matrix which in common use cases is likely to be too large to fit in memory."}
Parameter_1 =  {"Name":"with_scaling", "Type": ["bool"], "Default":True, "Possible":[True, False], 
               "Definition":"If True, scale the data to interquartile range."}
Parameter_2 =  {"Name":"min", "Type": ["float"], "Default":25.0, "Possible":["float"], 
               "Definition":"Quantile range used to calculate scale_. By default this is equal to the IQR, i.e., min is the first quantile and max is the third quantile."}
Parameter_3 =  {"Name":"max", "Type": ["float"], "Default":75.0, "Possible":["float"], 
               "Definition":"Quantile range used to calculate scale_. By default this is equal to the IQR, i.e., min is the first quantile and max is the third quantile."}
Parameter_4 =  {"Name":"copy", "Type": ["bool"], "Default":True, "Possible":[True, False], 
               "Definition":"If False, try to avoid a copy and do inplace scaling instead. This is not guaranteed to always work inplace; e.g. if the data is not a NumPy array or scipy.sparse CSR matrix, a copy may still be returned."}
Parameter_5 = {"Name":"unit_variance", "Type": ["bool"], "Default":False, "Possible":[True, False],
               "Definition":"If True, scale data so that normally distributed features have a variance of 1. In general, if the difference between the x-values of q_max and q_min for a standard normal distribution is greater than 1, the dataset will be scaled down. If less than 1, the dataset will be scaled up."}
Parameter_6 = {"Name":"column", "Type": ["select"], "Default":"", "Possible":["col_names"],
               "Definition":"Column to perform the preoptimization on."}

Parameters = {"Parameter_0":Parameter_0, "Parameter_1":Parameter_1,"Parameter_2":Parameter_2, "Parameter_3":Parameter_3, "Parameter_4":Parameter_4,
              "Parameter_5":Parameter_5, "Parameter_6":Parameter_6}

list_standardization.append(Preoptimizer.Preoptimizer(Name, Display_Name, Definition, Parameters))


def perform_Preopt(data, i, df):
    # get method
    method = data["Preopt_" + str(i)]

    new_df = df.copy()

    ### Standard Scaler
    if method == "StandardScaler":
        copy = True
        if data["Preopt_" + str(i) + "_copy_Input"] == "False":
            copy = False

        with_mean = True
        if data["Preopt_" + str(i) + "_with_mean_Input"] == "False":
            with_mean = False

        with_std = True
        if data["Preopt_" + str(i) + "_with_std_Input"] == "False":
            with_std = False

        pp = preprocessing.StandardScaler(copy=copy,
                            with_mean=with_mean,
                            with_std=with_std)
        
        index_of_column = df.columns.get_loc(data["Preopt_" + str(i) + "_column_Input"])

        temp = pp.fit_transform(df[[data["Preopt_" + str(i) + "_column_Input"]]]).flatten()

        new_df.iloc[:,index_of_column] = pp.fit_transform(df[[data["Preopt_" + str(i) + "_column_Input"]]]).flatten()

    ## Minmax Scaler
    if method == "MinMaxScaler":
        min = 0
        if data["Preopt_" + str(i) + "_min_Input"] != "" and data["Preopt_" + str(i) + "_min_Input"] != None:
            min = int(data["Preopt_" + str(i) + "_min_Input"])

        max = 1
        if data["Preopt_" + str(i) + "_max_Input"] != "" and data["Preopt_" + str(i) + "_max_Input"] != None:
            max = int(data["Preopt_" + str(i) + "_max_Input"])
        
        feature_range = (min,max)


        copy = True
        if data["Preopt_" + str(i) + "_copy_Input"] == "False":
            copy = False

        clip = False
        if data["Preopt_" + str(i) + "_with_mean_Input"] == "True":
            clip = True

        pp = preprocessing.MinMaxScaler(feature_range=feature_range,
                            copy=copy,
                            clip=clip)
        
        index_of_column = df.columns.get_loc(data["Preopt_" + str(i) + "_column_Input"])

        temp = pp.fit_transform(df[[data["Preopt_" + str(i) + "_column_Input"]]]).flatten()

        new_df.iloc[:,index_of_column] = pp.fit_transform(df[[data["Preopt_" + str(i) + "_column_Input"]]]).flatten()

    ## MaxAbsScaler
    if method == "MaxAbsScaler":
        copy = True
        if data["Preopt_" + str(i) + "_copy_Input"] == "False":
            copy = False

        pp = preprocessing.MaxAbsScaler(copy=copy)
        
        index_of_column = df.columns.get_loc(data["Preopt_" + str(i) + "_column_Input"])

        temp = pp.fit_transform(df[[data["Preopt_" + str(i) + "_column_Input"]]]).flatten()

        new_df.iloc[:,index_of_column] = pp.fit_transform(df[[data["Preopt_" + str(i) + "_column_Input"]]]).flatten()

    ## RobustScaler
    if method == "RobustScaler":
        with_centering = True
        if data["Preopt_" + str(i) + "_with_centering_Input"] == "False":
            with_centering = False

        with_scaling = True
        if data["Preopt_" + str(i) + "_with_scaling_Input"] == "False":
            with_scaling = False

        min = 25.0
        if data["Preopt_" + str(i) + "_min_Input"] != "" and data["Preopt_" + str(i) + "_min_Input"] != None:
            min = float(data["Preopt_" + str(i) + "_min_Input"])

        max = 75.0
        if data["Preopt_" + str(i) + "_max_Input"] != "" and data["Preopt_" + str(i) + "_max_Input"] != None:
            max = float(data["Preopt_" + str(i) + "_max_Input"])

        quantile_range = (min,max)

        copy = True
        if data["Preopt_" + str(i) + "_copy_Input"] == "False":
            copy = False

        unit_variance = False
        if data["Preopt_" + str(i) + "_unit_variance_Input"] == "True":
            unit_variance = True

        pp = preprocessing.RobustScaler(with_centering=with_centering,
                                        with_scaling=with_scaling,
                                        quantile_range=quantile_range,
                                        copy=copy,
                                        unit_variance=unit_variance)
        
        index_of_column = df.columns.get_loc(data["Preopt_" + str(i) + "_column_Input"])

        temp = pp.fit_transform(df[[data["Preopt_" + str(i) + "_column_Input"]]]).flatten()

        new_df.iloc[:,index_of_column] = pp.fit_transform(df[[data["Preopt_" + str(i) + "_column_Input"]]]).flatten()

    return new_df