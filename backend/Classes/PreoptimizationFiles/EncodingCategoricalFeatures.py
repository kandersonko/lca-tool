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
list_ECF = []

def getECF():
    return list_ECF

# OrdinalEncoder
Name = "OrdinalEncoder"
Display_Name = "Ordinal Encoder"
Definition = ["Encode categorical features as an integer array.\n\nThe input to this transformer should be an array-like of integers or strings, denoting the values taken on by categorical (discrete) features. The features are converted to ordinal integers. This results in a single column of integers (0 to n_categories - 1) per feature."]
## This should only be added if 2-d array is given, however since we are allowing user to perform operation on one column only. We give it the possible values later.
#Parameter_0 =  {"Name":"categories", "Type": ["option"], "Default":"auto", "Possible":["auto", "columns"], 
#               "Definition":"Categories (unique values) per feature:\n\n‘auto’ : Determine categories automatically from the training data.\n\nlist : categories[i] holds the categories expected in the ith column. The passed categories should not mix strings and numeric values, and should be sorted in case of numeric values."}
Parameter_0 =  {"Name":"dtype", "Type": ["option"], "Default":np.float64, "Possible":["np.int32", "np.float64"], 
               "Definition":"Desired dtype of output."}
Parameter_1 =  {"Name":"handle_unknown", "Type": ["option"], "Default":"error", "Possible":["error", "use_encoded_value"], 
               "Definition":"When set to ‘error’ an error will be raised in case an unknown categorical feature is present during transform. When set to ‘use_encoded_value’, the encoded value of unknown categories will be set to the value given for the parameter unknown_value. In inverse_transform, an unknown category will be denoted as None."}
Parameter_2 =  {"Name":"unknown_value", "Type": ["option"], "Default":None, "Possible":["int", "np.nan", "None"], 
               "Definition":"When the parameter handle_unknown is set to ‘use_encoded_value’, this parameter is required and will set the encoded value of unknown categories. It has to be distinct from the values used to encode any of the categories in fit. If set to np.nan, the dtype parameter must be a float dtype."}
Parameter_3 =  {"Name":"encoded_missing_value", "Type": ["option_int"], "Default":"np.nan", "Possible":["int", "np.nan"], 
               "Definition":"Encoded value of missing categories. If set to np.nan, then the dtype parameter must be a float dtype."}
Parameter_4 = {"Name":"column", "Type": ["select"], "Default":"", "Possible":["col_names"],
               "Definition":"Column to perform the preoptimization on."}

Parameters = {"Parameter_0":Parameter_0, "Parameter_1":Parameter_1,"Parameter_2":Parameter_2,"Parameter_3":Parameter_3,
              "Parameter_4":Parameter_4}

list_ECF.append(Preoptimizer.Preoptimizer(Name, Display_Name, Definition, Parameters))

# OneHotEncoder
Name = "OneHotEncoder"
Display_Name = "One Hot Encoder"
Definition = ["Encode categorical features as a one-hot numeric array.\n\nThe input to this transformer should be an array-like of integers or strings, denoting the values taken on by categorical (discrete) features. The features are encoded using a one-hot (aka ‘one-of-K’ or ‘dummy’) encoding scheme. This creates a binary column for each category and returns a sparse matrix or dense array (depending on the sparse_output parameter)\n\nBy default, the encoder derives the categories based on the unique values in each feature. Alternatively, you can also specify the categories manually.\n\nThis encoding is needed for feeding categorical data to many scikit-learn estimators, notably linear models and SVMs with the standard kernels."]

## This should only be added if 2-d array is given, however since we are allowing user to perform operation on one column only. We give it the possible values later.
#Parameter_0 =  {"Name":"categories", "Type": ["option"], "Default":"auto", "Possible":["auto", "columns"], 
#               "Definition":"Categories (unique values) per feature:\n\n‘auto’ : Determine categories automatically from the training data.\n\nlist : categories[i] holds the categories expected in the ith column. The passed categories should not mix strings and numeric values, and should be sorted in case of numeric values."}
Parameter_0 =  {"Name":"drop", "Type": ["option"], "Default":None, "Possible":["first","if_binary","None"], 
               "Definition":"Specifies a methodology to use to drop one of the categories per feature. This is useful in situations where perfectly collinear features cause problems, such as when feeding the resulting data into an unregularized linear regression model.\n\nHowever, dropping one category breaks the symmetry of the original representation and can therefore induce a bias in downstream models, for instance for penalized linear classification or regression models.\n\nNone : retain all features (the default).\n\n‘first’ : drop the first category in each feature. If only one category is present, the feature will be dropped entirely.\n\n‘if_binary’ : drop the first category in each feature with two categories. Features with 1 or more than 2 categories are left intact.\n\nWhen max_categories or min_frequency is configured to group infrequent categories, the dropping behavior is handled after the grouping."}
