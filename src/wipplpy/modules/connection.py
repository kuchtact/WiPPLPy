"""
Define generic objects for accessing WiPPL devices' databases.
"""

import logging
import socket
from abc import ABC, abstractmethod

import MDSplus as mds


class MDSPlusConnection(ABC):
    """
    Define generalized routines for accessing MDSplus databases.
    """

    def __init__(self):
        self.connection_is_remote = None

    @abstractmethod
    def make_connection(self, shot_number):
        pass

    def _local_and_remote_connection(self, shot_number, tree_name, server_name):
        """
        Determine whether a local or remote connection is necessary, and then
        call the corresponding method.

        Parameters
        ----------
        shot_number : `int`
            The shot number from which to extract MDSplus data.
        tree_name : `str`
            String representing the tree name of the device's MDSplus database.
        server_name : `str`
            String representing the server in which the shot's data is located.
        """
        local_server = socket.gethostname()
        if local_server == server_name:
            try:
                self._local_connect(shot_number, tree_name, server_name)
            except Exception as e:
                logging.warning(
                    "Failed attempted local connection: `%s`\nTrying a"
                    " remote connection ...",
                    e,
                )
                try:
                    self._remote_connect(shot_number, tree_name, server_name)
                except Exception as e:
                    self.connection_is_remote = None  # reset the flag
                    logging.exception(
                        "Error -- unable to locally or remotely connect to `%s`"
                        ": `%s`",
                        server_name,
                        e,
                    )
                    raise

        else:
            try:
                self._remote_connect(shot_number, tree_name, server_name)
            except Exception as e:
                logging.warning(
                    "Failed attempted remote connection: `%s`\nTrying a"
                    " local connection ...",
                    e,
                )
                try:
                    self._local_connect(shot_number, tree_name, server_name)
                except Exception as e:
                    self.connection_is_remote = None  # reset the flag
                    logging.exception(
                        "Error -- unable to locally or remotely connect to `%s`"
                        ": `%s`",
                        server_name,
                        e,
                    )
                    raise

    def _local_connect(self, shot_number, tree_name, server_name):
        """
        Open a local MDSplus tree database.

        Parameters
        ----------
        shot_number : `int`
            The shot number from which to extract MDSplus data.
        tree_name : `str`
            String representing the tree name of the device's MDSplus database.
        server_name : `str`
            String representing the server in which the shot's data is located.
        """
        self.connection_is_remote = False

        logging.debug(
                "Attempting a local connection to `%s` ...",
                server_name
        )
        self.tree = mds.Tree(tree_name, shot_number)

    def _remote_connect(self, shot_number, tree_name, server_name):
        """
        Open a remote MDSplus tree database.

        Parameters
        ----------
        shot_number : `int`
            The shot number from which to extract MDSplus data.
        tree_name : `str`
            String representing the tree name of the device's MDSplus database.
        server_name : `str`
            String representing the server in which the shot's data is located.
        """
        self.connection_is_remote = True

        logging.debug(
                "Attempting a remote connection to `%s` ...\nIf it is taking"
                " too long to connect, double-check that you are using your"
                " WiscVPN static IP address.",
                server_name
        )
        self.tree = mds.Connection(server_name)
        self.tree.openTree(tree_name, shot_number)
