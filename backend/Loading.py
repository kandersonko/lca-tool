import os
import sys
import io
import base64

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from pathlib import Path
from werkzeug.utils import secure_filename



def getDataset(fileName):
     # convert csv to usable dataset
    ## Manual location currently...Will be changed when implemented in Host.
    ## Should further be changed when database is setup.
    baseFolder = os.getcwd()

    ManualLoc = Path(baseFolder) / "tests/sampleCSV_MLA_Classification/"

    filename = secure_filename(fileName)
    dataset_path = ManualLoc / filename.lower()
    dataset = pd.read_csv(dataset_path)

    return dataset
