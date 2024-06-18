"""
Define routines for accessing and extracting information from locally saved
config files.
"""

import configparser
import logging
import os

from WiPPLPy.modules.generic_get_data import lazy_get


class ConfigReader:
    """
    Access the local INI file containing relevant MDSplus labels and define
    methods for referring to each label.
    """

    def __init__(self, config_filepath=None):
        """
        Locate the appropriate INI file for accessing MDSplus datasets.

        Parameters
        ----------
        config_filepath : `str`
            The path name of the INI file.
        """
        self.config_filepath = config_filepath
        self.config = configparser.ConfigParser()

        if self.config_filepath is None:
            # Locate the standard INI file relative to this file's location
            this_file_directory = os.path.dirname(os.path.abspath(__file__))
            ini_file_path = os.path.abspath(
                os.path.join(this_file_directory, "../../../mdsplus_config.ini")
            )
            self.config_filepath = ini_file_path  # pass string path to argument

        if not os.path.exists(self.config_filepath):
            raise FileNotFoundError(
                f"INI file {self.config_filepath} not found. Please ensure"
                " that the file exists in the appropriate"
                " directory."
            )
        else:
            try:
                self.config.read(self.config_filepath)
            except FileNotFoundError:
                logging.exception(
                    "Error occurred while trying to read the INI file"
                    " located in `%s`. File was not found.",
                    self.config_filepath,
                )
                raise
            except SyntaxError:
                logging.exception(
                    "Error occurred while parsing the INI file located in"
                    " `%s`. Please ensure that the file format is correct.",
                    self.config_filepath,
                )
                raise
            except Exception as e:
                logging.exception(
                    "An unexpected error occurred while trying to read the"
                    " INI file located in `%s`: `%s`",
                    self.config_filepath,
                    e,
                )
                raise

    @lazy_get
    def BRB_remote_server(self):
        return self.config["BRB"]["mdsplus_server"]

    @lazy_get
    def BRB_tree(self):
        return self.config["BRB"]["mdsplus_tree"]

    @lazy_get
    def MST_runday_data_server(self):
        return self.config["MST"]["mdsplus_runday_data_server"]

    @lazy_get
    def MST_past_data_server(self):
        return self.config["MST"]["mdsplus_past_data_server"]

    @lazy_get
    def MST_tree(self):
        return self.config["MST"]["mdsplus_tree"]
