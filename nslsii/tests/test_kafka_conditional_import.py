import os
import subprocess
import sys

import pytest


def test_conditional_import_negative_case():
    """
    Test that bluesky_kafka is not imported when publish_documents_to_kafka=False.

    This is a "subprocess test" meaning the entire test function executes in a
    separate python interpreter and the pass/fail result is returned by sys.exit().
    This is necessary to guarantee bluesky_kakfa has not been imported as a result
    of other tests.
    """
    the_test = """
import pprint
import sys
from unittest.mock import Mock

import IPython.core.interactiveshell
import nslsii

#pprint.pprint(sys.modules)
ip = IPython.core.interactiveshell.InteractiveShell()
nslsii.configure_base(
    user_ns=ip.user_ns,
    # a mock databroker will be enough for this test
    broker_name=Mock(),
    bec=False,
    epics_context=False,
    magics=False,
    mpl=False,
    configure_logging=False,
    pbar=False,
    ipython_logging=False,
    # this is the important condition for the test
    publish_documents_to_kafka=False,
)

if "bluesky_kafka" in sys.modules:
    sys.exit(1)
else:
    sys.exit(0)    
"""
    proc = subprocess.run(
        [sys.executable, "-c", the_test],
    )

    if proc.returncode:
        pytest.fail(
            "The subprocess returned with non-zero exit status " f"{proc.returncode}."
        )


def test_conditional_import_positive_case():
    """
    Test that bluesky_kafka is imported when publish_documents_to_kafka=True.

    The connection to a Kafka broker will fail but that does not affect the test result.

    This is a "subprocess test" meaning the entire test function executes in a
    separate python interpreter and the pass/fail result is returned by sys.exit().
    This is necessary to guarantee bluesky_kakfa has not been imported as a result
    of other tests.
    """
    the_test = """
import pprint
import sys
from unittest.mock import Mock

import IPython.core.interactiveshell
import nslsii

#pprint.pprint(sys.modules)
ip = IPython.core.interactiveshell.InteractiveShell()
nslsii.configure_base(
    user_ns=ip.user_ns,
    # a mock databroker will be enough for this test
    broker_name=Mock(),
    bec=False,
    epics_context=False,
    magics=False,
    mpl=False,
    configure_logging=False,
    pbar=False,
    ipython_logging=False,
    # this is the important condition for the test
    publish_documents_to_kafka=True,
)
#pprint.pprint(sys.modules)
if "bluesky_kafka" in sys.modules:
    sys.exit(0)
else:
    sys.exit(1)    
"""
    proc = subprocess.run(
        [sys.executable, "-c", the_test],
        env={**os.environ, "BLUESKY_KAFKA_BOOTSTRAP_SERVERS": "127.0.0.1:9092"},
    )

    if proc.returncode:
        pytest.fail(
            "The subprocess returned with non-zero exit status " f"{proc.returncode}."
        )
