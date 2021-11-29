#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Main controller
"""
import sys

from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMenuBar, QMenu

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2021"
__credits__ = ["Lemahieu Antoine"]
__license__ = ""
__version__ = "0.1"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class menubarView(QMenuBar):
    def __init__(self):
        super().__init__()
        self.listener = None

        # File menu
        self.fileMenu = QMenu("&File", self)
        self.addMenu(self.fileMenu)

        # Open Menu
        self.openMenu = QMenu("&Open", self)
        self.fileMenu.addMenu(self.openMenu)
        openCNTFileAction = QAction("&CNT File", self)
        openCNTFileAction.triggered.connect(self.open_cnt_file_trigger)
        self.openMenu.addAction(openCNTFileAction)
        openSETFileAction = QAction("&SET File", self)
        openSETFileAction.triggered.connect(self.open_set_file_trigger)
        self.openMenu.addAction(openSETFileAction)

        saveFileAction = QAction("&Save", self)
        saveFileAction.triggered.connect(self.save_file_trigger)
        self.fileMenu.addAction(saveFileAction)
        exitAction = QAction("&Exit", self)
        exitAction.triggered.connect(self.exit_program_trigger)
        self.fileMenu.addAction(exitAction)

        # Help menu
        self.helpMenu = QMenu("&Help", self)
        self.addMenu(self.helpMenu)
        helpAction = QAction("&Help", self)
        helpAction.triggered.connect(self.help_trigger)
        self.helpMenu.addAction(helpAction)
        aboutAction = QAction("&About", self)
        aboutAction.triggered.connect(self.about_trigger)
        self.helpMenu.addAction(aboutAction)

    def open_cnt_file_trigger(self):
        path_to_file = "D:/Cours/Memoire/MasterThesis/Code/data/cnt/20200707_1208_pronation.cnt"
        self.listener.open_cnt_file_clicked(path_to_file)

    def open_set_file_trigger(self):
        path_to_file = "D:/Cours/Memoire/MasterThesis/Code/data/set/A1 ICAout 8 24 46 epochs_ALL_clean.set"
        self.listener.open_set_file_clicked(path_to_file)

    def save_file_trigger(self):
        self.listener.save_file_clicked()

    def exit_program_trigger(self):
        sys.exit(0)

    def help_trigger(self):
        print("HELP")

    def about_trigger(self):
        print("ABOUT")

    def set_listener(self, menubar_listener):
        self.listener = menubar_listener
