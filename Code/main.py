# -*- coding: utf-8 -*-
# Python 3.6.2

import mne
from mne.decoding import CSP

import numpy as np

import matplotlib.pyplot as plt

from pyriemann.classification import MDM
from pyriemann.estimation import Covariances, XdawnCovariances
from pyriemann.spatialfilters import Xdawn

from sklearn import preprocessing
from sklearn.model_selection import cross_val_score, KFold
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn import svm
from sklearn.metrics import roc_auc_score, roc_curve, plot_confusion_matrix
from sklearn.decomposition import FastICA

from sklearn.datasets import load_digits

from scipy import signal


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


def xDawn_Cov_MDM(epochs, y):
    print("xDawn_Cov_MDM")
    cross_val = KFold(n_splits=5, shuffle=True, random_state=43)

    x_dawn = mne.preprocessing.Xdawn()
    data = x_dawn.fit_transform(epochs, y)

    cov_data = Covariances("oas").transform(data)       # Compute covariance matrices

    mdm = MDM(metric=dict(mean='riemann', distance='riemann'))
    scores = cross_val_score(mdm, cov_data, y, cv=cross_val, n_jobs=1)
    final_score = np.mean(scores)
    print(final_score)  # 51.9
    return final_score


def xDawn_CSP_LR(epochs, y):
    print("xDawn_CSP_LR")
    cross_val = KFold(n_splits=5, shuffle=True, random_state=43)

    x_dawn = mne.preprocessing.Xdawn()
    data = x_dawn.fit_transform(epochs, y)

    csp = CSP(n_components=4, reg="ledoit_wolf", log=False)
    lr = LogisticRegression(max_iter=10000)
    csp_lr = Pipeline([("CSP", csp), ("LogisticRegression", lr)])
    scores = cross_val_score(csp_lr, data, y, cv=cross_val, n_jobs=1)
    final_score = np.mean(scores)
    print(final_score)  # 50.5
    return final_score


def CSP_LR(epochs, y):
    print("xDawn_CSP_LR")
    cross_val = KFold(n_splits=5, shuffle=True, random_state=43)

    csp = CSP(n_components=4, reg="ledoit_wolf", log=False)
    lr = LogisticRegression(max_iter=10000)
    csp_lr = Pipeline([("CSP", csp), ("LogisticRegression", lr)])
    scores = cross_val_score(csp_lr, epochs.get_data(), y, cv=cross_val, n_jobs=1)
    final_score = np.mean(scores)
    print(final_score)  # 50.6
    return final_score


def cov_MDM(epochs, y):
    print("cov_MDM")
    cross_val = KFold(n_splits=5, shuffle=True, random_state=43)

    cov_data = Covariances("oas").transform(epochs.get_data())  # Compute covariance matrices

    mdm = MDM(metric=dict(mean='riemann', distance='riemann'))
    scores = cross_val_score(mdm, cov_data, y, cv=cross_val, n_jobs=1)
    final_score = np.mean(scores)
    print(final_score)  # 51.8
    return final_score


def cov_LR(epochs, y):
    print("cov_LR")
    cross_val = KFold(n_splits=5, shuffle=True, random_state=43)

    cov_data = Covariances("oas").transform(epochs.get_data())  # Compute covariance matrices

    data_shape = cov_data.shape
    cov_data_shaped = cov_data.reshape((data_shape[0], data_shape[1]*data_shape[2]))

    lr_clf = LogisticRegression(max_iter=10000)
    scores = cross_val_score(lr_clf, cov_data_shaped, y, cv=cross_val)
    final_score = np.mean(scores)
    print(final_score)  # 50.5
    return final_score


def logistic_regression(epochs, y):
    print("Logistic Regression")
    cross_val = KFold(n_splits=5, shuffle=True, random_state=43)

    data = epochs.get_data()
    data_shape = data.shape
    data = data.reshape((data_shape[0], data_shape[1]*data_shape[2]))

    lr_clf = LogisticRegression(max_iter=10000)
    scores = cross_val_score(lr_clf, data, y, cv=cross_val, n_jobs=1)
    final_score = np.mean(scores)
    print(final_score)  # 59.2
    return final_score


def xDawn_LR(epochs, y):
    print("xDawn LR")
    cross_val = KFold(n_splits=5, shuffle=True, random_state=43)

    x_dawn = mne.preprocessing.Xdawn()
    data = x_dawn.fit_transform(epochs, y)

    data_shape = data.shape
    data = data.reshape((data_shape[0], data_shape[1]*data_shape[2]))

    lr_clf = LogisticRegression(max_iter=10000)
    scores = cross_val_score(lr_clf, data, y, cv=cross_val, n_jobs=1)
    final_score = np.mean(scores)
    print(final_score)  # 59.0
    return final_score


