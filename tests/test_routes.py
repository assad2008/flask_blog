def test_homepage_returns_post_list(client):
    response = client.get("/")

    assert response.status_code == 200
    assert b"Hello" in response.data
    assert b"Hello summary" in response.data


def test_archives_returns_post_list(client):
    response = client.get("/archives.html")

    assert response.status_code == 200
    assert b"Hello" in response.data


def test_post_detail_returns_existing_post(client):
    response = client.get("/posts/hello.html")

    assert response.status_code == 200
    assert b"Hello" in response.data
    assert b"<strong>world</strong>" in response.data


def test_post_detail_returns_404_for_missing_post(client):
    response = client.get("/posts/missing.html")

    assert response.status_code == 404


def test_topic_detail_returns_existing_topic(client):
    response = client.get("/topic/about.html")

    assert response.status_code == 200
    assert b"About" in response.data
    assert b"About page" in response.data


def test_topic_detail_returns_404_for_missing_topic(client):
    response = client.get("/topic/missing.html")

    assert response.status_code == 404


def test_page_route_returns_200(client):
    response = client.get("/page/1.html")

    assert response.status_code == 200
    assert b"Hello" in response.data
