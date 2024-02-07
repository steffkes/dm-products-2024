import pytest
import product


@pytest.mark.parametrize(
    "test_input,expected",
    [
        (
            "https://www.dm.de/dr-bronners-lippenpflege-balsam-baby-mild-p1018787830245.html",
            ("DE", 1018787830245),
        ),
        (
            "https://www.dm.de/essie-nagellack-go-ginza-249-p30104983.html",
            ("DE", 30104983),
        ),
        (
            "https://www.dm.de/maybelline-new-york-nagellack-super-stay-7-days-931-brownstore-p3600531640279.html",
            ("DE", 3600531640279),
        ),
        (
            "https://www.dm.de/nivea-antitranspirant-deospray-black-und-white-invisible-p4005900843760.html",
            ("DE", 4005900843760),
        ),
    ],
)
def test_match_store(test_input, expected):
    assert product.match_from_url(test_input) == expected
