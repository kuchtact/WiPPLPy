from pathlib import Path

import nox
from yaml import safe_load

supported_python_versions = ("3.9", "3.10", "3.11", "3.12")
maxpython = max(supported_python_versions)

# Set the default backend to conda if available, because it is probably
# needed to install MDSplus installation anyway. The next choice is uv
# because it has excellent performance when resolving requirements.
nox.options.default_venv_backend = "conda|uv|virtualenv"

# Load in the conda environment file.
environment = safe_load(Path("mamba_environment.yml").read_text())
channels = environment.get("channels")
conda = environment.get("dependencies")
requirements = conda.pop(-1).get("pip")


def install_environment(session):
    session.conda_install(*conda, channel=channels, silent=False)
    session.install(*requirements)


@nox.session(python=supported_python_versions, venv_backend="mamba")
def tests(session):
    """Run tests with pytest."""
    install_environment(session)
    session.run("pytest")


@nox.session(python=maxpython)
def docs(session):
    """Build documentation with Sphinx."""
    session.install("sphinx")
    session.run("sphinx-build", "-b", "html", "docs/source/", "docs/build/")
