#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Main controller
"""

import sys

from PyQt6.QtWidgets import QApplication

from main_model import mainModel
from main_view import mainView
from main_listener import mainListener

from menubar.menubar_controller import menubarController

from edit.dataset_info.dataset_info_controller import datasetInfoController
from edit.channel_location.channel_location_controller import channelLocationController

from tools.filter.filter_controller import filterController
from tools.resampling.resampling_controller import resamplingController
from tools.re_referencing.re_referencing_controller import reReferencingController
from tools.ICA_decomposition.ICA_decomposition_controller import icaDecompositionController
from tools.source_estimation.source_estimation_controller import sourceEstimationController

from plots.power_spectral_density.power_spectral_density_controller import powerSpectralDensityController
from plots.erp.erp_controller import erpController
from plots.time_frequency_ersp_itc.time_frequency_ersp_itc_controller import timeFrequencyErspItcController

from utils.stylesheet import get_stylesheet
from utils.waiting_while_processing.waiting_while_processing_controller import waitingWhileProcessingController

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
        self.main_model.set_listener(self)

        self.app = QApplication(sys.argv)
        self.app.setStyleSheet(get_stylesheet())

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
        self.ica_decomposition_controller = None
        self.source_estimation_controller = None

        self.power_spectral_density_controller = None
        self.erp_controller = None
        self.time_frequency_ersp_itc_controller = None

        self.waiting_while_processing_controller = None

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
        processing_title = "CNT file reading running, please wait."
        self.waiting_while_processing_controller = waitingWhileProcessingController(processing_title)
        self.main_model.open_cnt_file(path_to_file)

    def open_cnt_file_finished(self):
        processing_title_finished = "CNT file reading finished."
        self.waiting_while_processing_controller.stop_progress_bar(processing_title_finished)
        self.display_all_info()

    def open_set_file_clicked(self, path_to_file):
        processing_title = "SET file reading running, please wait."
        self.waiting_while_processing_controller = waitingWhileProcessingController(processing_title)
        self.main_model.open_set_file(path_to_file)

    def open_set_file_finished(self):
        processing_title_finished = "SET file reading finished."
        self.waiting_while_processing_controller.stop_progress_bar(processing_title_finished)
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

    def ica_decomposition_clicked(self):
        self.ica_decomposition_controller = icaDecompositionController()
        self.ica_decomposition_controller.set_listener(self)

    def ica_decomposition_information(self, ica_method):
        processing_title = "ICA decomposition running, please wait."
        self.waiting_while_processing_controller = waitingWhileProcessingController(processing_title)
        self.main_model.ica_data_decomposition(ica_method)

    def ica_decomposition_finished(self):
        ica_status = self.main_model.get_ica()
        self.main_view.update_ica_decomposition(ica_status)
        processing_title_finished = "ICA decomposition finished."
        self.waiting_while_processing_controller.stop_progress_bar(processing_title_finished)

    def source_estimation_clicked(self):
        self.source_estimation_controller = sourceEstimationController()
        self.source_estimation_controller.set_listener(self)

    def source_estimation_information(self, source_estimation_method, save_data, load_data, n_jobs):
        processing_title = "Source estimation running, please wait."
        self.waiting_while_processing_controller = waitingWhileProcessingController(processing_title)
        self.main_model.source_estimation(source_estimation_method, save_data, load_data, n_jobs)

    def source_estimation_finished(self, source_estimation_data):
        processing_title_finished = "Source estimation finished."
        self.waiting_while_processing_controller.stop_progress_bar(processing_title_finished)
        self.source_estimation_controller.plot_source_estimation(source_estimation_data)

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
        self.power_spectral_density_controller = powerSpectralDensityController()
        self.power_spectral_density_controller.set_listener(self)

    def plot_spectra_maps_information(self, method_psd, minimum_frequency, maximum_frequency):
        processing_title = "PSD running, please wait."
        self.waiting_while_processing_controller = waitingWhileProcessingController(processing_title)
        self.main_model.power_spectral_density(method_psd, minimum_frequency, maximum_frequency)

    def plot_spectra_maps_finished(self, psds, freqs):
        processing_title_finished = "PSD finished."
        self.waiting_while_processing_controller.stop_progress_bar(processing_title_finished)
        self.power_spectral_density_controller.plot_psd(psds, freqs)

    def plot_ERP_image_clicked(self):
        all_channels_names = self.main_model.get_all_channels_names()
        self.erp_controller = erpController(all_channels_names)
        self.erp_controller.set_listener(self)

    def plot_ERP_image_information(self, channels_selected):
        file_data = self.main_model.get_file_data()
        self.main_view.plot_erps(file_data, channels_selected)

    def plot_time_frequency_clicked(self):
        self.time_frequency_ersp_itc_controller = timeFrequencyErspItcController()
        self.time_frequency_ersp_itc_controller.set_listener(self)

    """
    Getters
    """
    def get_screen_geometry(self):
        screen = self.app.primaryScreen()
        size = screen.size()
        # rect = screen.availableGeometry()
        return size
