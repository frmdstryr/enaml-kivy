#------------------------------------------------------------------------------
# Copyright (c) 2016, frmdstryr.
# Copyright (c) 2014, Nucleic Development Team.
#
# Distributed under the terms of the MIT License.
#
# The full license is in the file LICENSE, distributed with this software.
#------------------------------------------------------------------------------
from kivy.clock import Clock


def deferredCall(callback, *args, **kwargs):
    """ Execute the callback on the main gui thread.

    This should only be called after the Clock is created.

    """
    Clock.schedule_once(lambda: callback(*args, **kwargs))


def timedCall(ms, callback, *args, **kwargs):
    """ Execute a callback on a timer in the main gui thread.

    This should only be called after the Clock is created.

    """
    Clock.schedule_once(lambda: callback(*args, **kwargs),ms/1000.0)
