import json
import unittest
from pyweb import PyWeb
from pyweb_types import PathParams, Request, Response
from sample_data import SampleData


class TestPyWeb(unittest.TestCase):
    def setUp(self) -> None:
        self.app = PyWeb()

    def test_GET_route_registration(self):
        """
        Test the registration of a GET route.
        """

        def test_handler(req: Request, path_params: PathParams = {}) -> Response:
            return self.app.response(200, json.dumps({"message": "GET request"}), {})

        # Register the route
        self.app.GET("/test", test_handler)

        # Check if the route was registered
        self.assertIn("GET", self.app.routes)
        get_routes = self.app.routes.get("GET")
        self.assertIsNotNone(get_routes)
        if get_routes:
            self.assertIn("/test", get_routes)
            self.assertEqual(get_routes["/test"], test_handler)
            event = SampleData().event("GET", "/test")
            self.assertDictEqual(
                test_handler(event, {}),
                {
                    "statusCode": 200,
                    "headers": {"Content-Type": "application/json"},
                    "body": '{"message": "GET request"}',
                },
            )
