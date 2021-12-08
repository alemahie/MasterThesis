#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Main controller
"""

from PySide6.QtWidgets import QWidget, QGridLayout, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel, QCheckBox, \
                              QScrollArea, QPushButton
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
    def __init__(self, all_channels_names):
        super().__init__()
        self.filter_listener = None

        self.low_frequency_line = QLineEdit()
        self.low_frequency_line.setText("0,1")
        self.low_frequency_line.setValidator(QDoubleValidator())
        self.high_frequency_line = QLineEdit()
        self.high_frequency_line.setText("45")
        self.high_frequency_line.setValidator(QDoubleValidator())

        self.channels_widget = QWidget()
        self.channels_vbox_layout = QVBoxLayout()

        self.select_unselect_widget = QWidget()
        self.select_unselect_hbox_layout = QHBoxLayout()
        self.select_all_channels = QPushButton("&Select All", self)
        self.select_all_channels.clicked.connect(self.select_all_channels_trigger)
        self.unselect_all_channels = QPushButton("&Unselect All", self)
        self.unselect_all_channels.clicked.connect(self.unselect_all_channels_trigger)
        self.select_unselect_hbox_layout.addWidget(self.select_all_channels)
        self.select_unselect_hbox_layout.addWidget(self.unselect_all_channels)
        self.select_unselect_widget.setLayout(self.select_unselect_hbox_layout)

        self.channels_vbox_layout.addWidget(self.select_unselect_widget)
        self.create_check_boxes(all_channels_names)
        self.channels_widget.setLayout(self.channels_vbox_layout)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.channels_widget)

        self.cancel = QPushButton("&Cancel", self)
        self.cancel.clicked.connect(self.cancel_filtering_trigger)
        self.confirm = QPushButton("&Confirm", self)
        self.confirm.clicked.connect(self.confirm_filtering_trigger)

        self.grid_layout = QGridLayout()
        self.setLayout(self.grid_layout)
        self.create_grid_layout()

    def create_check_boxes(self, all_channels_names):
        for i, channel in enumerate(all_channels_names):
            check_box = QCheckBox()
            check_box.setChecked(True)
            check_box.setText(channel)
            self.channels_vbox_layout.addWidget(check_box)

    def create_grid_layout(self):
        info_labels = ["Low Frequency (Hz) : ", "High Frequency (Hz) : ", "Channels : "]
        for i, label in enumerate(info_labels):
            self.grid_layout.addWidget(QLabel(label), i, 0)
        self.grid_layout.addWidget(self.low_frequency_line, 0, 1)
        self.grid_layout.addWidget(self.high_frequency_line, 1, 1)
        self.grid_layout.addWidget(self.scroll_area, 2, 1)
        self.grid_layout.addWidget(self.cancel, 3, 0)
        self.grid_layout.addWidget(self.confirm, 3, 1)

    """
    Triggers
    """
    def cancel_filtering_trigger(self):
        self.filter_listener.cancel_button_clicked()

    def confirm_filtering_trigger(self):
        low_frequency = None
        high_frequency = None
        if self.low_frequency_line.hasAcceptableInput():
            low_frequency = self.low_frequency_line.text()
            low_frequency = float(low_frequency.replace(',', '.'))
        if self.high_frequency_line.hasAcceptableInput():
            high_frequency = self.high_frequency_line.text()
            high_frequency = float(high_frequency.replace(',', '.'))
        channels_selected = self.get_all_channels_selected()
        if low_frequency is None:
            print("Error low freq")
        elif high_frequency is None:
            print("Error high freq")
        else:
            self.filter_listener.confirm_button_clicked(low_frequency, high_frequency, channels_selected)

    def select_all_channels_trigger(self):
        for i in range(1, self.channels_vbox_layout.count()):
            check_box = self.channels_vbox_layout.itemAt(i).widget()
            check_box.setChecked(True)

    def unselect_all_channels_trigger(self):
        for i in range(1, self.channels_vbox_layout.count()):
            check_box = self.channels_vbox_layout.itemAt(i).widget()
            check_box.setChecked(False)

    """
    Setters
    """
    def set_listener(self, listener):
        self.filter_listener = listener

    """
    Getters
    """
    def get_all_channels_selected(self):
        all_channels = []
        for i in range(1, self.channels_vbox_layout.count()):
            check_box = self.channels_vbox_layout.itemAt(i).widget()
            if check_box.isChecked():
                all_channels.append(check_box.text())
        return all_channels
