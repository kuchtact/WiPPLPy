"""
Define the BRBConnection() class specifically for making BRB-MDSplus connection
requests.
"""

# Local
from WiPPLPy.modules.config_reader import ConfigReader
from WiPPLPy.modules.connection import MDSPlusConnection


class BRBConnection(MDSPlusConnection):

    def __init__(self):
        """
        Initialize MST-relevant objects that are necessary for connecting to
        MDSplus.
        """
        self.remote_server = ConfigReader.BRB_remote_server 
        self.tree_name = ConfigReader.BRB_tree

    def make_connection(self, shot_number):
        """
        Establish an MDSplus connection to the appropriate BRB data server.

        Parameters
        ----------
        shot_number: 'int'
            The shot-number from which to extract MDSplus data.
        """
        # Use the MDSPlusConnection.make_connection() method
        self.make_connection(shot_number, use_server)


# End
