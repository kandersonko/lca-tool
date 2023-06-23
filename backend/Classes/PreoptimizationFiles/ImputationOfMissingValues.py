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
list_IoMV = []

def getIoMV():
    return list_IoMV

# SimpleImputer
Name = "SimpleImputer"
Display_Name = "Simple Imputer"
Definition = ["Univariate imputer for completing missing values with simple strategies.\n\nReplace missing values using a descriptive statistic (e.g. mean, median, or most frequent) along each column, or using a constant value."]

Parameter_0 = {"Name":"missing_values", "Type": ["All_options"], "Default":0.0, "Possible":["int","float","str","np.nan",None,"np.nan"],
             "Definition":"The placeholder for the missing values. All occurrences of missing_values will be imputed. For pandas’ dataframes with nullable integer dtypes with missing values, missing_values can be set to either np.nan or pd.NA."}
Parameter_1 = {"Name":"strategy", "Type": ["option"], "Default":"mean", "Possible":["mean","median","most_frequent","constant"],
             "Definition":"The imputation strategy.\n\nIf “mean”, then replace missing values using the mean along each column. Can only be used with numeric data.\n\nIf “median”, then replace missing values using the median along each column. Can only be used with numeric data.\n\nIf “most_frequent”, then replace missing using the most frequent value along each column. Can be used with strings or numeric data. If there is more than one such value, only the smallest is returned.\n\nIf “constant”, then replace missing values with fill_value. Can be used with strings or numeric data."}
Parameter_2 = {"Name":"fill_value", "Type": ["str_or_null"], "Default":None, "Possible":["str","None"],
             "Definition":"When strategy == “constant”, fill_value is used to replace all occurrences of missing_values. For string or object data types, fill_value must be a string. If None, fill_value will be 0 when imputing numerical data and “missing_value” for strings or object data types."}
Parameter_3 = {"Name":"verbose", "Type": ["int"], "Default":0, "Possible":["int"],
             "Definition":"Controls the verbosity of the imputer."}
Parameter_4 = {"Name":"copy", "Type": ["bool"], "Default":True, "Possible":[True,False],
             "Definition":"If True, a copy of X will be created. If False, imputation will be done in-place whenever possible. Note that, in the following cases, a new copy will always be made, even if copy=False:\n\nIf X is not an array of floating values;\n\nIf X is encoded as a CSR matrix;\n\nIf add_indicator=True."}
Parameter_5 = {"Name":"add_indicator", "Type": ["bool"], "Default":False, "Possible":[True,False],
             "Definition":"If True, a MissingIndicator transform will stack onto output of the imputer’s transform. This allows a predictive estimator to account for missingness despite imputation. If a feature has no missing values at fit/train time, the feature won’t appear on the missing indicator even if there are missing values at transform/test time."}
Parameter_6 = {"Name":"keep_empty_features", "Type": ["bool"], "Default":False, "Possible":[True,False],
             "Definition":'If True, features that consist exclusively of missing values when fit is called are returned in results when transform is called. The imputed value is always 0 except when strategy="constant" in which case fill_value will be used instead.'}

Parameters = {"Parameter_0":Parameter_0, "Parameter_1":Parameter_1, "Parameter_2":Parameter_2, "Parameter_3":Parameter_3,
              "Parameter_4":Parameter_4, "Parameter_5":Parameter_5, "Parameter_6":Parameter_6}

list_IoMV.append(Preoptimizer.Preoptimizer(Name, Display_Name, Definition, Parameters))

# IterativeImputer
Name = "IterativeImputer"
Display_Name = "Iterative Imputer"
Definition = ["Multivariate imputer that estimates each feature from all the others.\n\nA strategy for imputing missing values by modeling each feature with missing values as a function of other features in a round-robin fashion."]

# only BayesianRidge is given, we do not allow user to create own function
#Parameter_0 = {"Name":"estimator", "Type": ["option"], "Default":"BayesianRidge", "Possible":["BayesianRidge"],
#             "Definition":"The estimator to use at each step of the round-robin imputation. If sample_posterior=True, the estimator must support return_std in its predict method."}
Parameter_0 = {"Name":"missing_values", "Type": ["int_or_null"], "Default":"np.nan", "Possible":["int","np.nan"],
             "Definition":"The placeholder for the missing values. All occurrences of missing_values will be imputed. For pandas’ dataframes with nullable integer dtypes with missing values, missing_values should be set to np.nan, since pd.NA will be converted to np.nan."}
