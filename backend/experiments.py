import os
import sys
import json
from flask import Blueprint
from flask import Flask, request, render_template, g, redirect, url_for, flash
from flask import jsonify
import logging
from pathlib import Path

import pandas as pd
import numpy as np
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

from sklearn.metrics import accuracy_score, f1_score, precision_score

from sklearn.metrics import ConfusionMatrixDisplay
from sklearn.metrics import confusion_matrix

## Models
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from werkzeug.utils import secure_filename

from backend.calculator import Calculator

# sys.path.append("backend")
# sys.path.append("Classes")
# sys.path.insert(1, '/Classes/')
from backend import MLA
from backend import MLA_Validation
from backend import DLANN_Validation
from backend.Classes.PreoptimizationFiles import Preoptimization
from backend.Classes.PreoptimizationFiles import Standardization
from backend.Classes.NeuralNetworkFiles import NeuralNetwork
from backend.Classes.NeuralNetworkFiles import Core
from backend.Classes.NeuralNetworkFiles import Compiler
from backend.Classes.NeuralNetworkFiles import Validation as NN_Validation
from backend.Classes.NeuralNetworkFiles import Callbacks

from keras.utils import to_categorical 

from sklearn.model_selection import KFold

bp = Blueprint("experiments", __name__, url_prefix="/experiments")


logger = logging.getLogger()

# should be modified to work with a db or class if necessary.
# Otherwise, the choices being pre-available on page load will slightly speed the process.
@bp.before_app_request
def load_possible_experiments():
    list_Algorithms = MLA.getMLAs()
    # list for preoptimization options
    list_Preopt_Categories = Preoptimization.getPreopt_Categories()
    list_Standardization = Standardization.getStandardization()
    # list for Neural Network options
    list_Layer_Categories = NeuralNetwork.getLayer_Categories()
    list_Core = Core.getCore()
    # list for Callback options
    list_Callbacks = Callbacks.getCallbacks()

    #----------------Data Types-------------------------->
    g.data_types = ["Tabular", "Image", "Text", "Signal"]
    g.data_types_Name = ["Tabular", "Image", "Text", "Signal"]
    g.data_types_Info = [["Tabular is data that is displayed in columns or tables and does not pertain to the other data types."],
                      ["Image is data that is usually 3-dimentional corresponding to the three color spectrom, RGB"],
                      ["Text is data containing textual words or sentences."],
                      ["Signal is data containing time-series data corresponding to a signal format."]]
    g.Data_Types = zip(g.data_types, g.data_types_Name, g.data_types_Info)

    #----------------new Cycon--------------------------->
    # First choice is between various categories of ML 
    g.section_Method = ["MLA", "DLANN"]
    g.section_Method_Display_Name = ["Machine Learning Algorithm (MLA)", "Deep Learning Artifical Neural Networks (DLANN)"]
    g.section_Info = [["Machine learning algorithms are mathematical model mapping methods. They are used to learn patterns embedded in the existing training dataset in order to perform pattern recognition, classification, and prediction.\n\nCurrently, the only algorithms available on cycon is under the classification objective. Other objectives that will be added later include clustering and regression."],
                      ["DLANN info"]]
    g.Methodologies = zip(g.section_Method, g.section_Method_Display_Name, g.section_Info)

    # Obtain the selection of Algorithm Names and Definition.
    algorithm_Names = []
    algorithm_Definition = []
    algorithm_Names.append("")
    algorithm_Definition.append("")

    for algorithm in list_Algorithms:
        algorithm_Names.append(algorithm.getName())
        algorithm_Definition.append(algorithm.getDefinition())
    g.section_algorithm = algorithm_Names
    g.section_Info = algorithm_Definition
    g.Algorithms = zip(g.section_algorithm, g.section_Info)

    #----------------Preoptimiztion-------------------------->
    # create list of options to choose a category of preoptimization options.
    preopt_Category_Names = []
    preopt_Category_Display_Names = []
    preopt_Category_Definition = []

    for preopt_Category in list_Preopt_Categories:
        preopt_Category_Names.append(preopt_Category.getName())
        preopt_Category_Display_Names.append(preopt_Category.getDisplayName())
        preopt_Category_Definition.append(preopt_Category.getDefinition())
    g.section_preopt_Category_Names = preopt_Category_Names
    g.section_preopt_Category_Display_Names = preopt_Category_Display_Names
    g.section_preopt_Category_Info =  preopt_Category_Definition
    g.preopt_Categories = zip(g.section_preopt_Category_Names, g.section_preopt_Category_Display_Names, g.section_preopt_Category_Info)

    # create list of options for the first category of preoprtimization (I.E. Standardization)
    preopt_Names = []
    preopt_Display_Names = []
    preopt_Definition = []

    for preopt in list_Standardization:
        preopt_Names.append(preopt.getName())
        preopt_Display_Names.append(preopt.getDisplayName())
        preopt_Definition.append(preopt.getDefinition())
    g.section_preopt_Names = preopt_Names
    g.section_preopt_Display_Names = preopt_Display_Names
    g.section_preopt_Info =  preopt_Definition
    g.preopts = zip(g.section_preopt_Names, g.section_preopt_Display_Names, g.section_preopt_Info)

    #-------------------Neural Network Layers----------------------->
    # create list of options to choose a category of layer options.
    layer_Category_Names = []
    layer_Category_Display_Names = []
    layer_Category_Definition = []

    for layer_Category in list_Layer_Categories:
        layer_Category_Names.append(layer_Category.getName())
        layer_Category_Display_Names.append(layer_Category.getDisplayName())
        layer_Category_Definition.append(layer_Category.getDefinition())
    g.layer_Category_Names = layer_Category_Names
    g.layer_Category_Display_Names = layer_Category_Display_Names
    g.layer_Category_Info =  layer_Category_Definition
    g.NN_layer_Categories = zip(g.layer_Category_Names, g.layer_Category_Display_Names, g.layer_Category_Info)

    # create list of options for the first category of preoprtimization (I.E. Core)
    layer_Names = []
    layer_Display_Names = []
    layer_Definition = []

    for layer in list_Core:
        layer_Names.append(layer.getName())
        layer_Display_Names.append(layer.getDisplayName())
        layer_Definition.append(layer.getDefinition())
    g.layer_Names = layer_Names
    g.layer_Display_Names = layer_Display_Names
    g.layer_Info =  layer_Definition
    g.layers = zip(g.layer_Names, g.layer_Display_Names, g.layer_Info)

    #-------------------Callbacks----------------------->
    # create list of options to choose a callback options.
    callback_Names = []
    callback_Display_Names = []
    callback_Definition = []

    for callback in list_Callbacks:
        callback_Names.append(callback.getName())
        callback_Display_Names.append(callback.getDisplayName())
        callback_Definition.append(callback.getDefinition())
    g.callback_Names = callback_Names
    g.callback_Display_Names = callback_Display_Names
    g.callback_Info =  callback_Definition
    g.callbacks = zip(g.callback_Names, g.callback_Display_Names, g.callback_Info)

