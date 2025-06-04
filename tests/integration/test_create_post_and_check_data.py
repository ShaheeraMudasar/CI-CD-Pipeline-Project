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

def test_create_post_and_check_data_against_get_post_with_id():
    # GIVEN that we have a client, post and data from the post
    
    client = DynamoClient()

    # This is our data
    new_post = PostIn(
        title="This is a specific title",
        image_url="This is a specific url",
        image_text="This is a specific text"
    )

    # This is our specific id for the post.
    post_id = client.create_post(new_post)

    # WHEN we get a specific post using our id

    post = client.get_post(post_id)

    # THEN we compare the data to the data we sent in to see that it matches

    print("Checking post.id...")
    assert_that(post.id, equal_to(post_id))

    print("Checking post.title...")
    assert_that(post.title, equal_to(new_post.title))

    print("Checking post.image_url...")
    assert_that(post.image_url, equal_to(new_post.image_url))

    print("Checking post.image_text...")
    assert_that(post.image_text, equal_to(new_post.image_text))

    print("All checks passed.")