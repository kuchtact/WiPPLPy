"""
Under construction. Feel free to rename
variables and methods so that they are
more understandable and readable.
"""


class BRBConnection(MDSPlusConnection):

    def __init__(self):

        self.brb_server = ''
        self.tree_name = ''

    def make_connection(self, shot_number):

        """ Establish an MDSplus connection to
        the appropriate BRB data server.

        Parameters
        ----------
        shot_number: int
            The shot-number from which to extract
            MDSplus data. """

        use_server = self.brb_server

        self.make_connection(shot_number, use_server)


# End
