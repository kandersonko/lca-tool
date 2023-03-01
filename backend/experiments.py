import os
from flask import Blueprint
from flask import request, render_template, g, redirect, url_for, flash

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
    g.section_Choices = [[""], [""]]
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
    return render_template("experiments/LCA_Old.html")


@bp.route("/new_experiment")
def new_experiment():
    if not user_active(g.user):
        return redirect(url_for("auth.login"))
    return render_template("experiments/new_experiment.html")


@bp.route("/results")
def results():
    if not user_active(g.user):
        return redirect(url_for("auth.login"))
    return render_template("experiments/results.html")
