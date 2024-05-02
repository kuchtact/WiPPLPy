"""
This will contain a generic superclass for making MDSplus connections.

TODO: Add a MySQL connection and maybe other connection types as well?
"""

# Standard
import socket


class MDSPlusConnection:

    mdsplus_server = None
    tree_name = None

    def __init__(self, ...):
        self.is_remote_connection = None

    # Abstract method
    def make_connection(self, shot_number):
        # Choose whether to make a remote or local connection. Then return that connection.

    def determine_connection_type(self, server):

        local_server = socket.gethostname()

        if server == local_server:

            try:

                self._local_connect()

            except:

                self._remote_connect()

    def _local_connect(self, ...):
        # Make a local connection to the database.
        self.is_remote_connection = False

    def _remote_connect(self, ...):
        # Make a remote connection to the database.
        self.is_remote_connection = True
