#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Main controller
"""

import sys

from menubar import menubar_view, menubar_listener

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2021"
__credits__ = ["Lemahieu Antoine"]
__license__ = ""
__version__ = "0.1"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class menubarController(menubar_listener.menubarListener):
    def __init__(self):
        self.listener = None
        self.toolbarView = menubar_view.menubarView()
        self.toolbarView.set_listener(self)

    def open_cnt_file_clicked(self, path_to_file):
        self.listener.open_cnt_file_clicked(path_to_file)

    def open_set_file_clicked(self, path_to_file):
        self.listener.open_set_file_clicked(path_to_file)

    def save_file_clicked(self):
        self.listener.save_file_clicked()

    def exit_program_clicked(self):
        sys.exit(0)

    def set_listener(self, main_listener):
        self.listener = main_listener

    def get_view(self):
        return self.toolbarView
