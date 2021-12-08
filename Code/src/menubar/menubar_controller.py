#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Main controller
"""

import sys

from menubar.menubar_listener import menubarListener
from menubar.menubar_view import menubarView

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2021"
__credits__ = ["Lemahieu Antoine"]
__license__ = ""
__version__ = "0.1"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class menubarController(menubarListener):
    def __init__(self):
        self.main_listener = None
        self.menubar_view = menubarView()
        self.menubar_view.set_listener(self)

    def enable_menu_when_file_loaded(self):
        self.menubar_view.enable_menu_when_file_loaded()

    """
    Menu buttons clicked
    """
    def open_fif_file_clicked(self, path_to_file):
        self.main_listener.open_fif_file_clicked(path_to_file)

    def open_cnt_file_clicked(self, path_to_file):
        self.main_listener.open_cnt_file_clicked(path_to_file)

    def open_set_file_clicked(self, path_to_file):
        self.main_listener.open_set_file_clicked(path_to_file)

    def save_file_clicked(self):
        self.main_listener.save_file_clicked()

    def save_file_as_clicked(self):
        self.main_listener.save_file_as_clicked()

    def exit_program_clicked(self):
        sys.exit(0)

    def filter_clicked(self):
        self.main_listener.filter_clicked()

    def resampling_clicked(self):
        self.main_listener.resampling_clicked()

    def re_referencing_clicked(self):
        self.main_listener.re_referencing_clicked()

    def plot_data_clicked(self):
        self.main_listener.plot_data_clicked()

    def help_clicked(self):
        print("Help")

    def about_clicked(self):
        print("About")

    """
    Setters
    """
    def set_listener(self, main_listener):
        self.main_listener = main_listener

    """
    Getters
    """
    def get_view(self):
        return self.menubar_view
