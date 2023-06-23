import os
import sys
import io
import base64

import pandas as pd
import numpy as np

from backend.Classes.PreoptimizationFiles import Preoptimizer

import matplotlib.pyplot as plt

from sklearn import preprocessing

from sklearn.preprocessing import QuantileTransformer


# Create a list of standardization preoptimizations to select from.
list_NonLT = []

def getNonLT():
    return list_NonLT

# QuantileTransformer
Name = "QuantileTransformer"
Display_Name = "Quantile Transformer"
Definition = ["Transform features using quantiles information.\n\nThis method transforms the features to follow a uniform or a normal distribution. Therefore, for a given feature, this transformation tends to spread out the most frequent values. It also reduces the impact of (marginal) outliers: this is therefore a robust preprocessing scheme.\n\nThe transformation is applied on each feature independently. First an estimate of the cumulative distribution function of a feature is used to map the original values to a uniform distribution. The obtained values are then mapped to the desired output distribution using the associated quantile function. Features values of new/unseen data that fall below or above the fitted range will be mapped to the bounds of the output distribution. Note that this transform is non-linear. It may distort linear correlations between variables measured at the same scale but renders variables measured at different scales more directly comparable."]

Parameter_0 =  {"Name":"n_quantiles", "Type": ["int"], "Default":1000, "Possible":["int"], 
               "Definition":"Number of quantiles to be computed. It corresponds to the number of landmarks used to discretize the cumulative distribution function. If n_quantiles is larger than the number of samples, n_quantiles is set to the number of samples as a larger number of quantiles does not give a better approximation of the cumulative distribution function estimator."}
Parameter_1 =  {"Name":"output_distribution", "Type": ["option"], "Default":"uniform", "Possible":["uniform","normal"], 
               "Definition":"Marginal distribution for the transformed data. The choices are ‘uniform’ (default) or ‘normal’."}
Parameter_2 =  {"Name":"ignore_implicit_zeros", "Type": ["bool"], "Default":False, "Possible":[True, False], 
               "Definition":"Only applies to sparse matrices. If True, the sparse entries of the matrix are discarded to compute the quantile statistics. If False, these entries are treated as zeros."}
Parameter_3 =  {"Name":"subsample", "Type": ["int"], "Default":10000, "Possible":["int"], 
               "Definition":"Maximum number of samples used to estimate the quantiles for computational efficiency. Note that the subsampling procedure may differ for value-identical sparse and dense matrices."}
Parameter_4 =  {"Name":"random_state", "Type": ["int_or_null"], "Default":None, "Possible":["int","None"], 
               "Definition":"Determines random number generation for subsampling and smoothing noise. Please see subsample for more details. Pass an int for reproducible results across multiple function calls."}
Parameter_5 =  {"Name":"copy", "Type": ["bool"], "Default":True, "Possible":[True, False], 
               "Definition":"Set to False to perform inplace transformation and avoid a copy (if the input is already a numpy array)."}
Parameter_6 = {"Name":"column", "Type": ["select"], "Default":"", "Possible":["col_names"],
               "Definition":"Column to perform the preoptimization on."}

Parameters = {"Parameter_0":Parameter_0, "Parameter_1":Parameter_1,"Parameter_2":Parameter_2, "Parameter_3":Parameter_3,
              "Parameter_4":Parameter_4, "Parameter_5":Parameter_5,"Parameter_6":Parameter_6}

list_NonLT.append(Preoptimizer.Preoptimizer(Name, Display_Name, Definition, Parameters))

# PowerTransformer
Name = "PowerTransformer"
Display_Name = "Power Transformer"
Definition = ["Apply a power transform featurewise to make data more Gaussian-like.\n\nPower transforms are a family of parametric, monotonic transformations that are applied to make data more Gaussian-like. This is useful for modeling issues related to heteroscedasticity (non-constant variance), or other situations where normality is desired.\n\nCurrently, PowerTransformer supports the Box-Cox transform and the Yeo-Johnson transform. The optimal parameter for stabilizing variance and minimizing skewness is estimated through maximum likelihood.\n\nBox-Cox requires input data to be strictly positive, while Yeo-Johnson supports both positive or negative data.\n\nBy default, zero-mean, unit-variance normalization is applied to the transformed data."]

