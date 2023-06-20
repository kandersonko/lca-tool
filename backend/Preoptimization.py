import os
import sys
import io
import base64

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt


class Preoptimization:
    def __init__(self, name, definition, parameters):
        self.name = name
        self.definition = definition
        self.parameters = parameters
    
    def getName(self):
        return self.name

    def getDefinition(self):
        return self.definition

    def getParameters(self):
        return self.parameters

list_Preopts = []

def getPreopts():
    return list_Preopts

# Information of the Preoptimization options.
## Category Encoders:
### OrdinalEncoder
Name = "OrdinalEncoder"
Definition = ["Encode categorical features as an integer array.\n\nThe input to this transformer should be an array-like of integers or strings, denoting the values taken on by categorical (discrete) features. The features are converted to ordinal integers. This results in a single column of integers (0 to n_categories - 1) per feature."]
Parameter_0 =  {"Name":"categories", "Type": ["option"], "Default":"auto", "Possible":["auto", "columns"], 
               "Definition":"Categories (unique values) per feature:\n\n‘auto’ : Determine categories automatically from the training data.\n\nlist : categories[i] holds the categories expected in the ith column. The passed categories should not mix strings and numeric values, and should be sorted in case of numeric values."}
Parameter_1 =  {"Name":"dtype", "Type": ["dtype_number"], "Default":np.float64, "Possible":["np.int32", "np.float64"], 
               "Definition":"Desired dtype of output."}
Parameter_2 =  {"Name":"handle_unknown", "Type": ["option"], "Default":"error", "Possible":["error", "use_encoded_value"], 
               "Definition":"When set to ‘error’ an error will be raised in case an unknown categorical feature is present during transform. When set to ‘use_encoded_value’, the encoded value of unknown categories will be set to the value given for the parameter unknown_value. In inverse_transform, an unknown category will be denoted as None."}
Parameter_3 =  {"Name":"handle_value", "Type": ["option"], "Default":"error", "Possible":["error", "use_encoded_value"], 
               "Definition":"When the parameter handle_unknown is set to ‘use_encoded_value’, this parameter is required and will set the encoded value of unknown categories. It has to be distinct from the values used to encode any of the categories in fit. If set to np.nan, the dtype parameter must be a float dtype."}
Parameter_4 =  {"Name":"encoded_missing_calue", "Type": ["int_or_npnan"], "Default":np.nan, "Possible":["int", "np.nan"], 
               "Definition":"Encoded value of missing categories. If set to np.nan, then the dtype parameter must be a float dtype."}

Parameters = {"Parameter_0":Parameter_0, "Parameter_1":Parameter_1,"Parameter_2":Parameter_2,"Parameter_3":Parameter_3,
             "Parameter_4":Parameter_4}

list_Preopts.append(Preoptimization(Name, Definition, Parameters))

## Feature Scaling:
Name = "StandardScaler"
Definition = ["Standardize features by removing the mean and scaling to unit variance.\n\nThe standard score of a sample x is calculated as:\n\nz = (x - u) / s\n\nwhere u is the mean of the training samples or zero if with_mean=False, and s is the standard deviation of the training samples or one if with_std=False.\n\nCentering and scaling happen independently on each feature by computing the relevant statistics on the samples in the training set. Mean and standard deviation are then stored to be used on later data using transform.\n\nStandardization of a dataset is a common requirement for many machine learning estimators: they might behave badly if the individual features do not more or less look like standard normally distributed data (e.g. Gaussian with 0 mean and unit variance).\n\nFor instance many elements used in the objective function of a learning algorithm (such as the RBF kernel of Support Vector Machines or the L1 and L2 regularizers of linear models) assume that all features are centered around 0 and have variance in the same order. If a feature has a variance that is orders of magnitude larger than others, it might dominate the objective function and make the estimator unable to learn from other features correctly as expected.\n\nThis scaler can also be applied to sparse CSR or CSC matrices by passing with_mean=False to avoid breaking the sparsity structure of the data."]
Parameter_0 =  {"Name":"copy", "Type": ["bool"], "Default":True, "Possible":[True, False], 
               "Definition":"If False, try to avoid a copy and do inplace scaling instead. This is not guaranteed to always work inplace; e.g. if the data is not a NumPy array or scipy.sparse CSR matrix, a copy may still be returned."}
