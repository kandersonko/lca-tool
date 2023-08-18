import base64

import pandas as pd
import numpy as np

from backend.Classes.NeuralNetworkFiles import Callback
from backend.Classes import HyperParameters

import matplotlib.pyplot as plt

from tensorflow import keras
import tensorflow as tf

# Create a list of Callbacks to select from.
list_Callbacks = []

def getCallbacks():
    return list_Callbacks

# Add after figureing out the model save issue.
## ModelCheckpoint
Name = "ModelCheckpoint"
Display_Name = "Model Checkpoint"
Definition = ['Callback to save the Keras model or model weights at some frequency.\n\nModelCheckpoint callback is used in conjunction with training using model.fit() to save a model or weights (in a checkpoint file) at some interval, so the model or weights can be loaded later to continue the training from the state saved.\n\nA few options this callback provides include:\n\nWhether to only keep the model that has achieved the "best performance" so far, or whether to save the model at the end of every epoch regardless of performance.\nDefinition of "best"; which quantity to monitor and whether it should be maximized or minimized.\nThe frequency it should save at. Currently, the callback supports saving at the end of every epoch, or after a fixed number of training batches.\nWhether only weights are saved, or the whole model is saved.\n\nNote: If you get WARNING:tensorflow:Can save best model only with <name> available, skipping see the description of the monitor argument for details on how to get this right.']
# Will have to decide for the websites storage system.
#Parameter_0 = {"Name":"filepath", "Type": ["int"], "Default_option":"", "Default_value":"", "Possible":["int"],
#             "Definition":'Callback to save the Keras model or model weights at some frequency.\n\nModelCheckpoint callback is used in conjunction with training using model.fit() to save a model or weights (in a checkpoint file) at some interval, so the model or weights can be loaded later to continue the training from the state saved.\n\nA few options this callback provides include:\n\nWhether to only keep the model that has achieved the "best performance" so far, or whether to save the model at the end of every epoch regardless of performance.\nDefinition of "best"; which quantity to monitor and whether it should be maximized or minimized.\nThe frequency it should save at. Currently, the callback supports saving at the end of every epoch, or after a fixed number of training batches.\nWhether only weights are saved, or the whole model is saved.\n\nNote: If you get WARNING:tensorflow:Can save best model only with <name> available, skipping see the description of the monitor argument for details on how to get this right.'}
Parameter_0 = {"Name":"monitor", "Type": ["option"], "Default_option":"val_loss", "Default_value":"val_loss", "Possible":["loss","val_loss","accuracy"],
             "Definition":"The metric name to monitor."}
Parameter_1 = {"Name":"verbose", "Type": ["int"], "Default_option":0, "Default_value":0, "Possible":["int"],
             "Definition":"Verbosity mode, 0 or 1. Mode 0 is silent, and mode 1 displays messages when the callback takes an action."}
Parameter_2 = {"Name":"save_best_only", "Type": ["bool"], "Default_option":False, "Default_value":False, "Possible":[True,False],
             "Definition":"if save_best_only=True, it only saves when the model is considered the 'best' and the latest best model according to the quantity monitored will not be overwritten. If filepath doesn't contain formatting options like {epoch} then filepath will be overwritten by each new better model."}
Parameter_3 = {"Name":"save_weights_only", "Type": ["bool"], "Default_option":False, "Default_value":False, "Possible":[True,False],
             "Definition":"if True, then only the model's weights will be saved (model.save_weights(filepath)), else the full model is saved (model.save(filepath))."}
Parameter_4 = {"Name":"mode", "Type": ["option"], "Default_option":"auto", "Default_value":"auto", "Possible":["auto","min","max"],
             "Definition":"one of {'auto', 'min', 'max'}. If save_best_only=True, the decision to overwrite the current save file is made based on either the maximization or the minimization of the monitored quantity. For val_acc, this should be max, for val_loss this should be min, etc. In auto mode, the mode is set to max if the quantities monitored are 'acc' or start with 'fmeasure' and are set to min for the rest of the quantities."}
Parameter_5 = {"Name":"save_freq", "Type": ["option_int"], "Default_option":"epoch", "Default_value":"epoch", "Possible":["epoch","int"],
             "Definition":"'epoch' or integer. When using 'epoch', the callback saves the model after each epoch. When using integer, the callback saves the model at end of this many batches. If the Model is compiled with steps_per_execution=N, then the saving criteria will be checked every Nth batch. Note that if the saving isn't aligned to epochs, the monitored metric may potentially be less reliable (it could reflect as little as 1 batch, since the metrics get reset every epoch). Defaults to 'epoch'."}
