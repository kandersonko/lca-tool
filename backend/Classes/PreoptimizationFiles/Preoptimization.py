import os
import sys
import io
import base64

import pandas as pd
import numpy as np
from pathlib import Path

import matplotlib.pyplot as plt

from sklearn import preprocessing
from sklearn.preprocessing import OrdinalEncoder
from werkzeug.utils import secure_filename

from backend.Classes.PreoptimizationFiles import Preoptimizer

from backend.Classes.PreoptimizationFiles import Discretization
from backend.Classes.PreoptimizationFiles import EncodingCategoricalFeatures
from backend.Classes.PreoptimizationFiles import GeneratingPolynomialFeatures
from backend.Classes.PreoptimizationFiles import ImputationOfMissingValues
from backend.Classes.PreoptimizationFiles import NonLinearTransformation
from backend.Classes.PreoptimizationFiles import Normalization
from backend.Classes.PreoptimizationFiles import RemoveData
from backend.Classes.PreoptimizationFiles import Standardization

class Preopt_Category:
    def __init__(self, name, display_name, definition):
        self.name = name
        self.display_name = display_name
        self.definition = definition
    
    def getName(self):
        return self.name

    def getDisplayName(self):
        return self.display_name

    def getDefinition(self):
        return self.definition

# Create a list of possible categories to sect from.
list_Preopt_Categories = []

def getPreopt_Categories():
    return list_Preopt_Categories

## Preoptimization options are located at https://scikit-learn.org/stable/modules/preprocessing.html#discretization

# Standardization
Name = "Standardization"
Display_Name = "Standardization"
Definition = ["Standardization of datasets is a common requirement for many machine learning estimators implemented in scikit-learn; they might behave badly if the individual features do not more or less look like standard normally distributed data: Gaussian with zero mean and unit variance.\n\nIn practice we often ignore the shape of the distribution and just transform the data to center it by removing the mean value of each feature, then scale it by dividing non-constant features by their standard deviation.\n\nFor instance, many elements used in the objective function of a learning algorithm (such as the RBF kernel of Support Vector Machines or the l1 and l2 regularizers of linear models) may assume that all features are centered around zero or have variance in the same order. If a feature has a variance that is orders of magnitude larger than others, it might dominate the objective function and make the estimator unable to learn from other features correctly as expected."]

list_Preopt_Categories.append(Preopt_Category(Name, Display_Name, Definition))

# Non-linear Transformation
Name = "NonlinearTransformation"
Display_Name = "Non-linear Transformation"
Definition = ["Two types of transformations are available: quantile transforms and power transforms. Both quantile and power transforms are based on monotonic transformations of the features and thus preserve the rank of the values along each feature.\n\nQuantile transforms put all features into the same desired distribution based on the formula G^(-1)(F(X)) where F is the cumulative distribution function of the feature and G^(-1) the quantile function of the desired output distribution G. This formula is using the two following facts: (i) X if is a random variable with a continuous cumulative distribution function F then is uniformly distributed on F(X); (ii) U if is a random variable with uniform distribution on [0,1] then G^(-1)(U) has distribution G. By performing a rank transformation, a quantile transform smooths out unusual distributions and is less influenced by outliers than scaling methods. It does, however, distort correlations and distances within and across features.\n\nPower transforms are a family of parametric transformations that aim to map data from any distribution to as close to a Gaussian distribution."]

list_Preopt_Categories.append(Preopt_Category(Name, Display_Name, Definition))

# Normalization
Name = "Normalization"
Display_Name = "Normalization"
Definition = ["Normalization is the process of scaling individual samples to have unit norm. This process can be useful if you plan to use a quadratic form such as the dot-product or any other kernel to quantify the similarity of any pair of samples.\n\nThis assumption is the base of the Vector Space Model often used in text classification and clustering contexts."]

list_Preopt_Categories.append(Preopt_Category(Name, Display_Name, Definition))

# Encoding Categorical Features
Name = "EncodingCategoricalFeatures"
Display_Name = "Encoding Categorical Features"
Definition = ['Often features are not given as continuous values but categorical. For example a person could have features ["male", "female"], ["from Europe", "from US", "from Asia"], ["uses Firefox", "uses Chrome", "uses Safari", "uses Internet Explorer"]. Such features can be efficiently coded as integers, for instance ["male", "from US", "uses Internet Explorer"] could be expressed as [0, 1, 3] while ["female", "from Asia", "uses Chrome"] would be [1, 2, 1].']

list_Preopt_Categories.append(Preopt_Category(Name, Display_Name, Definition))

