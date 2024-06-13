"""
Create objects pertaining to accessing databases for the MST device.
"""

from datetime import date
import math

from WiPPLPy.modules.config_reader import ConfigReader
from WiPPLPy.modules.connection import MDSPlusConnection


class MSTConnection(MDSPlusConnection):
    """
    Open the MST-MDSplus database for a given shot number.
    """
    def __init__(self, config_reader = ConfigReader()):
        """
        Initialize class attributes.

        Parameters
        ----------
        config_reader : `WiPPLPy.modules.config_reader.ConfigReader`
            Class object that reads from the INI file containing MDSplus
            labels.
        """
        self.config_reader = config_reader

    def data_location(self, shot_number):
        """
        Determine the server in which the given shot number's data is stored.

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
        Run-day and past days' data are stored on separate servers for MST. This
        routine selects the appropriate server based on the shot-number syntax.
        For example, the shot '1230419031' corresponds to shot 31 from April 19,
        2023, from which it can be determined whether the date is the present
        run-day or a past day.
        """
        # Prepare the date in MST's shot syntax
        date_today = date.today()
        millenium_index = math.floor(date_today.year / 1000) - 1
        date_mst_syntax = millenium_index + date_today.strftime('%y%m%d')

        shot_string = str(shot_number)

        # Compare the shot string to the date
        if shot_string[:-3] == date_mst_syntax:
            server_name = self.config_reader.MST_runday_data_server
        else:
            server_name = self.config_reader.MST_past_data_server
        logging.debug(
                "Shot `%s` data is stored on the `%s` server.",
                shot_string,
                server_name
                )

        return server_name

    def make_connection(self, shot_number):
        """ 
        Establish an MDSplus connection to the appropriate MST data server.

        Parameters
        ----------
        shot_number : `int`
            The shot number from which to extract MDSplus data.
        """
        self._local_and_remote_connection(
                shot_number, 
                self.config_reader.MST_tree,
                self.data_location(shot_number)
                )