## Removed due to experimental options.
#Parameter_7 = {"Name":"options", "Type": ["bool"], "Default_option":"None", "Default_value":"None", "Possible":[True,False,"None"],
#             "Definition":"A boolean specifying whether the placeholder to be created is sparse. Only one of 'ragged' and 'sparse' can be True. Note that, if sparse is False, sparse tensors can still be passed into the input - they will be densified with a default value of 0."}
Parameter_6 = {"Name":"initial_value_threshold", "Type": ["float"], "Default_option":"None", "Default_value":"None", "Possible":["float"],
             "Definition":"Floating point initial 'best' value of the metric to be monitored. Only applies if save_best_value=True. Only overwrites the model weights already saved if the performance of current model is better than this value."}

Parameters = {"Parameter_0":Parameter_0, "Parameter_1":Parameter_1, "Parameter_2":Parameter_2, "Parameter_3":Parameter_3,
              "Parameter_4":Parameter_4, "Parameter_5":Parameter_5, "Parameter_6":Parameter_6}

#list_Callbacks.append(Callback.Callback(Name, Display_Name, Definition, Parameters))

# Add after figureing out the model save issue.
## BackupAndRestore
Name = "BackupAndRestore"
Display_Name = "Backup And Restore"
Definition = ['Callback to back up and restore the training state.\n\nBackupAndRestore callback is intended to recover training from an interruption that has happened in the middle of a Model.fit execution, by backing up the training states in a temporary checkpoint file (with the help of a tf.train.CheckpointManager), at the end of each epoch. Each backup overwrites the previously written checkpoint file, so at any given time there is at most one such checkpoint file for backup/restoring purpose.\n\nIf training restarts before completion, the training state (which includes the Model weights and epoch number) is restored to the most recently saved state at the beginning of a new Model.fit run. At the completion of a Model.fit run, the temporary checkpoint file is deleted.\n\nNote that the user is responsible to bring jobs back after the interruption. This callback is important for the backup and restore mechanism for fault tolerance purpose, and the model to be restored from a previous checkpoint is expected to be the same as the one used to back up. If user changes arguments passed to compile or fit, the checkpoint saved for fault tolerance can become invalid.\n\nNote:\n\nThis callback is not compatible with eager execution disabled.\nA checkpoint is saved at the end of each epoch. After restoring, Model.fit redoes any partial work during the unfinished epoch in which the training got restarted (so the work done before the interruption doesn`t affect the final model state).\nThis works for both single worker and multi-worker modes. When Model.fit is used with tf.distribute, it supports tf.distribute.MirroredStrategy, tf.distribute.MultiWorkerMirroredStrategy, tf.distribute.TPUStrategy, and tf.distribute.experimental.ParameterServerStrategy.']
# Will have to decide for the websites storage system.
#Parameter_0 = {"Name":"backup_dir", "Type": ["int"], "Default_option":"", "Default_value":"", "Possible":["int"],
#             "Definition":'String, path to store the checkpoint. e.g. backup_dir = os.path.join(working_dir, 'backup'). This is the directory in which the system stores temporary files to recover the model from jobs terminated unexpectedly. The directory cannot be reused elsewhere to store other files, e.g. by the BackupAndRestore callback of another training run, or by another callback (e.g. ModelCheckpoint) of the same training.'}
Parameter_0 = {"Name":"save_freq", "Type": ["option_int"], "Default_option":"epoch", "Default_value":"epoch", "Possible":["epoch","int","False"],
             "Definition":"'epoch', integer, or False. When set to 'epoch' the callback saves the checkpoint at the end of each epoch. When set to an integer, the callback saves the checkpoint every save_freq batches. Set save_freq to False if only using preemption checkpointing (with save_before_preemption=True)."}
Parameter_1 = {"Name":"delete_checkpoint", "Type": ["bool"], "Default_option":True, "Default_value":True, "Possible":["bool"],
             "Definition":"Boolean, default to True. This BackupAndRestore callback works by saving a checkpoint to back up the training state. If delete_checkpoint=True, the checkpoint will be deleted after training is finished. Use False if you'd like to keep the checkpoint for future usage."}
