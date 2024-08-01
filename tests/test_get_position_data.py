from datetime import datetime

import pytest
from asyncmock import AsyncMock
import aiohttp

from app.constants import REQUEST_HEADERS
from app.main import get_position_data
from tests.conftest import JOB_ITEM_URL


@pytest.mark.asyncio
async def test_get_cat_fact_mocked(mocker, job_item_html):
    mocker.patch("app.main.download_site").return_value.__aenter__.return_value.text = AsyncMock(
        return_value=job_item_html
    )

    async with aiohttp.ClientSession() as session:
        job_item = await get_position_data(session, JOB_ITEM_URL, REQUEST_HEADERS)

    assert job_item["title"] == "Energy engineer"
    assert job_item["subtitle"] == "Vasquez-Davidson"
    assert (
        "Party prevent live. Quickly candidate change although. Together type music "
        "hospital." in job_item["description"]
    )
    assert job_item["location"] == "Christopherville, AA"
    assert job_item["posted"] == datetime.strptime("2021-04-08", "%Y-%d-%m")
