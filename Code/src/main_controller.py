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

from edit.dataset_info.dataset_info_controller import datasetInfoController
from edit.channel_location.channel_location_controller import channelLocationController

from tools.filter.filter_controller import filterController
from tools.resampling.resampling_controller import resamplingController
from tools.re_referencing.re_referencing_controller import reReferencingController

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
        self.main_model = mainModel()

        self.app = QApplication()

        self.main_view = mainView()
        self.screen_size = self.get_screen_geometry()
        self.main_view.resize(0.8 * self.screen_size.width(), 0.8 * self.screen_size.height())

        self.menubar_controller = menubarController()
        self.menubar_controller.set_listener(self)
        self.menubar_view = self.menubar_controller.get_view()
        self.main_view.setMenuBar(self.menubar_view)

        self.dataset_info_controller = None
        self.channel_location_controller = None

        self.filter_controller = None
        self.resampling_controller = None
        self.re_referencing_controller = None

        self.main_view.show()

        sys.exit(self.app.exec())

    def display_all_info(self):
        all_info = self.main_model.get_all_displayed_info()
        self.main_view.display_info(all_info)
        self.menubar_controller.enable_menu_when_file_loaded()

    """
    File menu
    """
    def open_fif_file_clicked(self, path_to_file):
        self.main_model.open_fif_file(path_to_file)
        self.display_all_info()

    def open_cnt_file_clicked(self, path_to_file):
        self.main_model.open_cnt_file(path_to_file)
        self.display_all_info()

    def open_set_file_clicked(self, path_to_file):
        self.main_model.open_set_file(path_to_file)
        self.display_all_info()

    def save_file_clicked(self):
        if self.main_model.is_fif_file():
            path_to_file = self.main_model.get_file_path_name()
        else:
            path_to_file = self.main_view.get_path_to_file()
        self.main_model.save_file(path_to_file)
        self.main_view.update_path_to_file(self.main_model.get_file_path_name())

    def save_file_as_clicked(self):
        path_to_file = self.main_view.get_path_to_file()
        self.main_model.save_file_as(path_to_file)
        self.main_view.update_path_to_file(self.main_model.get_file_path_name())

    """
    Edit menu
    """
    def dataset_info_clicked(self):
        sampling_rate = self.main_model.get_sampling_frequency()
        time_points_epochs = self.main_model.get_number_of_frames()
        start_time = self.main_model.get_epochs_start()
        self.dataset_info_controller = datasetInfoController(sampling_rate, time_points_epochs, start_time)
        self.dataset_info_controller.set_listener(self)

    def event_values_clicked(self):
        pass

    def channel_location_clicked(self):
        channel_location = self.main_model.get_channels_locations()
        channel_names = self.main_model.get_all_channels_names()
        self.channel_location_controller = channelLocationController(channel_location, channel_names)
        self.channel_location_controller.set_listener(self)

    def select_data_clicked(self):
        pass

    def select_data_events_clicked(self):
        pass

    """
    Tools menu
    """
    def filter_clicked(self):
        all_channels_names = self.main_model.get_all_channels_names()
        self.filter_controller = filterController(all_channels_names)
        self.filter_controller.set_listener(self)

    def filter_information(self, low_frequency, high_frequency, channels_selected):
        self.main_model.filter(low_frequency, high_frequency, channels_selected)
        self.main_view.update_dataset_size(self.main_model.get_dataset_size())

    def resampling_clicked(self):
        frequency = self.main_model.get_sampling_frequency()
        self.resampling_controller = resamplingController(frequency)
        self.resampling_controller.set_listener(self)

    def resampling_information(self, frequency):
        self.main_model.resampling(frequency)
        self.main_view.update_sampling_frequency(frequency)
        self.main_view.update_dataset_size(self.main_model.get_dataset_size())

    def re_referencing_clicked(self):
        reference = self.main_model.get_reference()
        all_channels_names = self.main_model.get_all_channels_names()
        self.re_referencing_controller = reReferencingController(reference, all_channels_names)
        self.re_referencing_controller.set_listener(self)

    def re_referencing_information(self, references):
        self.main_model.re_referencing(references)
        self.main_view.update_reference(references)

    def inspect_reject_data_clicked(self):
        pass

    def decompose_ICA_clicked(self):
        pass

    def source_estimation_clicked(self):
        pass

    """
    Plot menu
    """
    def plot_channel_locations_clicked(self):
        file_data = self.main_model.get_file_data()
        self.main_view.plot_channel_locations(file_data)

    def plot_data_clicked(self):
        file_data = self.main_model.get_file_data()
        file_type = self.main_model.get_file_type()
        self.main_view.plot_data(file_data, file_type)

    def plot_spectra_maps_clicked(self):
        pass

    def plot_channel_properties_clicked(self):
        pass

    def plot_ERP_image_clicked(self):
        pass

    def plot_time_frequency_clicked(self):
        pass

    """
    Getters
    """
    def get_screen_geometry(self):
        screen = self.app.primaryScreen()
        size = screen.size()
        # rect = screen.availableGeometry()
        return size