Parameter_2 = {"Name":"save_before_preemption", "Type": ["bool"], "Default_option":False, "Default_value":False, "Possible":[True,False],
             "Definition":"A boolean value instructing whether to turn on the automatic checkpoint saving for preemption/maintenance events. This only supports tf.distribute.MultiWorkerMirroredStrategy on Google Cloud Platform or Google Borg for now."}

Parameters = {"Parameter_0":Parameter_0, "Parameter_1":Parameter_1, "Parameter_2":Parameter_2}

#list_Callbacks.append(Callback.Callback(Name, Display_Name, Definition, Parameters))

## TensorBoard

## EarlyStopping
Name = "EarlyStopping"
Display_Name = "Early Stopping"
Definition = ["Stop training when a monitored metric has stopped improving.\n\nAssuming the goal of a training is to minimize the loss. With this, the metric to be monitored would be 'loss', and mode would be 'min'. A model.fit() training loop will check at end of every epoch whether the loss is no longer decreasing, considering the min_delta and patience if applicable. Once it`s found no longer decreasing, model.stop_training is marked True and the training terminates.\n\nThe quantity to be monitored needs to be available in logs dict. To make it so, pass the loss or metrics at model.compile().# Will have to decide for the websites storage system."]
Parameter_0 = {"Name":"monitor", "Type": ["option"], "Default_option":"val_loss", "Default_value":"val_loss", "Possible":["loss","val_loss","accuracy"],
             "Definition":"Quantity to be monitored."}
Parameter_1 = {"Name":"min_delta", "Type": ["float"], "Default_option":0, "Default_value":0, "Possible":["float"],
             "Definition":"Minimum change in the monitored quantity to qualify as an improvement, i.e. an absolute change of less than min_delta, will count as no improvement."}
Parameter_2 = {"Name":"patience", "Type": ["int"], "Default_option":0, "Default_value":0, "Possible":["int"],
             "Definition":"Number of epochs with no improvement after which training will be stopped."}
Parameter_3 = {"Name":"verbose", "Type": ["int"], "Default_option":0, "Default_value":0, "Possible":["int"],
             "Definition":"Verbosity mode, 0 or 1. Mode 0 is silent, and mode 1 displays messages when the callback takes an action."}
Parameter_4 = {"Name":"mode", "Type": ["option"], "Default_option":"auto", "Default_value":"auto", "Possible":["auto","min","max"],
             "Definition":'One of {"auto", "min", "max"}. In min mode, training will stop when the quantity monitored has stopped decreasing; in "max" mode it will stop when the quantity monitored has stopped increasing; in "auto" mode, the direction is automatically inferred from the name of the monitored quantity.'}
Parameter_5 = {"Name":"baseline", "Type": ["float"], "Default_option":"", "Default_value":"", "Possible":["float"],
             "Definition":"Baseline value for the monitored quantity. Training will stop if the model doesn't show improvement over the baseline."}
Parameter_6 = {"Name":"restore_best_weights", "Type": ["bool"], "Default_option":False, "Default_value":False, "Possible":[True,False],
             "Definition":"Whether to restore model weights from the epoch with the best value of the monitored quantity. If False, the model weights obtained at the last step of training are used. An epoch will be restored regardless of the performance relative to the baseline. If no epoch improves on baseline, training will run for patience epochs and restore weights from the best epoch in that set."}
# For some reason, this callback doesnt actually have this function. Even though listed on keras.
#Parameter_7 = {"Name":"start_from_epoch", "Type": ["int"], "Default_option":0, "Default_value":0, "Possible":["int"],
#             "Definition":"Number of epochs to wait before starting to monitor improvement. This allows for a warm-up period in which no improvement is expected and thus training will not be stopped."}



Parameters = {"Parameter_0":Parameter_0, "Parameter_1":Parameter_1, "Parameter_2":Parameter_2, "Parameter_3":Parameter_3,
              "Parameter_4":Parameter_4, "Parameter_5":Parameter_5, "Parameter_6":Parameter_6}

list_Callbacks.append(Callback.Callback(Name, Display_Name, Definition, Parameters))

## LearningRateScheduler

## ReduceLROnPlateau
Name = "ReduceLROnPlateau"
Display_Name = "Reduce Learning Rate on Plateau"
Definition = ["Reduce learning rate when a metric has stopped improving.\n\nModels often benefit from reducing the learning rate by a factor of 2-10 once learning stagnates. This callback monitors a quantity and if no improvement is seen for a 'patience' number of epochs, the learning rate is reduced."]
Parameter_0 = {"Name":"monitor", "Type": ["option"], "Default_option":"val_loss", "Default_value":"val_loss", "Possible":["loss","val_loss","accuracy"],
             "Definition":"Quantity to be monitored."}