# Discretization
Name = "Discretization"
Display_Name = "Discretization"
Definition = ["Discretization (otherwise known as quantization or binning) provides a way to partition continuous features into discrete values. Certain datasets with continuous features may benefit from discretization, because discretization can transform the dataset of continuous attributes to one with only nominal attributes.\n\nOne-hot encoded discretized features can make a model more expressive, while maintaining interpretability. For instance, pre-processing with a discretizer can introduce nonlinearity to linear models. For more advanced possibilities, in particular smooth ones, see Generating polynomial features further below."]

list_Preopt_Categories.append(Preopt_Category(Name, Display_Name, Definition))

# Imputation of Missing Values
Name = "ImputationofMissingValues"
Display_Name = "Imputation of Missing Values"
Definition = ["For various reasons, many real world datasets contain missing values, often encoded as blanks, NaNs or other placeholders. Such datasets however are incompatible with scikit-learn estimators which assume that all values in an array are numerical, and that all have and hold meaning. A basic strategy to use incomplete datasets is to discard entire rows and/or columns containing missing values. However, this comes at the price of losing data which may be valuable (even though incomplete). A better strategy is to impute the missing values, i.e., to infer them from the known part of the data."]

list_Preopt_Categories.append(Preopt_Category(Name, Display_Name, Definition))

# Generating Polynomial Features
Name = "GeneratingPolynomialFeatures"
Display_Name = "Generating Polynomial Features"
Definition = ["Often it’s useful to add complexity to a model by considering nonlinear features of the input data. We show two possibilities that are both based on polynomials: The first one uses pure polynomials, the second one uses splines, i.e. piecewise polynomials."]

list_Preopt_Categories.append(Preopt_Category(Name, Display_Name, Definition))

# This may be implemented later, but is currently to complex for initial implementation of preoptimization
# What is does is allow the user to create a custom function for preoptimization.
# Custom Transformers
#Name = ""
#Display_name = ""
#Definition = [""]

# Remove Data
Name = "RemoveData"
Display_Name = "Remove Data"
Deginition = ["Preoptimization that simply removes information from the dataset."]

list_Preopt_Categories.append(Preopt_Category(Name, Display_Name, Definition))

#list_Preopt_Categories.append(Preopt_Category(Name, Display_Name, Definition))

# Obtain the list of preoptimization from all categories via their separate python files
list_Discretization = Discretization.getDiscretization()
list_ECF = EncodingCategoricalFeatures.getECF()
list_GPF = GeneratingPolynomialFeatures.getGPF()
list_IoMV = ImputationOfMissingValues.getIoMV()
list_NonLV = NonLinearTransformation.getNonLT()
list_Normalization = Normalization.getNormalization()
list_RemoveData = RemoveData.getRemoveData()
list_Standardization = Standardization.getStandardization()

# Create a list of possible Preoptimizations. (Old method, to be removed later)
list_Preopts = []

def getPreopts():
    return list_Preopts

# Information of the Preoptimization options.
## Category Encoders:
### OrdinalEncoder
Name = "OrdinalEncoder"
Display_Name = "Ordinal Encoder"
Definition = ["Encode categorical features as an integer array.\n\nThe input to this transformer should be an array-like of integers or strings, denoting the values taken on by categorical (discrete) features. The features are converted to ordinal integers. This results in a single column of integers (0 to n_categories - 1) per feature."]
## This should only be added if 2-d array is given, however since we are allowing user to perform operation on one column only. We give it the possible values later.
#Parameter_0 =  {"Name":"categories", "Type": ["option"], "Default":"auto", "Possible":["auto", "columns"], 
#               "Definition":"Categories (unique values) per feature:\n\n‘auto’ : Determine categories automatically from the training data.\n\nlist : categories[i] holds the categories expected in the ith column. The passed categories should not mix strings and numeric values, and should be sorted in case of numeric values."}
### Removed due to json issues and no other types are listed as acceptable on sklearn. Will be implemented at a later date if necessary
#Parameter_1 =  {"Name":"dtype", "Type": ["dtype_number"], "Default":np.float64, "Possible":["np.int32", "np.float64"], 
#               "Definition":"Desired dtype of output."}
Parameter_0 =  {"Name":"handle_unknown", "Type": ["option"], "Default":"error", "Possible":["error", "use_encoded_value"], 
               "Definition":"When set to ‘error’ an error will be raised in case an unknown categorical feature is present during transform. When set to ‘use_encoded_value’, the encoded value of unknown categories will be set to the value given for the parameter unknown_value. In inverse_transform, an unknown category will be denoted as None."}
Parameter_1 =  {"Name":"unknown_value", "Type": ["option"], "Default":"None", "Possible":["int", "np.nan", "None"], 
               "Definition":"When the parameter handle_unknown is set to ‘use_encoded_value’, this parameter is required and will set the encoded value of unknown categories. It has to be distinct from the values used to encode any of the categories in fit. If set to np.nan, the dtype parameter must be a float dtype."}
