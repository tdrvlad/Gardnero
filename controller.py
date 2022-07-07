import connexion
import six
from typing import Dict
from typing import Tuple
from typing import Union

from openapi_server.models.inline_response200 import InlineResponse200  # noqa: E501
from openapi_server import util

import time
from timeloop import Timeloop
from datetime import timedelta

# tl = Timeloop()
# @tl.job(interval=timedelta(seconds=2))
def sample_job(job_id):
    print(f"Job {job_id} current time : {time.ctime()}")


TIMELOOP_CIRCUITS = {}
CIRCUITS_CONFIG = {}

def config_circuit(circuit_id, days_period, execution_time):  # noqa: E501
    """config_circuit

    Configure the time period # noqa: E501

    :param circuit_id: Circuit ID.
    :type circuit_id: str
    :param days_period: Number of days between execution.
    :type days_period:
    :param execution_time: Duration for the Circuit execution in seconds.
    :type execution_time: int

    :rtype: Union[str, Tuple[str, int], Tuple[str, int, Dict[str, str]]
    """

    global TIMELOOP_CIRCUITS, CIRCUITS_CONFIG

    if circuit_id in TIMELOOP_CIRCUITS.keys():
        TIMELOOP_CIRCUITS[circuit_id].stop()

    TIMELOOP_CIRCUITS[circuit_id] = Timeloop()
    TIMELOOP_CIRCUITS[circuit_id]._add_job(
        sample_job,
        interval=timedelta(seconds=days_period),
        job_id=circuit_id
    )
    TIMELOOP_CIRCUITS[circuit_id].start(block=False)
    CIRCUITS_CONFIG[circuit_id] = [days_period, execution_time]
    return 'Done'


def get_circuits():  # noqa: E501
    """get_circuits

    Retrieve the current Circuits configuration. # noqa: E501


    :rtype: Union[List[InlineResponse200], Tuple[List[InlineResponse200], int], Tuple[List[InlineResponse200], int, Dict[str, str]]
    """
    response = []
    global CIRCUITS_CONFIG
    for k, v in CIRCUITS_CONFIG.items():
        response.append([k, v[0], v[1]])
    return response


def start_circuit(circuit_id):  # noqa: E501
    """start_circuit

    Trigger the execution of a Circuit # noqa: E501

    :param circuit_id: Circuit ID.
    :type circuit_id: str

    :rtype: Union[str, Tuple[str, int], Tuple[str, int, Dict[str, str]]
    """
    return 'do some magic!'
