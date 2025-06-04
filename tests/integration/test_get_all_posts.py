from hamcrest import assert_that, equal_to, contains_inanyorder

from app.models import PostIn
from app.storage.ddb import DynamoClient


def test_get_all_posts():
    # GIVEN a client
    client = DynamoClient()

    # two new posts are created
    post_1 = PostIn(
        title="This #1 post",
        image_url="number1.com",
        image_text="This is the #1",
    )

    post_2 = PostIn(
        title="This #2 post",
        image_url="number2.com",
        image_text="This is the #2",
    )

    id_1 = client.create_post(post_1)
    id_2 = client.create_post(post_2)

    # WHEN listing all posts
    all_posts = client.list_posts()

    # THEN the created posts by id and title

    # Filtrera så att endast de två skapade inläggen är det som kontrolleras
    filtered = {(p.id, p.title) for p in all_posts if p.id in {id_1, id_2}}

    # Här förväntar vi oss att de två inläggen finns med i resultatet
    expected = {(id_1, post_1.title), (id_2, post_2.title)}
    assert_that(filtered, equal_to(expected))
