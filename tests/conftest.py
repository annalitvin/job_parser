import pytest

JOB_ITEM_URL = "https://realpython.github.io/fake-jobs/jobs/senior-python-developer-0.html"


@pytest.fixture
def job_item_html():
    mock_response = """
    <!DOCTYPE html>
        <html>
          <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>Fake Python</title>
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@0.9.2/css/bulma.min.css">
          </head>
          <body>
          <section class="section">
            <div class="container mb-5">
              <h1 class="title is-1">
                Fake Python
              </h1>
              <p class="subtitle is-3">
                Fake Jobs for Your Web Scraping Journey
              </p>
            </div>
            <div class="container">
            <div id="ResultsContainer" class="columns is-multiline">
            <div class="box">
        <h1 class="title is-2">Energy engineer</h1>
        <h2 class="subtitle is-4 company">Vasquez-Davidson</h2>
        <div class="content">
            <p>Party prevent live. Quickly candidate change although. Together type music hospital. Every speech support
            time operation wear often.</p>
            <p id="location"><strong>Location:</strong> Christopherville, AA</p>
            <p id="date"><strong>Posted:</strong> 2021-04-08</p>
        </div>
        </div>

            </div>
            </div>
          </section>
          </body>
        </html>
    """
    return mock_response
