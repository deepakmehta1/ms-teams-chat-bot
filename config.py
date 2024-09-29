#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
import os
from dotenv import load_dotenv

""" Bot Configuration """

dotenv_path = os.path.join(".env")
load_dotenv(dotenv_path)

from decouple import config


class DefaultConfig:
    """Bot Configuration"""

    PORT = 3978
    APP_ID = config("MICROSOFT_APP_ID", "app_id")
    APP_PASSWORD = config("MICROSOFT_APP_PASSWORD", "pwd")
    APP_TYPE = config("MICROSOFT_APP_TYPE", "MultiTenant")
    CONNECTION_NAME = config("CONNECTION_NAME", "test-connection")
    AUTH_AUDIENCE = config("AUTH0_AUDIENCE", "")
    AUTH_ISSUER = config("AUTH0_ISSUER", "")
    AUTH_ALGORITHM = config("AUTH0_ALGORITHM", "")
