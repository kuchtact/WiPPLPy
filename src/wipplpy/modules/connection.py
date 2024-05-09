"""
Define generic superclasses for accessing devices' databases.

TODO: Add a MySQL connection and maybe other connection types as well?
"""

from abc import ABC, abstractmethod
import MDSplus as mds
import socket


class MDSPlusConnection(ABC):
    """
    Create the generic superclass for generating MDSplus connections.
    """
    def __init__(self, ...):
        self.is_remote_connection = None # bool tracking if conn. is remote

    @abstractmethod
    def make_connection(self, shot_number):
        pass

    def _local_and_remote_connection(self, shot_number, tree_name, server_name):
        """
        Determine whether a local or remote connection is necessary, and then
        execute the corresponding method.

        Parameters
        ----------
        shot_number : `int`
            The shot number from which to extract MDSplus data.
        """
        local_server = socket.gethostname()
        if local_server == server_name:
            try:
                self._local_connect(shot_number, tree_name)
            except (ConnectionRefusedError, TimeoutError) as e:
                # Local connection did not work. Try a remote connection
                self._remote_connect(shot_number, tree_name, server_name)
            except Exception as e:
                # An unexpected exception is raised
                print("An error occurred while attempting to connect to"
                        f" {server_name}:", e
                        )

        else:
            try:
                self._remote_connect(shot_number, tree_name, server_name)
            except Exception as e:
                # An unexpected exception is raised
                print("An error occurred while attempting to remotely connect"
                        f" to {server_name}:", e
                        )

    def _local_connect(self, shot_number, tree_name):
        """
        Locally connect to the MDSplus database.

        Parameters
        ----------
        shot_number : `int`
            The shot number from which to extract MDSplus data.
        tree_name : `str`
            String representing the tree name of the device's MDSplus database.
        """
        self.is_remote_connection = False
        
        tree = mds.Tree(tree_name, shot_number) # open tree for given shot

    def _remote_connect(self, shot_number, tree_name, server_name):
        """
        Remotely connect to the MDSplus database.

        Parameters
        ----------
        shot_number : `int`
            The shot number from which to extract MDSplus data.
        tree_name : `str`
            String representing the tree name of the device's MDSplus database.
        server_name : `str`
            String representing the server in which the shot's data is located.
        """
        self.is_remote_connection = True

        conn = mds.Connection(server_name) # connect to given server
        tree = conn.openTree(tree_name, shot_number) # open tree for given shot
