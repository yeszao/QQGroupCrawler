from main import get_qq_members, get_groups


def test_get_data():
    with open("members1.html", "r") as f:
        content = f.read()
    members = get_qq_members(content)
    assert len(members) == 7

    with open("members2.html", "r") as f:
        content = f.read()
    members = get_qq_members(content)
    assert len(members) == 8


def test_get_groups():
    with open("example-group-list.html", "r") as f:
        content = f.read()
    groups = get_groups(content)
    assert len(groups) == 32
