#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Main controller
"""

from edit.filter.filter_view import filterView

__author__ = "Lemahieu Antoine"
__copyright__ = "Copyright 2021"
__credits__ = ["Lemahieu Antoine"]
__license__ = ""
__version__ = "0.1"
__maintainer__ = "Lemahieu Antoine"
__email__ = "Antoine.Lemahieu@ulb.be"
__status__ = "Dev"


class filterController:
    def __init__(self):
        self.mainListener = None
        self.filterView = filterView()
        self.filterView.set_listener(self)

        self.filterView.show()
