#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Channel location controller
"""

from edit.channel_location.channel_location_listener import channelLocationListener
from edit.channel_location.channel_location_view import channelLocationView

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2021"
__credits__ = ["Lemahieu Antoine"]
__license__ = ""
__version__ = "0.1"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class channelLocationController(channelLocationListener):
    def __init__(self, channel_location, channel_names):
        self.main_listener = None
        self.dataset_info_view = channelLocationView(channel_location, channel_names)
        self.dataset_info_view.set_listener(self)

        self.dataset_info_view.show()

    def cancel_button_clicked(self):
        self.dataset_info_view.close()

    def confirm_button_clicked(self):
        self.dataset_info_view.close()

    """
    Setters
    """
    def set_listener(self, listener):
        self.main_listener = listener
