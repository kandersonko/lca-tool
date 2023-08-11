import os
import sys
import io
import base64

import pandas as pd
import numpy as np

# Gets the parameters of the Preoptimizer.
## Method placed in this class for all subclasses to be able to call.
def getParameters(Preopt_Name, list_P):
    Parameters = {}

    for preopt in list_P:
        if preopt.getName() == Preopt_Name:
            Parameters = preopt.getParameters()
            return Parameters

    return Parameters

# get settings to fill the model parameters.
def getSettings(data, Parameters, counter, operation):
    settings = {}

    # contains the naming fill for the counter if there is one associated to the preopt process.
    fill = ""
    if counter != -1:
        fill = operation + "_" + str(counter) + "_"

    # Cycle through parameters
    for i in range(len(Parameters)):
        # get name
        settings["Parameter_" + str(i) + "_Name"] = Parameters["Parameter_" + str(i)]["Name"]

        if Parameters["Parameter_" + str(i)]["Type"][0] == "option_input" or Parameters["Parameter_" + str(i)]["Type"][0] == "option_input_dtype":
            if data[fill + Parameters["Parameter_" + str(i)]["Name"] + "_Input"] == "string":
                settings["Parameter_" + str(i)] = data[fill + Parameters["Parameter_" + str(i)]["Name"] + "_Input"]
                settings["Parameter_" + str(i)] = convertToType("string", Parameters["Parameter_" + str(i)]["Type"], data[fill + Parameters["Parameter_" + str(i)]["Name"] + "_String_Input"])
            elif data[fill + Parameters["Parameter_" + str(i)]["Name"] + "_Input"] == "int":
                settings["Parameter_" + str(i)] = data[fill + Parameters["Parameter_" + str(i)]["Name"] + "_Input"]
                settings["Parameter_" + str(i)] = convertToType("int", Parameters["Parameter_" + str(i)]["Type"], data[fill + Parameters["Parameter_" + str(i)]["Name"] + "_Int_Input"])
            elif data[fill + Parameters["Parameter_" + str(i)]["Name"] + "_Input"] == "float":
                settings["Parameter_" + str(i)] = data[fill + Parameters["Parameter_" + str(i)]["Name"] + "_Input"]
                settings["Parameter_" + str(i)] = convertToType("float", Parameters["Parameter_" + str(i)]["Type"], data[fill + Parameters["Parameter_" + str(i)]["Name"] + "_Float_Input"])
            else:
                settings["Parameter_" + str(i)] = data[fill + Parameters["Parameter_" + str(i)]["Name"] + "_Input"]
                settings["Parameter_" + str(i)] = convertToType(settings["Parameter_" + str(i)], Parameters["Parameter_" + str(i)]["Type"])

        else:
            settings["Parameter_" + str(i)] = data[fill + Parameters["Parameter_" + str(i)]["Name"] + "_Input"]
            settings["Parameter_" + str(i)] = convertToType(settings["Parameter_" + str(i)], Parameters["Parameter_" + str(i)]["Type"])

    return settings


def convertToType(value, Type, additionalInput = 0):
    if Type[0] == "int":
        if value == "null" or value == "None" or value == "":
            return None
        else:
            return int(value)

    elif Type[0] == "float":
        return float(value)

    elif Type[0] == "str":
        if value == "null" or value == "None" or value == "":
            return None
        else:
            return value

    elif Type[0] == "bool":
        if value == "true" or value == True:
            return True
        elif value == "false" or value == False:
            return False
        else: 
            return None
            

    elif Type[0] == "option":
        if value == "null" or value == "None" or value == "":
            return None
        else:
            return value

    elif Type[0] == "option_dtype":
        if value == "null" or value == "None" or value == "":
            return None
        elif value == "np.int32":
            return np.int32
        elif value == "np.int64":
            return np.int64
        elif value == "np.float32":
            return np.float32
        elif value == "np.float64":
            return np.float64
        elif value == "int":
            return int
        elif value == "str":
            return str
        elif value == "float":
            return float
        elif value == "bool":
            return bool
        else:
            return value

    elif Type[0] == "option_input":
        if value == "null" or value == "None" or value == "":
            return None
        else:
            if value == "string":
                return additionalInput
            elif value == "int":
                return int(additionalInput)
            elif value == "float":
                return float(additionalInput)
            else:
                return value

    elif Type[0] == "option_integer":
        if value == "null" or value == "None" or value == "":
            return None
        else:
            return int(value)

    elif Type[0] == "option_input_dtype":
        if value == "null" or value == "None" or value == "":
            return None
        else:
            if value == "string":
                return additionalInput
            elif value == "int":
                return int(additionalInput)
            elif value == "float":
                return float(additionalInput)
            elif value == "np.nan":
                return np.nan
            elif value == "np.int32":
                return np.int32
            elif value == "np.int64":
                return np.int64
            elif value == "np.float32":
                return np.float32
            elif value == "np.float64":
                return np.float64
            else:
                return value

    else:
        return value
