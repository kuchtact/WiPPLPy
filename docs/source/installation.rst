.. _installation:

************
Installation
************

Installing WiPPLPy as a Contributor
===================================

This installation is very similar to how PlasmaPy installation is done for
contributors: https://docs.plasmapy.org/en/stable/contributing/getting_ready.html.
We've done some copy-pasting as to which steps should be followed.

If you are stuck or don't understand something, please ask for help or take a
look at the `PlasmaPy's code contribution workflow`_.

Pre-requisites
--------------

.. _opening-a-terminal:

Opening a terminal
^^^^^^^^^^^^^^^^^^

The commands in this page are intended to be run in a ``Unix`` terminal. If you
are new to Unix, check out this `Unix tutorial`_ and these `frequently used
Unix commands`_.

Windows
"""""""

There are several options for terminals on Windows.

* Powershell_ comes pre-installed with Windows. These instructions cover
  `opening Powershell`_. We recommend Powershell for a quick start, if Windows
  is the only operating system you use, or if you have not used Unix before.

* We recommend `Windows Subsystem for Linux`_ (WSL) if you are familiar with
  Unix, you use macOS or Linux too, or you expect to contribute to WiPPLPy
  extensively. These instructions cover `installing WSL`_. If you choose WSL,
  follow the tabs for :guilabel:`Linux/WSL` below.

macOS
"""""

In the :guilabel:`Finder`, go to :guilabel:`Applications`. Enter the
:guilabel:`Utilities` folder and double click on :guilabel:`Terminal`.

Linux/WSL
"""""""""

Open a terminal by using :kbd:`Ctrl + Alt + T`.

.. _installing-python:

Installing Python
^^^^^^^^^^^^^^^^^

We suggest using Mamba_ to install Python_. Mamba_ is a versatile package and
environment management system which is widely used in the data science and
scientific Python communities that is similar to Conda_. It is a command line
interface for installing packages.

* If you already have Conda_ installed, then follow the `installing Mamba from
  an existing Conda install`_.

* Otherwise, follow the `installing Mamba`_ instructions.

Using git and GitHub
^^^^^^^^^^^^^^^^^^^^

Code contributions to WiPPLPy are made using git_ and GitHub_. Before
contributing code to WiPPLPy, please take the following steps:

#. `Sign up on GitHub`_ for a free account.

#. Verify that git_ is installed by
   :ref:`opening a terminal <opening-a-terminal>` and running:

   .. code-block:: bash

      git --version

   If there is an error, follow these instructions to `install git`_.

#. Optionally, configure git_ with your name with a command like:

   .. code-block:: bash

      git config --global user.name "Your Name"

   You can also configure git_ with your email with a command like:

   .. code-block:: bash

      git config --global user.email "your.email@example.com"

   You may also set your default editor with a command like the
   following, where ``notepad`` can be replaced with the name or path of
   your preferred editor:

   .. code-block:: bash

      git config --global core.editor notepad

   For different editor and configuration options, check out `git
   commands for setup and config`_.

#. `Add a new SSH key to your GitHub account`_. This step is needed for
   authentication purposes.

Forking and cloning the repository
----------------------------------

#. Log into `GitHub`_.

#. Go to the `WiPPLPy repository`_.

#. Create a fork of WiPPLPy by clocking on :guilabel:`Fork`, followed by
   :guilabel:`Create Fork`.

#. :ref:`Open a terminal <opening-a-terminal>`. Navigate to the folder where
   you want to clone the WiPPLPy repository. For example, to clone the
   repository into the :file:`~/repos/` directory, run:

   .. code-block:: bash

      mkdir ~/repos
      cd ~/repos

#. Clone_ the WiPPLPy repository with the following command, replacing
   ``YOUR-USERNAME`` with your GitHub username. This will create a
   subdirectory called :file:`WiPPLPy/` containing your local clone of
   the repository.

   .. code-block:: bash

      git clone git@github.com:YOUR-USERNAME/WiPPLPy.git

   .. tip::

      If you have trouble connecting to GitHub, you may need to `add a
      new SSH key to your GitHub account`_.

#. Enter the newly created directory with:

   .. code-block:: bash

      cd WiPPLPy

#. Add a remote_ called ``upstream`` for the `WiPPLPy's repository`
   by using the following command.

   .. code-block:: bash

      git remote add upstream git@github.com:kuchtact/WiPPLPy.git

   If you run ``git remote -v``, you should see that ``origin``
   corresponds to your fork_ and ``upstream`` corresponds to
   the `WiPPLPy repository`_.

Installing WiPPLPy from a Fork
------------------------------

Once Mamba_ is installed and you have cloned your fork of the git repository
then we need to create an environment for running the code in.

#. :ref:`Open a terminal <opening-a-terminal>`.