Parameter_1 =  {"Name":"sparse", "Type": ["bool"], "Default":True, "Possible":[True, False], 
               "Definition":"Will return sparse matrix if set True else will return an array."}
Parameter_2 =  {"Name":"sparse_output", "Type": ["bool"], "Default":True, "Possible":[True,False], 
               "Definition":"Will return sparse matrix if set True else will return an array."}
Parameter_3 =  {"Name":"dtype", "Type": ["option"], "Default":float, "Possible":["bool","int", "float"], 
               "Definition":"Desired dtype of output."}
Parameter_4 =  {"Name":"handle_unknown", "Type": ["option"], "Default":"error", "Possible":["error", "ignore", "infrequent_if_exist"], 
               "Definition":"Specifies the way unknown categories are handled during transform.\n\n‘error’ : Raise an error if an unknown category is present during transform.\n\n‘ignore’ : When an unknown category is encountered during transform, the resulting one-hot encoded columns for this feature will be all zeros. In the inverse transform, an unknown category will be denoted as None.\n\n‘infrequent_if_exist’ : When an unknown category is encountered during transform, the resulting one-hot encoded columns for this feature will map to the infrequent category if it exists. The infrequent category will be mapped to the last position in the encoding. During inverse transform, an unknown category will be mapped to the category denoted 'infrequent' if it exists. If the 'infrequent' category does not exist, then transform and inverse_transform will handle an unknown category as with handle_unknown='ignore'. Infrequent categories exist based on min_frequency and max_categories. Read more in the User Guide."}
Parameter_5 =  {"Name":"min_frequency", "Type": ["int_or_float_or_null"], "Default":None, "Possible":["int", "float", "None"], 
               "Definition":"Specifies the minimum frequency below which a category will be considered infrequent.\n\nIf int, categories with a smaller cardinality will be considered infrequent.\n\nIf float, categories with a smaller cardinality than min_frequency * n_samples will be considered infrequent."}
Parameter_6 =  {"Name":"max_categories", "Type": ["int_or_null"], "Default":None, "Possible":["int", "None"], 
               "Definition":"Specifies an upper limit to the number of output features for each input feature when considering infrequent categories. If there are infrequent categories, max_categories includes the category representing the infrequent categories along with the frequent categories. If None, there is no limit to the number of output features."}
Parameter_7 = {"Name":"column", "Type": ["select"], "Default":"", "Possible":["col_names"],
               "Definition":"Column to perform the preoptimization on."}

Parameters = {"Parameter_0":Parameter_0, "Parameter_1":Parameter_1,"Parameter_2":Parameter_2,"Parameter_3":Parameter_3,
              "Parameter_4":Parameter_4, "Parameter_5":Parameter_5,"Parameter_6":Parameter_6,"Parameter_7":Parameter_7}

list_ECF.append(Preoptimizer.Preoptimizer(Name, Display_Name, Definition, Parameters))

## Label Encoding:
Name = "LabelEncoder"
Display_Name = "Label Encoder"
Definition = ["Encode target labels with value between 0 and n_classes-1.\n\nThis transformer should be used to encode target values, i.e. y, and not the input X."]

Parameters = {}

list_ECF.append(Preoptimizer.Preoptimizer(Name, Display_Name, Definition, Parameters))

## Dummy Variables:
Name = "DummyVariables"
Display_Name = "Dummy Variables"
Definition = ["converts string entires for numeric representation for each columns."]
Parameter_0 =  {"Name":"prefix", "Type": ["str"], "Default":None, "Possible":["str"], 
               "Definition":"String to append DataFrame column names. Pass a list with length equal to the number of columns when calling get_dummies on a DataFrame. Alternatively, prefix can be a dictionary mapping column names to prefixes."}
Parameter_1 =  {"Name":"prefix_sep", "Type": ["str"], "Default":"_", "Possible":["str"], 
               "Definition":"If appending prefix, separator/delimiter to use. Or pass a list or dictionary as with prefix."}
Parameter_2 =  {"Name":"dummy_na", "Type": ["bool"], "Default":False, "Possible":[True,False], 
               "Definition":"Add a column to indicate NaNs, if False NaNs are ignored."}
Parameter_3 =  {"Name":"dtype", "Type": ["option"], "Default":"bool", "Possible":["bool","float","int"], 
               "Definition":"Data type for new columns. Only a single dtype is allowed."}
Parameter_4 = {"Name":"column", "Type": ["select"], "Default":"", "Possible":["col_names"],
               "Definition":"Column to perform the preoptimization on."}

Parameters = {"Parameter_0":Parameter_0, "Parameter_1":Parameter_1,"Parameter_2":Parameter_2,"Parameter_3":Parameter_3,"Parameter_4":Parameter_4}

list_ECF.append(Preoptimizer.Preoptimizer(Name, Display_Name, Definition, Parameters))

