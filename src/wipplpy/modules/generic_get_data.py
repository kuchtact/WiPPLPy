import logging
import re

import numpy as np
from MDSplus.connection import Connection, MdsIpException
from MDSplus.mdsExceptions import MDSplusException, SsSUCCESS
from modules.shot_loader import get_remote_shot_tree
from scipy.io import loadmat, savemat


# This lazy get property is taken from https://towardsdatascience.com/what-is-lazy-evaluation-in-python-9efb1d3bfed0
def lazy_get(function):
    """
    Change a function to be used like an attribute and give it the ability to only load when called.

    Parameters
    ----------
    function : function
    """
    attribute_name = "_" + function.__name__

    @property
    def _lazy_get(self):
        if not hasattr(self, attribute_name) or getattr(self, attribute_name) is None:
            setattr(self, attribute_name, function(self))

        # Attempt to return a copy of the result so that it is difficult to change the object.
        result = getattr(self, attribute_name)
        try:
            return result.copy()
        except (SyntaxError, AttributeError):
            return result

    @_lazy_get.setter
    def _lazy_get(self, value):
        setattr(self, attribute_name, value)

    @_lazy_get.deleter
    def _lazy_get(self):
        logging.debug(
            "Deleting `{}` by setting `{}` of `{}` to `None`.".format(
                function.__name__, attribute_name, self
            )
        )
        setattr(self, attribute_name, None)

    return _lazy_get


class Get:
    def __init__(self, call_string, name=None, signal=True):
        """
        Class for holding get calls and certain info about the call.

        Parameters
        ----------
        call_string : str
            String to use when calling from the database.
        name : None or str, default=None
            Descriptive name of call to use when saving this call. Must be at most length 31. If None, use the call string.
        signal : bool, default=True
            Whether the get call will pull a signal from the tree.
        """
        self.call_string = call_string
        if name is None:
            self.name = self.to_matlab_name(call_string)
        else:
            self.name = name
        self.signal = signal

    def __str__(self) -> str:
        if self.signal:
            return f"Get({self.call_string}, is_signal)"
        else:
            return f"Get({self.call_string})"

    def full_str(self, index_range=None, sample_period=1):
        """
        Get the full call string to send to MDSplus.

        Parameters
        ----------
        index_range : tuple[int] or None, default=None
        sample_period : int, default=1

        Returns
        -------
        str
            Call string to be used for data.
        """
        if self.signal:
            if index_range is not None:
                if sample_period != 1:
                    return "DATA( {call} )[{start} : {end} : {step}]".format(
                        call=self.call_string,
                        start=index_range[0],
                        end=index_range[1],
                        step=sample_period,
                    )
                else:
                    return "DATA( {call} )[{start} : {end}]".format(
                        call=self.call_string, start=index_range[0], end=index_range[1]
                    )
            elif sample_period != 1:
                return "DATA( {call} )[0 : shape( {call} )[0] : {step}]".format(
                    call=self.call_string, step=sample_period
                )
            else:
                return f"DATA( {self.call_string} )"
        else:
            return self.call_string

    @staticmethod
    def to_matlab_name(call_string):
        """
        Convert a call string into a name that can be used in .mat files.

        Parameters
        ----------
        call_string : str
            String used when calling MDSplus.

        Returns
        -------
        str
            Call string after cleaning illicit characters and reducing length.
        """
        # Convert the string into a valid variable name for matlab.
        # Keep only alphanumerics and underscores by using a regex call.
        cleaned_string = re.sub("[^0-9a-zA-Z_]", "", call_string)
        # Remove all digits at the start of the string.
        while len(cleaned_string) != 0 and cleaned_string[0].isdigit():
            cleaned_string = cleaned_string[1:]
        # If we have removed all characters from the string then log a warning.
        if len(cleaned_string) == 0:
            logging.warning(
                "Length of string after cleaning for get call name is now zero. Setting call name as 'invalid_matlab_name'."
            )
            cleaned_string = "invalid_matlab_string"

        return cleaned_string[:31]