def SVM(epochs, y):
    print("Support Vector Machine")
    cross_val = KFold(n_splits=5, shuffle=True, random_state=43)
    data = epochs.get_data()
    data_shape = data.shape
    data = data.reshape((data_shape[0], data_shape[1]*data_shape[2]))

    svm_clf = svm.SVC(kernel='linear', probability=True)
    scores = cross_val_score(svm_clf, data, y, cv=cross_val)
    final_score = np.mean(scores)
    print(final_score)  # 59.5
    # compute_vizualisation(svm_clf, X_test, y_test, "Support Vector Machine")
    return final_score


def cov_SVM(epochs, y):
    print("cov_SVM")
    cross_val = KFold(n_splits=5, shuffle=True, random_state=43)

    cov_data = Covariances("oas").transform(epochs.get_data())  # Compute covariance matrices

    data_shape = cov_data.shape
    cov_data_shaped = cov_data.reshape((data_shape[0], data_shape[1]*data_shape[2]))

    svm_clf = svm.SVC(kernel='linear', probability=True)
    scores = cross_val_score(svm_clf, cov_data_shaped, y, cv=cross_val)
    final_score = np.mean(scores)
    print(final_score)  # 50.7
    # compute_vizualisation(svm_clf, X_test, y_test, "Support Vector Machine")
    return final_score


def PSD_LR(epochs, y):
    print("Power spectral density LR")
    cross_val = KFold(n_splits=5, shuffle=True, random_state=43)

    data = epochs.get_data()
    psd_data = signal.welch(data)

    # data_shape = data.shape
    # data = data.reshape((data_shape[0], data_shape[1]*data_shape[2]))

    lr_clf = LogisticRegression(max_iter=10000)
    scores = cross_val_score(lr_clf, psd_data, y, cv=cross_val, n_jobs=1)
    final_score = np.mean(scores)
    print(final_score)
    return final_score


def ICA_LR(epochs, y):
    print("ICA LR")
    cross_val = KFold(n_splits=5, shuffle=True, random_state=43)

    data = epochs.get_data()
    data_shape = data.shape
    data = data.reshape((data_shape[0], data_shape[1]*data_shape[2]))
    transformer = FastICA(max_iter=1000, random_state=43)    # n_components=50 ,
    data_transformed = transformer.fit_transform(data)

    lr_clf = LogisticRegression(max_iter=10000)
    scores = cross_val_score(lr_clf, data_transformed, y, cv=cross_val, n_jobs=1)
    final_score = np.mean(scores)
    print(final_score)
    return final_score


def classification_run(epochs, y):
    all_results = []
    all_results.append(xDawn_Cov_MDM(epochs, y))
    all_results.append(xDawn_CSP_LR(epochs, y))
    all_results.append(CSP_LR(epochs, y))
    all_results.append(cov_MDM(epochs, y))
    all_results.append(cov_LR(epochs, y))
    all_results.append(logistic_regression(epochs, y))
    all_results.append(xDawn_LR(epochs, y))
    all_results.append(SVM(epochs, y))
    all_results.append(cov_SVM(epochs, y))
    print(all_results)


def epochs_from_data(data, data_information):
    channels_names = ["AF3", "F7", "F3", "FC5", "T7", "P7", "O1", "O2", "P8", "T8", "FC6", "F4", "F8", "AF4"]
    # channels_names = ["P7", "O1", "O2", "P8"]
    sampling_frequency = 128  # Hz
    filter_lfreq = 1.0
    filter_hfreq = 40.0
    tmin, tmax = 0, 1

    """
    new_data = []
    for i in range(len(data)):
        add = []
        add.append(data[i][6])
        add.append(data[i][7])
        add.append(data[i][8])
        add.append(data[i][9])
        new_data.append(add)
    data = np.array(new_data)
    """

    event_id = {'one': 1, 'zero': 0}
    info = mne.create_info(ch_names=channels_names, ch_types=['eeg']*len(channels_names), sfreq=sampling_frequency)
    info.set_montage("standard_1020")

    epochs = mne.EpochsArray(data, info, events=data_information, event_id=event_id)
    epochs.crop(tmin, tmax)

    epochs.filter(filter_lfreq, filter_hfreq, method="iir")

    return epochs


def mnist_epoc_classification():
    """
    Load the data and run the pipelines.
    """
    # data_path = "D:\\Cours\\Mémoire\\MasterThesis\\EEG_datasets\\MindBigData-MNIST-EPOC\\mnist_epoc.txt"
    # file = open(data_path)
    # data_information, data = read_mnist_epoc_file_data(file)
    # save_npy_file(data, data_information)

    print("Load")
    data_path = "D:\\Cours\\Mémoire\\MasterThesis\\EEG_datasets\\MindBigData-MNIST-EPOC\\ZeroAndOne_full\\"
    data = np.load(data_path + "data.npy")
    data_information = np.load(data_path + "data_information.npy")

    events = []
    for i in range(len(data_information)):
        events.append([data_information[i][0], 0, data_information[i][1]])
    data_information = np.array(events)

    y = []
    for i in range(len(data_information)):
        y.append(data_information[i][2])
    y = np.array(y)

    epochs = epochs_from_data(data, data_information)
    classification_run(epochs, y)


def main():
    mnist_epoc_classification()


if __name__ == "__main__":
    main()
