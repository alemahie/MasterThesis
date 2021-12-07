#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Main model
"""

from os.path import getsize

from mne import read_epochs
from mne.io import read_raw_fif, read_raw_eeglab, read_epochs_eeglab

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

    def open_fif_file(self, path_to_file):
        print(path_to_file[-7:-4])
        if path_to_file[-7:-4] == "raw":
            self.file_type = "Raw"
            self.file_data = read_raw_fif(path_to_file, preload=True)
        else:
            self.file_type = "Epochs"
            self.file_data = read_epochs(path_to_file, preload=True)
        self.file_path_name = path_to_file

    def open_cnt_file(self, path_to_file):
        self.file_data = cnt_file_reader.get_raw_from_cnt(path_to_file)
        self.file_type = "Raw"
        self.file_path_name = path_to_file

    def open_set_file(self, path_to_file):
        try:
            mne_item = read_raw_eeglab(path_to_file, preload=True)
            self.file_type = "Raw"
        except:
            mne_item = read_epochs_eeglab(path_to_file)
            self.file_type = "Epochs"
        self.file_data = mne_item
        self.file_path_name = path_to_file

    def save_file(self, path_to_file):
        if self.is_fif_file():
            self.file_data.save(path_to_file, overwrite=True)
        else:
            self.save_file_as(path_to_file)

    def save_file_as(self, path_to_file):
        if self.file_type == "Raw":
            self.file_path_name = path_to_file + "-raw.fif"
        else:
            self.file_path_name = path_to_file + "-epo.fif"
        self.file_data.save(self.file_path_name)

    def filter(self, low_frequency, high_frequency, channels_selected):
        self.file_data.filter(l_freq=low_frequency, h_freq=high_frequency, picks=channels_selected)

    def resampling(self):
        print("Resampling")

    def re_referencing(self):
        print("Re-referencing")

    def is_fif_file(self):
        return self.file_path_name[-3:] == "fif"

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
        if self.file_type == "Raw":
            return 1
        else:
            return len(self.file_data)

    def get_epochs_start(self):
        return round(self.file_data.times[0], 3)

    def get_epochs_end(self):
        return round(self.file_data.times[-1], 3)

    def get_number_of_frames(self):
        return len(self.file_data.times)

    def get_reference(self):
        return "Unknown"

    def get_channels_locations(self):
        return "Montage 10-05"

    def get_ICA(self):
        return False

    def get_dataset_size(self):
        if self.file_path_name[-3:] == "set":
            return round(getsize(self.file_path_name[:-3] + "fdt") / (1024 ** 2), 3)
        else:
            return round(getsize(self.file_path_name) / (1024 ** 2), 3)

    def get_all_channels_names(self):
        return self.file_data.ch_names
