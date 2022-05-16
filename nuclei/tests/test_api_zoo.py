import pytest
from nuclei.api_zoo import ROUTING, validate_or_refresh_token


@pytest.fixture()
def mock_authenticate(monkeypatch):
    # mock the authenticate call
    def mock_call(*args, **kwargs) -> None:
        return None
    monkeypatch.setattr("nuclei.api_zoo.authenticate", mock_call)


def test_routing_table():
    # integration test. Get routes from internet services.
    assert "gef-map" in ROUTING


@pytest.mark.parametrize(
    "token",
    [
        None,
        "Debug",
        (
            "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9."
            "eyJpYXQiOjE2MTU4OTcxNjgsIm5iZiI6MTYxNTg5NzE2OCwianRpIjoiNmFjNWYzMWUtOTIwNS"
            "00NjJiLTliNzgtMjY4NjIyM2UwOGMyIiwiZXhwIjoxNjE1OTQwMzY4LCJpZGVudGl0eSI6InJp"
            "dGNoaWU0NkBnbWFpbC5jb20iLCJmcmVzaCI6ZmFsc2UsInR5cGUiOiJhY2Nlc3MiLCJ1c2VyX2"
            "NsYWltcyI6eyJhbGxvd2VkX2FjY2VzcyI6ImFkbWluIiwibGltaXQiOnsibnVsbCI6bnVsbH19"
            "fQ."
            "M_Hyozg8KkWLz-mUpvpktbWCKwONp1pLwn9aufy3cPY"
        ),
        (
            "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9."
            "eyJpYXQiOjE2MTU4OTcxNjgsIm5iZiI6MTYxNTg5NzE2OCwianRpIjoiNmFjNWYzMWUtOTIwNS"
            "00NjJiLTliNzgtMjY4NjIyM2UwOGMyIiwiZXhwIjoxNjE1OTQwMzY4LCJpZGVudGl0eSI6InJp"
            "dGNoaWU0NkBnbWFpbC5jb20iLCJmcmVzaCI6ZmFsc2UsInR5cGUiOiJhY2Nlc3MiLCJ1c2VyX2"
            "NsYWltcyI6eyJhbGxvd2VkX2FjY2VzcyI6ImFkbWluIiwibGltaXQiOnsibnVsbCI6bnVsbH19"
            "fQ."
            "this-is-not-a-real-JWT"
        ),
        (
            "eyJ0eX-this-is-not-a-real-JWT."
            "eyJpYXQiOjE2MTU4OTcxNjgsIm5iZiI6MTYxNTg5NzE2OCwianRpIjoiNmFjNWYzMWUtOTIwNS"
            "00NjJiLTliNzgtMjY4NjIyM2UwOGMyIiwiZXhwIjoxNjE1OTQwMzY4LCJpZGVudGl0eSI6InJp"
            "dGNoaWU0NkBnbWFpbC5jb20iLCJmcmVzaCI6ZmFsc2UsInR5cGUiOiJhY2Nlc3MiLCJ1c2VyX2"
            "NsYWltcyI6eyJhbGxvd2VkX2FjY2VzcyI6ImFkbWluIiwibGltaXQiOnsibnVsbCI6bnVsbH19"
            "fQ."
            "M_Hyozg8KkWLz-mUpvpktbWCKwLwn9aufy3cPY"
        ),
        (
            "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9."
            "eyJpYXQ-this-is-not-a-real-JWT."
            "M_Hyozg8KkWLz-mUpvpktbWCKwLwn9aufy3cPY"
        ),
        (
            "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9."
            "eyJpYXQiOjE2MTU4OTcxNjgsIm5iZiI6MTYxNTg5NzE2OCwianRpIjoiNmFjNWYzMWUtOTIwN."
            "M_Hyozg8KkWLz-mUpvpktbWCKwLwn9aufy3cPY"
        ),
    ],
)
def test_validate_or_refresh_token(token, mock_authenticate):
    """
    Tests the multiple invalid JWT tokens, which should lead to a refresh of the token (returns 1)
    """
    assert validate_or_refresh_token(token) == 1
