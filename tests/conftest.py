"""Point the app at a throwaway database before any test imports app modules."""

import os
import tempfile

_TEST_DB_DIR = tempfile.mkdtemp(prefix="evt1-tests-")
os.environ["DATABASE_URL"] = f"sqlite:///{os.path.join(_TEST_DB_DIR, 'evt1-test.db')}"
