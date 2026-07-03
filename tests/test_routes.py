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


def test_base_template_exposes_mobile_responsive_contract(client):
    response = client.get("/")

    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "Mobile readable responsive overrides" in html
    assert "@media (max-width:640px)" in html
    assert "overflow-wrap:anywhere" in html
    assert "min(86vw, 320px)" in html
    assert "touch-action:manipulation" in html


def test_mobile_responsive_contract_prevents_right_overflow(client):
    response = client.get("/posts/hello.html")

    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert ".site-header .container{min-width:0" in html
    assert ".site-nav{min-width:0;flex:1" in html
    assert ".post-card{max-width:100%;min-width:0" in html
    assert "article,.article-header,.article-body{max-width:100%;min-width:0" in html


def test_mobile_responsive_contract_is_shared_by_content_pages(client):
    for path in ("/posts/hello.html", "/archives.html", "/topic/about.html"):
        response = client.get(path)

        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "Mobile readable responsive overrides" in html
