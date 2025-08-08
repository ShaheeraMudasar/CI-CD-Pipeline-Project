import os

import pytest
import requests
from hamcrest import assert_that, contains_string, equal_to, instance_of, is_


@pytest.fixture
def app_url():
    """Hämta AppRunner-URL från miljövariabel."""
    url = os.getenv("APPRUNNER_URL")
    if not url:
        pytest.fail("APPRUNNER_URL environment variable not set")

    # Säkerställ att URL har korrekt schema (AppRunner använder HTTPS)
    url = url.rstrip("/")
    if not url.startswith(("http://", "https://")):
        url = f"https://{url}"

    return url


def test_health_endpoint(app_url: str):
    """Testa att health-endpointen returnerar 200 OK."""
    # GIVEN en driftsatt applikation med en health-endpoint
    health_url = f"{app_url}/api/v1/health"

    # WHEN vi begär hälsostatus
    response = requests.get(health_url)

    # THEN ska svaret vara utan fel
    assert_that(response.status_code, is_(equal_to(200)))


def test_home_page_loads(app_url: str):
    """Testa att startsidan laddas korrekt."""
    # GIVEN en driftsatt applikation
    home_url = app_url
    page_title = "DevOps1-bloggen"

    # WHEN vi begär startsidan
    response = requests.get(home_url)

    # THEN ska sidan laddas och innehålla förväntad titel
    assert_that(response.status_code, is_(equal_to(200)))
    assert_that(response.headers["content-type"], contains_string("text/html"))
    assert_that(response.text.lower(), contains_string(page_title.lower()))


def test_api_posts_endpoint(app_url: str):
    """Testa att posts API-endpointen fungerar."""
    # GIVEN en driftsatt applikation med ett posts-API
    posts_url = f"{app_url}/api/v1/posts"

    # WHEN vi begär listan med inlägg
    response = requests.get(posts_url)

    # THEN ska vi få ett giltigt svar
    assert_that(response.status_code, is_(equal_to(200)))

    data = response.json()
    assert_that(data, is_(instance_of(list)))
    # Ska returnera tom lista eller inlägg, båda är giltiga
