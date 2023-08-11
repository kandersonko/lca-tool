import os
import sys
import io
import base64

from backend.Classes.NeuralNetworkFiles import NeuralNetwork

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from pathlib import Path
from werkzeug.utils import secure_filename

from sklearn.metrics import accuracy_score, f1_score, precision_score

from sklearn.metrics import ConfusionMatrixDisplay
from sklearn.metrics import confusion_matrix

from backend.Classes.PreoptimizationFiles import Preoptimization
from backend.Classes.NeuralNetworkFiles import Compiler

from backend import Loading

def Split(data):
    try:
        # convert csv to usable dataset
        ##df_act = getDataset(data['csvFileName'])
        df_act = pd.read_csv(data['csvFile'], index_col=None)
        
        # Cycle through the choices of preotimization
        for i in range(int(data["preoptCounter"])):
            # Get the choice of preoptimization.
            preopt_method = data["Preopt_" + str(i)]
            # Perform the preoptimization on the dataset.
            df_act = Preoptimization.perform_Preopt(data, i, df_act)

        df = df_act.to_numpy()

        # Split dataset to training and testing set
        random_state = None
        if data["NN_Random_State_Input"] != "":
            random_state = int(data["NN_Random_State_Input"])
        shuffle = False
        if data["NN_Shuffle"] == "True":
            shuffle = True
    
        train_set, test_set = train_test_split(df, test_size=float(data["NN_Split_Test_Input"]), shuffle=shuffle, random_state = random_state)

        length = train_set.shape[1] -1

        x_train = train_set[:,0:length]
        y_train = train_set[:,length]
        x_test = test_set[:,0:length]
        y_test = test_set[:,length]

        y_train = tuple(y_train)
        y_test = tuple(y_test)

        x_train = np.asarray(x_train).astype('float32')
        y_train = np.array(y_train)
        x_test = np.asarray(x_test).astype('float32')
        y_test = np.array(y_test)

        model = NeuralNetwork.createModel(data)

        Compiler.compileModel(model, data)
        #model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

        history = model.fit(x_train, y_train, epochs=10, batch_size=7)

        y_pred = model.predict(x_test)
        y_pred = np.argmax(y_pred, axis = 1)

        y_test = np.argmax(y_test, axis = 1)

        labels = np.unique(y_test)

        # Obtain the Metrics
        Accuracy = accuracy_score(y_test, y_pred)
        F1 = f1_score(y_test, y_pred, average=None)
        F1_micro = f1_score(y_test, y_pred, average='micro')
        F1_macro = f1_score(y_test, y_pred, average='macro')
        Precision = precision_score(y_test, y_pred, average=None)
        Precision_micro = precision_score(y_test, y_pred, average='micro')
        Precision_macro = precision_score(y_test, y_pred, average='macro')

        # Create confusion matrix
        confusion_matrix(y_test, y_pred)

        cm = confusion_matrix(y_test, y_pred, labels=labels)
        color = 'white'
        disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=labels)
        disp.plot()
        my_stringIObytes = io.BytesIO()
        plt.savefig(my_stringIObytes, format='jpg')
        my_stringIObytes.seek(0)
        my_base64_jpgData = base64.b64encode(my_stringIObytes.read()).decode()
        
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

        #Metrics.update(settings)

        status = "worked"
        msg = ""

        return status, msg, Metrics

    except Exception as e:
        Metrics = ""
        msg = str(e)
        status = "error"

        return status, msg, Metrics