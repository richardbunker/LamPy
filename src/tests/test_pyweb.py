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

    def test_POST_route_registration(self):
        """
        Test the registration of a GET route.
        """

        def test_handler(req: Request, path_params: PathParams = {}) -> Response:
            return self.app.response(200, json.dumps({"message": "POST request"}), {})

        # Register the route
        self.app.POST("/test", test_handler)

        # Check if the route was registered
        self.assertIn("POST", self.app.routes)
        post_routes = self.app.routes.get("POST")
        self.assertIsNotNone(post_routes)
        if post_routes:
            self.assertIn("/test", post_routes)
            self.assertEqual(post_routes["/test"], test_handler)
            event = SampleData().event("POST", "/test")
            self.assertDictEqual(
                test_handler(event, {}),
                {
                    "statusCode": 200,
                    "headers": {"Content-Type": "application/json"},
                    "body": '{"message": "POST request"}',
                },
            )

    def test_unregistered_method(self):
        """
        Test the handling of an unregistered method.
        """
        event = SampleData().event("PUT", "/test")
        response = self.app.handle(event)
        self.assertDictEqual(
            response, {"statusCode": 405, "headers": {"Content-Type": "application/json"}, "body": "Method not allowed"}
        )

    def test_unregistered_route(self):
        """
        Test the handling of an unregistered route.
        """

        def test_handler(req: Request, path_params: PathParams = {}) -> Response:
            return self.app.response(200, json.dumps({"message": "GET request"}), {})

        self.app.GET("/", test_handler)
        event = SampleData().event("GET", "/unregistered")
        response = self.app.handle(event)
        self.assertDictEqual(
            response, {"statusCode": 404, "headers": {"Content-Type": "application/json"}, "body": "Not found"}
        )
        event_2 = SampleData().event("GET", "/")
        response_2 = self.app.handle(event_2)
        self.assertDictEqual(
            response_2,
            {
                "statusCode": 200,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"message": "GET request"}),
            },
        )

    def test_path_params(self):
        """
        Test the handling of path parameters.
        """

        def test_handler(req: Request, path_params: PathParams) -> Response:
            return self.app.response(200, json.dumps(path_params), {})

        self.app.GET("/user/:user_id", test_handler)
        self.app.GET("/posts", test_handler)
        event = SampleData().event("GET", "/user/123")
        response = self.app.handle(event)
        self.assertDictEqual(
            response,
            {
                "statusCode": 200,
                "headers": {"Content-Type": "application/json"},
                "body": json.dumps({"user_id": "123"}),
            },
        )
        event_2 = SampleData().event("GET", "/posts")
        response_2 = self.app.handle(event_2)
        self.assertDictEqual(
            response_2, {"statusCode": 200, "headers": {"Content-Type": "application/json"}, "body": json.dumps({})}
        )
