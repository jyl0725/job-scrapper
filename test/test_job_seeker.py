import pytest
import requests
from unittest.mock import patch
from job_scrapper import JobScraper, Level, NoListingException

@pytest.fixture
def mock_get_request():
    with patch('requests.get') as mock_get:
        yield mock_get

def test_get_job_ids(mock_get_request):
    # Mock the requests.get method to return the correct response body
    mock_response = mock_get_request.return_value
    mock_response.status_code = 200
    mock_response.text = """
        <html>
        <head></head>
        <body>
            <li>
                <div class="base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card" data-entity-urn="urn:li:jobPosting:3645698557">
                    <a href="https://www.linkedin.com/jobs/view/software-developer-senior-at-booz-allen-hamilton-3645698557">
                        <h3 class="base-search-card__title">Software Developer, Senior</h3>
                    </a>
                </div>
            </li>
            <li>
                <div class="base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card" data-entity-urn="urn:li:jobPosting:3645757263">
                    <a href="https://www.linkedin.com/jobs/view/principal-applications-analyst-at-nevada-national-security-site-3645757263">
                        <h3 class="base-search-card__title">Principal Applications Analyst</h3>
                    </a>
                </div>
            </li>
        </body>
        </html>
    """

    # Call the method that uses requests.get
    job_scraper = JobScraper("test", False, Level.ENTRY, "day")
    job_ids = job_scraper.get_job_ids(2)

    # Assertions
    assert isinstance(job_ids, list)
    assert len(job_ids) == 2
    assert job_ids == ["3645698557", "3645757263"]
    

def test_get_job_ids_no_result(mock_get_request):
    # Mock the requests.get method to return the correct response body
    mock_response = mock_get_request.return_value
    mock_response.status_code = 200
    mock_response.text = """
        <html>
        <head></head>
        <body>
        </body>
        </html>
    """

    # Assertions
    job_scraper = JobScraper("test", False, Level.ENTRY, "day")
    with pytest.raises(NoListingException):
        job_scraper.get_job_ids(2)