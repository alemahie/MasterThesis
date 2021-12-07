#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Main controller
"""

import sys

from PySide6.QtWidgets import QApplication

from main_model import mainModel
from main_view import mainView
from main_listener import mainListener
from menubar.menubar_controller import menubarController
from edit.filter.filter_controller import filterController

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2021"
__credits__ = ["Lemahieu Antoine"]
__license__ = ""
__version__ = "0.1"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class mainController(mainListener):
    def __init__(self):
        self.mainModel = mainModel()

        self.app = QApplication()

        self.mainView = mainView()
        self.screen_size = self.get_screen_geometry()
        self.mainView.resize(0.8*self.screen_size.width(), 0.8*self.screen_size.height())

        self.menubarController = menubarController()
        self.menubarController.set_listener(self)
        self.menubarView = self.menubarController.get_view()
        self.mainView.setMenuBar(self.menubarView)

        self.filterController = None

        self.mainView.show()

        sys.exit(self.app.exec())

    def display_all_info(self):
        all_info = self.mainModel.get_all_displayed_info()
        self.mainView.display_info(all_info)
        self.menubarController.enable_menu_when_file_loaded()

    """
    Menu Buttons Clicked
    """
    def open_fif_file_clicked(self, path_to_file):
        self.mainModel.open_fif_file(path_to_file)
        self.display_all_info()

    def open_cnt_file_clicked(self, path_to_file):
        self.mainModel.open_cnt_file(path_to_file)
        self.display_all_info()

    def open_set_file_clicked(self, path_to_file):
        self.mainModel.open_set_file(path_to_file)
        self.display_all_info()

    def save_file_clicked(self, path_to_file):
        self.mainModel.save_fif_file(path_to_file)

    def save_file_as_clicked(self, path_to_file):
        self.mainModel.save_fif_file(path_to_file)

    def filter_clicked(self):
        all_channels_names = self.mainModel.get_all_channels_names()
        self.filterController = filterController(all_channels_names)
        self.filterController.set_listener(self)

    def filter_information(self, low_frequency, high_frequency, channels_selected):
        self.mainModel.filter(low_frequency, high_frequency, channels_selected)

    def resampling_clicked(self):
        self.mainModel.resampling()

    def re_referencing_clicked(self):
        self.mainModel.re_referencing()

    def plot_data_clicked(self):
        print("Plot data")

    """
    Getters
    """
    def get_screen_geometry(self):
        screen = self.app.primaryScreen()
        size = screen.size()
        # rect = screen.availableGeometry()
        return size
