import os
import sys
import json
from flask import Blueprint
from flask import Flask, request, render_template, g, redirect, url_for, flash

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

# sys.path.append("backend")
# sys.path.append("Classes")
# sys.path.insert(1, '/Classes/')
from backend import MLA
from backend import Validation

from sklearn.model_selection import KFold

bp = Blueprint("experiments", __name__, url_prefix="/experiments")

# should be modified to work with a db or class if necessary.
# Otherwise, the choces being pre-available on page load will slightly speed the process.
@bp.before_app_request
def load_possible_experiments():
    list_Algorithms = MLA.getMLAs()

    # ----------------new Cycon--------------------------->
    # First choice is between various categories of ML
    g.section_Method = [
        "MLA: Machine Learning Algorithm",
        "DLANN: Deep Learning Artifical Neural Networks",
    ]
    g.section_Info = [["MLA info"], ["DLANN info"]]
    g.Methodologies = zip(g.section_Method, g.section_Info)

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

    # First choice is between LCA and MLA
    g.section_Method = [
        "MLA: Machine Learning Algorithm",
        "DLANN: Deep Learning Artifical Neural Networks",
    ]
    g.section_Info = [["MLA info"], ["DLANN info"]]
    g.Methodologies = zip(g.section_Method, g.section_Info)

    # Second section is name project and objective
    ## Nothing needs to be pulled from the database here.

    # Third section, load dataset.
    ## some info on what the dataset need to be should be pulled from the database
    g.section_Choices = [["LCA"], ["MLA"]]
    g.section_Info = [
        [
            "Dataset should contain the Life cycle inventory (LCI)",
            "Should be in the form...(will add later)",
        ],
        ["Dataset should be in a CSV file."],
    ]
    g.LoadDataset = zip(g.section_Choices, g.section_Info)

    # Obtains and displays files already inside the database. (will implement later).
    g.csvfiles = ["temp1.csv", "temp2.csv"]

    # Forth section, preoptimization
    g.section_Choices = [
        ["PCA: Principal Component Analysis", "None"],
        ["PCA: Principal Component Analysis", "None"],
    ]
    g.section_Info = [
        ["PCA: Info", "None: No preoptimization will be performed"],
        ["PCA: Info", "None: No preoptimization will be performed"],
    ]
    g.Preoptimization = zip(g.section_Choices, g.section_Info)

    # Fifth section, Method
    # g.section_Choices = [["Social analysis method",
    #                       "Cost analysis method",
    #                       "Environmental analysis method"],
    #                      ["SVM", "KNN"]]
    # g.section_Info = [["Social analysis method: \nIndicator Value = Sum m-n [Sum i-n (Score/Total Score)] x Score / Number of Metrics (see the example on social assessment page)",
    #                       "Cost analysis method: \nCup = Raw Material Mass * Collection/Transportation Cost, \nCmid = Raw Material Mass * Production Cost, \nCdown = Final Product Mass * Distribution Cost",
    #                       "Environmental analysis method: \nEup = Mass * Emission Factor Up, \nEmid = Mass * Emission Factor Mid, \nEdown = Mass * Emission Factor Down * Distance "] ,
    #                  ["SVM: Info", "KNN: Info"]]
    # g.Methods = zip(g.section_Choices, g.section_Info)

    # Sixth section, Validation
    g.section_Choices = [[None], ["k-Fold", "Split"]]
    g.section_Info = [
        [None],
        [
            "k-Fold: Please give one number for the number of folds",
            "Split: Please give the percentage for the training, testing, sets or training, testing and validation sets organized in train - test or train - test - validation format. Example: 80 - 10 - 10",
        ],
    ]
    g.Validation = zip(g.section_Choices, g.section_Info)

    # Seventh section, Metics
    g.section_Choices = [[None], ["ACC", "F1", "ROC"]]
    g.section_Info = [[None], ["ACC: Info", "F1: Info", "ROC: Info"]]
    g.Metric = zip(g.section_Choices, g.section_Info)


@bp.route("/lca")
def lca():
    return render_template("experiments/lca.html")


@bp.route("/cycon")
def cycon():
    return render_template("experiments/cycon.html")


@bp.route("/run_experiment", methods=["POST"])
def run_experiment():
    output = request.get_json()
    formData = json.loads(output)

    data = formData["form"]

    # Split
    if data["validation"] == "Split":
        Metrics = Validation.Split(data)

    # K-Fold
    elif data["validation"] == "K-Fold":
        Metrics = Validation.K_Fold(data)

    # Open json file for the experiment.
    baseFolder = os.getcwd()
    locationSavedResults = baseFolder + "\\SavedResults\\"
    if os.path.exists(locationSavedResults + data["projectName"] + ".json"):
        os.remove(locationSavedResults + data["projectName"] + ".json")
        fp = open(locationSavedResults + data["projectName"] + ".json", "a")
    else:
        fp = open(locationSavedResults + data["projectName"] + ".json", "a")

    # write to json file
    metrics_Dump = json.dumps(Metrics)

    fp.write(metrics_Dump)

    # close the connection
    fp.close()

    return json.dumps(Metrics)


@bp.route("/getResults", methods=["POST"])
def getResults():
    output = request.get_json()
    formData = json.loads(output)

    data = formData["form"]

    baseFolder = os.getcwd()
    locationSavedResults = baseFolder + "\\SavedResults\\"
    fp = open(locationSavedResults + data["projectName"] + ".json", "r")

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


@bp.route("/results")
def results():
    return render_template("experiments/results.html")
