import os
from typing import cast
from pyweb_types import Environment


def get_environment() -> Environment:
    environments = ["LOCAL", "DEVELOPMENT", "PRODUCTION"]
    env = os.getenv("ENVIRONMENT")
    if env is None:
        raise ValueError("Environment not set")
    if env not in environments:
        raise ValueError(f"Invalid environment: {env}")
    else:
        return cast(Environment, env)