class Data:
    @staticmethod
    def _get_tree(tree_or_shot_number):
        """
        Get the tree for the shot number passed or just return the passed tree.

        Parameters
        ----------
        tree_or_shot_number : Connection or int
        """
        if isinstance(tree_or_shot_number, Connection):
            return tree_or_shot_number
        else:
            int_shot_number = int(tree_or_shot_number)
            logging.debug(
                "Shot number {} (int {}) passed when creating data object. Getting tree connection.".format(
                    tree_or_shot_number, int_shot_number
                )
            )
            return get_remote_shot_tree(int_shot_number)

    def __init__(
        self,
        tree,
        variable_booleans: iter,
        get_calls: iter,
        ignore_errors=False,
        silence_error_logging=False,
        time_index_range=None,
        time_range=None,
        sample_period=1,
        load_filepath=None,
    ):
        """
        Generic class for dealing with data from a remote MDSplus database.

        Parameters
        ----------
        tree : Connection or int
            MDSplus tree to take data from or shot number to use.
        variable_booleans : list of bool
            Which variables to get data for.
        get_calls : list of Get
            Calls to the database for each variable.
        ignore_errors : bool, default=False
            Whether to skip errors when getting data from the tree.
        time_index_range : None or tuple of two int, default=None
            If None, load all data. If a tuple then all signal variables only retrieve data in that index range.
        time_range : None or tuple of two float, default=None
            If None, load all data. If a tuple then all signal variables only retrieve data in that time range.
        sample_period : int, default=1
            Downsampling rate of signal to use when doing call. The default is 1 which means no downsampling.
        load_filepath : None or str, default=None
            Filepath to try to load data from instead of doing MDSplus calls. If None, don't try to load data from a file.

        Returns
        -------
        variable_vals : list
            Values of each variable that is wanted.

        Attributes
        ----------
        shot_number : int
            The shot number this Data is from.


        Methods
        -------
        to_raw_index(time_index)
            Convert a time index to an index that can be used for working with arrays of data.
        """
        # TODO: Add `get`, `save`, and `save_all` to the 'Methods' section.
        # If the tree is really a shot number then delay getting the tree until it's needed.
        try:
            self.shot_number = int(tree)
        except ValueError:
            self.shot_number = tree.shot_number

        self.ignore_errors = ignore_errors
        self.silence_error_logging = silence_error_logging

        self._tree = None

        # Initialize the time index range as empty and then try to get something for it. We do this because some code in _to_time_index_range requires it.
        self.time_index_range = None
        self.sample_period = sample_period
        if time_index_range is not None:
            self.time_index_range = time_index_range
        elif time_range is not None:
            self.time_index_range = self._to_time_index_range(time_range)
            del self.time

        if len(variable_booleans) != len(get_calls):
            raise ValueError(
                "variable_booleans and get_calls do not have the same number of elements ({} and {} respectively).".format(
                    len(variable_booleans), len(get_calls)
                )
            )
        elif len(get_calls) == 0:
            logging.info("Did not do any get calls for preloading data into object.")

        # Hold all the calls and call data gotten from MDSplus.
        # TODO: Change how calls are saved so that we can change loaded attributes and save the update.
        self.saved_calls = {}
        # Hold the loaded mat file.
        self.load_filepath = load_filepath
        if load_filepath is not None:
            logging.debug(
                "Loading .mat file at path '{}' to be used when loading data.".format(
                    load_filepath
                )
            )
            # Load the matrix and reduce matrix dimension as much as possible.
            try:
                self.loaded_mat_dict = loadmat(load_filepath, squeeze_me=True)
                logging.info(
                    "Loaded file '{}' has the following keys:\n{}".format(
                        load_filepath, self.loaded_mat_dict.keys()
                    )
                )
            except FileNotFoundError:
                logging.warning(
                    "Could not load file '{}' as it does not yet exist. Will call data from database instead.".format(
                        load_filepath
                    )
                )
                self.loaded_mat_dict = None
        else:
            self.loaded_mat_dict = None

        variable_vals = self._get_individuals(variable_booleans, get_calls)

        return variable_vals

    def _get_my_tree(self):
        if self._tree is None or self._tree.shot_number != self.shot_number:
            self._tree = self._get_tree(self.shot_number)
            self.shot_number = self._tree.shot_number
        return self._tree

    def _set_my_tree(self, new_tree):
        self._tree = new_tree
        self.shot_number = new_tree.shot_number

    tree = property(_get_my_tree, _set_my_tree)

    def _to_time_index_range(self, time_range):
        """
        Change a time range that is in seconds into an index range so that we can only get data in some range.

        Parameters
        ----------
        time_range : tuple of two floats
            Times in seconds from experiment start.

        Returns
        -------
        index_range : tuple of two ints
            Indices from start of digitizer recording.
        """
        index_range = (
            self._to_time_index(time_range[0]),
            self._to_time_index(time_range[1]),
        )
        if index_range[0] >= index_range[1]:
            logging.error(
                "Time range {} was not in the possible data times ({start}, {end}).".format(
                    time_range, start=self.time[0], end=self.time[-1]
                )
            )
            raise ValueError("Invalid time range {} since no data falls in range.")

        logging.debug(
            "Changed time range {} to index range {} for indexing signal data.".format(
                time_range, index_range
            )
        )
        return index_range

    def _to_time_index(self, time):
        """
        Change a time in seconds to data index.

        Parameters
        ----------
        time : float
            Time in seconds from experiment start.

        Returns
        -------
        index : int
            Data index from start of digitizer recording.
        """
        try:
            times = self.time
        except AttributeError:
            logging.error(
                "Object has no 'time' attribute so can't figure out how to change time range to index range for data."
            )
            raise

        if time < times[0]:
            index = 0
        elif time > times[-1]:
            index = times.size
        else:
            index = np.argmax(times >= time)

        return index

    def _get_individuals(self, variable_booleans, get_calls):
        """
        Get all data that has a True boolean associated with it.

        Parameters
        ----------
        variable_booleans : list of bool
        get_calls : list of Get

        Returns
        -------
        list
            List of all data gotten from MDSplus using get calls.
        """
        variable_values = []
        for i in range(len(variable_booleans)):
            if variable_booleans[i]:
                value = self.get(get_calls[i])
                variable_values.append(value)
            else:
                logging.debug(
                    "Skipping get call since boolean is False: '{}'".format(
                        get_calls[i]
                    )
                )
                variable_values.append(None)

        return variable_values

    def _get_many(self, tree, variable_booleans, get_calls):
        # TODO: Currently using a GetMany instance fails to call everything from the database. This needs to be fixed on the MDSplus end.
        # TODO: Add signal handling.
        # TODO: Add call saving.
        # TODO: Add SsSUCCESS error handling.
        logging.debug(f"Constructing GetMany instance using get calls:\n{get_calls}")
        getmany_instance = tree.getMany()
        getmany_keys = []
        # Append instructions to instance.
        for i, call in enumerate(get_calls):
            key = f"{i}: {call}"
            getmany_keys.append(key)

            if variable_booleans[i]:
                getmany_instance.append(key, call)
        # Execute all the calls.
        logging.debug("Executing network call for data object initialization.")
        result = getmany_instance.execute()

        # Populate the variable list.
        logging.debug("Assigning variable values.")
        variable_vals = []
        for i in range(len(variable_booleans)):
            if variable_booleans[i]:
                call = get_calls[i]
                key = getmany_keys[i]
                logging.debug(f"Assigning from call: {call}")
                try:
                    variable_vals.append(result[key]["value"].value)
                except KeyError:
                    if not self.silence_error_logging:
                        if "error" in result[key]:
                            logging.error(
                                "Error getting from tree using get call '{}'. Error was:\n{}".format(
                                    get_calls[i], result[key]["error"]
                                )
                            )
                        else:
                            logging.error(
                                "No error returned from call but could not find 'value' key in call result."
                            )
                    if not self.ignore_errors:
                        raise
            else:
                logging.debug(
                    "Skipping assignment since false boolean from call: {}".format(
                        get_calls[i]
                    )
                )
                variable_vals.append(None)
        return variable_vals

    def get(  # noqa: PLR0912, PLR0915
        self, get_call, np_data_type=np.float64, change_data=True, load_from_saved=True
    ):
        """
        Get data from the mdsplus tree and change it to the correct type using a get call.

        Parameters
        ----------
        get_call : str or Get
            A string or Get object that defines the call to use on the tree.
        np_data_type : data-type, default=np.float64
            The numpy data type to change the data to.
        change_data : bool, default=True
            Whether to change the data type of what MDSplus returns.
        load_from_saved : bool, default=True
            Whether to try to load the data from the saved calls.

        Returns
        -------
        data : `np_data_type` or MDSplus data-type
            The data from the tree.
        """
        logging.debug(f"Trying to get data using `{get_call}`.")
        if isinstance(get_call, Get):
            call_string = get_call.full_str(self.time_index_range, self.sample_period)
            save_name = get_call.to_matlab_name(call_string)
        elif isinstance(get_call, str):
            logging.info("Get call is a string and thus can't use time indexing.")
            call_string = get_call
            save_name = Get.to_matlab_name(call_string)

        if load_from_saved and hasattr(self, "saved_calls"):
            if save_name in self.saved_calls:
                logging.debug(
                    "Loading '{}' from saved calls instead of making new call.".format(
                        save_name
                    )
                )
                return self.saved_calls[save_name]

            if self.loaded_mat_dict is not None and save_name in self.loaded_mat_dict:
                logging.debug(
                    "Loading '{}' from loaded mat file instead of making new call.".format(
                        save_name
                    )
                )
                self.saved_calls[save_name] = self.loaded_mat_dict[save_name]
                return self.loaded_mat_dict[save_name]

        # Check that the shot number of the tree associated with this object is still connected to the same shot.
        # This may not occur as the tree is a global tree. TODO: Check if this ever happens.
        if self.shot_number != self.tree.shot_number:
            logging.info("Tree has changed shot number. Getting new tree.")
            self.tree = get_remote_shot_tree(self.shot_number)

        try_loading = True
        max_tries = 2
        num_tries = 0
        while try_loading:
            try_loading = False
            num_tries += 1
            logging.debug(f"Getting data from database using '{call_string}'.")
            try:
                node = self.tree.get(call_string)
            except MdsIpException:
                if not self.silence_error_logging:
                    logging.exception(
                        "Shot #{}: Error getting data from node using get call '{}'. No data available.".format(
                            self.shot_number, call_string
                        )
                    )
                if not self.ignore_errors:
                    logging.exception(
                        "Shot #{}: Error getting data from node using get call '{}'. No data available.".format(
                            self.shot_number, call_string
                        )
                    )
                    raise
            except SsSUCCESS:
                # Sometimes mdsplus raises a 'SsSUCCESS' exception. This may be because the connection object is bad. Thus we need to create a new connection object.
                if num_tries > max_tries:
                    logging.exception(
                        "Shot #{}: Error getting data from node using get call '{}'. Exceeded number of attempts ({}). Error was due to 'SsSUCCESS'.".format(
                            self.shot_number, call_string, max_tries
                        )
                    )
                    raise
                else:
                    logging.info(
                        "Silencing 'SsSUCCESS' error that MDSplus raised. Reconnecting to server."
                    )
                    try_loading = True
                    self.tree = get_remote_shot_tree(self.shot_number, reconnect=True)

        if self.ignore_errors:
            try:
                data = node.data()
            except Exception:
                return np.array()
        else:
            data = node.data()

        logging.debug("Got data from tree.")
        if change_data:
            data = data.astype(np_data_type)
            logging.debug(f"Changed data to type '{np_data_type}'.")

        # Only save calls if the dictionary exists. The dictionary doesn't exist during some stages of initialization so that we don't save incorrect data.
        if hasattr(self, "saved_calls"):
            # logging.debug("Adding data from get call with `save_name='{}'` into `saved_calls`.".format(save_name))
            if save_name in self.saved_calls:
                logging.warning(
                    "Save name ({}) is the same as a save name already in the data to save dictionary. Overwriting old data."
                )
            self.saved_calls[save_name] = data

        return data

    def to_raw_index(self, time_index):
        """
        Convert an index that works for the entire time range and change it to work for this objects arrays.

        Parameters
        ----------
        time_index : int or np.array[int]
            Index of array in time where `time_index = 0` refers to the very
            first data point for the signals.

        Returns
        -------
        raw_index : int
            Index of array in time where `raw_index = 0` refers to the very
            first data point for this objects signals which may be different
            due to the `time_index_range` of this object.
        """
        if self.time_index_range is not None:
            return time_index - self.time_index_range[0]
        else:
            return time_index

    def save(self, filepath):
        """
        Save data currently called from MDSplus as a '.mat' file that this object got.

        Parameters
        ----------
        filepath : str
            Path to file where the data should be saved.

        Notes
        -----
        This also saves all data from a previously loaded `.mat` file if one was associated with this object.
        """
        if filepath.strip()[-4:] != ".mat":
            logging.warning(
                "Saving calls to file {} but this file has no '.mat' extension.".format(
                    filepath
                )
            )

        if self.loaded_mat_dict is not None:
            for key in self.loaded_mat_dict:
                if key not in self.saved_calls:
                    self.saved_calls[key] = self.loaded_mat_dict[key]

        logging.debug(
            "Saving data with names '{}' to file '{}'.".format(
                self.saved_calls.keys(), filepath
            )
        )
        savemat(filepath, self.saved_calls)

    def save_all(self, filepath):
        """
        Similar to `save` but first calls all `@lazy_get` functions then saves that data along with any other called data.

        Parameters
        ----------
        filepath : str
            Path to file where the data should be saved.
        """
        # Get all the items in the class. If any are of type `property` then that is a call to MDSplus most likely.
        class_items = self.__class__.__dict__.items()
        call_functions = [k for k, v in class_items if isinstance(v, property)]
        logging.debug(f"Calling functions {call_functions} before saving.")
        for f in call_functions:
            try:
                logging.debug(f"Calling function '{f}'.")
                getattr(self, f)
            except MDSplusException as e:
                logging.warning(
                    "An MDSplus exception occurred while executing '{}'. Exception was:\n{}".format(
                        f, e
                    )
                )
            except Exception as e:
                logging.warning(
                    "A non-MDSplus exception occurred while executing '{}'. Exception was:\n{}".format(
                        f, e
                    )
                )

        self.save(filepath)


