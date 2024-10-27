import unittest
from io import StringIO
from contextlib import redirect_stdout
from unittest.mock import patch
from logger import Logger
from pyweb_types import Request


class TestLogger(unittest.TestCase):
    def test_logger_output(self):
        """
        Test that the logger outputs the correct message.
        """
        req: Request = {
            "requestContext": {"http": {"method": "GET", "path": "/test/path"}},
            "queryStringParameters": {"param1": "value1"},
            "headers": {"Header1": "HeaderValue1"},
            "body": "Test body",
        }
        environment = "PRODUCTION"
        with StringIO() as buf, redirect_stdout(buf):
            Logger.request(req, environment)
            output = buf.getvalue()
            self.assertIn("[GET] /test/path", output)

    def test_logger_does_not_output_in_non_production_environments(self):
        """
        Test that the logger does not output in non-production environments.
        """
        req: Request = {
            "requestContext": {"http": {"method": "GET", "path": "/test/path"}},
            "queryStringParameters": {"param1": "value1"},
            "headers": {"Header1": "HeaderValue1"},
            "body": "Test body",
        }
        environment = "LOCAL"
        with StringIO() as buf, redirect_stdout(buf):
            Logger.request(req, environment)
            output = buf.getvalue()
            self.assertEqual(output, "")
