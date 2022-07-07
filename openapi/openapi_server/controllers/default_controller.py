import connexion
import six
from typing import Dict
from typing import Tuple
from typing import Union

from openapi_server.models.inline_response200 import InlineResponse200  # noqa: E501
from openapi_server import util


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
    return 'do some magic!'


def get_circuits():  # noqa: E501
    """get_circuits

    Retrieve the current Circuits configuration [CircuitId, DaysPeriod, ExecutionTime]. # noqa: E501


    :rtype: Union[List[InlineResponse200], Tuple[List[InlineResponse200], int], Tuple[List[InlineResponse200], int, Dict[str, str]]
    """
    return 'do some magic!'


def start_circuit(circuitl_id):  # noqa: E501
    """start_circuit

    Trigger the execution of a Circuit # noqa: E501

    :param circuitl_id: Circuit ID.
    :type circuitl_id: str

    :rtype: Union[str, Tuple[str, int], Tuple[str, int, Dict[str, str]]
    """
    return 'do some magic!'
