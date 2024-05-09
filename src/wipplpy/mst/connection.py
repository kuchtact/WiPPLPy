"""
Create the MSTConnection() class for making MST-MDSplus connection requests.
"""

from datetime import date
import math

from WiPPLPy.modules.config_reader import ConfigReader
from WiPPLPy.modules.connection import MDSPlusConnection


class MSTConnection(MDSPlusConnection):
    def __init__(self):
        """
        Initialize MST-relevant objects necessary for connecting to MDSplus.
        """
        self.runday_data_server_name = ConfigReader.MST_runday_data_server
        self.past_data_server_name = ConfigReader.MST_past_data_server
        self.servers_dictionary = {
                True: self.runday_data_server_name,
                False: self.past_data_server_name
                }
        self.tree_name = ConfigReader.MST_tree() 

    @staticmethod
    def data_location(shot_number):
        """
        Determine the server name where shot data is stored.

        Parameters
        ----------
        shot_number : `int`
            The shot number from which to extract MDSplus data.

        Returns
        -------
        server_name : `str`
            String representing the server in which the shot's data is located.

        Notes
        -----
        Run-day and past days' data are stored in separate servers for MST.
        This routine chooses which server is needed based on the shot number
        syntax. E.g., the shot `1230419031` corresponds to shot 31 from April
        19, 2023.
        """
        # Prepare the date in MST shot-syntax
        date_today = date.today()
        millenium_index = math.floor(date_today.year / 1000) - 1
        date_mst_syntax = millenium_index + date_today.strftime('%y%m%d')

        shot_string = str(shot_number)

        # Compare the shot string to the date
        run_day = (shot_string[:-3] == date_mst_syntax)
        server_name = self.servers_dictionary[run_day]()
        logging.debug(
                "Shot '%s' data is stored on the '%s' server.",
                shot_string,
                server_name
                )

        return server_name

    def make_connection(self, shot_number, tree_name):
        """ 
        Establish an MDSplus connection to the appropriate MST data server.

        Parameters
        ----------
        shot_number : `int`
            The shot number from which to extract MDSplus data.
        tree_name : `str`
            String representing the tree name of the device's MDSplus database.
        """
        self.make_connection(
                shot_number, 
                self.tree_name,
                self.data_location(shot_number)
                )
