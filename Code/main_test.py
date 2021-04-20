# -*- coding: utf-8 -*-
# Python 3.6.2

"""
Parce que c'est marrant.
        _
    .__(.)<  (KWAK)
     \___)
~~~~~~~~~~~~~~~~~~~~
"""

import time
import mne
from mne.channels import make_standard_montage
from mne.decoding import CSP

import numpy as np
import pickle
import os
import sys

import matplotlib.pyplot as plt

from pyriemann.classification import MDM, FgMDM, TSclassifier
from pyriemann.estimation import Covariances, XdawnCovariances, CospCovariances, HankelCovariances
from pyriemann.tangentspace import TangentSpace, FGDA
from pyriemann.spatialfilters import Xdawn
from pyriemann.channelselection import ElectrodeSelection as pyriemannElectrodeSelection

from sklearn import preprocessing
from sklearn.model_selection import cross_val_score, KFold, LeaveOneOut, cross_val_predict, train_test_split
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn import svm, metrics, datasets, linear_model, tree
from sklearn.metrics import auc, roc_auc_score, roc_curve, confusion_matrix, plot_confusion_matrix, plot_roc_curve
from sklearn.neural_network import MLPClassifier

from scipy import signal

from mne.decoding import CSP as MNE_CSP
from mne.io import concatenate_raws, read_raw_edf
from mne.datasets import eegbci


# ============================================= #
# ====================MNIST==================== #
# ============================================= #


def read_one_file_data_line(line, number_of_channels_scanned, data, data_information):
    line_data = line.split("\t")
    if int(line_data[5]) >= 256 and int(line_data[4]) != -1:  #
        if number_of_channels_scanned == 0:
            data_information.append([])
            data.append([])

            # data_information[-1].append(int(line_data[0]))  # id
            data_information[-1].append(int(line_data[1]))  # event
            # data_information[-1].append(line_data[2])       # device
            # data_information[-1].append(line_data[3])       # channel
            data_information[-1].append(int(line_data[4]))  # code  / number
            # data_information[-1].append(int(line_data[5]))  # size
        new_data = []
        string = ""
        for char in line_data[6]:  # data
            if char == ",":
                new_data.append(float(string) / 1000)
                string = ""
            else:
                string += char
            if len(new_data) == 256:
                break
        if len(new_data) == 255:
            new_data.append(float(string) / 1000)
        numpy_data = np.asarray(new_data, dtype=np.float64, order='C')
        data[-1].append(numpy_data)
    return data_information, data


def read_mnist_epoc_file_data(file):
    """
    Read the mnist with epoc headset data file.
    Each event has 14 channels.
    :param file: opened mnist epoc data file.
    :return: data_information: List containing in order:
                id: integer, for reference.
                event: integer, used to distinguish same event captured at different brain locations.
                device: string, device initials, EP here.
                channel: string, channel name.
                code: integer, the digit
                size: integer, data size
             data: The EEG data. A list of size :
                number of event (up to 900000) * number of channels * number of data for this channel on this event.
    """
    data_information = []
    data = []
    number_of_channels_scanned = 0

    for line in file:
        data_information, data = read_one_file_data_line(line, number_of_channels_scanned, data, data_information)

        number_of_channels_scanned += 1
        if number_of_channels_scanned == 14:
            number_of_channels_scanned = 0
            # if len(data) == 10000:
            #    break

    return np.array(data_information), np.array(data, dtype=np.float64)


def save_npy_file(data, data_information):
    """
    Save the data, data information and data concatenated into npy files.
    """
    concatenated_data = np.empty((len(data), 14 * 256))
    for i in range(len(data)):
        concatenated_data[i] = np.concatenate(data[i])

    data_without_channels = []
    for i in range(len(data)):
        for j in range(len(data[i])):
            data_without_channels.append(data[i][j])
    data_without_channels = np.array(data_without_channels)

    path = "D:\\Cours\\Mémoire\\MasterThesis\\EEG_datasets\\MindBigData-MNIST-EPOC\\All_full\\"
    np.save(path + "data.npy", data)
    np.save(path + "data_information.npy", data_information)
    np.save(path + "data_concatenated.npy", concatenated_data)
    np.save(path + "data_without_channels.npy", data_without_channels)