Parameter_2 =  {"Name":"encoded_missing_value", "Type": ["option_int"], "Default":"np.nan", "Possible":["int", "np.nan"], 
               "Definition":"Encoded value of missing categories. If set to np.nan, then the dtype parameter must be a float dtype."}
Parameter_3 = {"Name":"column", "Type": ["select"], "Default":"", "Possible":["col_names"],
               "Definition":"Column to perform the preoptimization on."}

Parameters = {"Parameter_0":Parameter_0, "Parameter_1":Parameter_1,"Parameter_2":Parameter_2,"Parameter_3":Parameter_3}

list_Preopts.append(Preoptimizer.Preoptimizer(Name, Display_Name, Definition, Parameters))

## Standard Scaling:
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

list_Preopts.append(Preoptimizer.Preoptimizer(Name, Display_Name, Definition, Parameters))

## Label Encoding:
Name = "LabelEncoder"
Display_Name = "Label Encoder"
Definition = ["Encode target labels with value between 0 and n_classes-1.\n\nThis transformer should be used to encode target values, i.e. y, and not the input X."]

Parameters = {}

list_Preopts.append(Preoptimizer.Preoptimizer(Name, Display_Name, Definition, Parameters))

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

list_Preopts.append(Preoptimizer.Preoptimizer(Name, Display_Name, Definition, Parameters))

## Drop Columns:
Name = "RemoveColumn"
Display_Name = "Remove Column"
Definition = ["Remove column from the dataset."]
Parameter_0 = {"Name":"column", "Type": ["select"], "Default":"", "Possible":["col_names"],
             "Definition":"The column name to remove from the dataset."}

Parameters = {"Parameter_0":Parameter_0}

list_Preopts.append(Preoptimizer.Preoptimizer(Name, Display_Name, Definition, Parameters))

## Drop Rows:
Name = "RemoveRow"
Display_Name = "Remove Row"
Definition = ["Remove row from the dataset."]
Parameter_0 = {"Name":"row", "Type": ["int"], "Default":"", "Possible":["int"],
             "Definition":"The index number of the row to remove."}

Parameters = {"Parameter_0":Parameter_0}

list_Preopts.append(Preoptimizer.Preoptimizer(Name, Display_Name, Definition, Parameters))

## Drop null values Removal:
Name = "DropRowsContainingNullValues"
Display_Name = "Drop Rows Containing Null Values"
Definition = ["Removes the rows that contain null value entires in any of the columns."]

Parameters = {}

list_Preopts.append(Preoptimizer.Preoptimizer(Name, Display_Name, Definition, Parameters))

## Outlier Removal:

## PCA: Principal Component Analysis

# Other Methods

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

    baseFolder = os.getcwd()

    ManualLoc = Path(baseFolder) / "tests/sampleCSV_MLA_Classification/"

    filename = secure_filename(fileName)
    dataset_path = ManualLoc / filename.lower()
    dataset = pd.read_csv(dataset_path)

    return dataset

# Return the column titles in an array.
def getCSVColumnTitles(data):
    df = getDataset(data)

    titles_list = list(df.columns.values)

    results = {"Tiltes":titles_list}

    return results

# Returns all preoptimizations from a Category
def getCategoryPreopts(Category_Name):
    info = []
    if Category_Name == "Discretization":
        preopts = list_Discretization
    if Category_Name == "EncodingCategoricalFeatures":
        preopts = list_ECF
    if Category_Name == "GeneratingPolynomialFeatures":
        preopts = list_GPF
    if Category_Name == "ImputationofMissingValues":
        preopts = list_IoMV
    if Category_Name == "NonlinearTransformation":
        preopts = list_NonLV
    if Category_Name == "Normalization":
        preopts = list_Normalization
    if Category_Name == "RemoveData":
        preopts = list_RemoveData
    if Category_Name == "Standardization":
        preopts = list_Standardization

    for preopt in preopts:
        preopt_info = {"Name": preopt.getName(), "Display_Name": preopt.getDisplayName()}
        info.append(preopt_info)

    return info

def getCSV_PDF(data):
    try: 
        # convert csv to usable dataset
        df = getDataset(data['csvFileName'])

        # perform preoptimization
        if data["Perform_Preopt"] == "Yes":
            # Cycle through the choices
            for i in range(int(data["preoptCounter"])):
                # Get the choice of preoptimization.
                preopt_method = data["Preopt_" + str(i)]
                # Perform the preoptimization on the dataset.
                df = perform_Preopt(data, i, df)

        dataframe = df.to_html()

        null_count = df.isnull().sum().rename_axis('Column').reset_index(name='Number of Null Instances')
        null_count = null_count.to_html()

        index_of_class_col = df.columns.get_loc(data["class_col"])

        number_classes = ""

        if data["class_col"] != None and data["class_col"] != "": 
            number_classes = df[df.columns[index_of_class_col]].value_counts().rename_axis('Unique Values').reset_index(name='counts')
            number_classes = number_classes.to_html()
            shape = df.shape
    
        kde_base64 = []
        if data["kde_ind"] != None and data["kde_ind"] != "": 
            if data["class_col"] != None and data["class_col"] != "": 
                classes = df[df.columns[index_of_class_col]].unique()

                X = df.loc[:, df.columns != df.columns[index_of_class_col]].values.astype('float64')
                Y = df[df.columns[index_of_class_col]].values

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
                "shape": shape,
                "null_Count": null_count,
                "Number_Classes": number_classes,
                "kde_plots": kde_base64}
    
        status = "worked"
        msg = ""

        return status, msg, PDF

    except Exception as e:
        PDF = ""
        msg = str(e)
        status = "error"

        return status, msg, PDF

