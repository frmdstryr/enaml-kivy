#------------------------------------------------------------------------------
# Copyright (c) 2014, Nucleic Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#------------------------------------------------------------------------------
from atom.api import Dict

from enaml.mime_data import MimeData

class KvMimeData(object):
    """ A Qt implementation of an Enaml MimeData object.

    """
    _q_data = Dict()

    def __init__(self, data=None):
        """ Initialize a QtMimeData object.

        Parameters
        ----------
        data : QMimeData, optional
            The mime data to wrap. If not provided, one will be created.

        """
        self._q_data = data or {}

    def q_data(self):
        """ Get the internal QMimeData object.

        This method is for toolkit backend use only.

        Returns
        -------
        result : QMimeData
            The Qt specific mime data object.

        """
        return self._q_data

    def formats(self):
        """ Get a list of the supported mime type formats.

        Returns
        -------
        result : list
            A list of mime types supported by the data.

        """
        return self._q_data.keys()

    def has_format(self, mime_type):
        """ Test whether the data supports the given mime type.

        Parameters
        ----------
        mime_type : unicode
            The mime type of interest.

        Returns
        -------
        result : bool
            True if there is data for the given type, False otherwise.

        """
        return mime_type in self._q_data

    def remove_format(self, mime_type):
        """ Remove the data entry for the given mime type.

        Parameters
        ----------
        mime_type : unicode
            The mime type of interest.

        """
        del self._q_data[mime_type]

    def data(self, mime_type):
        """ Get the data for the specified mime type.

        Parameters
        ----------
        mime_type : unicode
            The mime type of interest.

        Returns
        -------
        result : str
            The data for the specified mime type.

        """
        return self._q_data[mime_type]

    def set_data(self, mime_type, data):
        """ Set the data for the specified mime type.

        Parameters
        ----------
        mime_type : unicode
            The mime type of interest.

        data : str
            The serialized data for the given type.

        """
        self._q_data[mime_type] = data
