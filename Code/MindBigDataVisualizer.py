import matplotlib.pyplot as plt
import numpy as np


# ================================================ #
# ====================IMAGENET==================== #
# ================================================ #


def read_imagenet_file_data(file):
    data = []
    channels_names = []
    for line in file:
        data.append([])
        string = ""
        first = True
        for char in line:
            if char == ',':
                if not first:
                    data[-1].append(float(string))
                else:
                    channels_names.append(string)
                    first = False
                string = ""
            else:
                string += char
    return channels_names, data


def plot_imagenet_file():
    while True:
        print("Please enter a file name : ", end="")
        file_name = input()
        file_name = "MindBigData_Imagenet_Insight_n00007846_48383_1_794"
        if file_name == "exit":
            break
        else:
            file = ""
            try:
                file = open("D:\\Cours\\Mémoire\\MasterThesis\\EEG_datasets\\MindBigData-Imagenet\\" + file_name + ".csv")
            except:
                print("This file doesn't exist, please enter a new name.")
            finally:
                channels_names, data = read_imagenet_file_data(file)
                plot_imagenet_data(channels_names, data)
                file.close()


def plot_imagenet_data(channels_names, data):
    for i in range(5):
        x = np.linspace(0, len(data[i])-2, len(data[i])-1)
        plt.figure(figsize=(10, 3))
        plt.plot(x, data[i][1:])
        plt.xlabel("Time steps")
        plt.ylabel("EEG electrical signal")
        plt.title("EEG electrical signal by time, at 128Hz, for the " + channels_names[i] + " channel")
        plt.show()


# ============================================= #
# ====================MNIST==================== #
# ============================================= #


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
             data: The EEG data.
    """
    data_information = []
    data = []
    counter = 0
    for line in file:
        counter += 1
        data_information.append([])
        data.append([])

        line_data = line.split("\t")
        data_information[-1].append(int(line_data[0]))  # id
        data_information[-1].append(int(line_data[1]))  # event
        data_information[-1].append(line_data[2])       # device
        data_information[-1].append(line_data[3])       # channel
        data_information[-1].append(int(line_data[4]))  # code
        data_information[-1].append(int(line_data[5]))  # size

        string = ""
        for char in line_data[6]:   # data
            if char == ",":
                data[-1].append(float(string))
                string = ""
            else:
                string += char

        if counter == 1400:
            break

    return data_information, data


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
        x = np.linspace(0, len(data[i])-2, len(data[i])-1)
        plt.figure(figsize=(10, 3))
        plt.plot(x, data[i][1:])
        plt.xlabel("Time steps")
        plt.ylabel("EEG electrical signal")
        plt.title("EEG electrical signal by time, at 128Hz, for the " + data_information[i][3] + " channel")
        plt.show()