Parameter_1 = {"Name":"sample_posterior", "Type": ["bool"], "Default":False, "Possible":[True,False],
             "Definition":"Whether to sample from the (Gaussian) predictive posterior of the fitted estimator for each imputation. Estimator must support return_std in its predict method if set to True. Set to True if using IterativeImputer for multiple imputations."}
Parameter_2 = {"Name":"max_iter", "Type": ["int"], "Default":10, "Possible":["int"],
             "Definition":"Maximum number of imputation rounds to perform before returning the imputations computed during the final round. A round is a single imputation of each feature with missing values. The stopping criterion is met once max(abs(X_t - X_{t-1}))/max(abs(X[known_vals])) < tol, where X_t is X at iteration t. Note that early stopping is only applied if sample_posterior=False."}
Parameter_3 = {"Name":"tol", "Type": ["float"], "Default":0.003, "Possible":["float"],
             "Definition":"Tolerance of the stopping condition."}
Parameter_4 = {"Name":"n_nearest_features", "Type": ["int_or_null"], "Default":None, "Possible":["int","None"],
             "Definition":"Number of other features to use to estimate the missing values of each feature column. Nearness between features is measured using the absolute correlation coefficient between each feature pair (after initial imputation). To ensure coverage of features throughout the imputation process, the neighbor features are not necessarily nearest, but are drawn with probability proportional to correlation for each imputed target feature. Can provide significant speed-up when the number of features is huge. If None, all features will be used."}
Parameter_5 = {"Name":"initial_strategy", "Type": ["option"], "Default":"mean", "Possible":["mean","median","most_frequent","constant"],
             "Definition":'Which strategy to use to initialize the missing values. Same as the strategy parameter in SimpleImputer.'}
Parameter_6 = {"Name":"imputation_order", "Type": ["option"], "Default":"ascending", "Possible":["ascending","descending","roman","arabic","random"],
             "Definition":"The order in which the features will be imputed. Possible values:\n\n'ascending': From features with fewest missing values to most.\n\n'descending': From features with most missing values to fewest.\n\n'roman': Left to right.\n\n'arabic': Right to left.\n\n'random': A random order for each round."}
Parameter_7 = {"Name":"skip_complete", "Type": ["bool"], "Default":True, "Possible":[True,False],
             "Definition":'If True then features with missing values during transform which did not have any missing values during fit will be imputed with the initial imputation method only. Set to True if you have many features with no missing values at both fit and transform time to save compute.'}
Parameter_8 = {"Name":"min_value", "Type": ["float_or_ninf"], "Default":"-np.inf", "Possible":["float","-np.inf"],
             "Definition":'Minimum possible imputed value. Broadcast to shape (n_features,) if scalar. If array-like, expects shape (n_features,), one min value for each feature. The default is -np.inf.'}
Parameter_9 = {"Name":"max_value", "Type": ["float_or_inf"], "Default":"np.inf", "Possible":["float","np.inf"],
             "Definition":'Maximum possible imputed value. Broadcast to shape (n_features,) if scalar. If array-like, expects shape (n_features,), one max value for each feature. The default is np.inf.'}
Parameter_10 = {"Name":"verbose", "Type": ["int"], "Default":0, "Possible":["int"],
             "Definition":'Verbosity flag, controls the debug messages that are issued as functions are evaluated. The higher, the more verbose. Can be 0, 1, or 2.'}
Parameter_11 = {"Name":"random_state", "Type": ["int_or_null"], "Default":None, "Possible":["int","None"],
             "Definition":'The seed of the pseudo random number generator to use. Randomizes selection of estimator features if n_nearest_features is not None, the imputation_order if random, and the sampling from posterior if sample_posterior=True. Use an integer for determinism.'}
Parameter_12 = {"Name":"add_indicator", "Type": ["bool"], "Default":False, "Possible":[True,False],
             "Definition":'If True, a MissingIndicator transform will stack onto output of the imputer’s transform. This allows a predictive estimator to account for missingness despite imputation. If a feature has no missing values at fit/train time, the feature won’t appear on the missing indicator even if there are missing values at transform/test time.'}
