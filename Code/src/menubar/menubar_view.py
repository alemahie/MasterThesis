#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Main controller
"""

from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMenuBar, QMenu, QFileDialog

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
        self.menubarListener = None

        # File menu
        self.fileMenu = QMenu("&File", self)
        self.addMenu(self.fileMenu)
        self.openMenu = QMenu("&Open", self)
        self.create_open_menu()
        self.fileMenu.addMenu(self.openMenu)
        self.create_file_menu()

        # Edit menu
        self.editMenu = QMenu("&Edit", self)
        self.addMenu(self.editMenu)
        self.create_edit_menu()
        self.editMenu.setEnabled(False)

        # Plot menu
        self.plotMenu = QMenu("Plot", self)
        self.addMenu(self.plotMenu)
        self.create_plot_menu()
        self.plotMenu.setEnabled(False)

        # Help menu
        self.helpMenu = QMenu("&Help", self)
        self.addMenu(self.helpMenu)
        self.create_help_menu()

    def create_open_menu(self):
        openFifFileAction = QAction("&FIF File", self)
        openFifFileAction.triggered.connect(self.open_fif_file_trigger)
        self.openMenu.addAction(openFifFileAction)
        self.openMenu.addSeparator()
        openCntFileAction = QAction("&CNT File", self)
        openCntFileAction.triggered.connect(self.open_cnt_file_trigger)
        self.openMenu.addAction(openCntFileAction)
        openSetFileAction = QAction("&SET File", self)
        openSetFileAction.triggered.connect(self.open_set_file_trigger)
        self.openMenu.addAction(openSetFileAction)

    def create_file_menu(self):
        # Save
        self.fileMenu.addSeparator()
        saveFileAction = QAction("&Save", self)
        saveFileAction.triggered.connect(self.save_file_trigger)
        saveFileAction.setEnabled(False)
        self.fileMenu.addAction(saveFileAction)
        saveFileAsAction = QAction("&Save As", self)
        saveFileAsAction.triggered.connect(self.save_file_as_trigger)
        saveFileAsAction.setEnabled(False)
        self.fileMenu.addAction(saveFileAsAction)
        # Other
        self.fileMenu.addSeparator()
        exitAction = QAction("&Exit", self)
        exitAction.triggered.connect(self.exit_program_trigger)
        self.fileMenu.addAction(exitAction)

    def create_edit_menu(self):
        filterAction = QAction("&Filter", self)
        filterAction.triggered.connect(self.filter_trigger)
        self.editMenu.addAction(filterAction)
        resamplingAction = QAction("&Resampling", self)
        resamplingAction.triggered.connect(self.resampling_trigger)
        resamplingAction.setEnabled(False)
        self.editMenu.addAction(resamplingAction)
        reReferencingAction = QAction("&Re-Referencing", self)
        reReferencingAction.triggered.connect(self.re_referencing_trigger)
        reReferencingAction.setEnabled(False)
        self.editMenu.addAction(reReferencingAction)

    def create_plot_menu(self):
        plotDataAction = QAction("&Plot data", self)
        plotDataAction.triggered.connect(self.plot_data_trigger)
        self.plotMenu.addAction(plotDataAction)

    def create_help_menu(self):
        helpAction = QAction("&Help", self)
        helpAction.triggered.connect(self.help_trigger)
        helpAction.setEnabled(False)
        self.helpMenu.addAction(helpAction)
        aboutAction = QAction("&About", self)
        aboutAction.triggered.connect(self.about_trigger)
        aboutAction.setEnabled(False)
        self.helpMenu.addAction(aboutAction)

    def enable_menu_when_file_loaded(self):
        menu_actions = self.fileMenu.actions()
        menu_actions[2].setEnabled(True)    # Save
        menu_actions[3].setEnabled(True)    # Save As
        self.editMenu.setEnabled(True)
        self.plotMenu.setEnabled(True)

    """
    Triggers
    """
    def open_fif_file_trigger(self):
        path_to_file = QFileDialog().getOpenFileName(self, "Open file", "*.fif")
        self.menubarListener.open_fif_file_clicked(path_to_file[0])

    def open_cnt_file_trigger(self):
        path_to_file = QFileDialog().getOpenFileName(self, "Open file", "*.cnt")
        self.menubarListener.open_cnt_file_clicked(path_to_file[0])

    def open_set_file_trigger(self):
        path_to_file = QFileDialog().getOpenFileName(self, "Open file", "*.set")
        self.menubarListener.open_set_file_clicked(path_to_file[0])

    def save_file_trigger(self):
        self.menubarListener.save_file_clicked()

    def save_file_as_trigger(self):
        self.menubarListener.save_file_as_clicked()

    def exit_program_trigger(self):
        self.menubarListener.exit_program_clicked()

    def filter_trigger(self):
        self.menubarListener.filter_clicked()

    def resampling_trigger(self):
        self.menubarListener.resampling_clicked()

    def re_referencing_trigger(self):
        self.menubarListener.re_referencing_clicked()

    def plot_data_trigger(self):
        self.menubarListener.plot_data_clicked()

    def help_trigger(self):
        self.menubarListener.help_clicked()

    def about_trigger(self):
        self.menubarListener.about_clicked()

    """
    Setters
    """
    def set_listener(self, menubar_listener):
        self.menubarListener = menubar_listener
