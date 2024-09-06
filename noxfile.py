import nox

supported_python_versions = ("3.9", "3.10", "3.11", "3.12")
maxpython = max(supported_python_versions)

# Set the default backend to conda if available, because it is probably
# needed to install MDSplus installation anyway. The next choice is uv
# because it has excellent performance when resolving requirements.
nox.options.default_venv_backend = "conda|uv|virtualenv"


@nox.session(python=supported_python_versions)
def tests(session):
    """Run tests with pytest."""
    session.install(".")
    session.run(pytest)


@nox.session(python=maxpython)
def docs(session):
    """Build documentation with Sphinx."""
    session.install("sphinx")
    session.run("sphinx-build", "-b", "html", "docs/source/", "docs/build/")