def plot_mnist_epoc_file():
    file = ""
    try:
        file = open("D:\\Cours\\Mémoire\\MasterThesis\\EEG_datasets\\MindBigData-MNIST-EPOC\\mnist_epoc.txt")
    except:
        print("Error while reading the file.")
    finally:
        data_information, data = read_mnist_epoc_file_data(file)
        plot_one_mnist_epoc_data(data_information, data)
        file.close()


def plot_one_mnist_epoc_data(data_information, data):
    for i in range(14):
        x = np.linspace(0, len(data[i]) - 2, len(data[i]) - 1)
        plt.figure(figsize=(10, 3))
        plt.plot(x, data[i][1:])
        plt.xlabel("Time steps")
        plt.ylabel("EEG electrical signal")
        plt.title("EEG electrical signal by time, at 128Hz, for the " + data_information[i][3] + " channel")
        plt.show()


def read_mnist_insight_file_data(file, channels_number):
    data_information = []
    data = []
    counter = 0
    number_of_channels_scanned = 0

    print("Read")

    for line in file:
        counter += 1

        data_information, data = read_one_file_data_line(line, number_of_channels_scanned, data, data_information)

        number_of_channels_scanned += 1
        if number_of_channels_scanned == channels_number:
            number_of_channels_scanned = 0

        if counter == channels_number * 10:
            break

    return np.array(data_information), np.array(data, dtype=object)


def write_transformed_data(transformed_data):
    try:
        file = open(
            "D:\\Cours\\Mémoire\\MasterThesis\\EEG_datasets\\MindBigData-MNIST-Insight\\mnist_insight_transformed.txt",
            "w")
    except:
        print("Error while reading the file.")
    finally:
        print("Write")
        for i in range(len(transformed_data)):
            for j in range(len(transformed_data[i])):
                file.write(str(round(transformed_data[i][j], 4)))
                file.write("\t")
            file.write("\n")
        file.close()


def data_transformation():
    file = ""
    try:
        file = open("D:\\Cours\\Mémoire\\MasterThesis\\EEG_datasets\\MindBigData-MNIST-Insight\\mnist_insight.txt")
    except:
        print("Error while reading the file.")
    finally:
        channels_number = 5
        frequency = 128
        data_information, data = read_mnist_insight_file_data(file, channels_number)  # 2*3, 2*5*(~256)

        transformed_data = []
        for i in range(len(data_information)):  # event
            time_elapsed = 0
            for j in range(data_information[i][2]):  # epoch
                transformed_data.append([])
                # transformed_data[-1].append(time_elapsed)
                for k in range(channels_number):  # channels
                    transformed_data[-1].append(data[i][k][j] / 1000)
                time_elapsed += round(1000 / frequency, 4)

        # write_transformed_data(transformed_data)
        file.close()
        return data_information, transformed_data


# ====================================================== #
# ====================CLASSIFICATION==================== #
# ====================================================== #

def roc_curve_plot(false_positive_rate, true_positive_rate, roc_score, title):
    roc_score_legend = "SVC (AUC = " + str(round(roc_score, 2)) + ")"
    plt.plot(false_positive_rate, true_positive_rate, color='orange', label=roc_score_legend)
    plt.plot([0, 1], [0, 1], '--', color='b')
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title("ROC curve of " + title)     # Receiver operating characteristic
    plt.legend()
    plt.show()


def compute_ROC_curve_and_score(classifier, data_concatenated, y, title):
    y_scores = classifier.predict_proba(data_concatenated)[:, 1]
    roc_score = roc_auc_score(y, y_scores)
    false_positive_rate, true_positive_rate, thresholds = roc_curve(y, y_scores)
    roc_curve_plot(false_positive_rate, true_positive_rate, roc_score, title)


def compute_confusion_matrix(classifier, data_concatenated, y):
    plot_confusion_matrix(classifier, data_concatenated, y, normalize='true')
    plt.show()


