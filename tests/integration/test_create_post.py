from hamcrest import assert_that, equal_to
from fastapi.testclient import TestClient

from app.models import PostIn
from app.storage.ddb import DynamoClient
from app.start import app


def test_create_post_adds_post_in_db():
    # GIVEN post details are given
    client = TestClient(app)
    db = DynamoClient()

    form_data = {
        "password": "admin123",
        "title" : "unique_test_post",
        "image_url": "https://test.com/image",
        "image_text": "test_image" 
     }
    
    response = client.post("admin/create", data=form_data, follow_redirects= False)

    assert_that (response.status_code, equal_to(302))

    posts = db.list_posts()
    matched_post = [p for p in posts if p.title == "unique_test_post"]
    assert_that(len(matched_post), equal_to(1))

    # client = DynamoClient()
    # posts = client.list_posts()
    # size_before = len(posts)

    # # WHEN attempted to create a new post

    # client.create_post(post)

    # size_after = len(client.list_posts())

    # # THEN it returns the list's size is increased by one

    # assert_that(size_after, equal_to(size_before + 1))
