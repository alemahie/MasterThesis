#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Main model
"""

from mne.io import read_raw_eeglab, read_epochs_eeglab

from utils import cnt_file_reader

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2021"
__credits__ = ["Lemahieu Antoine"]
__license__ = ""
__version__ = "0.1"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class mainModel:
    def __init__(self):
        self.file_path_name = None
        self.file_type = None
        self.file_data = None

    def open_cnt_file(self, path_to_file):
        self.file_data = cnt_file_reader.get_raw_from_cnt(path_to_file)
        self.file_type = "Raw"
        self.file_path_name = path_to_file

    def open_set_file(self, path_to_file):
        mne_item = read_raw_eeglab(path_to_file)
        print(mne_item)

        mne_item_2 = read_epochs_eeglab(path_to_file)
        print(mne_item_2)

    """
    Getters
    """
    def get_all_displayed_info(self):
        all_info = [self.get_file_path_name(), self.get_file_type(), self.get_number_of_channels(),
                    self.get_sampling_frequency(), self.get_number_of_epochs(), self.get_epochs_start(),
                    self.get_epochs_end(), self.get_number_of_frames(), self.get_reference(),
                    self.get_channels_locations(), self.get_ICA(), self.get_dataset_size()]
        return all_info

    def get_file_path_name(self):
        return self.file_path_name

    def get_file_type(self):
        return self.file_type

    def get_number_of_channels(self):
        return len(self.file_data.ch_names)

    def get_sampling_frequency(self):
        return self.file_data.info.get("sfreq")

    def get_number_of_epochs(self):
        return 1

    def get_epochs_start(self):
        return 0

    def get_epochs_end(self):
        return 0

    def get_number_of_frames(self):
        return self.file_data.times

    def get_reference(self):
        return None

    def get_channels_locations(self):
        return "Montage 10-05"

    def get_ICA(self):
        return False

    def get_dataset_size(self):
        return 0

