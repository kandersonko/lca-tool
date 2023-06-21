import os
import sys
import io
import base64

from backend import MLA

import pandas as pd
import numpy as np
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

from sklearn.metrics import accuracy_score, f1_score, precision_score

from sklearn.metrics import ConfusionMatrixDisplay
from sklearn.metrics import confusion_matrix

from sklearn.model_selection import KFold
from sklearn.model_selection import StratifiedKFold


def getDataset(fileName):
     # convert csv to usable dataset
    ## Manual location currently...Will be changed when implemented in Host.
    ## Should further be changed when database is setup.

    ManualLoc = "/backend/tests/sampleCSV_MLA_Classification/"

    dataset = pd.read_csv(ManualLoc + fileName)

    return dataset.to_numpy()


def Split(data):
    # convert csv to usable dataset
    df = getDataset(data['csvFileName'])

    # Split dataset to training and testing set
    random_state = None
    if data["Random_State_Input"] != "":
        random_state = int(data["Random_State_Input"])
    shuffle = False
    if data["Shuffle"] == "True":
        shuffle = True
    stratify = None
    if data["Stratify"] == "True":
        stratify = df[:,length]
    
    train_set, test_set = train_test_split(df, test_size=float(data[data['validation'] + "_Input"]), shuffle=shuffle, random_state = random_state, stratify = stratify)

    length = train_set.shape[1] -1

    x_train = train_set[:,0:length]
    y_train = train_set[:,length]
    x_test = test_set[:,0:length]
    y_test = test_set[:,length]

    #model = KNeighborsClassifier(n_neighbors=3)
    model, settings = MLA.createModel(data)

    # Perform the Method.
    model.fit(x_train, y_train)

    # Predict the testset
    y_pred = model.predict(x_test)

    # Obtain the Metrics
    Accuracy = accuracy_score(y_test, y_pred)
    F1 = f1_score(y_test, y_pred, average=None)
    F1_micro = f1_score(y_test, y_pred, average='micro')
    F1_macro = f1_score(y_test, y_pred, average='macro')
    Precision = precision_score(y_test, y_pred, average=None)
    Precision_micro = precision_score(y_test, y_pred, average='micro')
    Precision_macro = precision_score(y_test, y_pred, average='macro')

    # create a confusion matrix
    #def fig_to_base64(fig):
    #    img = io.BytesIO()
    #    fig.savefig(img, format='png',
    #            bbox_inches='tight')
    #    img.seek(0)

    #    return base64.b64encode(img.getvalue())

    confusion_matrix(y_test, y_pred)

    cm = confusion_matrix(y_test, y_pred, labels=model.classes_)
    color = 'white'
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=model.classes_)
    disp.plot()
    my_stringIObytes = io.BytesIO()
    plt.savefig(my_stringIObytes, format='jpg')
    my_stringIObytes.seek(0)
    my_base64_jpgData = base64.b64encode(my_stringIObytes.read()).decode()
    #temp = os.getcwd()
    #plt.savefig(temp + '\\backend\\static\\Images\\' + data['projectName'] + '.png')

    #data_uri = base64.b64encode(open('conf_matrix.png', 'rb').read()).decode('utf-8')
    #img_tag = '<img src="data:image/png;base64,{0}">'.format(data_uri)

    #encoded = fig_to_base64(fig)
    #my_html = '<img src="data:image/png;base64, {}">'.format(encoded.decode('utf-8'))


    # Send the Metrics
    Metrics = {"Validation": "Split",

               "Accuracy_Intro": 'Accuracy: ',
               "Precision_Intro": "Precision for Each Class: ",
               "Precision_micro_Intro": "Precision (Micro): ",
               "Precision_macro_Intro": "Precision (Macro): ",
               "F1_Intro": "F1 for each Class: ",
               "F1_micro_Intro": "F1 (Micro): ",
               "F1_macro_Intro": "F1 (Macro): ",

                "Accuracy": Accuracy,
                "Precision": Precision.tolist(),
                "Precision_micro": Precision_micro,
                "Precision_macro": Precision_macro,
                "F1": F1.tolist(),
                "F1_micro": F1_micro,
                "F1_macro": F1_macro,

                "cm_overall": my_base64_jpgData,
                
                "Val_Random_State": random_state,
                "Val_Shuffle": shuffle}

    Metrics.update(settings)

    return Metrics


