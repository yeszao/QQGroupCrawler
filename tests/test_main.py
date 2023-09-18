from main import get_data


def test_get_data():
    with open("example.html", "r") as f:
        content = f.read()

    members = get_data(content, 123456)
    assert len(members) == 7

