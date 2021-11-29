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
from menubar import menubar_controller

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

        self.toolbarController = menubar_controller.menubarController()
        self.toolbarController.set_listener(self)
        self.toolbarView = self.toolbarController.get_view()
        self.mainView.setMenuBar(self.toolbarView)

        self.mainView.show()

        sys.exit(self.app.exec())

    def open_cnt_file_clicked(self, path_to_file):
        self.mainModel.open_cnt_file(path_to_file)
        all_info = self.mainModel.get_all_displayed_info()
        self.mainView.display_info(all_info)

    def open_set_file_clicked(self, path_to_file):
        self.mainModel.open_set_file(path_to_file)

    def save_file_clicked(self):
        print("save main")

    def get_screen_geometry(self):
        screen = self.app.primaryScreen()
        size = screen.size()
        # rect = screen.availableGeometry()
        return size