def K_Fold(data):
    # convert csv to usable dataset
    df = getDataset(data['csvFileName'])

    length = df.shape[1] -1

    X = df[:,0:length]
    y = df[:,length]

    random_state = None
    if data["Random_State_Input"] != "":
        random_state = int(data["Random_State_Input"])
    shuffle = False
    if data["Shuffle"] == "True":
        shuffle = True

    if data["Stratify"] == "False":
        kf = KFold(n_splits=int(data[data['validation'] + "_Input"]), shuffle=shuffle, random_state = random_state)
    if data["Stratify"] == "True":
        kf = StratifiedKFold(n_splits=int(data[data['validation'] + "_Input"]), shuffle=shuffle, random_state = random_state)

    kf.get_n_splits(X)

    acc_list = []
    prec_list = []
    prec_micro_list = []
    prec_macro_list = []
    f1_list = []
    f1_micro_list = []
    f1_macro_list = []
    cm_list = []
    y_test_list = np.empty(1)
    y_predict_list = np.empty(1)

    for i, (train_index, test_index) in enumerate(kf.split(X)):
        print("Fold: " + str(i) + " ===============================")
        x_train = X[train_index]
        y_train = y[train_index]
        x_test = X[test_index]
        y_test = y[test_index]
            
        model, settings = MLA.createModel(data)

        model.fit(X[train_index], y[train_index])
    
        y_pred = model.predict(X[test_index])
    
        acc = accuracy_score(y[test_index], y_pred)
        prec = precision_score(y[test_index], y_pred, average=None)
        prec_micro = precision_score(y[test_index], y_pred, average='micro')
        prec_macro = precision_score(y[test_index], y_pred, average='macro')
        f1 = f1_score(y[test_index], y_pred, average=None)
        f1_micro = f1_score(y[test_index], y_pred, average='micro')
        f1_macro = f1_score(y[test_index], y_pred, average='macro')
    
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
        color = 'white'
        disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=model.classes_)
        disp.plot()
        my_stringIObytes = io.BytesIO()
        plt.savefig(my_stringIObytes, format='jpg')
        my_stringIObytes.seek(0)
        my_base64_jpgData = base64.b64encode(my_stringIObytes.read()).decode()
        cm_list.append(my_base64_jpgData)

    
    acc_list = np.array(acc_list)
    prec_list = np.array(prec_list)
    prec_micro_list = np.array(prec_micro_list)
    prec_macro_list = np.array(prec_macro_list)
    f1_list = np.array(f1_list)
    f1_micro_list = np.array(f1_micro_list)
    f1_macro_list = np.array(f1_macro_list)
    cm_list = np.array(cm_list)


    y_test_list = np.delete(y_test_list, 0)
    y_predict_list = np.delete(y_predict_list, 0)

    acc_average = np.average(acc_list)
    prec_average = np.average(prec_list, axis = 0)
    prec_micro_average = np.average(prec_micro_list)
    prec_macro_average = np.average(prec_macro_list)
    f1_average = np.average(f1_list, axis = 0)
    f1_micro_average = np.average(f1_micro_list)
    f1_macro_average = np.average(f1_macro_list)

    cm = confusion_matrix(y_test_list, y_predict_list, labels=model.classes_)
    color = 'white'
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=model.classes_)
    disp.plot()
    my_stringIObytes = io.BytesIO()
    plt.savefig(my_stringIObytes, format='jpg')
    my_stringIObytes.seek(0)
    my_base64_jpgData = base64.b64encode(my_stringIObytes.read()).decode()

    # Send the Metrics
    Metrics = {"Validation": "K-Fold",

               "Accuracy_Intro": 'Accuracy: ',
               "Precision_Intro": "Precision for Each Class: ",
               "Precision_micro_Intro": "Precision (Micro): ",
               "Precision_macro_Intro": "Precision (Macro): ",
               "F1_Intro": "F1 for each Class: ",
               "F1_micro_Intro": "F1 (Micro): ",
               "F1_macro_Intro": "F1 (Macro): ",

               "Accuracy_Intro_Overall": 'Average Accuracy: ',
               "Precision_Intro_Overall": "Average Precision for Each Class: ",
               "Precision_micro_Intro_Overall": "Average Precision (Micro): ",
               "Precision_macro_Intro_Overall": "Average Precision (Macro): ",
               "F1_Intro_Overall": "Average F1 for each Class: ",
               "F1_micro_Intro_Overall": "Average F1 (Micro): ",
               "F1_macro_Intro_Overall": "Average F1 (Macro): ",

                "acc_list": acc_list.tolist(), 
                "prec_list": prec_list.tolist(),
                "prec_micro_list": prec_micro_list.tolist(),
                "prec_macro_list": prec_macro_list.tolist(),
                "f1_list": f1_list.tolist(),
                "f1_micro_list": f1_micro_list.tolist(),
                "f1_macro_list": f1_macro_list.tolist(),
                "cm_list": cm_list.tolist(),
                "acc_average": acc_average,
                "prec_average": prec_average.tolist(),
                "prec_micro_average": prec_micro_average,
                "prec_macro_average": prec_macro_average,
                "f1_average": f1_average.tolist(),
                "f1_micro_average": f1_micro_average,
                "f1_macro_average": f1_macro_average,
                "cm_overall": my_base64_jpgData,
                
                "Val_Random_State": random_state,
                "Val_Shuffle": shuffle}

    Metrics.update(settings)

    return Metrics