class Port:
    def __init__(self, parent_probe: Data, port_tag_prefix: str) -> None:
        """
        This class holds information about the port a probe is attached to.

        Parameters
        ----------
        parent_probe : Data
            The probe owning this Port object.
        port_tag_prefix : str
            Prefix for each tag in the port tree for a probe. This should only
            contain letters, numbers, and underscores.

        Attributes
        ----------
        alpha_deg, alpha_rad, beta_deg, beta_rad, gamma_deg, gamma_rad : float
            Tilt angles of port with respect to the North, East, and Down (NED)
            coordinate vectors in degrees and radians.
        clocking_deg, clocking_rad : float
            Rotation of probe. Clocking is 0 when the x direction of the probe
            is pointed along a meridian towards the North pole of the BRB.
            Increases as probe is rotate clockwise looking into the ball from
            the outside.
        insert : float
            Insertion distance of probe in meters. Insertion of 0 means the
            probe is at the radius of the port.
        lat_deg, lat_rad, long_deg, long_rad : float
            Latitude and longitude of port in degrees and radians.
        rport : float
            Radius of port in meters.

        Examples
        --------
        >>> from speed_bdot1.get_data import Speed_Bdot1_Data
        >>> speed_data = Speed_Bdot1_Data(60000)
        >>> speed_port = Port(speed_data, 'speed_bdot1_')
        """
        self.parent_probe = parent_probe
        self.port_tag_prefix = port_tag_prefix

    @lazy_get
    def alpha_deg(self):
        return self.parent_probe.get(
            Get(f"\\{self.port_tag_prefix}alpha", signal=False)
        )

    @lazy_get
    def alpha_rad(self):
        return np.deg2rad(self.alpha_deg)

    @lazy_get
    def beta_deg(self):
        return self.parent_probe.get(Get(f"\\{self.port_tag_prefix}beta", signal=False))

    @lazy_get
    def beta_rad(self):
        return np.deg2rad(self.beta_deg)

    @lazy_get
    def gamma_deg(self):
        return self.parent_probe.get(
            Get(f"\\{self.port_tag_prefix}gamma", signal=False)
        )

    @lazy_get
    def gamma_rad(self):
        return np.deg2rad(self.gamma_deg)

    @lazy_get
    def insert(self):
        return self.parent_probe.get(
            Get(f"\\{self.port_tag_prefix}insert", signal=False)
        )

    @lazy_get
    def lat_deg(self):
        return self.parent_probe.get(Get(f"\\{self.port_tag_prefix}lat", signal=False))

    @lazy_get
    def lat_rad(self):
        return np.deg2rad(self.lat_deg)

    @lazy_get
    def long_deg(self):
        return self.parent_probe.get(Get(f"\\{self.port_tag_prefix}long", signal=False))

    @lazy_get
    def long_rad(self):
        return np.deg2rad(self.long_deg)

    @lazy_get
    def rport(self):
        return self.parent_probe.get(
            Get(f"\\{self.port_tag_prefix}rport", signal=False)
        )

    @lazy_get
    def clocking_deg(self):
        # Some probes don't have a clocking value set so we assume it's zero.
        try:
            return self.parent_probe.get(
                Get(f"\\{self.port_tag_prefix}clock", signal=False)
            )
        except MdsIpException:
            logging.warning("Could not get clocking value. Returning clocking of 0.")
            return 0

    @lazy_get
    def clocking_rad(self):
        try:
            return np.deg2rad(self.clocking_deg)
        except MdsIpException:
            logging.warning("Could not get clocking value. Returning clocking of 0.")
            return 0