Parameter_0 =  {"Name":"method", "Type": ["option"], "Default":"yeo-johnson", "Possible":["yeo-johnson","box-cox"], 
               "Definition":"The power transform method. Available methods are:\n\n‘yeo-johnson’, works with positive and negative values\n\n‘box-cox’, only works with strictly positive values"}
Parameter_1 =  {"Name":"standardize", "Type": ["bool"], "Default":True, "Possible":[True,False], 
               "Definition":"Set to True to apply zero-mean, unit-variance normalization to the transformed output."}
Parameter_2 =  {"Name":"copy", "Type": ["bool"], "Default":True, "Possible":[True, False], 
               "Definition":"Set to False to perform inplace transformation and avoid a copy (if the input is already a numpy array)."}
Parameter_3 = {"Name":"column", "Type": ["select"], "Default":"", "Possible":["col_names"],
               "Definition":"Column to perform the preoptimization on."}

Parameters = {"Parameter_0":Parameter_0, "Parameter_1":Parameter_1,"Parameter_2":Parameter_2, "Parameter_3":Parameter_3}

list_NonLT.append(Preoptimizer.Preoptimizer(Name, Display_Name, Definition, Parameters))

def perform_Preopt(data, i, df):
    # get method
    method = data["Preopt_" + str(i)]

    new_df = df.copy()

    ## QuantileTransformer
    if method == "QuantileTransformer":
        n_quantiles = 1000
        if data["Preopt_" + str(i) + "_n_quantiles_Input"] != "" and data["Preopt_" + str(i) + "_n_quantiles_Input"] != None:
            n_quantiles = int(data["Preopt_" + str(i) + "_n_quantiles_Input"])

        output_distribution = data["Preopt_" + str(i) + "_output_distribution_Input"]

        ignore_implicit_zeros = False
        if data["Preopt_" + str(i) + "_with_centering_Input"] == "True":
            ignore_implicit_zeros = True

        subsample = 10000
        if data["Preopt_" + str(i) + "_subsample_Input"] != "" and data["Preopt_" + str(i) + "_subsample_Input"] != None:
            subsample = int(data["Preopt_" + str(i) + "_subsample_Input"])

        random_state = None
        if data["Preopt_" + str(i) + "_random_state_Input"] != "" and data["Preopt_" + str(i) + "_random_state_Input"] != None:
            random_state = int(data["Preopt_" + str(i) + "_random_state_Input"])

        copy = True
        if data["Preopt_" + str(i) + "_copy_Input"] == "False":
            copy = False

        pp = preprocessing.QuantileTransformer(n_quantiles=n_quantiles,
                                               output_distribution=output_distribution,
                                               ignore_implicit_zeros=ignore_implicit_zeros,
                                               subsample=subsample,
                                               random_state=random_state,
                                               copy=copy)
        
        index_of_column = df.columns.get_loc(data["Preopt_" + str(i) + "_column_Input"])

        temp = pp.fit_transform(df[[data["Preopt_" + str(i) + "_column_Input"]]]).flatten()

        new_df.iloc[:,index_of_column] = pp.fit_transform(df[[data["Preopt_" + str(i) + "_column_Input"]]]).flatten()

    ## PowerTransformer
    if method == "PowerTransformer":
        parameter_method = data["Preopt_" + str(i) + "_method_Input"]

        standardize = True
        if data["Preopt_" + str(i) + "_standardize_Input"] == "True":
            standardize = False

        copy = True
        if data["Preopt_" + str(i) + "_copy_Input"] == "False":
            copy = False

        pp = preprocessing.PowerTransformer(method=parameter_method,
                                               standardize=standardize,
                                               copy=copy)
        
        index_of_column = df.columns.get_loc(data["Preopt_" + str(i) + "_column_Input"])

        temp = pp.fit_transform(df[[data["Preopt_" + str(i) + "_column_Input"]]]).flatten()

        new_df.iloc[:,index_of_column] = pp.fit_transform(df[[data["Preopt_" + str(i) + "_column_Input"]]]).flatten()

    return new_df