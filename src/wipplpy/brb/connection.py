"""
Create the BRBConnection() class for making BRB-MDSplus connection requests.
"""

from WiPPLPy.modules.config_reader import ConfigReader
from WiPPLPy.modules.connection import MDSPlusConnection


class BRBConnection(MDSPlusConnection):
    def __init__(self):
        """
        Initialize BRB-relevant objects necessary for connecting to MDSplus.
        """
        self.remote_server_name = ConfigReader.BRB_remote_server()
        self.tree_name = ConfigReader.BRB_tree()

    def make_connection(self, shot_number, tree_name, server_name):
        """
        Establish an MDSplus connection to the appropriate BRB data server.

        Parameters
        ----------
        shot_number : `int`
            The shot number from which to extract MDSplus data.
        tree_name : `str`
            String representing the tree name of the device's MDSplus database.
        server_name : `str`
            String representing the server in which the shot's data is located.
        """
        self.make_connection(
                shot_number,
                self.tree_name,
                self.remote_server_name
                )
