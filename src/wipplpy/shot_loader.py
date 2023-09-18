"""Load a shot from an MDSplus tree using a local or remote connection."""
import json
import logging
import os

import MDSplus as mds
from MDSplus.mdsExceptions import MDSplusException, SsSUCCESS

# TODO: Add MySQL Connection object.
mds_connection = None
global_tree = None


def get_connector(server_name, reconnect=False):
    """
    Get the MDSplus connector for a remote connection.

    Parameters
    ----------
    server_name : str
        Server ip address.
    reconnect : bool, default=False
        Whether to force a reconnection to the server.

    Returns
    -------
    mds.Connection
        Connection to the server without a tree connection.
    """
    global mds_connection
    if reconnect:
        logging.debug("Forcing reconnection to server.")
        try:
            mds_connection.closeAllTrees()
        except Exception as e:
            logging.debug(
                "Tried to close all trees from old connection. Exception occurred but ignoring. Exception was:\n{}".format(
                    e
                )
            )

    elif isinstance(mds_connection, mds.Connection):
        if mds_connection.hostspec == server_name:
            logging.info(
                "Found pre-existing connector that is connected to {host}. Using this connector since same as {server}.".format(
                    host=mds_connection.hostspec, server=server_name
                )
            )
            return mds_connection
        else:
            logging.info(
                "Found pre-existing connector that is connected to {host}. This is not the same as {server} so making new connection.".format(
                    host=mds_connection.hostspec, server=server_name
                )
            )

    logging.debug(
        "Trying to make connection to {}. If this takes a while you may have forgotten to use the UW VPN.".format(
            server_name
        )
    )
    mds_connection = mds.Connection(server_name)
    logging.info("Connected to {server}.".format(server=server_name))
    return mds_connection


def get_remote_shot_tree(
    shot_number,
    tree_name=None,
    server_name=None,
    load_config_path=os.path.join(
        os.path.realpath(os.path.dirname(__file__)), "shot_loading_config.json"
    ),
    reconnect=False,
):
    """
    Get the MDSplus tree from a remote server for a specific shot number. By default load the tree and server name from the shot_loading_config.json.

    Parameters
    ----------
    shot_number : int
        Number of the shot to get data for.
    tree_name : str, default=None
        Name of the MDSplus tree to use. By default load from config file.
    server_name : str, default=None
        Name of the server with the MDSplus tree. By default load from config file.
    load_config_path : str, default='brb_operations/analysis/modules/shot_loading_config.json'
        Path to file for loading the config.
    reconnect : bool, default=False
        Whether to force a reconnection to the server. This is used if the connection dies.

    Returns
    -------
    mds.Connection
    """
    if server_name is None or tree_name is None:
        try:
            with open(load_config_path, "r") as config_file:
                logging.debug(
                    "Successfully opened '{path}'.".format(path=load_config_path)
                )
                config = json.load(config_file)
        except (
            IOError
        ):  # TODO: Change this to FileNotFoundError once code moved to python3.
            logging.error(
                "Could not find shot_loading config file at '{path}'.".format(
                    path=load_config_path
                )
            )
            raise

    if server_name is None:
        server_name = config["server_name"]

    if tree_name is None:
        tree_name = config["tree_name"]

    global global_tree
    if isinstance(global_tree, mds.Connection) and not reconnect:
        if (
            global_tree.hostspec == server_name
            and global_tree.tree_name == tree_name
            and global_tree.shot_number == shot_number
        ):
            logging.debug(
                "Found pre-existing global tree for this server, tree, shot combination. Using that."
            )
            return global_tree
        else:
            logging.debug(
                "Found pre-existing tree with different server and/or tree and/or shot number. Getting new tree."
            )

    connection = get_connector(server_name, reconnect)

    logging.debug(
        "Getting shot {shot} on tree {tree} on server {server}.".format(
            shot=shot_number, tree=tree_name, server=server_name
        )
    )
    try:
        connection.openTree(tree_name, shot_number)
    except SsSUCCESS:
        try:
            connection = get_connector(server_name, reconnect=True)
            connection.openTree(tree_name, shot_number)
        except MDSplusException:
            logging.exception(
                "Error opening shot #{} on tree '{}' after retrying connection.".format(
                    shot_number, tree_name
                )
            )
            raise
    except MDSplusException:
        logging.exception(
            "Error opening shot #{} on tree '{}'.".format(shot_number, tree_name)
        )
        raise

    # Set a tree name and shot number attribute to make getting these values easy.
    connection.tree_name = tree_name
    if shot_number == 0:
        connection.shot_number = int(connection.get("$shot"))
    else:
        connection.shot_number = shot_number

    logging.info("Opened shot {} tree.".format(shot_number))
    global_tree = connection
    return global_tree


def most_recent_shot():
    """
    Get the most recent shot number from MDSplus.

    Returns
    -------
    int
        Most recent shot number.
    """
    try:
        tree = get_remote_shot_tree(0)
    except SsSUCCESS:
        tree = get_remote_shot_tree(0, reconnect=True)

    return tree.shot_number
