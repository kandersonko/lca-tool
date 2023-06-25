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
list_GPF = []

def getGPF():
    return list_GPF

# PolynomialFeatures
Name = "PolynomialFeatures"
Display_Name = "Polynomial Features"
Definition = ["Generate polynomial and interaction features.\n\nGenerate a new feature matrix consisting of all polynomial combinations of the features with degree less than or equal to the specified degree. For example, if an input sample is two dimensional and of the form [a, b], the degree-2 polynomial features are [1, a, b, a^2, ab, b^2]."]

Parameter_0 =  {"Name":"min_degree", "Type": ["int"], "Default":0, "Possible":["int"], 
               "Definition":"The minimum polynomial degree of the generated features.\n\nNote that min_degree=0 and min_degree=1 are equivalent as outputting the degree zero term is determined by include_bias."}
Parameter_1 =  {"Name":"max_degree", "Type": ["int"], "Default":2, "Possible":["int"], 
               "Definition":"The maximum polynomial degree of the generated features."}
Parameter_2 =  {"Name":"interaction_only", "Type": ["bool"], "Default":False, "Possible":[True, False], 
               "Definition":"If True, only interaction features are produced: features that are products of at most degree distinct input features, i.e. terms with power of 2 or higher of the same input feature are excluded:\n\nincluded: x[0], x[1], x[0] * x[1], etc.\n\nexcluded: x[0] ** 2, x[0] ** 2 * x[1], etc."}
Parameter_3 =  {"Name":"include_bias", "Type": ["bool"], "Default":True, "Possible":[True, False], 
               "Definition":"If True (default), then include a bias column, the feature in which all polynomial powers are zero (i.e. a column of ones - acts as an intercept term in a linear model)."}
Parameter_4 =  {"Name":"order", "Type": ["option"], "Default":"C", "Possible":["C","F"], 
               "Definition":"Order of output array in the dense case. 'F' order is faster to compute, but may slow down subsequent estimators."}

Parameters = {"Parameter_0":Parameter_0, "Parameter_1":Parameter_1,"Parameter_2":Parameter_2, "Parameter_3":Parameter_3,
              "Parameter_4":Parameter_4}

list_GPF.append(Preoptimizer.Preoptimizer(Name, Display_Name, Definition, Parameters))

# SplineTransformer
Name = "SplineTransformer"
Display_Name = "Spline Transformer"
Definition = ['Generate univariate B-spline bases for features.\n\nGenerate a new feature matrix consisting of n_splines=n_knots + degree - 1 (n_knots - 1 for extrapolation="periodic") spline basis functions (B-splines) of polynomial order=`degree` for each feature.']

Parameter_0 =  {"Name":"n_knots", "Type": ["int"], "Default":5, "Possible":["int"], 
               "Definition":"Number of knots of the splines if knots equals one of {‘uniform’, ‘quantile’}. Must be larger or equal 2. Ignored if knots is array-like."}
Parameter_1 =  {"Name":"degree", "Type": ["int"], "Default":3, "Possible":["int"], 
               "Definition":"The polynomial degree of the spline basis. Must be a non-negative integer."}
Parameter_2 =  {"Name":"knots", "Type": ["option"], "Default":"uniform", "Possible":["uniform","quantile"], 
               "Definition":"Set knot positions such that first knot <= features <= last knot.\n\nIf ‘uniform’, n_knots number of knots are distributed uniformly from min to max values of the features.\n\nIf ‘quantile’, they are distributed uniformly along the quantiles of the features."}
Parameter_3 =  {"Name":"extrapolation", "Type": ["option"], "Default":"constant", "Possible":["error","constant","linear","continue","periodic"], 
               "Definition":"If ‘error’, values outside the min and max values of the training features raises a ValueError. If ‘constant’, the value of the splines at minimum and maximum value of the features is used as constant extrapolation. If ‘linear’, a linear extrapolation is used. If ‘continue’, the splines are extrapolated as is, i.e. option extrapolate=True in scipy.interpolate.BSpline. If ‘periodic’, periodic splines with a periodicity equal to the distance between the first and last knot are used. Periodic splines enforce equal function values and derivatives at the first and last knot. For example, this makes it possible to avoid introducing an arbitrary jump between Dec 31st and Jan 1st in spline features derived from a naturally periodic “day-of-year” input feature. In this case it is recommended to manually set the knot values to control the period."}
Parameter_4 =  {"Name":"include_bias", "Type": ["bool"], "Default":True, "Possible":[True,False], 
               "Definition":"If True (default), then the last spline element inside the data range of a feature is dropped. As B-splines sum to one over the spline basis functions for each data point, they implicitly include a bias term, i.e. a column of ones. It acts as an intercept term in a linear models."}
Parameter_5 =  {"Name":"order", "Type": ["option"], "Default":"C", "Possible":["C","F"], 
               "Definition":"Order of output array in the dense case. 'F' order is faster to compute, but may slow down subsequent estimators."}

Parameters = {"Parameter_0":Parameter_0, "Parameter_1":Parameter_1,"Parameter_2":Parameter_2, "Parameter_3":Parameter_3,
              "Parameter_4":Parameter_4, "Parameter_5":Parameter_5}

list_GPF.append(Preoptimizer.Preoptimizer(Name, Display_Name, Definition, Parameters))

def perform_Preopt(data, i, df):
    # get method
    method = data["Preopt_" + str(i)]

    new_df = df.copy()

    # PolynomialFeatures
    if method == "PolynomialFeatures":
        min_degree = int(data["Preopt_" + str(i) + "_min_degree_Input"])
        max_degree = int(data["Preopt_" + str(i) + "_max_degree_Input"])

        degree = (min_degree,max_degree)

        interaction_only = False
        if data["Preopt_" + str(i) + "_interaction_only_Input"] == "True":
            interaction_only = True

        include_bias = True
        if data["Preopt_" + str(i) + "_include_bias_Input"] == "False":
            include_bias = False

        order = data["Preopt_" + str(i) + "_order_Input"]
        
        enc = preprocessing.PolynomialFeatures(degree=degree,
                                                interaction_only=interaction_only,
                                                include_bias=include_bias,
                                                order=order)

        new_df[data["Preopt_" + str(i) + "_column_Input"]] = enc.fit_transform(df[[data["Preopt_" + str(i) + "_column_Input"]]])


    # SplineTransformer
    if method == "SplineTransformer":
        n_knots = int(data["Preopt_" + str(i) + "_n_knots_Input"])
        degree = int(data["Preopt_" + str(i) + "_degree_Input"])

        knots = data["Preopt_" + str(i) + "_knots_Input"]
        extrapolation = data["Preopt_" + str(i) + "_extrapolation_Input"]

        include_bias = True
        if data["Preopt_" + str(i) + "_include_bias_Input"] == "False":
            include_bias = False

        order = data["Preopt_" + str(i) + "_order_Input"]

        enc = preprocessing.SplineTransformer(n_knots=n_knots,
                                              degree=degree,
                                              knots=knots,
                                              extrapolation=extrapolation,
                                              include_bias=include_bias,
                                              order=order)

        new_df[data["Preopt_" + str(i) + "_column_Input"]] = enc.fit_transform(df[[data["Preopt_" + str(i) + "_column_Input"]]])

    return new_df