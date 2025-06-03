import boto3
from hamcrest import assert_that, contains_string, equal_to, is_

from app.storage.ddb import DynamoClient
from app.models import PostIn

def test_create_post_adds_post_in_db():
    # GIVEN post details are given
    post = PostIn(
            id = "test_post_id",
            title = "test_post_title",
            image_url = "https://hereismyimage.com",
            image_text = "test_image",
        )

    client = DynamoClient()
    posts = client.list_posts()
    size_before = len(posts)

    # WHEN attempted to create a new post

    client.create_post(post)

    size_after = len(client.list_posts())

    # THEN it returns the list's size is increased by one

    assert_that (size_after, equal_to(size_before+1))
