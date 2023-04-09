import json
from http import HTTPStatus
from typing import Mapping, Optional

import aiohttp
import pytest

from .test_settings import test_settings


@pytest.fixture
def make_http_request():
    async def inner(
            service_path: str,
            method: str = 'GET',
            params: Optional[Mapping[str, str]] = None,
            data: Optional[Mapping[dict, dict]] = None,
            headers: Optional[dict] = None,
            path: Optional[Mapping[str, str]] = None,
    ):
        service_url = 'http://{}:{}/api/v11'.format(test_settings.service_url, test_settings.service_port)
        if path:
            url = service_url + service_path + f'/{path}'
        else:
            url = service_url + service_path
        async with aiohttp.request(method=method, url=url, params=params, json=data, headers=headers) as response:
            status = response.status
            if status in [HTTPStatus.OK, HTTPStatus.CREATED, HTTPStatus.ACCEPTED]:
                body = json.loads(await response.text())
            else:
                body = None
        return {'body': body, 'status': status}

    return inner
