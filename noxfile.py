import nox

supported_python_versions = ("3.9", "3.10", "3.11", "3.12")
maxpython = max(supported_python_versions)

# Set the default backend to conda if available, because it is probably
# needed to install MDSplus installation anyway. The next choice is uv
# because it has excellent performance when resolving requirements.
nox.options.default_venv_backend = "conda|uv|virtualenv"


def install_environment(
    session, venv_backend, environment_path="mamba_environment.yml"
):
    session.run(
        *[
            venv_backend,
            "env",
            "update",
            "--prefix",
            session.virtualenv.location,
            "--file",
            environment_path,
        ],
        silent=False,
    )


@nox.session(python=supported_python_versions, venv_backend="mamba")
def tests(session):
    """Run tests with pytest."""
    install_environment(session, session.venv_backend)
    session.run("pytest")


@nox.session(python=maxpython)
def docs(session):
    """Build documentation with Sphinx."""
    session.install("sphinx")
    session.run("sphinx-build", "-b", "html", "docs/source/", "docs/build/")
