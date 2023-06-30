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
from backend import Validation
from backend.Classes.PreoptimizationFiles import Preoptimization
from backend.Classes.PreoptimizationFiles import Standardization

from sklearn.model_selection import KFold

bp = Blueprint("experiments", __name__, url_prefix="/experiments")


logger = logging.getLogger()

# should be modified to work with a db or class if necessary.
# Otherwise, the choces being pre-available on page load will slightly speed the process.
@bp.before_app_request
def load_possible_experiments():
    list_Algorithms = MLA.getMLAs()
    list_Preoptimizations = Preoptimization.getPreopts()
    list_Preopt_Categories = Preoptimization.getPreopt_Categories()
    list_Standardization = Standardization.getStandardization()

    # ----------------new Cycon--------------------------->
    # First choice is between various categories of ML
    g.section_Method = ["MLA", "DLANN"]
    g.section_Method_Display_Name = [
        "Machine Learning Algorithm (MLA)",
        "Deep Learning Artifical Neural Networks (DLANN)",
    ]
    g.section_Info = [
        [
            "Machine learning algorithms are mathematical model mapping methods. They are used to learn patterns embedded in the existing training dataset in order to perform pattern recognition, classification, and prediction.\n\nCurrently, the only algorithms available on cycon is under the classification objective. Other objectives that will be added later include clustering and regression."
        ],
        ["DLANN info"],
    ]
    g.Methodologies = zip(
        g.section_Method, g.section_Method_Display_Name, g.section_Info
    )

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

    # obtain the selection of preoptimization options and definitions.
    preopt_Names = []
    preopt_Display_Names = []
    preopt_Definition = []

    preopt_Names.append("")
    preopt_Display_Names.append("")
    preopt_Definition.append("")

    for preopt in list_Preoptimizations:
        preopt_Names.append(preopt.getName())
        preopt_Display_Names.append(preopt.getDisplayName())
        preopt_Definition.append(preopt.getDefinition())
    g.section_preopt = preopt_Names
    g.section_preopt_names = preopt_Display_Names
    g.section_Info = preopt_Definition
    g.Preoptimizations = zip(g.section_preopt, g.section_preopt_names, g.section_Info)

    # create list of options to choose a category of preoptimization options.
    preopt_Category_Names = []
    preopt_Category_Display_Names = []
    preopt_Category_Definition = []

    # preopt_Category_Names.append("")
    # preopt_Category_Display_Names.append("")
    # preopt_Category_Definition.append("")

    for preopt_Category in list_Preopt_Categories:
        preopt_Category_Names.append(preopt_Category.getName())
        preopt_Category_Display_Names.append(preopt_Category.getDisplayName())
        preopt_Category_Definition.append(preopt_Category.getDefinition())
    g.section_preopt_Category_Names = preopt_Category_Names
    g.section_preopt_Category_Display_Names = preopt_Category_Display_Names
    g.section_preopt_Category_Info = preopt_Category_Definition
    g.preopt_Categories = zip(
        g.section_preopt_Category_Names,
        g.section_preopt_Category_Display_Names,
        g.section_preopt_Category_Info,
    )

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
    g.section_preopt_Info = preopt_Definition
    g.preopts = zip(
        g.section_preopt_Names, g.section_preopt_Display_Names, g.section_preopt_Info
    )


# Old LCA for testing purposes, REMOVE BEFORE SUBMITTING.
@bp.route("/LCA_Old")
def LCA_Old():
    return render_template("experiments/LCA_Old.html")


@bp.route("/lca")
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
        output = dict(result=result, name=name, equation=equation)
        results.append(output)

        if not evaluated:
            flash(str(result))

    logger.debug("=== results: %s | dtype %s", results, type(results))
    return jsonify(processes=results)


@bp.route("/run_experiment", methods=["POST"])
def run_experiment():
    output = request.get_json()
    formData = json.loads(output)

    data = formData["form"]

    # Split
    if data["validation"] == "Split":
        status, msg, Metrics = Validation.Split(data)

    # K-Fold
    elif data["validation"] == "K-Fold":
        status, msg, Metrics = Validation.K_Fold(data)

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

    data = formData["form"]

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


@bp.route("/results")
def results():
    return render_template("experiments/results.html")


@bp.route("/getCSVResults", methods=["POST"])
def getCSVResults():
    output = request.get_json()
    formData = json.loads(output)

    data = formData["form"]

    status, msg, info = Preoptimization.getCSV_PDF(data)

    Results = [status, msg, info]

    return json.dumps(Results)


@bp.route("/getPreoptParameters", methods=["POST"])
def getPreoptParameters():
    output = request.get_json()
    data = json.loads(output)

    Parameters = Preoptimization.getParameters(data["Preopt"])

    return json.dumps(Parameters)


# Gets the colummn names inside the csv.
@bp.route("/getCSVColumnTitles", methods=["POST"])
def getCSVColumnTitles():
    output = request.get_json()
    data = json.loads(output)

    columnTitles = Preoptimization.getCSVColumnTitles(data["csvFileName"])

    return json.dumps(columnTitles)
