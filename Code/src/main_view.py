#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Main view
"""

from PySide6.QtWidgets import QMainWindow, QGridLayout, QLabel, QWidget

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2021"
__credits__ = ["Lemahieu Antoine"]
__license__ = ""
__version__ = "0.1"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class mainView(QMainWindow):
    def __init__(self):
        super().__init__()

        self.info_labels = ["Filename : ", "File Type : ", "Number of Channels : ", "Sampling Frequency (Hz) : ",
                            "Number of Epochs : ", "Epoch start (sec) : ", "Epoch end (sec) : ",
                            "Number of Frames/Frames per Epoch : ", "Reference : ", "Channel Locations : ",
                            "ICA : ", "Dataset Size (Mb) : "]

        self.centralWidget = QWidget()

        self.grid_layout = QGridLayout(self)
        self.centralWidget.setLayout(self.grid_layout)

        for i, info in enumerate(self.info_labels):
            self.grid_layout.addWidget(QLabel(info), i, 0)
        for i in range(12):
            self.grid_layout.addWidget(QLabel(str(i)), i, 1)

        self.setCentralWidget(self.centralWidget)

    def display_info(self, all_info):
        for i in range(12):
            label_item = self.grid_layout.itemAtPosition(i, 1).widget()
            label_item.setText(str(all_info[i]))
