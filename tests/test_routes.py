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
    assert "@media (max-width:768px)" in html
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
    assert "article,.article-header,.article-body{width:100%;max-width:100%;min-width:0" in html


def test_mobile_code_blocks_do_not_expand_page_width(client):
    response = client.get("/posts/hello.html")

    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "margin-left:-.35rem;margin-right:-.35rem" not in html
    assert "margin-left:0;margin-right:0" in html


def test_mobile_article_and_code_blocks_have_explicit_width_constraints(client):
    response = client.get("/posts/hello.html")

    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "article,.article-header,.article-body{width:100%;max-width:100%;min-width:0" in html
    assert "width:100%;max-width:100%;min-width:0;overflow-x:auto" in html


def test_mobile_responsive_contract_is_shared_by_content_pages(client):
    for path in ("/posts/hello.html", "/archives.html", "/topic/about.html"):
        response = client.get(path)

        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "Mobile readable responsive overrides" in html


def test_public_theme_exposes_professional_editorial_contract(client):
    response = client.get("/")

    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "Professional editorial polish" in html
    assert "--surface-paper" in html
    assert "--shadow-card-hover" in html
    assert ".article-summary" in html
    assert "text-wrap:balance" in html


def test_topic_summary_uses_theme_class(client):
    response = client.get("/topic/about.html")

    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert 'class="article-summary"' in html
    assert 'style="color:var(--text-secondary);font-size:.95rem;margin-top:.25rem;"' not in html


def test_public_theme_keeps_mobile_navigation_single_row_contract(client):
    response = client.get("/")

    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert ".site-header .container{min-width:0" in html
    assert ".site-nav{min-width:0;flex:1" in html
    assert "overflow-x:auto" in html
    assert "scrollbar-width:none" in html
