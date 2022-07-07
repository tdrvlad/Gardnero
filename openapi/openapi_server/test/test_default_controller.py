# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from openapi_server.models.inline_response200 import InlineResponse200  # noqa: E501
from openapi_server.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_config_circuit(self):
        """Test case for config_circuit

        
        """
        query_string = [('circuitlId', 'circuitl_id_example'),
                        ('daysPeriod', 3.4),
                        ('executionTime', 56)]
        headers = { 
            'Accept': 'application/yaml',
        }
        response = self.client.open(
            '/configureCircuit',
            method='POST',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_circuits(self):
        """Test case for get_circuits

        
        """
        headers = { 
            'Accept': 'application/yaml',
        }
        response = self.client.open(
            '/circuits',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_start_circuit(self):
        """Test case for start_circuit

        
        """
        query_string = [('circuitlId', 'circuitl_id_example')]
        headers = { 
            'Accept': 'application/yaml',
        }
        response = self.client.open(
            '/startCircuit',
            method='POST',
            headers=headers,
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
