#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Waiting while processing controller
"""

from utils.waiting_while_processing.waiting_while_processing_view import waitingWhileProcessingView
from utils.waiting_while_processing.waiting_while_processing_listener import waitingWhileProcessingListener

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2021"
__credits__ = ["Lemahieu Antoine"]
__license__ = ""
__version__ = "0.1"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class waitingWhileProcessingController(waitingWhileProcessingListener):
    def __init__(self, processing_title):
        self.waiting_while_processing_view = waitingWhileProcessingView(processing_title)
        self.waiting_while_processing_view.set_listener(self)

        self.waiting_while_processing_view.show()

    def stop_progress_bar(self, processing_title_finished):
        self.waiting_while_processing_view.stop_progress_bar(processing_title_finished)

    def continue_button_clicked(self):
        self.waiting_while_processing_view.close()