Parameter_1 = {"Name":"factor", "Type": ["float"], "Default_option":0.1, "Default_value":0.1, "Possible":["float"],
             "Definition":"Factor by which the learning rate will be reduced. new_lr = lr * factor."}
Parameter_2 = {"Name":"patience", "Type": ["int"], "Default_option":10, "Default_value":10, "Possible":["int"],
             "Definition":"Number of epochs with no improvement after which training will be stopped."}
Parameter_3 = {"Name":"verbose", "Type": ["int"], "Default_option":0, "Default_value":0, "Possible":["int"],
             "Definition":"Verbosity mode, 0 or 1. Mode 0 is silent, and mode 1 displays messages when the callback takes an action."}
Parameter_4 = {"Name":"mode", "Type": ["option"], "Default_option":"auto", "Default_value":"auto", "Possible":["auto","min","max"],
             "Definition":'One of {"auto", "min", "max"}. In min mode, training will stop when the quantity monitored has stopped decreasing; in "max" mode it will stop when the quantity monitored has stopped increasing; in "auto" mode, the direction is automatically inferred from the name of the monitored quantity.'}
Parameter_5 = {"Name":"min_delta", "Type": ["float"], "Default_option":0.0001, "Default_value":0.0001, "Possible":["float"],
             "Definition":"Threshold for measuring the new optimum, to only focus on significant changes."}
Parameter_6 = {"Name":"cooldown", "Type": ["int"], "Default_option":0, "Default_value":0, "Possible":["int"],
             "Definition":"Number of epochs to wait before resuming normal operation after lr has been reduced."}
Parameter_7 = {"Name":"min_lr", "Type": ["float"], "Default_option":0, "Default_value":0, "Possible":["float"],
             "Definition":"lower bound on the learning rate."}

Parameters = {"Parameter_0":Parameter_0, "Parameter_1":Parameter_1, "Parameter_2":Parameter_2, "Parameter_3":Parameter_3,
              "Parameter_4":Parameter_4, "Parameter_5":Parameter_5, "Parameter_6":Parameter_6, "Parameter_7":Parameter_7}

list_Callbacks.append(Callback.Callback(Name, Display_Name, Definition, Parameters))


## RemoteMonitor

## LambdaCallback

## TerminateOnNaN

## CSVLogger

## ProgbarLogger



# Creates the Callbacks to be added to the model fit method.
def create_callback(data, i):
    # get callback method name
    callback = data["Callback_" + str(i)]

    # get the chosen settings for the layer
    Parameters = HyperParameters.getParameters(data["Callback_" + str(i)], list_Callbacks)
    settings = HyperParameters.getSettings(data, Parameters, i, Callback.getName())

    new_callback = ""

    ## EarlyStopping
    if callback == "EarlyStopping":

        # Create the layer
        new_callback = tf.keras.callbacks.EarlyStopping(monitor=settings["Parameter_0"], min_delta=settings["Parameter_1"], patience=settings["Parameter_2"],
                                                        verbose=settings["Parameter_3"], mode=settings["Parameter_4"], baseline=settings["Parameter_5"],
                                                        restore_best_weights=settings["Parameter_6"])
    
    ## ReduceLROnPlateau
    if callback == "ReduceLROnPlateau":

        new_callback = tf.keras.callbacks.ReduceLROnPlateau(monitor=settings["Parameter_0"], factor=settings["Parameter_1"], patience=settings["Parameter_2"],
                                                            verbose=settings["Parameter_3"], mode=settings["Parameter_4"], min_delta=settings["Parameter_5"],
                                                            cooldown=settings["Parameter_6"], min_lr=settings["Parameter_7"])
        
    return new_callback



# Method to pull all parameters from a given callback option
def getParameters(Callback_Name):
    Parameters = {}
    
    # Check Core
    for callback in list_Callbacks:
        if callback.getName() == Callback_Name:
            Parameters = callback.getParameters()
            return Parameters

    return Parameters

def createCallbacks(data):

    if int(data["callbackCounter"]) > 0:
        set_callbacks = []

        for i in range(int(data["callbackCounter"])):
            callback = create_callback(data, i)
            set_callbacks.append(callback)
    else:
        set_callbacks = None

    return set_callbacks