#. Navigate to the directory for your clone of WiPPLPy, which should be
   named :file:`WiPPLPy`. For example, if you ran the ``git clone``
   command in the :file:`~/repos/` directory, then run:

   .. code-block:: bash

      cd ~/repos/WiPPLPy

   .. note::

      In Windows, the directory path will be :file:`C:\\Users\\<username>\\repos\\WiPPLPy`.

#. Create a Mamba_ environment using the packages from
   :file:`mamba_environment.yml`. If you are on Windows, Linux, or macOS that
   doesn't use the silicon processor you can do so by running:

   .. code-block:: bash

      mamba env create -f ./mamba_environment.yml

   If you are on a computer that uses the Mac silicon processor you can do so by

   .. code-block:: bash

      CONDA_SUBDIR=osx-64 mamba env create -f ./mamba_environment.yml

   This will create a new environment called ``WiPPLPy``.

#. Activate the environment and start python by running:

   .. code-block:: bash

      mamba activate WiPPLPy
      python

#. We need to add the :file:`WiPPLPy/source/` directory to the Python path. We
   can find the path to :file:`WiPPLPy/source/` and the :file:`site-packages`
   directory by running the following Python code:

   .. code-block:: python

      from distutils.sysconfig import get_python_lib

      print("site-packaged directory:", get_python_lib())
      import os

      print("WiPPLPy source code directory:", os.getcwd())

6. Exit out of python and navigate to the :file:`site-packages` directory that
   was printed. It should end in :file:`site-packages`.

7. Create a file called :file:`wipplpy.pth`. This file should contain the path
   to the :file:`WiPPLPy/src/` directory. For example, if the path to the
   :file:`WiPPLPy/src/` directory is :file:`/Users/username/repos/WiPPLPy/src/`
   then the :file:`wipplpy.pth` file should contain the following:

   .. code-block:: bash

      /Users/username/repos/WiPPLPy/src/

#. Test that the installation was successful by running the following Python
   code:

   .. code-block:: python

      from wipplpy.modules import shot_loader

   If there are no errors then the installation was successful.


Installing WiscVPN for Remote Data Access
-----------------------------------------

To access data remotely, you will need to have access to the UW-Madison Plasma
Network. This can be done by `installing WiscVPN`_ and getting your static IP
address added to the network.


Creating Documentation
======================

To create the documentation, you will need to have `nox`_ installed. `nox`_
then installs `Sphinx`_ and creates the documentation when you run the
following command::

    nox -s docs

This will create the documentation in the :file:`docs/build/html/` directory.
Open the documentation by double clicking on the :file:`index.html` file in the
:file:`docs/build/html/` directory.

Installing Pre-commit
=====================

Follow the instruction found here: https://docs.plasmapy.org/en/stable/contributing/pre-commit.html

.. _Sphinx: https://www.sphinx-doc.org/en/master/usage/installation.html
.. _`nox`: https://nox.thea.codes
.. _Add a new SSH key to your GitHub account: https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account
.. _clone: https://github.com/git-guides/git-clone
.. _Conda: https://docs.conda.io
.. _Mamba: https://mamba.readthedocs.io/en/latest/index.html
.. _Python: https://www.python.org
.. _fork: https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/about-forks
.. _frequently used Unix commands: https://faculty.tru.ca/nmora/Frequently%20used%20UNIX%20commands.pdf
.. _install git: https://git-scm.com/book/en/v2/Getting-Started-Installing-Git
.. _installing Mamba from an existing Conda install: https://mamba.readthedocs.io/en/latest/installation/mamba-installation.html#existing-conda-install-not-recommended
.. _installing Conda: https://conda.io/projects/conda/en/latest/user-guide/install/index.html
.. _installing Mamba: https://github.com/conda-forge/miniforge?tab=readme-ov-file#install
.. _installing WSL: https://learn.microsoft.com/en-us/windows/wsl/install
.. _opening Powershell: https://learn.microsoft.com/en-us/powershell/scripting/windows-powershell/starting-windows-powershell?view=powershell-7.3
.. _powershell: https://learn.microsoft.com/en-us/powershell
.. _remote: https://github.com/git-guides/git-remote
.. _sign up on GitHub: https://github.com/join
.. _unix tutorial: https://www.hpc.iastate.edu/guides/unix-introduction/unix-tutorial-1
.. _Windows Subsystem for Linux: https://learn.microsoft.com/en-us/windows/wsl
.. _git: https://git-scm.com
.. _GitHub: https://github.com
.. _WiPPLPy repository: https://github.com/kuchtact/WiPPLPy
.. _PlasmaPy's code contribution workflow: https://docs.plasmapy.org/en/stable/contributing/workflow.html
.. _installing WiscVPN: https://it.wisc.edu/services/wiscvpn/
