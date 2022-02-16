#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Dataset info view
"""

from PySide6.QtWidgets import QWidget, QGridLayout

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2021"
__credits__ = ["Lemahieu Antoine"]
__license__ = ""
__version__ = "0.1"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class datasetInfoView(QWidget):
    def __init__(self):
        super().__init__()
        self.dataset_info_listener = None

        self.grid_layout = QGridLayout()
        self.setLayout(self.grid_layout)

    """
    Triggers
    """
    def cancel_filtering_trigger(self):
        self.dataset_info_listener.cancel_button_clicked()

    def confirm_filtering_trigger(self):
        self.dataset_info_listener.confirm_button_clicked()

    """
    Setters
    """
    def set_listener(self, listener):
        self.dataset_info_listener = listener
