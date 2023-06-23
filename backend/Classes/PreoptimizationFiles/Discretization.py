import os
import sys
import io
import base64

import pandas as pd
import numpy as np

from backend.Classes.PreoptimizationFiles import Preoptimizer

import matplotlib.pyplot as plt

from sklearn import preprocessing
from sklearn.neural_network import BernoulliRBM

# Create a list of standardization preoptimizations to select from.
list_Discretization = []

def getDiscretization():
    return list_Discretization

# KBinsDiscretizer
Name = "KBinsDiscretizer"
Display_Name = "K-Bins Discretizer"
Definition = ["Bin continuous data into intervals."]
Parameter_0 =  {"Name":"n_bins", "Type": ["int"], "Default":5, "Possible":["int"], 
               "Definition":"The number of bins to produce. Raises ValueError if n_bins < 2."}
Parameter_1 =  {"Name":"encode", "Type": ["option"], "Default":"onehot", "Possible":["onehot", "onehot-dense","ordinal"], 
               "Definition":"Method used to encode the transformed result.\n\n‘onehot’: Encode the transformed result with one-hot encoding and return a sparse matrix. Ignored features are always stacked to the right.\n\n‘onehot-dense’: Encode the transformed result with one-hot encoding and return a dense array. Ignored features are always stacked to the right.\n\n‘ordinal’: Return the bin identifier encoded as an integer value."}
Parameter_2 =  {"Name":"strategy", "Type": ["option"], "Default":"quantile", "Possible":["uniform", "quantile", "kmeans"], 
               "Definition":"Strategy used to define the widths of the bins.\n\n‘uniform’: All bins in each feature have identical widths.\n\n‘quantile’: All bins in each feature have the same number of points.\n\n‘kmeans’: Values in each bin have the same nearest center of a 1D k-means cluster."}
Parameter_3 =  {"Name":"dtype", "Type": ["option"], "Default":None, "Possible":["None", "np.float32","np.float64"], 
               "Definition":"The desired data-type for the output. If None, output dtype is consistent with input dtype. Only np.float32 and np.float64 are supported."}
Parameter_4 =  {"Name":"subsample", "Type": ["int_or_null"], "Default":None, "Possible":["int", "None"], 
               "Definition":"Maximum number of samples, used to fit the model, for computational efficiency. Used when strategy='quantile'. subsample=None means that all the training samples are used when computing the quantiles that determine the binning thresholds. Since quantile computation relies on sorting each column of X and that sorting has an n log(n) time complexity, it is recommended to use subsampling on datasets with a very large number of samples."}
Parameter_5 =  {"Name":"random_state", "Type": ["int_or_null"], "Default":None, "Possible":["int", "None"], 
               "Definition":"Determines random number generation for subsampling. Pass an int for reproducible results across multiple function calls. See the subsample parameter for more details."}
Parameter_6 = {"Name":"column", "Type": ["select"], "Default":"", "Possible":["col_names"],
               "Definition":"Column to perform the preoptimization on."}

Parameters = {"Parameter_0":Parameter_0,"Parameter_1":Parameter_1,"Parameter_2":Parameter_2,"Parameter_3":Parameter_3,
              "Parameter_4":Parameter_4,"Parameter_5":Parameter_5,"Parameter_6":Parameter_6}

list_Discretization.append(Preoptimizer.Preoptimizer(Name, Display_Name, Definition, Parameters))


# Binarizer
Name = "Binarizer"
Display_Name = "Binarizer"
Definition = ["Binarize data (set feature values to 0 or 1) according to a threshold.\n\nValues greater than the threshold map to 1, while values less than or equal to the threshold map to 0. With the default threshold of 0, only positive values map to 1.\n\nBinarization is a common operation on text count data where the analyst can decide to only consider the presence or absence of a feature rather than a quantified number of occurrences for instance.\n\nIt can also be used as a pre-processing step for estimators that consider boolean random variables (e.g. modelled using the Bernoulli distribution in a Bayesian setting)."]
Parameter_0 =  {"Name":"threshold", "Type": ["float"], "Default":0.0, "Possible":["float"], 
               "Definition":"Feature values below or equal to this are replaced by 0, above it by 1. Threshold may not be less than 0 for operations on sparse matrices."}
Parameter_1 =  {"Name":"copy", "Type": ["bool"], "Default":True, "Possible":[True,False], 
               "Definition":"Set to False to perform inplace binarization and avoid a copy (if the input is already a numpy array or a scipy.sparse CSR matrix)."}
Parameter_2 = {"Name":"column", "Type": ["select"], "Default":"", "Possible":["col_names"],
               "Definition":"Column to perform the preoptimization on."}

Parameters = {"Parameter_0":Parameter_0,"Parameter_1":Parameter_1,"Parameter_2":Parameter_2}

list_Discretization.append(Preoptimizer.Preoptimizer(Name, Display_Name, Definition, Parameters))


# FunctionTransformer
## Left out as allowing user to either create or select from a created list of functions for transforming X and y would cause large amount of work and checks.

def perform_Preopt(data, i, df):
    # get method
    method = data["Preopt_" + str(i)]

    new_df = df.copy()

    # KBinsDiscretizer
    if method == "KBinsDiscretizer":
        n_bins = int(data["Preopt_" + str(i) + "_n_bins_Input"]) 

        encode = data["Preopt_" + str(i) + "_encode_Input"] 

        strategy = data["Preopt_" + str(i) + "_strategy_Input"] 

        dtype = None
        if data["Preopt_" + str(i) + "_strategy_Input"] == "np.float32":
            dtype = np.float32
        if data["Preopt_" + str(i) + "_strategy_Input"] == "np.float64":
            dtype = np.float64

        subsample == None
        if data["Preopt_" + str(i) + "_subsample_Input"] != "None" and data["Preopt_" + str(i) + "_subsample_Input"] != "":
            subsample = int(data["Preopt_" + str(i) + "_subsample_Input"])

        random_state == None
        if data["Preopt_" + str(i) + "_random_state_Input"] != "None" and data["Preopt_" + str(i) + "_random_state_Input"] != "":
            random_state = int(data["Preopt_" + str(i) + "_random_state_Input"])

        enc = preprocessing.KBinsDiscretizer(n_bins=n_bins,
                                             encode=encode,
                                             strategy=strategy,
                                             dtype=dtype,
                                             subsample=subsample,
                                             random_state=random_state)

        new_df[data["Preopt_" + str(i) + "_column_Input"]] = enc.fit_transform(df[[data["Preopt_" + str(i) + "_column_Input"]]])

    # Binarizer
    if method == "Binarizer":
        threshold = float(data["Preopt_" + str(i) + "_threshold_Input"])

        copy = True
        if data["Preopt_" + str(i) + "_copy_Input"] == "False":
            copy = False

        enc = preprocessing.Binarizer(threshold=threshold,
                                             copy=copy)

        new_df[data["Preopt_" + str(i) + "_column_Input"]] = enc.fit_transform(df[[data["Preopt_" + str(i) + "_column_Input"]]])

    return new_df