# Old LCA for testing purposes, REMOVE BEFORE SUBMITTING.
@bp.route("/LCA_Old")
def LCA_Old():
    return render_template("experiments/LCA_Old.html")

# REMOVE ASAP
@bp.route("/new_experiment")
def new_experiment():
    return render_template("experiments/new_experiment.html")

@bp.route("/lca", methods=["GET"])
def lca():
    return render_template("experiments/lca.html")

@bp.route("/cycon")
def cycon():
    return render_template("experiments/cycon.html")


@bp.route("/calculate", methods=["POST"])
def calculate():
    processes_input = request.form.get("processes")
    processes = json.loads(processes_input)
    logger.debug("=== Equations: %s %s", processes, processes_input)
    calculator = Calculator()

    results = []
    for process in processes:
        filename = process.get("filename")
        csv_file = request.files.get(filename)
        equation = process.get("equation")
        name = process.get("name")
        logger.debug("=== Process (file): %s %s %s", filename, csv_file, request.form)
        evaluated, result = calculator.evaluate(equation=equation, csv_file=csv_file)
        output = dict(result=result, name=name)
        results.append(output)

        if not evaluated:
            flash(str(result))

    logger.debug("=== results: %s | dtype %s", results, type(results))
    return jsonify(processes=results)


@bp.route("/run_experiment", methods=["POST"])
def run_experiment():    
    processes_input = request.form.get("processes")
    data = json.loads(processes_input)

    filename = request.form.get("csvFileName")
    csv_file = request.files.get("csvFile")

    data["csvFileName"] = filename
    data["csvFile"] = csv_file

    # Perform MLA if chosen
    if data['methodology'] == "MLA":
        # Split
        if data['validation'] == "Split":
            status, msg, Metrics = MLA_Validation.Split(data)

        # K-Fold
        elif data['validation'] == "K-Fold":
            status, msg, Metrics = MLA_Validation.K_Fold(data)

        if status == "worked":
            # Open json file for the experiment.
            baseFolder = os.getcwd()
            locationSavedResults = Path(baseFolder) / "SavedResults"
            filename = secure_filename(data["projectName"] + ".json")
            filepath = locationSavedResults / filename.lower()
            if os.path.exists(filepath):
                os.remove(filepath)
                fp = open(filepath, "a")
            else:
                fp = open(filepath, "a")
    
            # write to json file
            metrics_Dump = json.dumps(Metrics)

            fp.write(metrics_Dump)

            # close the connection
            fp.close()

        Results = [status, msg, Metrics]

    # Perform Deep Learning Neural Network.
    if data['methodology'] == "DLANN":
        # Split
        status, msg, Metrics = DLANN_Validation.Split(data)

        if status == "worked":
            # Open json file for the experiment.
            baseFolder = os.getcwd()
            locationSavedResults = Path(baseFolder) / "SavedResults"
            filename = secure_filename(data["projectName"] + ".json")
            filepath = locationSavedResults / filename.lower()
            if os.path.exists(filepath):
                os.remove(filepath)
                fp = open(filepath, "a")
            else:
                fp = open(filepath, "a")
    
            # write to json file
            metrics_Dump = json.dumps(Metrics)

            fp.write(metrics_Dump)

            # close the connection
            fp.close()

        Results = [status, msg, Metrics]

    return json.dumps(Results)

