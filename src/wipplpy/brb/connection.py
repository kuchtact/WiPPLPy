"""
Create objects pertaining to accessing databases for the BRB device.
"""

from wipplpy.modules.config_reader import MDSplusConfigReader
from wipplpy.modules.connection import MDSplusConnection


class BRBConnection(MDSplusConnection):
    """
    Open the BRB-MDSplus database for a given shot number.
    """

    def __init__(self, config_reader=MDSplusConfigReader()):
        """
        Initialize class attributes.

        Parameters
        ----------
        config_reader : `WiPPLPy.modules.config_reader.MDSplusConfigReader`
            Class object that reads from the INI file containing MDSplus
            labels.
        """
        self.config_reader = config_reader

    def make_connection(self, shot_number):
        """
        Establish an MDSplus connection to the appropriate BRB data server.

        Parameters
        ----------
        shot_number : `int`
            The shot number from which to extract MDSplus data.
        """
        self._local_and_remote_connection(
            shot_number,
            self.config_reader.BRB_tree,
            self.config_reader.BRB_remote_server
        )
