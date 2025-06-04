from uuid import uuid4

from hamcrest import assert_that, equal_to

from app.models import PostIn
from app.storage.ddb import DynamoClient


def test_get_post_by_id_returns_post():
    # GIVEN a post exists in database
    db = DynamoClient()

    unique_title = f"test-title-{uuid4()}"
    post = PostIn(title=unique_title, image_url="https://img", image_text="text")

    post_id = db.create_post(post)

    # WHEN searrching for it by its post_id

    matched_post = [p for p in db.list_posts() if p.id == post_id]

    # THEN it should be found with correct details
    assert_that(matched_post[0].title, equal_to(post.title))
