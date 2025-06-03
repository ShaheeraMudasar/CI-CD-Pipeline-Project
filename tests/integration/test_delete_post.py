from hamcrest import assert_that, equal_to

from app.models import PostIn
from app.storage.ddb import DynamoClient


def test_delete_post_from_db():
    client = DynamoClient()
    posts = len(client.list_posts())

    post = PostIn(title="title_test_post", image_url="testurl.com", image_text="test_text")

    post_id = client.create_post(post)

    posts_after_create = len(client.list_posts())

    assert_that(posts_after_create, equal_to(posts + 1))

    client.delete_post(post_id)

    posts_after_delete = len(client.list_posts())

    assert_that(posts_after_delete, equal_to(posts_after_create - 1))
