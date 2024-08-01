from os import path

INDEX_SITE_PAGE = (
    "https://raw.githubusercontent.com/realpython/fake-jobs/" "9ed86ca6a4ef4a439a28935e44829c8b7e9694cf/index.html"
)
REQUEST_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) " "Gecko/20100101 Firefox/104.0",
    "Accept": "*/*",
}
# Index page
APPLY_BUTTON_TEXT = "Apply"
RESULTS_CONTAINER_ID = "ResultsContainer"
CARD_BLOCK_CLASS = "column is-half"
CARD_FOOTER_CLASS = "card-footer"
# Job page
JOB_CONTAINER_ID = "ResultsContainer"
BOX_CLASS = "box"
CONTENT_CLASS = "content"
LOCATION_ID = "location"
POSTED_DATE_ID = "date"

parent_dir = path.dirname(path.abspath(__file__))
JOB_ITEMS_PARQUET_FILE_PATH = path.join(parent_dir, "job_items.parquet")
