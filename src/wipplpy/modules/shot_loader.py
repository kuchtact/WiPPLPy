"""Load a shot from an MDSplus tree using a local or remote connection."""

import json
import logging
import os

import MDSplus as mds
from MDSplus.mdsExceptions import MDSplusException, SsSUCCESS

# TODO: Add MySQL Connection object.
_mds_connection = None
_global_tree = None


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
    global _mds_connection  # noqa: PLW0603
    if reconnect:
        logging.debug("Forcing reconnection to server.")
        try:
            _mds_connection.closeAllTrees()
        except Exception as e:
            logging.debug(
                f"Tried to close all trees from old connection. Exception occurred but ignoring. Exception was:\n{e}"
            )

    elif isinstance(_mds_connection, mds.Connection):
        if _mds_connection.hostspec == server_name:
            logging.info(
                f"Found pre-existing connector that is connected to {_mds_connection.hostspec}. Using this connector since same as {server_name}."
            )
            return _mds_connection
        else:
            logging.info(
                f"Found pre-existing connector that is connected to {_mds_connection.hostspec}. This is not the same as {server_name} so making new connection."
            )

    logging.debug(
        f"Trying to make connection to {server_name}. If this takes a while you may have forgotten to use the UW VPN."
    )
    _mds_connection = mds.Connection(server_name)
    logging.info(f"Connected to {server_name}.")
    return _mds_connection


def get_remote_shot_tree(  # noqa: PLR0912
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
            with open(load_config_path) as config_file:
                logging.debug(f"Successfully opened '{load_config_path}'.")
                config = json.load(config_file)
        except (
            OSError
        ):  # TODO: Change this to FileNotFoundError once code moved to python3.
            logging.error(
                f"Could not find shot_loading config file at '{load_config_path}'."
            )
            raise

    if server_name is None:
        server_name = config["server_name"]

    if tree_name is None:
        tree_name = config["tree_name"]

    global _global_tree  # noqa: PLW0603
    if isinstance(_global_tree, mds.Connection) and not reconnect:
        if (
            _global_tree.hostspec == server_name
            and _global_tree.tree_name == tree_name
            and _global_tree.shot_number == shot_number
        ):
            logging.debug(
                "Found pre-existing global tree for this server, tree, shot combination. Using that."
            )
            return _global_tree
        else:
            logging.debug(
                "Found pre-existing tree with different server and/or tree and/or shot number. Getting new tree."
            )

    connection = get_connector(server_name, reconnect)

    logging.debug(
        f"Getting shot {shot_number} on tree {tree_name} on server {server_name}."
    )
    try:
        connection.openTree(tree_name, shot_number)
    except SsSUCCESS:
        try:
            connection = get_connector(server_name, reconnect=True)
            connection.openTree(tree_name, shot_number)
        except MDSplusException:
            logging.exception(
                f"Error opening shot #{shot_number} on tree '{tree_name}' after retrying connection."
            )
            raise
    except MDSplusException:
        logging.exception(f"Error opening shot #{shot_number} on tree '{tree_name}'.")
        raise

    # Set a tree name and shot number attribute to make getting these values easy.
    connection.tree_name = tree_name
    if shot_number == 0:
        connection.shot_number = int(connection.get("$shot"))
    else:
        connection.shot_number = shot_number

    logging.info(f"Opened shot {shot_number} tree.")
    _global_tree = connection
    return _global_tree


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
