#
# Author: Rohtash Lakra
#
import os

# Select the testing env, so that '.env.test' (not the development '.env') is used and the tests use the test database.
# NOTE: 'unittest' discovery imports the application's packages before this package, so the testing env must be
# selected when the process starts, i.e. run the tests with `make test` or `ENV_TYPE=test python -m unittest`.
os.environ["ENV_TYPE"] = "test"

from settings import ENV_FILE  # noqa: E402

if ENV_FILE != ".env.test":
    # Fail fast instead of silently running the tests against the development database.
    raise RuntimeError(
        f"The tests must run with ENV_TYPE=test (loaded env file is '{ENV_FILE}'). "
        "Use `make test`, ./runUnitTests.sh or `ENV_TYPE=test python -m unittest`."
    )

# The FastAPI application under test (tests are executed from the project root, like the application).
from main import app  # noqa: E402