Parameter_1 =  {"Name":"with_mean", "Type": ["bool"], "Default":True, "Possible":[True, False], 
               "Definition":"If True, center the data before scaling. This does not work (and will raise an exception) when attempted on sparse matrices, because centering them entails building a dense matrix which in common use cases is likely to be too large to fit in memory."}
Parameter_2 =  {"Name":"with_std", "Type": ["bool"], "Default":True, "Possible":[True, False], 
               "Definition":"If True, scale the data to unit variance (or equivalently, unit standard deviation)."}

Parameters = {"Parameter_0":Parameter_0, "Parameter_1":Parameter_1,"Parameter_2":Parameter_2,"Parameter_3":Parameter_3,
             "Parameter_4":Parameter_4}

list_Preopts.append(Preoptimization(Name, Definition, Parameters))

## Label Encoding:
Name = "LabelEncoder"
Definition = ["Encode target labels with value between 0 and n_classes-1.\n\nThis transformer should be used to encode target values, i.e. y, and not the input X."]

Parameters = {}

list_Preopts.append(Preoptimization(Name, Definition, Parameters))

## Dummy Variables:
Nme = "DummyVariables"
Definition = ["converts string entires for numeric representation for each columns."]

Parameters = {}

list_Preopts.append(Preoptimization(Name, Definition, Parameters))

## Drop Columns:
Name = "RemoveColumns"
Definition = ["Remove the range of columns from the dataset."]
Parameter = {"Name":"columns", "Type": ["list_ints"], "Default":None, "Possible":["int"],
             "Definition":"The index number of the columns to remove.\n\nCan be given as a range (0-10) or separate integer ids (0,1,2,3,4,5,6,7,8,9)"}

Parameters = {}

list_Preopts.append(Preoptimization(Name, Definition, Parameters))

## Drop Rows:
Name = "RemoveRows"
Definition = ["Remove the range of rows from the dataset."]
Parameter = {"Name":"rows", "Type": ["list_ints"], "Default":None, "Possible":["int"],
             "Definition":"The index number of the rows to remove.\n\nCan be given as a range (0-10) or separate integer ids (0,1,2,3,4,5,6,7,8,9)"}

Parameters = {}

list_Preopts.append(Preoptimization(Name, Definition, Parameters))

## Drop null values Removal:
Nme = "DropNullValueRows"
Definition = ["Removes the rows that contain null value entires in any of the columns."]

Parameters = {}

list_Preopts.append(Preoptimization(Name, Definition, Parameters))

## Outlier Removal:

## PCA: Principal Component Analysis

# Other Methods

# Method to pull all parameters from a given method
def getParameters(algorithm_Name):
    Parameters = {}
    for algorithm in list_MLAs:
        if algorithm.getName() == algorithm_Name:
            Parameters = algorithm.getParameters()
    return Parameters

