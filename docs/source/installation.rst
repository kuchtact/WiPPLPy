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
look at the `PlasmaPy's conde contribution workflow`_.

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
   :file:`mamba_environment.yml`. If you are on a computer that does not use 
   the Mac silicon processor you can do so by running

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
      print('site-packaged directory:', get_python_lib())
      import os
      print('WiPPLPy source code directory:', os.getcwd())

#. Exit out of python and nagigate to the :file:`site-packages` directory that 
   was printed. It should end in :file:`site-packages`.

#. Create a file called :file:`wipplpy.pth`. This file should contain the path 
   to the :file:`WiPPLPy/source/` directory. For example, if the path to the 
   :file:`WiPPLPy/source/` directory is :file:`/Users/username/repos/WiPPLPy/source/` 
   then the :file:`wipplpy.pth` file should contain the following:

   .. code-block:: bash

      /Users/username/repos/WiPPLPy/source/

#. Test that the installation was successful by running the following Python 
   code:

   .. code-block:: python

      from wipplpy.modules import shot_loader

   If there are no errors then the installation was successful.


Creating Documentation
======================

To create the documentation, you will need to have `Sphinx`_ installed and 
`make`_. This should have already been installed when you created your Mamba environment.

Then, you can create the documentation by entering the ``docs/`` directory and 
running the following command::

    make html

This will create the documentation in the :file:`docs/build/html/` directory. 
Open the documentation by double clicking on the :file:`index.html` file in the 
:file:`docs/build/html/` directory.

.. _Sphinx: https://www.sphinx-doc.org/en/master/usage/installation.html
.. _make: https://www.gnu.org/software/make/
.. _Add a new SSH key to your GitHub account: https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account
.. _clone: https://github.com/git-guides/git-clone
.. _Conda: https://docs.conda.io
.. _Mamba: https://mamba.readthedocs.io/en/latest/index.html
.. _creating an environment: https://docs.anaconda.com/navigator/tutorials/manage-environments/#creating-a-new-environment
.. _Python: https://www.python.org
.. _download Python: https://www.python.org/downloads
.. _fork: https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/working-with-forks/about-forks
.. _frequently used Unix commands: https://faculty.tru.ca/nmora/Frequently%20used%20UNIX%20commands.pdf
.. _git commands for setup and config: https://git-scm.com/book/en/v2/Appendix-C%3A-Git-Commands-Setup-and-Config
.. _install git: https://git-scm.com/book/en/v2/Getting-Started-Installing-Git
.. _install Graphviz: https://graphviz.org/download
.. _install pandoc: https://pandoc.org/installing.html
.. _installing Mamba from an existing Conda install: https://mamba.readthedocs.io/en/latest/installation/mamba-installation.html#existing-conda-install-not-recommended
.. _installing Conda: https://conda.io/projects/conda/en/latest/user-guide/install/index.html
.. _installing Mamba: https://github.com/conda-forge/miniforge?tab=readme-ov-file#install
.. _installing Python: https://realpython.com/installing-python
.. _installing WSL: https://learn.microsoft.com/en-us/windows/wsl/install
.. _miniconda: https://docs.conda.io/en/latest/miniconda.html
.. _opening Powershell: https://learn.microsoft.com/en-us/powershell/scripting/windows-powershell/starting-windows-powershell?view=powershell-7.3
.. _powershell: https://learn.microsoft.com/en-us/powershell
.. _Real Python: https://realpython.com
.. _remote: https://github.com/git-guides/git-remote
.. _sign up on GitHub: https://github.com/join
.. _terminal user guide: https://support.apple.com/guide/terminal/welcome/mac
.. _unix tutorial: https://www.hpc.iastate.edu/guides/unix-introduction/unix-tutorial-1
.. _using an environment: https://docs.anaconda.com/navigator/tutorials/manage-environments/#using-an-environment
.. _venv: https://docs.python.org/3/library/venv.html
.. _virtual environment: https://realpython.com/python-virtual-environments-a-primer
.. _Windows Subsystem for Linux: https://learn.microsoft.com/en-us/windows/wsl
.. _WSL: https://learn.microsoft.com/en-us/windows/wsl
.. _git: https://git-scm.com
.. _GitHub: https://github.com
.. _WiPPLPy repository: https://github.com/kuchtact/WiPPLPy
.. _PlasmaPy's conde contribution workflow: https://docs.plasmapy.org/en/stable/contributing/workflow.html

