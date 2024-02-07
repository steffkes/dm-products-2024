import pytest
import store


@pytest.mark.parametrize(
    "test_input,expected",
    [
        ("https://www.dm.de/store", None),
        ("https://www.dm.de/store/de-10/essen/ruettenscheider-strasse-104", ("DE", 10)),
        ("https://www.dm.de/store/de-100/haan/neuer-markt-40-42", ("DE", 100)),
        ("https://www.dm.de/store/de-1240/wuerzburg/erthalstrasse-32-b", ("DE", 1240)),
        ("https://www.dm.de/store/de-2834/hamburg/harkortstrasse-81e", ("DE", 2834)),
    ],
)
def test_match_store(test_input, expected):
    assert store.match_from_url(test_input) == expected