# Method to pull all parameters from a given preoptimization option
def getParameters(Preopt_Name):
    Parameters = {}
    #list_Discretization = Discretization.getDiscretization()
    #list_ECF = EncodingCategoricalFeatures.getECF()
    #list_GPF = GeneratingPolynomialFeatures.getGPF()
    #list_IoMV = ImputationOfMissingValues.getIoMV()
    #list_NonLV = NonLinearTransformation.getNonLT()
    #list_Normalization = Normalization.getNormalization()
    #list_RemoveData = RemoveData.getRemoveData()
    #list_Standardization = Standardization.getStandardization()

    for preopt in list_Preopts:
        if preopt.getName() == Preopt_Name:
            Parameters = preopt.getParameters()
            return Parameters
    
    for preopt in list_Discretization:
        if preopt.getName() == Preopt_Name:
            Parameters = preopt.getParameters()
            return Parameters

    for preopt in list_ECF:
        if preopt.getName() == Preopt_Name:
            Parameters = preopt.getParameters()
            return Parameters

    for preopt in list_GPF:
        if preopt.getName() == Preopt_Name:
            Parameters = preopt.getParameters()
            return Parameters

    for preopt in list_IoMV:
        if preopt.getName() == Preopt_Name:
            Parameters = preopt.getParameters()
            return Parameters

    for preopt in list_NonLT:
        if preopt.getName() == Preopt_Name:
            Parameters = preopt.getParameters()
            return Parameters

    for preopt in list_Normalization:
        if preopt.getName() == Preopt_Name:
            Parameters = preopt.getParameters()
            return Parameters

    for preopt in list_RemoveData:
        if preopt.getName() == Preopt_Name:
            Parameters = preopt.getParameters()
            return Parameters

    for preopt in list_Standardization:
        if preopt.getName() == Preopt_Name:
            Parameters = preopt.getParameters()
            return Parameters


    return Parameters

# Method to check the chosen preoptimization method and perform it on the dataset.
def perform_Preopt(data, i, df):
    # get method
    method = data["Preopt_" + str(i)]

    new_df = df

    # Perform the preoptimization method based on the chosen selection.
    ## Categorical Encoding.
    ### Ordinal Encoder
    if method == "OrdinalEncoder":
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

        enc = OrdinalEncoder(categories=[df[data["Preopt_" + str(i) + "_column_Input"]].unique().tolist()],
                             handle_unknown=data["Preopt_" + str(i) + "_handle_unknown_Input"],
                             unknown_value=unknown_Value,
                             encoded_missing_value=enc_miss_value
        )

        new_df[data["Preopt_" + str(i) + "_column_Input"]] = enc.fit_transform(df[[data["Preopt_" + str(i) + "_column_Input"]]])

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

        sc = preprocessing.StandardScaler(copy=copy,
                            with_mean=with_mean,
                            with_std=with_std)
        
        index_of_column = df.columns.get_loc(data["Preopt_" + str(i) + "_column_Input"])

        temp = sc.fit_transform(df[[data["Preopt_" + str(i) + "_column_Input"]]]).flatten()

        new_df.iloc[:,index_of_column] = sc.fit_transform(df[[data["Preopt_" + str(i) + "_column_Input"]]]).flatten()


    ### Label Encoder
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

    ## Removal
    if method == "RemoveColumn":
        new_df = df.drop(columns=[data["Preopt_" + str(i) + "_column_Input"]])

    if method == "RemoveRow":
        new_df = df.drop([int(data["Preopt_" + str(i) + "_row_Input"])])

    ## Null instances
    ### Remove all
    if method == "DropRowsContainingNullValues":
        new_df = df.dropna(axis=0)

    ## Standardization options
    if method == "StandardScaler" or method == "MinMaxScaler" or method == "MaxAbsScaler" or method == "RobustScaler":
        new_df = Standardization.perform_Preopt(data, i, df)

    if method == "RemoveColumn" or method == "RemoveRow" or method == "DropRowsContainingNullValues":
        new_df = RemoveData.perform_Preopt(data, i, df)

    return new_df
