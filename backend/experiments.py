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

#sys.path.append("backend")
#sys.path.append("Classes")
#sys.path.insert(1, '/Classes/')
from backend import MLA
from backend import Validation
from backend import Preoptimization

from sklearn.model_selection import KFold

bp = Blueprint("experiments", __name__, url_prefix="/experiments")


logger = logging.getLogger()

# should be modified to work with a db or class if necessary.
# Otherwise, the choces being pre-available on page load will slightly speed the process.
@bp.before_app_request
def load_possible_experiments():
    list_Algorithms = MLA.getMLAs()
    list_Preoptimizations = Preoptimization.getPreopts()

    #----------------new Cycon--------------------------->
    # First choice is between various categories of ML 
    g.section_Method = ["MLA: Machine Learning Algorithm", "DLANN: Deep Learning Artifical Neural Networks"]
    g.section_Info = [["Machine learning algorithms are mathematical model mapping methods. They are used to learn patterns embedded in the existing training dataset in order to perform pattern recognition, classification, and prediction.\n\nCurrently, the only algorithms available on cycon is under the classification objective. Other objectives that will be added later include clustering and regression."],
                      ["DLANN info"]]
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

    # obtain the selection of preoptimization options and definitions.
    preopt_Names = []
    preopt_Definition = []
    preopt_Names.append("")
    preopt_Definition.append("")

    for preopt in list_Preoptimizations:
        preopt_Names.append(preopt.getName())
        preopt_Definition.append(preopt.getDefinition())
    g.section_preopt = preopt_Names
    g.section_Info = preopt_Definition
    g.Preoptimizations = zip(g.section_preopt, g.section_Info)




# Old LCA for testing purposes, REMOVE BEFORE SUBMITTING.
@bp.route("/LCA_Old")
def LCA_Old():
    return render_template("experiments/LCA_Old.html")


# REMOVE ASAP
@bp.route("/new_experiment")
def new_experiment():
    return render_template("experiments/new_experiment.html")


@bp.route("/lca")
def lca():
    return render_template("experiments/lca.html")


@bp.route("/cycon")
def cycon():
    return render_template("experiments/cycon.html")


@bp.route("/calculate", methods=["POST"])
def calculate():
    variables = request.form.get("variables")
    equation = request.form.get("equation")
    csv_file = request.files.get("csv_file")
    calculator = Calculator(equation=equation, variables=variables, csv_file=csv_file)

    evaluated, results = calculator.evaluate()
    logger.debug("calculate: %s", csv_file)

    if not evaluated:
        flash(str(results))
        return jsonify(results=[])
    else:
        return jsonify(results=results.to_html(index=False))


@bp.route("/run_experiment", methods=["POST"])
def run_experiment():    
    output = request.get_json()
    formData = json.loads(output)

    data = formData['form']

    # Split
    if data['validation'] == "Split":
        Metrics = Validation.Split(data)

    # K-Fold
    elif data['validation'] == "K-Fold":
        Metrics = Validation.K_Fold(data)

    
    # Open json file for the experiment.
    baseFolder = os.getcwd()
    locationSavedResults = baseFolder + "\\SavedResults\\"
    if os.path.exists(locationSavedResults + data['projectName'] + ".json"):
        os.remove(locationSavedResults + data['projectName'] + ".json")
        fp = open(locationSavedResults + data['projectName'] + ".json", 'a')
    else:
        fp = open(locationSavedResults + data['projectName'] + ".json", 'a')
    
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

    data = formData['form']

    baseFolder = os.getcwd()
    locationSavedResults = baseFolder + "\\SavedResults\\"
    fp = open(locationSavedResults + data['projectName'] + ".json", 'r')

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


@bp.route("/getCSVResults", methods=["POST"])
def getCSVResults():
    output = request.get_json()
    formData = json.loads(output)

    data = formData['form']

    pdfs = Preoptimization.getCSV_PDF(data)

    return json.dumps(pdfs)
