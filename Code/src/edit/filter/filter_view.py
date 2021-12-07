#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Main controller
"""

from PySide6.QtWidgets import QWidget, QFormLayout, QLineEdit, QListWidget, QCheckBox
from PySide6.QtGui import QDoubleValidator

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2021"
__credits__ = ["Lemahieu Antoine"]
__license__ = ""
__version__ = "0.1"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class filterView(QWidget):
    def __init__(self):
        super().__init__()
        self.filterListener = None

        low_frequency_line = QLineEdit()
        low_frequency_line.setValidator(QDoubleValidator())
        high_frequency_line = QLineEdit()
        high_frequency_line.setValidator(QDoubleValidator())
        channels_list = QListWidget()

        all_channels_names = ["a", "b", "c", "d", "e"]
        for i, channel in enumerate(all_channels_names):
            channels_list.insertItem(i, channel)

        self.form_layout = QFormLayout()
        self.form_layout.addRow("Low Frequency (Hz) : ", low_frequency_line)
        self.form_layout.addRow("High Frequency (Hz) : ", high_frequency_line)
        self.form_layout.addRow("Channels : ", channels_list)

        self.setLayout(self.form_layout)

    """
    Setters
    """
    def set_listener(self, listener):
        self.filterListener = listener
