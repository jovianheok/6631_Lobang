from ..image_utils import extract_background_image_url


def test_extract_background_image_url_standard_style():
    style = "background-image:url('https://cdn.example.com/photo.jpg')"
    assert extract_background_image_url(style) == "https://cdn.example.com/photo.jpg"


def test_extract_background_image_url_with_quotes_and_spaces():
    style = 'background-image: url("https://cdn.example.com/photo 2.jpg");'
    assert extract_background_image_url(style) == "https://cdn.example.com/photo 2.jpg"


def test_extract_background_image_url_returns_none_for_missing_style():
    assert extract_background_image_url(None) is None


def test_extract_background_image_url_returns_none_for_no_match():
    assert extract_background_image_url("background-color:#fff") is None


def test_extract_background_image_url_returns_none_for_none_value():
    assert extract_background_image_url("background-image:none") is None
