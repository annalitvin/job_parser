import uuid
import pyarrow as pa
import pyarrow.parquet as pq

from asyncio import Task
from datetime import datetime, date
from typing import List, Dict

import aiohttp
import asyncio

from bs4.element import Tag, ResultSet
from aiohttp import ClientResponse
from bs4 import BeautifulSoup

from app.constants import INDEX_SITE_PAGE
from app.constants import REQUEST_HEADERS
from app.constants import APPLY_BUTTON_TEXT
from app.constants import LOCATION_ID
from app.constants import POSTED_DATE_ID
from app.constants import RESULTS_CONTAINER_ID
from app.constants import JOB_CONTAINER_ID
from app.constants import CONTENT_CLASS
from app.constants import BOX_CLASS
from app.constants import CARD_FOOTER_CLASS
from app.constants import CARD_BLOCK_CLASS
from app.constants import JOB_ITEMS_PARQUET_FILE_PATH
from app.schemas.job_items import JobItem


async def download_site(session: aiohttp.ClientSession, url: str, headers: dict) -> ClientResponse:
    """Download site page by url"""
    response = await session.get(url, headers=headers)
    return response


def get_page_soup_html(text: str) -> BeautifulSoup:
    """Get content to parse web-page with  BeautifulSoup object using html parser.
    Doc: https://www.crummy.com/software/BeautifulSoup/bs4/doc"""
    return BeautifulSoup(text, "html.parser")


def get_job_items(soup: BeautifulSoup) -> ResultSet:
    """Get job items from index page."""
    results_container: Tag = soup.find("div", id=RESULTS_CONTAINER_ID)
    jobs: ResultSet = results_container.find_all("div", class_=CARD_BLOCK_CLASS)
    return jobs


async def get_position_data(session: aiohttp.ClientSession, url: str, headers: dict) -> Dict:
    """Grabs data from particular job position."""
    async with await download_site(session, url, headers) as response:
        job_page: BeautifulSoup = get_page_soup_html(await response.text())
        job_container: Tag = job_page.find(id=JOB_CONTAINER_ID)
        box: Tag = job_container.find("div", class_=BOX_CLASS)
        title: str = box.h1.get_text()
        subtitle: str = box.h2.get_text()
        content: Tag = box.find(class_=CONTENT_CLASS)
        description: str = content.p.text.strip()
        location: str = content.find(id=LOCATION_ID).text.split(":")[1].strip()
        posted: str = content.find(id=POSTED_DATE_ID).text.split(":")[1].strip()
        posted_date: datetime = datetime.strptime(posted, "%Y-%d-%m")

        return JobItem(
            id=str(uuid.uuid4()),
            title=title,
            subtitle=subtitle,
            description=description,
            location=location,
            posted=posted_date,
        ).model_dump()


async def gather_data():
    """Collects JobItem objects. Each of which represents information obtained from job item page."""
    async with aiohttp.ClientSession() as session:
        response: ClientResponse = await download_site(session, INDEX_SITE_PAGE, REQUEST_HEADERS)
        main_page: BeautifulSoup = get_page_soup_html(await response.text())
        job_positions: ResultSet = get_job_items(main_page)
        tasks: List[Task] = []
        for item in job_positions:
            card_footer: Tag = item.find("footer", class_=CARD_FOOTER_CLASS)
            position_detail_href: str = card_footer.find("a", string=APPLY_BUTTON_TEXT)["href"]
            task: Task = asyncio.create_task(get_position_data(session, position_detail_href, REQUEST_HEADERS))
            tasks.append(task)
        return await asyncio.gather(*tasks)


async def main():
    """Main coroutine."""
    return await gather_data()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    done = loop.run_until_complete(main())

    job_items = pa.array(done)
    schema = pa.schema(
        [
            pa.field("id", pa.string()),
            pa.field("title", pa.string()),
            pa.field("subtitle", pa.string()),
            pa.field("description", pa.string()),
            pa.field("location", pa.string()),
            pa.field("posted", pa.timestamp("us")),
        ],
        metadata={"day": f"{date.today().day}"},
    )
    job_items_table = pa.Table.from_pylist(job_items, schema=schema)
    pq.write_table(job_items_table, JOB_ITEMS_PARQUET_FILE_PATH)
