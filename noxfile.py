import nox


PYTHON_VERSIONS=("3.10", "3.11", "3.12")


@nox.session(python=PYTHON_VERSIONS)
def tests(session):
    """Run tests with pytest."""
    session.install(".")
    session.run(pytest)


@nox.session(python="3.12")
def build_docs(session):
    """Build documentation with Sphinx."""
    session.install("sphinx")
    session.run("sphinx-build", "-b", "html", "docs/source/", "docs/build/")
