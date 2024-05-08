"""
Define the MSTConnection() class specifically for making MST-MDSplus connection
requests. 
"""

# Standard
from datetime import date
import math

# Local
from WiPPLPy.modules.config_reader import ConfigReader
from WiPPLPy.modules.connection import MDSPlusConnection


class MSTConnection(MDSPlusConnection):

    def __init__(self):
        """
        Initialize MST-relevant objects that are necessary for connecting to
        MDSplus.
        """
        self.remote_server = ConfigReader.MST_remote_server 
        self.local_server = ConfigReader.MST_local_server 
        self.servers_dictionary = {
                True: self.remote_server,
                False: self.local_server}
        self.tree_name = ConfigReader.MST_tree 

    @staticmethod
    def data_location(shot_number):
        """
        Determine the location (server) of a shot's data.

        Parameters
        ----------
        shot_number : `int`
            The shot-number from which to extract MDSplus data.

        Returns
        -------
        server_name : `str`
            String representing the server in which the shot's data is located.

        Notes
        -----
        Run-day data are stored in the Juno server, whereas past-days' data are
        instead stored in the Toni server. This method uses the MST shot-number
        syntax to determine the server to use, e.g., the shot 1230419031 corre-
        sponds to shot-31 from April 19, 2023.
        """
        date_today = date.today()
        millenium_index = math.floor(date_today.year / 1000) - 1
        date_mst_syntax = millenium_index + date_today.strftime('%y%m%d')
        shot_string = str(shot_number)
        run_day = (shot_string[:-3] == date_mst_syntax)
        server_name = self.servers_dictionary[run_day]

        return server_name

    def make_connection(self, shot_number):
        """ 
        Establish an MDSplus connection to the appropriate MST data server.

        Parameters
        ----------
        shot_number: 'int'
            The shot-number from which to extract MDSplus data.
        """
        # Use the MDSPlusConnection.make_connection() method
        self.make_connection(shot_number, self.data_location(shot_number))


# End
