#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Main controller
"""

from edit.filter.filter_view import filterView
from edit.filter.filter_listener import filterListener

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2021"
__credits__ = ["Lemahieu Antoine"]
__license__ = ""
__version__ = "0.1"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class filterController(filterListener):
    def __init__(self, all_channels_names):
        self.mainListener = None
        self.filterView = filterView(all_channels_names)
        self.filterView.set_listener(self)

        self.filterView.show()

    def cancel_button_clicked(self):
        self.filterView.close()

    def confirm_button_clicked(self, low_frequency, high_frequency, channels_selected):
        self.mainListener.filter_information(low_frequency, high_frequency, channels_selected)
        self.filterView.close()

    """
    Setters
    """
    def set_listener(self, listener):
        self.mainListener = listener
