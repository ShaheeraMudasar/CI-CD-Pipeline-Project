from hamcrest import assert_that, not_none, equal_to

from app.models import PostIn, PostOut
from app.storage.ddb import DynamoClient

def test_create_post():
    # GIVEN that we have a client

    client = DynamoClient()

    # WHEN we create a new post
    
    post = PostIn(
        title="This is a test post", 
        image_url="thisisthetesturl.com", 
        image_text="This is the image text"
    )

    post_id = client.create_post(post)

    # THEN we should get an post_id back

    assert_that(post_id, not_none())
