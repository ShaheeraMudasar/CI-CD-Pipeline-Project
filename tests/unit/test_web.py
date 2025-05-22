import subprocess
from unittest.mock import AsyncMock, patch

# from app.routers.web import index, get_uptime
import pytest
from hamcrest import assert_that, contains_string, equal_to, instance_of, is_
from starlette.datastructures import FormData
from starlette.requests import Request
from starlette.responses import RedirectResponse

from app.routers import web


# This unit test checks if index function returns valid html response for all posts
@pytest.mark.asyncio
async def test_index_returns_template_response():
    mock_request = Request(scope={"type": "http"})
    mock_posts = [{"id": "1", "title": "Test"}]

    with patch("app.routers.web.get_dynamo_client") as mock_client:
        mock_client.return_value.list_posts = AsyncMock(return_value=mock_posts)

        response = await web.index(mock_request)

        assert_that(response.template.name, contains_string("index.html"))
        assert_that(response.context["posts"], mock_posts)


# This unit test checks if get git commit hash function successfully returns the latest commit hash
def test_get_git_commit_hash_success():
    # GIVEN
    latest_hash = b"abc123"
    with patch("subprocess.check_output", return_value=latest_hash):
        # WHEN
        result = web.get_git_commit_hash()
        # THEN
        assert_that(result, equal_to("abc123"))


# This unit test checks output if get git commit hash function fails to return latest commit hash
def test_get_git_commit_hash_fail():
    # GIVEN
    with patch("subprocess.check_output", side_effect=subprocess.CalledProcessError(1, "git")):
        # WHEN
        result = web.get_git_commit_hash()
        # THEN
        assert_that(result, equal_to("Unknown git command"))


# This unit test checks if get_uptime function returns valid uptime
def test_get_uptime():
    # GIVEN
    with (
        patch.object(web, "start_time", 1000),
        patch("app.routers.web.time.time", return_value=4661),
    ):
        # WHEN
        result = web.get_uptime()
        # THEN
        assert_that(result, equal_to("1h 1m 1s"))


# This unit test checks if post view post function returns post when post is available
@pytest.mark.asyncio
async def test_view_post_returns_template_for_valid_post():
    # GIVEN
    mock_request = Request(scope={"type": "http"})
    fake_post = {"id": "1", "title": "Test Post"}
    with patch("app.routers.web.get_dynamo_client") as mock_client:
        mock_client.return_value.get_post = AsyncMock(return_value=fake_post)

        # WHEN
        response = await web.view_post(mock_request, "1")

        # THEN
        assert_that(response.template.name, equal_to("post.html"))
        assert_that(response.context["post"], is_(fake_post))


# This unit test checks if post view post function returns the error when post is not available
@pytest.mark.asyncio
async def test_view_post_returns_404_for_missing_post():
    # GIVEN
    mock_request = Request(scope={"type": "http"})
    with patch("app.routers.web.get_dynamo_client") as mock_client:
        mock_client.return_value.get_post = AsyncMock(return_value=None)

        # WHEN
        response = await web.view_post(mock_request, "nonexistent")

        # THEN
        assert_that(response.status_code, equal_to(404))
        assert_that(response.body.decode(), equal_to("Post not found"))


# This unit test checks if admin_panel function displays the admin panel
#@pytest.mark.asyncio
#async def test_admin_panel_shows_admin_web_page():
    # GIVEN
  #  fake_post = [{"test_request": "1", "title": "Test Post"}]
   # mock_request = Request(scope={"type": "http"})
   # with patch("app.routers.web.get_dynamo_client") as mock_client:
    #    mock_client.return_value.list_posts = AsyncMock(return_value=fake_post)
        # WHEN
     #   response = await web.admin_panel(mock_request)
        # THEN
      #  assert_that(response.template.name, equal_to("admin.html"))
       # assert_that(response.context["posts"], is_(fake_post))
       # assert_that(response.context["error"], is_(None))

@pytest.mark.asyncio
async def test_admin_panel_shows_admin_web_page():
    # GIVEN
    fake_post = [{"test_request": "1", "title": "Test Post"}]
    mock_request = Request(scope={"type": "http"})
    with (
        patch ("app.routers.web.feature_admin_enabled", return_value = True),
        patch("app.routers.web.get_dynamo_client") as mock_client
        ):
        mock_client.return_value.list_posts = AsyncMock(return_value=fake_post) 
        # WHEN
        response = await web.admin_panel(mock_request)
        # THEN
        assert_that(response.template.name, equal_to("admin.html"))
        assert_that(response.context["posts"], is_(fake_post))
        assert_that(response.context["error"], is_(None))


# This unit test verifies that a post is successfully created and the user is redirected to the homepage when the admin feature is enabled and the correct password is provided.


@pytest.mark.asyncio
async def test_create_post_from_form_redirects_on_success():
    # GIVEN
    form_data = FormData(
        {
            "password": "admin123",
            "title": "New Post",
            "image_url": "http://image.com/img.jpg",
            "image_text": "Nice pic",
        }
    )
    scope = {"type": "http", "method": "POST"}
    request = Request(scope, receive=lambda: {"type": "http.request", "body": b""})
    request._form = form_data  # simulated filled form for fast api

    with (
        patch("app.routers.web.feature_admin_enabled", return_value=True),
        patch("app.routers.web.get_admin_password", return_value="admin123"),
        patch("app.routers.web.get_dynamo_client") as mock_client,
    ):
        mock_client.return_value.create_post = AsyncMock()

        # WHEN
        response = await web.create_post_from_form(
            request,
            password="admin123",
            title="New Post",
            image_url="http://image.com/img.jpg",
            image_text="Nice pic",
        )

        # THEN
        assert_that(response, instance_of(RedirectResponse))
        assert_that(response.status_code, equal_to(302))
        assert_that(str(response.headers["location"]), equal_to("/"))


# This unit test checks if the post is deleted and is redirected to home page


@pytest.mark.asyncio
async def test_delete_post_from_form_redirects_on_success():
    # GIVEN
    form_data = FormData({"password": "admin123", "post_id": "1"})
    scope = {"type": "http", "method": "POST"}

    async def receive():
        return {"type": "http.request", "body": b""}

    request = Request(scope, receive=receive)
    request._form = form_data

    with (
        patch("app.routers.web.feature_admin_enabled", return_value=True),
        patch("app.routers.web.get_admin_password", return_value="admin123"),
        patch("app.routers.web.get_dynamo_client") as mock_client,
    ):
        mock_client.return_value.delete_post = AsyncMock(return_value=True)

        # WHEN
        response = await web.delete_post_from_form(request, password="admin123", post_id="1")

        # THEN
        assert_that(response, instance_of(RedirectResponse))
        assert_that(response.status_code, equal_to(302))
        assert_that(str(response.headers["location"]), equal_to("/"))


# This unit test checks if the status route shows the right output


@pytest.mark.asyncio
async def test_status_returns_status_template_with_health_data():
    # GIVEN
    mock_request = Request(scope={"type": "http"})
    with (
        patch("app.routers.web.get_git_commit_hash", return_value="abc123"),
        patch("app.routers.web.get_uptime", return_value="1h 2m 3s"),
    ):
        # WHEN
        response = await web.status(mock_request)

        # THEN
        assert_that(response.template.name, equal_to("status.html"))
        assert_that(response.context["status"], equal_to("Healthy"))
        assert_that(response.context["commit_hash"], equal_to("abc123"))
        assert_that(response.context["uptime"], equal_to("1h 2m 3s"))
