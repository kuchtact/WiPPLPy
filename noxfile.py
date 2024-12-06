import nox

supported_python_versions = ("3.9", "3.10", "3.11", "3.12")
maxpython = max(supported_python_versions)

# Set the default backend to conda if available, because it is probably
# needed to install MDSplus installation anyway. The next choice is uv
# because it has excellent performance when resolving requirements.
nox.options.default_venv_backend = "mamba|conda"


def install_environment(session, environment_path="mamba_environment.yml"):
    session.run(
        *[
            session.venv_backend,
            "env",
            "update",
            "--verbose",
            "--prefix",
            session.virtualenv.location,
            "--file",
            environment_path,
        ],
        silent=False,
    )


test_specifiers: list = [
    nox.param("run all tests", id="all"),
    nox.param("with code coverage", id="cov"),
]

with_coverage: tuple[str, ...] = (
    "--cov=wipplpy",
    "--cov-report=xml",
    "--cov-config=pyproject.toml",
    "--cov-append",
    "--cov-report",
    "xml:coverage.xml",
)


@nox.session(python=supported_python_versions)
@nox.parametrize("test_specifier", test_specifiers)
def tests(session, test_specifier):
    """Run tests with pytest."""
    install_environment(session)

    options = []
    if test_specifier == "with code coverage":
        options += with_coverage

    session.run("pytest", *options)


@nox.session(python=maxpython)
def docs(session):
    """Build documentation with Sphinx."""
    session.install("sphinx")
    session.run("sphinx-build", "-b", "html", "docs/source/", "docs/build/")
