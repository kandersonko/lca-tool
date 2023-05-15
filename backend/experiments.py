import os
import json
from flask import Blueprint
from flask import request, render_template, g, redirect, url_for, flash

import pandas as pd
import numpy as np
from sklearn.svm import SVC
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

from sklearn.metrics import accuracy_score, f1_score, precision_score

from sklearn.metrics import ConfusionMatrixDisplay
from sklearn.metrics import confusion_matrix

import base64

from backend.utils import user_active

bp = Blueprint("experiments", __name__, url_prefix="/experiments")

# should be modified to work with a db
@bp.before_app_request
def load_possible_experiments():

    # First choice is between LCA and MLA
    g.section_Method = ["LCA: Life Cycle Assessment", "MLA: Machine Learning Algorithm"]
    g.section_Info = [["LCA info"], ["MLA info"]]
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
    g.section_Choices = [
        [
            "Social analysis method",
            "Cost analysis method",
            "Environmental analysis method",
        ],
        ["SVM", "KNN"],
    ]
    g.section_Info = [
        [
            "Social analysis method: \nIndicator Value = Sum m-n [Sum i-n (Score/Total Score)] x Score / Number of Metrics (see the example on social assessment page)",
            "Cost analysis method: \nCup = Raw Material Mass * Collection/Transportation Cost, \nCmid = Raw Material Mass * Production Cost, \nCdown = Final Product Mass * Distribution Cost",
            "Environmental analysis method: \nEup = Mass * Emission Factor Up, \nEmid = Mass * Emission Factor Mid, \nEdown = Mass * Emission Factor Down * Distance ",
        ],
        ["SVM: Info", "KNN: Info"],
    ]
    g.Methods = zip(g.section_Choices, g.section_Info)

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


@bp.route("/LCA_Old")
def LCA_Old():
    if not user_active(g.user):
        return redirect(url_for("auth.login"))
    return render_template("experiments/cycon.html")


@bp.route("/new_experiment")
def new_experiment():
    if not user_active(g.user):
        return redirect(url_for("auth.login"))
    return render_template("experiments/new_experiment.html")


@bp.route("/run_experiment", methods=["POST"])
def run_experiment():
    output = request.get_json()
    data = json.loads(output)

    # Retrieve the data.
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

    # Split dataset to training and testing set
    train_set, test_set = train_test_split(
        df, test_size=float(Validation_Option), random_state=1, shuffle=True
    )

    length = train_set.shape[1] - 1

    x_train = train_set[:, 0:length]
    y_train = train_set[:, length]
    x_test = test_set[:, 0:length]
    y_test = test_set[:, length]

    # Perform the Method.
    model = SVC(kernel="rbf", random_state=1)
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
    def fig_to_base64(fig):
        img = io.BytesIO()
        fig.savefig(img, format="png", bbox_inches="tight")
        img.seek(0)

        return base64.b64encode(img.getvalue())

    confusion_matrix(y_test, y_pred)

    cm = confusion_matrix(y_test, y_pred, labels=model.classes_)
    color = "white"
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=model.classes_)
    disp.plot()
    temp = os.getcwd()
    plt.savefig(temp + "\\backend\\static\\Images\\" + fileName + ".png")

    data_uri = base64.b64encode(open("conf_matrix.png", "rb").read()).decode("utf-8")
    img_tag = '<img src="data:image/png;base64,{0}">'.format(data_uri)

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

    return json.dumps(Metrics)


@bp.route("/results")
def results():
    if not user_active(g.user):
        return redirect(url_for("auth.login"))
    return render_template("experiments/results.html")
