"""
Extract from the local config the names of the servers and trees associated
with the MDSplus databases for MST and BRB.
"""

import configparser
import os


class ConfigReader:

    def __init__(self):
        """
        Read the server- and tree-names of BRB and MST into variables for easy
        global access.
        """
        # Fetch the INI file located in the same directory
        config_file = os.path.join(
                os.path.dirname(__file__),
                'mdsplus_config.ini')

        config = configparser.ConfigParser() # initialize configparser
        config.read(ini_file_path)

        # Retrieve server-names from the INI config file
        self.BRB_remote_server = config['BRB']['mdsplus_server']
        self.MST_remote_server = config['MST']['mdsplus_runday_server']
        self.MST_local_server = config['MST']['mdsplus_pastday_server']

        # Retrieve tree-names from the INI config file
        self.BRB_tree = config['BRB']['mdsplus_tree_name']
        self.MST_tree = config['MST']['mdsplus_tree_name']


# End