def compute_vizualisation(classifier, data, y, title):
    compute_confusion_matrix(classifier, data, y)
    compute_ROC_curve_and_score(classifier, data, y, title)


def classification_run(data, data_concatenated, y):
    X_train, X_test, y_train, y_test = train_test_split(data_concatenated, y, random_state=42)

    print("Logistic Regression")
    # LogisticRegression(max_iter=10000)
    lr_clf = LogisticRegression(max_iter=10000)
    lr_clf.fit(X_train, y_train)
    print(lr_clf.score(X_test, y_test))
    compute_vizualisation(lr_clf, X_test, y_test, "Logistic Regression")

    print("Support Vector Machine")
    # svm_clf = svm.SVC(kernel='linear', C=1, random_state=42, probability=True)
    svm_clf = svm.SVC(kernel='linear', probability=True)
    svm_clf.fit(X_train, y_train)
    print(svm_clf.score(X_test, y_test))
    compute_vizualisation(svm_clf, X_test, y_test, "Support Vector Machine")


def mnist_epoc_classification():
    """
    Load the data and run the pipelines.
    """
    # data_path = "D:\\Cours\\Mémoire\\MasterThesis\\EEG_datasets\\MindBigData-MNIST-EPOC\\mnist_epoc.txt"
    # file = open(data_path)
    # data_information, data = read_mnist_epoc_file_data(file)
    # save_npy_file(data, data_information)

    # channels_names = ["AF3", "F7", "F3", "FC5", "T7", "P7", "O1", "O2", "P8", "T8", "FC6", "F4", "F8", "AF4"]
    # sampling_frequency = 128  # Hz
    # filter_lfreq = 1.
    # filter_hfreq = 20.
    # tmin, tmax = 0, 0

    # montage = make_standard_montage("standard_1020")
    # info = mne.create_info(ch_names=channels_names, ch_types=['eeg']*14, sfreq=sampling_frequency)
    # info.set_montage("standard_1020")

    # (n_epochs, n_channels, n_times)

    print("Load")
    data_path = "D:\\Cours\\Mémoire\\MasterThesis\\EEG_datasets\\MindBigData-MNIST-EPOC\\ZeroAndOne_full\\"
    data = np.load(data_path + "data.npy")
    data_information = np.load(data_path + "data_information.npy")
    data_concatenated = np.load(data_path + "data_concatenated.npy")

    y = []
    for i in range(len(data_information)):
        y.append(data_information[i][1])
    y = np.array(y)

    classification_run(data, data_concatenated, y)


def small_dataset():
    data_path = "D:\\Cours\\Mémoire\\MasterThesis\\EEG_datasets\\Psychophysics_1subject_80trials\\dataset.set"
    filter_lfreq = 0.
    filter_hfreq = 45.
    tmin, tmax = -1.0, 1.0  # start and end of the epoch around the event

    raw = mne.io.read_raw_eeglab(data_path, preload=True)

    raw.set_eeg_reference(ref_channels='average')
    picks = mne.pick_channels(raw.ch_names, include=[])
    # raw.filter(filter_lfreq, filter_hfreq, method="iir", picks=picks)
    events, events_dict = mne.events_from_annotations(raw)

    print("===")
    print(events)
    print("===")
    print(events_dict)

    fig = mne.viz.plot_events(events, event_id=events_dict, sfreq=raw.info['sfreq'], first_samp=raw.first_samp)

    epochs = mne.Epochs(raw, events, events_dict, tmin, tmax, proj=True, picks=picks, baseline=None, preload=True,
                        verbose=False)
    epochs_data = epochs.get_data()

    print("===")
    print(epochs)
    print("===")

    # Get data from epochs in a 3D array (epoch x channel x time)
    print(len(epochs_data))
    print(len(epochs_data[0]))
    print(len(epochs_data[0][0]))

    # ====================
    # np.save("test.npy", epochs_data)


def main():
    mnist_epoc_classification()


if __name__ == "__main__":
    main()
