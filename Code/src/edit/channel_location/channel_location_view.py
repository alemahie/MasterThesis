#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Channel location view
"""

from PySide6.QtWidgets import QWidget, QGridLayout, QPushButton, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2021"
__credits__ = ["Lemahieu Antoine"]
__license__ = ""
__version__ = "0.1"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class channelLocationView(QWidget):
    def __init__(self, channel_location, channel_names):
        super().__init__()
        self.channel_location_listener = None

        self.vertical_layout = QVBoxLayout()
        self.setLayout(self.vertical_layout)

        self.channel_name_line = QLineEdit()
        self.channel_name_line.setText(channel_names[0])
        self.x_coordinate_line = QLineEdit()
        self.x_coordinate_line.setText(str(round(channel_location[channel_names[0]][1], 3)))
        self.y_coordinate_line = QLineEdit()
        self.y_coordinate_line.setText(str(round(channel_location[channel_names[0]][0], 3)))
        self.z_coordinate_line = QLineEdit()
        self.z_coordinate_line.setText(str(round(channel_location[channel_names[0]][2], 3)))

        self.info_widget = QWidget()
        self.info_grid_layout = QGridLayout()
        self.info_grid_layout.addWidget(QLabel("Channel location information : "), 0, 0)
        self.info_grid_layout.addWidget(QLabel("Channel name : "), 1, 0)
        self.info_grid_layout.addWidget(QLabel("X coordinate : "), 2, 0)
        self.info_grid_layout.addWidget(QLabel("Y coordinate : "), 3, 0)
        self.info_grid_layout.addWidget(QLabel("Z coordinate : "), 4, 0)
        self.info_grid_layout.addWidget(self.channel_name_line, 1, 1)
        self.info_grid_layout.addWidget(self.x_coordinate_line, 2, 1)
        self.info_grid_layout.addWidget(self.y_coordinate_line, 3, 1)
        self.info_grid_layout.addWidget(self.z_coordinate_line, 4, 1)
        self.info_widget.setLayout(self.info_grid_layout)

        self.change_channel_widget = QWidget()
        self.change_channel_layout = QHBoxLayout()
        self.previous_button = QPushButton("&Previous", self)
        self.previous_button.clicked.connect(self.previous_button_trigger)
        self.next_button = QPushButton("&Next", self)
        self.next_button.clicked.connect(self.next_button_trigger)
        self.channel_number = QLineEdit()
        self.channel_number.setText(str(1))
        self.change_channel_layout.addWidget(self.previous_button)
        self.change_channel_layout.addWidget(self.channel_number)
        self.change_channel_layout.addWidget(self.next_button)
        self.change_channel_widget.setLayout(self.change_channel_layout)

        self.cancel_confirm_widget = QWidget()
        self.cancel_confirm_layout = QHBoxLayout()
        self.cancel = QPushButton("&Cancel", self)
        self.cancel.clicked.connect(self.cancel_channel_location_trigger)
        self.confirm = QPushButton("&Confirm", self)
        self.confirm.clicked.connect(self.confirm_channel_location_trigger)
        self.cancel_confirm_layout.addWidget(self.cancel)
        self.cancel_confirm_layout.addWidget(self.confirm)
        self.cancel_confirm_widget.setLayout(self.cancel_confirm_layout)

        self.vertical_layout.addWidget(self.info_widget)
        self.vertical_layout.addWidget(self.change_channel_widget)
        self.vertical_layout.addWidget(self.cancel_confirm_widget)

    """
    Triggers
    """
    def cancel_channel_location_trigger(self):
        self.channel_location_listener.cancel_button_clicked()

    def confirm_channel_location_trigger(self):
        self.channel_location_listener.confirm_button_clicked()

    def previous_button_trigger(self):
        print("previous")

    def next_button_trigger(self):
        print("next")

    """
    Setters
    """
    def set_listener(self, listener):
        self.channel_location_listener = listener