# get settings to fill the model parameters.
def getSettings(data, Parameters):
    settings = {}
    settings["Parameter_Length"] = len(Parameters)

    # Cycle through parameters
    for i in range(len(Parameters)):
        temp = Parameters["Parameter_" + str(i)]["Name"]+"_checked"

        # get name
        settings["Parameter_" + str(i) + "_Name"] = Parameters["Parameter_" + str(i)]["Name"]

        # get default
        if data[Parameters["Parameter_" + str(i)]["Name"]+"_checked"] == "false":
            settings["Parameter_" + str(i)] = Parameters["Parameter_" + str(i)]["Default"]
            # convert to acceptable type
            settings["Parameter_" + str(i)] = convertToType(settings["Parameter_" + str(i)], Parameters["Parameter_" + str(i)]["Type"])

        elif data[Parameters["Parameter_" + str(i)]["Name"]+"_checked"] == "true":
            temp = Parameters["Parameter_" + str(i)]["Type"]
            if Parameters["Parameter_" + str(i)]["Type"][0] == "option_float":
                settings["Parameter_" + str(i)] = data[Parameters["Parameter_" + str(i)]["Name"] + "_Input"]
                settings["Parameter_" + str(i)] = convertToType(settings["Parameter_" + str(i)], Parameters["Parameter_" + str(i)]["Type"], data[Parameters["Parameter_" + str(i)]["Name"] + "_Float_Input"])
            else:
                settings["Parameter_" + str(i)] = data[Parameters["Parameter_" + str(i)]["Name"] + "_Input"]
                settings["Parameter_" + str(i)] = convertToType(settings["Parameter_" + str(i)], Parameters["Parameter_" + str(i)]["Type"])

    return settings


def convertToType(value, Type, additionalNumber = 0):
    if Type[0] == "int":
        return int(value)
    elif Type[0] == "float":
        return float(value)
    elif Type[0] == "bool":
        if value == "true" or value == True:
            return True
        elif value == "false" or value == False:
            return False
    elif Type[0] == "int_or_null":
        if value == "null" or value == "None" or value == "":
            return None
        elif value != None:
            return int(value)
        else:
            return value
    elif Type[0] == "float_or_null":
        if value == "null" or value == "None" or value == "":
            return None
        elif value != None:
            return float(value)
        else:
            return value
    elif Type[0] == "option":
        if value == "null" or value == "None" or value == "":
            return None
        else:
            return value
    elif Type[0] == "option_float":
        if value == "null" or value == "None" or value == "":
            return None
        else:
            if value == "float":
                return float(additionalNumber)
            else:
                return value
    else:
        return value

# Method to process the proptimization options.


def getDataset(fileName):
     # convert csv to usable dataset
    ## Manual location currently...Will be changed when implemented in Host.
    ## Should further be changed when database is setup.

    ManualLoc = "/backend/tests/sampleCSV_MLA_Classification/"

    dataset = pd.read_csv(ManualLoc + fileName)

    return dataset

def getCSV_PDF(data):
    # convert csv to usable dataset
    df = getDataset(data['csvFileName'])

    dataframe = df.to_html()

    null_count = df.isnull().sum().rename_axis('Column').reset_index(name='Number of Null Instances')
    null_count = null_count.to_html()

    number_classes = ""

    if data["class_col"] != None and data["class_col"] != "": 
        number_classes = df[df.columns[int(data["class_col"])]].value_counts().rename_axis('Unique Values').reset_index(name='counts')
        number_classes = number_classes.to_html()
    
    kde_base64 = []
    if data["kde_ind"] != None and data["kde_ind"] != "": 
        if data["class_col"] != None and data["class_col"] != "": 
            classes = df[df.columns[int(data["class_col"])]].unique()

            X = df.loc[:, df.columns != df.columns[int(data["class_col"])]].values.astype('float64')
            Y = df[df.columns[int(data["class_col"])]].values

            for class_name in classes:
                temp = X[Y == class_name]
                pd.DataFrame(X[Y == class_name]).plot.kde(ind=int(data["kde_ind"]), legend=True)
                plt.legend(loc='best', title='Column')
                title = 'Likelihood KDE Plots for the ' + str(class_name) + ' Class'
                plt.title(title);

                plt.plot()
                my_stringIObytes = io.BytesIO()
                plt.savefig(my_stringIObytes, format='jpg')
                my_stringIObytes.seek(0)
                my_base64_jpgData = base64.b64encode(my_stringIObytes.read()).decode()

                kde_base64.append(my_base64_jpgData)

    PDF = { "csv_Short": dataframe,
            "null_Count": null_count,
            "Number_Classes": number_classes,
            "kde_plots": kde_base64}
    
    return PDF