@bp.route("/getResults", methods=["POST"])
def getResults(): 
    output = request.get_json()
    formData = json.loads(output)

    data = formData['form']

    baseFolder = os.getcwd()
    locationSavedResults = Path(baseFolder) / "SavedResults"
    filename = data["projectName"] + ".json"
    filepath = locationSavedResults / filename.lower()
    fp = open(filepath, "r")

    Metrics = json.load(fp)

    # close the connection
    fp.close()
    
    return json.dumps(Metrics)


@bp.route("/getAlgorithmParameters", methods=["POST"])
def getAlgorithmParameters():
    output = request.get_json()
    data = json.loads(output)

    Parameters = MLA.getParameters(data["Algorithm"])

    return json.dumps(Parameters)

@bp.route("/getCategoryPreopts", methods=["POST"])
def getCategoryPreopts():
    output = request.get_json()
    data = json.loads(output)

    preopts = Preoptimization.getCategoryPreopts(data["Category"])

    return json.dumps(preopts)

@bp.route("/getCategoryLayers", methods=["POST"])
def getCategoryLayers():
    output = request.get_json()
    data = json.loads(output)

    layers = NeuralNetwork.getCategoryLayers(data["Category"])

    return json.dumps(layers)


@bp.route("/results")
def results():
    return render_template("experiments/results.html")


@bp.route("/getCSVResults", methods=["POST"])
def getCSVResults():
    processes_input = request.form.get("processes")
    data = json.loads(processes_input)

    filename = request.form.get("csvFileName")
    csv_file = request.files.get("csvFile")

    data["csvFileName"] = filename
    data["csvFile"] = csv_file

    status, msg, info = Preoptimization.getCSV_PDF(data)

    Results = [status, msg, info]

    return json.dumps(Results)

@bp.route("/getModelSummary", methods=["POST"])
def getModelSummary():
    processes_input = request.form.get("processes")
    data = json.loads(processes_input)

    status, msg, info = NeuralNetwork.getModelSummary(data)

    Results = [status, msg, info]

    return json.dumps(Results)

@bp.route("/downloadCSV", methods=["POST"])
def downloadCSV():
    processes_input = request.form.get("processes")
    data = json.loads(processes_input)

    filename = request.form.get("csvFileName")
    csv_file = request.files.get("csvFile")

    data["csvFileName"] = filename
    data["csvFile"] = csv_file

    status, msg, info = Preoptimization.downloadCSV(data)

    Results = [status, msg, info]

    return json.dumps(Results)

@bp.route("/getPreoptParameters", methods=["POST"])
def getPreoptParameters():
    output = request.get_json()
    data = json.loads(output)

    Parameters = Preoptimization.getParameters(data["Preopt"])

    return json.dumps(Parameters)

@bp.route("/getLayerParameters", methods=["POST"])
def getLayerParameters():
    output = request.get_json()
    data = json.loads(output)

    Parameters = NeuralNetwork.getParameters(data["Layer"])

    return json.dumps(Parameters)

@bp.route("/getCallbackParameters", methods=["Post"])
def getCallbackParameters():
    output = request.get_json()
    data = json.loads(output)

    Parameters = Callbacks.getParameters(data["Callback"])

    return json.dumps(Parameters)

# Gets the colummn names inside the csv.
@bp.route("/getCSVColumnTitles", methods=["POST"])
def getCSVColumnTitles():
    filename = request.form.get("csvFileName")
    csv_file = request.files.get("csvFile")

    data = {"csvFileName": filename, "csvFile": csv_file}

    columnTitles = Preoptimization.getCSVColumnTitles(data)

    return json.dumps(columnTitles)

# Gets all the options that is available via the keras model.compile 
@bp.route("/getCompilerOptions", methods=["POST"])
def getCompilerOptions():
    compiler_Options = Compiler.getCompilerOptions()

    return json.dumps(compiler_Options)

# Gets all the options that is available for the model to fit,train, and validate.
@bp.route("/getValidationOptions", methods=["POST"])
def getValidationOptions():
    validation_Options = NN_Validation.getValidationOptions()

    return json.dumps(validation_Options)