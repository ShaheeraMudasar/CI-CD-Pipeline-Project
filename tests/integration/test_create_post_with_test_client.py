from uuid import uuid4  # for unique post title

from fastapi.testclient import TestClient
from hamcrest import assert_that, equal_to

from app.start import app
from app.storage.ddb import DynamoClient


def test_create_post_adds_post_in_db():
    
    # GIVEN post details are given 
    
    client = TestClient(app)
    db = DynamoClient()

    unique_title = f"test-title-{uuid4()}"

    form_data = {
        "password": "admin123",
        "title": unique_title,
        "image_url": "https://test.com/image",
        "image_text": "test_image",
    }

    # WHEN try to create new post through route admin/create

    response = client.post("admin/create", data=form_data, follow_redirects=False)

    # THEN it returns redirecting status code 302 and checks if the new post exists in db
    assert_that(response.status_code, equal_to(302))

    posts = db.list_posts()
    matched_post = [p for p in posts if p.title == unique_title]
    assert_that(len(matched_post), equal_to(1))
