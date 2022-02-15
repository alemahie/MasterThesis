#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Main controller
"""

from abc import ABC, abstractmethod

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2021"
__credits__ = ["Lemahieu Antoine"]
__license__ = ""
__version__ = "0.1"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class mainListener(ABC):
    @abstractmethod
    def open_fif_file_clicked(self, path_to_file):
        pass

    @abstractmethod
    def open_cnt_file_clicked(self, path_to_file):
        pass

    @abstractmethod
    def open_set_file_clicked(self, path_to_file):
        pass

    @abstractmethod
    def save_file_clicked(self):
        pass

    @abstractmethod
    def save_file_as_clicked(self):
        pass

    @abstractmethod
    def filter_clicked(self):
        pass

    @abstractmethod
    def filter_information(self, low_frequency, high_frequency, channels_selected):
        pass

    @abstractmethod
    def resampling_clicked(self):
        pass

    @abstractmethod
    def resampling_information(self, frequency):
        pass

    @abstractmethod
    def re_referencing_clicked(self):
        pass

    @abstractmethod
    def re_referencing_information(self, references):
        pass

    @abstractmethod
    def plot_data_clicked(self):
        pass
