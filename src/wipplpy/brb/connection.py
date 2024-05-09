"""
Create the BRBConnection() class for making BRB-MDSplus connection requests.
"""

from WiPPLPy.modules.config_reader import ConfigReader
from WiPPLPy.modules.connection import MDSPlusConnection


class BRBConnection(MDSPlusConnection):
    def __init__(self, config_reader = ConfigReader()):
        """
        Initialize BRB-relevant objects necessary for connecting to MDSplus.

        Parameters
        ----------
        config_reader
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
        self.make_connection(
                shot_number,
                self.config_reader.BRB_tree,
                self.config_reader.BRB_remote_server
                )
