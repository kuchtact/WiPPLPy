"""
Extract from a local INI file the MDSplus labels for locating and accessing
datasets of MST and BRB.
"""

import configparser
import os
import sys

from generic_get_data import lazy_get


class ConfigReader:
    def __init__(self, config_file = None):
        """
        Locate the appropriate INI file for accessing MDSplus datasets.

        Parameters
        ----------
        config_file : `str`
            The path name of the INI file.
        """
        self.config_file = config_file

        # Fetch the INI file 
        if self.config_file is None:
            # Locate the standard INI file relative to this file's location
            this_file_directory = os.path.dirname(os.path.abspath(__file__))
            ini_file_path = os.path.abspath(os.path.join(
                    this_file_directory,
                    "../../../mdsplus_config.ini"
                    ))
            try:
                if not os.path.exists(ini_file_path):
                    raise FileNotFoundError("INI file mdsplus_config.ini"
                            " not found. Please ensure that the file exists"
                            " in the appropriate directory."
                            )
                # Read the INI file using configparser
                self.config = configparser.ConfigParser()
                self.config.read(ini_file_path)
            except FileNotFoundError as e:
                print(e)
            except Exception as e:
                # Handle exceptions other than being unable to locate the file
                print("An error occurred while trying to access the standard"
                        " MDSplus INI file:", e
                        )

        else:
            try:
                if not os.path.exists(self.config_file):
                    raise FileNotFoundError("INI file"
                            f" {self.config_file} not found. Please ensure"
                            " that the specified path correctly points to the"
                            " appropriate file."
                            )
                # Read the INI file using configparser
                self.config = configparser.ConfigParser()
                self.config.read(self.config_file)
            except FileNotFoundError as e:
                print(e)
            except Exception as e:
                # Handle exceptions other than being unable to locate the file
                print("An error occurred while trying to access the specified"
                        " MDSplus INI file:", e
                        )

    ### Define methods for loading MDSplus labels from the INI file ###
    @lazy_get
    def BRB_remote_server(self):
        return self.config['BRB']['mdsplus_server']
    
    @lazy_get
    def BRB_tree(self):
        return self.config['BRB']['mdsplus_tree']

    @lazy_get
    def MST_runday_data_server(self):
        return self.config['MST']['mdsplus_runday_data_server']

    @lazy_get
    def MST_past_data_server(self):
        return self.config['MST']['mdsplus_past_data_server']

    @lazy_get
    def MST_tree(self):
        return self.config['MST']['mdsplus_tree']
