.. _code_overview:

*************
Code Overview
*************

Code Operation
==============

Let's walk through how the code is structured and how it operates.

1. The user starts by creating a new instance of the :class:`.Example_Diagnostic` class. This class is a subclass of the :class:`.Data` class from the :file:`modules/generic_get_data.py`.

2. The :class:`.Example_Diagnostic` class has a method called :meth:`.Example_Diagnostic.example_value`. This attribute is really a property that is a wrapper around the :meth:`.Example_Diagnostic._example_value` method. When this method is called, it will then call the :meth:`.Data.get` method which has different options.

    1. If the user has previously called the :meth:`.Example_Diagnostic.example_value` method, then the data is already loaded into the ``Example_Diagnostic._example_value`` attribute and is returned.

    2. Try to load the data that is already on the computer. When the :class:`.Example_Diagnostic` instance is created, a ``load_filepath`` attribute can be set. If so, a dictionary is loaded in from that file. If that file contains the correct call string then the data is loaded in. If not, then the data is loaded in from the MDSPlus.

    3. Try to load the data from MDSPlus. If a connection has not yet been made to the MDSPlus server, then a connection is made. Once the connection is made then we can just do the normal MDSPlus syntax for getting data from a node.

3. Once the data is loaded in, it is packaged into an array and returned to the :class:`.Example_Diagnostic` instance. This sets the ``Example_Diagnostic._example_value`` attribute. Any future calls will use this value.