Parameter_13 = {"Name":"keep_empty_features", "Type": ["bool"], "Default":False, "Possible":[True,False],
             "Definition":'If True, features that consist exclusively of missing values when fit is called are returned in results when transform is called. The imputed value is always 0 except when initial_strategy="constant" in which case fill_value will be used instead.'}


Parameters = {"Parameter_0":Parameter_0, "Parameter_1":Parameter_1, "Parameter_2":Parameter_2, "Parameter_3":Parameter_3,
              "Parameter_4":Parameter_4, "Parameter_5":Parameter_5, "Parameter_6":Parameter_6, "Parameter_7":Parameter_7,
              "Parameter_8":Parameter_8, "Parameter_9":Parameter_9, "Parameter_10":Parameter_10, "Parameter_11":Parameter_11,
              "Parameter_12":Parameter_12, "Parameter_13":Parameter_13}

list_IoMV.append(Preoptimizer.Preoptimizer(Name, Display_Name, Definition, Parameters))

# KNNImputer
Name = "KNNImputer"
Display_Name = "K Nearest Neigbors (KNN) Imputer"
Definition = ["Imputation for completing missing values using k-Nearest Neighbors.\n\nEach sample’s missing values are imputed using the mean value from n_neighbors nearest neighbors found in the training set. Two samples are close if the features that neither is missing are close."]

Parameter_0 = {"Name":"missing_values", "Type": ["All_options"], "Default":0.0, "Possible":["int","float","str","np.nan",None,"np.nan"],
             "Definition":"The placeholder for the missing values. All occurrences of missing_values will be imputed. For pandas’ dataframes with nullable integer dtypes with missing values, missing_values can be set to either np.nan or pd.NA."}
Parameter_1 = {"Name":"n_neighbors", "Type": ["int"], "Default":5, "Possible":["int"],
             "Definition":"Number of neighboring samples to use for imputation."}
Parameter_2 = {"Name":"weights", "Type": ["option"], "Default":"uniform", "Possible":["uniform","distance"],
             "Definition":"Weight function used in prediction. Possible values:\n\n‘uniform’ : uniform weights. All points in each neighborhood are weighted equally.\n\n‘distance’ : weight points by the inverse of their distance. in this case, closer neighbors of a query point will have a greater influence than neighbors which are further away."}
# only nan_euclidean as we are not allowing user to create own function.
#Parameter_3 = {"Name":"metric", "Type": ["nan_euclidean"], "Default":0, "Possible":["int"],
#             "Definition":"Controls the verbosity of the imputer."}
Parameter_3 = {"Name":"copy", "Type": ["bool"], "Default":True, "Possible":[True,False],
             "Definition":"If True, a copy of X will be created. If False, imputation will be done in-place whenever possible. Note that, in the following cases, a new copy will always be made, even if copy=False:\n\nIf X is not an array of floating values;\n\nIf X is encoded as a CSR matrix;\n\nIf add_indicator=True."}
Parameter_4 = {"Name":"add_indicator", "Type": ["bool"], "Default":False, "Possible":[True,False],
             "Definition":"If True, a MissingIndicator transform will stack onto output of the imputer’s transform. This allows a predictive estimator to account for missingness despite imputation. If a feature has no missing values at fit/train time, the feature won’t appear on the missing indicator even if there are missing values at transform/test time."}
Parameter_5 = {"Name":"keep_empty_features", "Type": ["bool"], "Default":False, "Possible":[True,False],
             "Definition":'If True, features that consist exclusively of missing values when fit is called are returned in results when transform is called. The imputed value is always 0 except when strategy="constant" in which case fill_value will be used instead.'}

Parameters = {"Parameter_0":Parameter_0, "Parameter_1":Parameter_1, "Parameter_2":Parameter_2, "Parameter_3":Parameter_3,
              "Parameter_4":Parameter_4, "Parameter_5":Parameter_5}

list_IoMV.append(Preoptimizer.Preoptimizer(Name, Display_Name, Definition, Parameters))


# MissingIndicator
# Not implemented as of yet. 
# this only transforms a matrix to true, false values indicating if the values are missing.
# This would be useful to indicate which values to perform the other preoptimization on but should not be directly
# given to the user as a preoptimization option.
# I.E. give user an option to state the missing value indicator (-1, nan, 0 or null) and then use MissingIndicator
# to get a matix of those missing values and then use preoptimization.