# Method to check the chosen preoptimization method and perform it on the dataset.
def perform_Preopt(data, i, df):
    # get method
    method = data["Preopt_" + str(i)]

    new_df = df.copy()

    # OrdinalEncoder
    if method == "OrdinalEncoder":
        dtype = data["Preopt_" + str(i) + "_dtype_Input"]

        enc_miss_value = "";
        if data["Preopt_" + str(i) + "_encoded_missing_value_Input"] == "np.nan":
            enc_miss_value = np.nan
        else:
            enc_miss_value = int(data["Preopt_" + str(i) + "_encoded_missing_value_Input"])

        unknown_Value = "";
        if data["Preopt_" + str(i) + "_unknown_value_Input"] == "np.nan":
            unknown_Value = np.nan
        elif data["Preopt_" + str(i) + "_unknown_value_Input"] == "None":
            unknown_Value = None
        else:
            unknown_Value = int(data["Preopt_" + str(i) + "_unknown_value_Input"])

        enc = preprocessing.OrdinalEncoder(categories=[df[data["Preopt_" + str(i) + "_column_Input"]].unique().tolist()],
                             dtype=dtype,
                             handle_unknown=data["Preopt_" + str(i) + "_handle_unknown_Input"],
                             unknown_value=unknown_Value,
                             encoded_missing_value=enc_miss_value)

        new_df[data["Preopt_" + str(i) + "_column_Input"]] = enc.fit_transform(df[[data["Preopt_" + str(i) + "_column_Input"]]])
    
    # OneHotEncoder
    if method == "OneHotEncoder":
        drop = None
        if drop != "None" and drop != "":
            drop = data["Preopt_" + str(i) + "_None_Input"]

        sparse = True
        if data["Preopt_" + str(i) + "_sparse_Input"] == "False":
            sparse = False

        sparse_output = True
        if data["Preopt_" + str(i) + "_sparse_output_Input"] == "False":
            sparse_output = False

        parameter_dtype = float
        if data["Preopt_" + str(i) + "_dtype_Input"] == "bool":
            parameter_dtype = bool
        if data["Preopt_" + str(i) + "_dtype_Input"] == "int":
            parameter_dtype = int

        handle_unknown = data["Preopt_" + str(i) + "_handle_unknown_Input"]

        min_frequency = None
        if data["Preopt_" + str(i) + "_min_frequency_Input"] == "int":
            min_frequency = int(data["Preopt_" + str(i) + "_min_frequency_Int_Input"])
        if data["Preopt_" + str(i) + "_min_frequency_Input"] == "float":
            min_frequency = float(data["Preopt_" + str(i) + "_min_frequency_Float_Input"])

        max_categories = None
        if data["Preopt_" + str(i) + "_encoded_missing_value_Input"] != "None" and data["Preopt_" + str(i) + "_encoded_missing_value_Input"] != "":
            enc_miss_value = int(data["Preopt_" + str(i) + "_max_categories_Input"])

        enc = preprocessing.OneHotEncoder(categories=[df[data["Preopt_" + str(i) + "_column_Input"]].unique().tolist()],
                             dtype=parameter_dtype,
                             drop=drop,
                             sparse=sparse,
                             sparse_output=sparse_output,
                             handle_unknown=handle_unknown,
                             min_frequency=min_frequency,
                             max_categories=max_categories)

        new_df[data["Preopt_" + str(i) + "_column_Input"]] = enc.fit_transform(df[[data["Preopt_" + str(i) + "_column_Input"]]])

    # Label Encoder
    if method == "LabelEncoder":
        le = preprocessing.LabelEncoder()

        index_of_class_col = df.columns.get_loc(data["class_col"])

        temp = df[data["class_col"]].unique().tolist()
        le.fit(df[data["class_col"]].unique().tolist())
        new_df.iloc[:,index_of_class_col] = le.transform(df.iloc[:,index_of_class_col]) 

    # Dummy Variables
    if method == "DummyVariables":
        prefix = None
        if data["Preopt_" + str(i) + "_prefix_Input"] != "" and data["Preopt_" + str(i) + "_prefix_Input"] != None:
            prefix = data["Preopt_" + str(i) + "_prefix_Input"]

        dummy_na = False;
        if data["Preopt_" + str(i) + "_dummy_na_Input"] == "True":
            dummy_na = True;

        dtype_value = bool
        if data["Preopt_" + str(i) + "_dtype_Input"] == "float":
            dtype_value = float
        if data["Preopt_" + str(i) + "_dtype_Input"] == "int":
            dtype_value = int


        new_df = pd.get_dummies(data=df,
                                prefix=prefix,
                                prefix_sep=data["Preopt_" + str(i) + "_prefix_sep_Input"],
                                dummy_na=dummy_na,
                                columns=[data["Preopt_" + str(i) + "_column_Input"]],
                                dtype=dtype_value)

    return new_df