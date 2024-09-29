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
    APP_ID = '047c163b-876b-4401-9434-1f67a1c87173'
    APP_PASSWORD = 'UJ58Q~fJNXf8FDMdGN_Lh6l5M8m6847tIe~qOa2k'
    APP_TYPE = config("MicrosoftAppType", "MultiTenant")
    APP_TENANTID = config("MicrosoftAppTenantId", "")
    CONNECTION_NAME = config("ConnectionName", "test-connection")
    AUTH_AUDIENCE = config("Auth0Audience", "")
    AUTH_ISSUER = config("Auth0Issuer", "")
    AUTH_ALGORITHM = config("Auth0Algorithm", "")
    GCD_ORCH_TEMPLATE = config("OrchestrationTemplateID", "")
    GCD_ORCH_TEMPLATE_VERSION = config("OrchestrationTemplateVersionID", "")
    LLM_FLOW_SERVICE_URL = config("LLMFlowServiceURL", "")
