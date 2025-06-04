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

def test_create_post_and_get_post_with_id():
    # GIVEN that we have a client and a post

    client = DynamoClient()

    new_post = PostIn(
        title="This is a test post", 
        image_url="thisisthetesturl.com", 
        image_text="This is the image text"
    )

    post_id = client.create_post(new_post)

    # WHEN we use that post_id to get a specific post

    post = client.get_post(post_id)
    print(post)

    # THEN we should get the post in return

    assert_that(post, not_none())
