from hamcrest import assert_that, not_none, equal_to

from app.models import PostIn, PostOut
from app.storage.ddb import DynamoClient
