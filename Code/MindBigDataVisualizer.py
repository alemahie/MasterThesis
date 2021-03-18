import matplotlib.pyplot as plt
import numpy as np


def read_input_file_data(file):
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


def plot_input_file():
    while True:
        print("Please enter a file name : ", end="")
        file_name = input()
        file_name = "MindBigData_Imagenet_Insight_n00007846_48383_1_794"
        if file_name == "exit":
            break
        else:
            file = ""
            try:
                file = open("D:\\Cours\\Mémoire\\MasterThesis\\MindBigData_Dataset\\MindBigData-Imagenet\\" + file_name + ".csv")
            except:
                print("This file doesn't exist, please enter a new name.")
            finally:
                channels_names, data = read_input_file_data(file)
                plot_file(channels_names, data)
                file.close()


def plot_file(channels_names, data):
    for i in range(5):
        x = np.linspace(0, len(data[i])-2, len(data[i])-1)
        plt.figure(figsize=(10, 3))
        plt.plot(x, data[i][1:])
        plt.xlabel("Time steps")
        plt.ylabel("EEG electrical signal")
        plt.title("EEG electrical signal by time, at 128Hz, for the " + channels_names[i] + " channel")
        plt.show()
