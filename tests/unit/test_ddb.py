from unittest.mock import MagicMock
from hamcrest import assert_that, equal_to
from app.models import PostListItem
from app.storage.ddb import DynamoClient

def test_list_posts_returns_sorted():
    # Create instance of the class
    client = DynamoClient()

    # Replace the internal _table with a MagicMock
    client._table = MagicMock()
    client._table.scan.return_value = {
        "Items": [
            {"id": "2", "title": "Second", "created_at": "2024-05-02"},
            {"id": "1", "title": "First", "created_at": "2024-05-01"},
        ]
    }

    # Call the method
    result = client.list_posts()

    # Check the result
    expected = [
        PostListItem(id="1", title="First"),
        PostListItem(id="2", title="Second")
    ]
    assert_that(result, equal_to(expected))
