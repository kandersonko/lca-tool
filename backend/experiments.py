import os
import sys
import json
from flask import Blueprint
from flask import Flask, request, render_template, g, redirect, url_for, flash
from flask import jsonify
import logging

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
from backend.calculator import Calculator

from sklearn.model_selection import KFold

bp = Blueprint("experiments", __name__, url_prefix="/experiments")


logger = logging.getLogger()

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


@bp.route("/mla")
def mla():
    return render_template("experiments/mla.html")


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


@bp.route("/run_experiment_1", methods=["POST"])
def run_experiment_1():
    output = request.get_json()
    data = json.loads(output)

    fileName = data["fileName"]
    csvFile = data["csvFile"]
    PreOpt = data["PreOpt"]
    Method = data["Method"]
    Validation = data["Validation"]
    Validation_Option = data["Validation_Option"]

    # convert csv to usable dataset
    ## Manual location currently...Will be changed when implemented in Host.
    ## Should further be changed when database is setup.
    ManualLoc = (
        "C://Users//vizen//Documents//College//Research//Cycon//sample_MLA_CSVs//"
    )

    dataset = pd.read_csv(ManualLoc + csvFile)

    df = dataset.to_numpy()

    # Split
    if data["Validation"] == "Split":
        # Split dataset to training and testing set
        train_set, test_set = train_test_split(
            df, test_size=float(Validation_Option), random_state=1, shuffle=True
        )

        length = train_set.shape[1] - 1

        x_train = train_set[:, 0:length]
        y_train = train_set[:, length]
        x_test = test_set[:, 0:length]
        y_test = test_set[:, length]

        if data["Method"] == "KNN":
            model = KNeighborsClassifier(n_neighbors=3)

        elif data["Method"] == "SVM":
            model = SVC(kernel="rbf", random_state=1)

        # Perform the Method.
        model.fit(x_train, y_train)

        # Predict the testset
        y_pred = model.predict(x_test)

        # Obtain the Metrics
        Accuracy = accuracy_score(y_test, y_pred)
        F1 = f1_score(y_test, y_pred, average=None)
        F1_micro = f1_score(y_test, y_pred, average="micro")
        F1_macro = f1_score(y_test, y_pred, average="macro")
        Precision = precision_score(y_test, y_pred, average=None)
        Precision_micro = precision_score(y_test, y_pred, average="micro")
        Precision_macro = precision_score(y_test, y_pred, average="macro")

        # create a confusion matrix
        # def fig_to_base64(fig):
        #    img = io.BytesIO()
        #    fig.savefig(img, format='png',
        #            bbox_inches='tight')
        #    img.seek(0)

        #    return base64.b64encode(img.getvalue())

        confusion_matrix(y_test, y_pred)

        cm = confusion_matrix(y_test, y_pred, labels=model.classes_)
        color = "white"
        disp = ConfusionMatrixDisplay(
            confusion_matrix=cm, display_labels=model.classes_
        )
        disp.plot()
        temp = os.getcwd()
        plt.savefig(temp + "\\backend\\static\\Images\\" + fileName + ".png")

        # data_uri = base64.b64encode(open('conf_matrix.png', 'rb').read()).decode('utf-8')
        # img_tag = '<img src="data:image/png;base64,{0}">'.format(data_uri)

        # encoded = fig_to_base64(fig)
        # my_html = '<img src="data:image/png;base64, {}">'.format(encoded.decode('utf-8'))

        # Send the Metrics
        Metrics = {
            "Accuracy": Accuracy,
            "F1": F1.tolist(),
            "F1_micro": F1_micro,
            "F1_macro": F1_macro,
            "Precision": Precision.tolist(),
            "Precision_micro": Precision_micro,
            "Precision_macro": Precision_macro,
        }

    # K-Fold
    elif data["Validation"] == "K-Fold":
        length = df.shape[1] - 1

        X = df[:, 0:length]
        y = df[:, length]

        kf = KFold(
            n_splits=int(data["Validation_Option"]), shuffle=True, random_state=1
        )
        kf.get_n_splits(X)

        acc_list = []
        prec_list = []
        prec_micro_list = []
        prec_macro_list = []
        f1_list = []
        f1_micro_list = []
        f1_macro_list = []
        y_test_list = np.empty(1)
        y_predict_list = np.empty(1)

        for i, (train_index, test_index) in enumerate(kf.split(X)):
            print("Fold: " + str(i) + " ===============================")
            x_train = X[train_index]
            y_train = y[train_index]
            x_test = X[test_index]
            y_test = y[test_index]

            if data["Method"] == "KNN":
                model = KNeighborsClassifier(n_neighbors=3)

            elif data["Method"] == "SVM":
                model = SVC(kernel="rbf", random_state=1)

            model.fit(X[train_index], y[train_index])

            y_pred = model.predict(X[test_index])

            acc = accuracy_score(y[test_index], y_pred)
            prec = precision_score(y[test_index], y_pred, average=None)
            prec_micro = precision_score(y[test_index], y_pred, average="micro")
            prec_macro = precision_score(y[test_index], y_pred, average="macro")
            f1 = f1_score(y[test_index], y_pred, average=None)
            f1_micro = f1_score(y[test_index], y_pred, average="micro")
            f1_macro = f1_score(y[test_index], y_pred, average="macro")

            acc_list.append(acc)
            prec_list.append(prec)
            prec_micro_list.append(prec_micro)
            prec_macro_list.append(prec_macro)
            f1_list.append(f1)
            f1_micro_list.append(f1_micro)
            f1_macro_list.append(f1_macro)
            y_test_list = np.concatenate((y_test_list, y[test_index]))
            y_predict_list = np.concatenate((y_predict_list, y_pred))

            cm = confusion_matrix(y[test_index], y_pred, labels=model.classes_)
            color = "white"
            disp = ConfusionMatrixDisplay(
                confusion_matrix=cm, display_labels=model.classes_
            )
            disp.plot()
            temp = os.getcwd()
            plt.savefig(
                temp
                + "\\backend\\static\\Images\\"
                + fileName
                + "_fold_"
                + str(i)
                + ".png"
            )

        acc_list = np.array(acc_list)
        prec_list = np.array(prec_list)
        prec_micro_list = np.array(prec_micro_list)
        prec_macro_list = np.array(prec_macro_list)
        f1_list = np.array(f1_list)
        f1_micro_list = np.array(f1_micro_list)
        f1_macro_list = np.array(f1_macro_list)

        y_test_list = np.delete(y_test_list, 0)
        y_predict_list = np.delete(y_predict_list, 0)

        acc_average = np.average(acc_list)
        prec_average = np.average(prec_list, axis=0)
        prec_micro_average = np.average(prec_micro_list)
        prec_macro_average = np.average(prec_macro_list)
        f1_average = np.average(f1_list, axis=0)
        f1_micro_average = np.average(f1_micro_list)
        f1_macro_average = np.average(f1_macro_list)

        cm = confusion_matrix(y_test_list, y_predict_list, labels=model.classes_)
        color = "white"
        disp = ConfusionMatrixDisplay(
            confusion_matrix=cm, display_labels=model.classes_
        )
        disp.plot()
        temp = os.getcwd()
        plt.savefig(temp + "\\backend\\static\\Images\\" + fileName + "_Collective.png")

        # Send the Metrics
        Metrics = {
            "acc_list": acc_list.tolist(),
            "prec_list": prec_list.tolist(),
            "prec_micro_list": prec_micro_list.tolist(),
            "prec_macro_list": prec_macro_list.tolist(),
            "f1_list": f1_list.tolist(),
            "f1_micro_list": f1_micro_list.tolist(),
            "f1_macro_list": f1_macro_list.tolist(),
            "acc_average": acc_average,
            "prec_average": prec_average.tolist(),
            "prec_micro_average": prec_micro_average,
            "prec_macro_average": prec_macro_average,
            "f1_average": f1_average.tolist(),
            "f1_micro_average": f1_micro_average,
            "f1_macro_average": f1_macro_average,
        }

    return json.dumps(Metrics)


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
