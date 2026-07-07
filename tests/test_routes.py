from pathlib import Path


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


def _read_css() -> str:
    """读取主题 CSS 文件全文。"""
    css_path = Path(__file__).resolve().parent.parent / "blog" / "static" / "light.css"
    return css_path.read_text(encoding="utf-8")


def test_base_template_exposes_mobile_responsive_contract(client):
    response = client.get("/")

    assert response.status_code == 200
    html = response.get_data(as_text=True)
    # 确认 CSS 以外部文件方式引入
    assert 'href="/static/light.css"' in html
    css = _read_css()
    assert "Mobile readable responsive overrides" in css
    assert "@media (max-width:768px)" in css
    assert "overflow-wrap: anywhere" in css
    assert "min(86vw, 320px)" in css
    assert "touch-action: manipulation" in css


def test_mobile_responsive_contract_prevents_right_overflow(client):
    response = client.get("/posts/hello.html")

    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert 'href="/static/light.css"' in html
    css = _read_css()
    assert ".site-header .container {" in css and "min-width: 0" in css
    assert ".site-nav {" in css and "min-width: 0" in css and "flex: 1" in css
    assert ".post-card {" in css and "max-width: 100%" in css and "min-width: 0" in css
    assert (
        "article," in css and ".article-header," in css and ".article-body {" in css
        and "width: 100%" in css and "max-width: 100%" in css and "min-width: 0" in css
    )


def test_mobile_code_blocks_do_not_expand_page_width(client):
    response = client.get("/posts/hello.html")

    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert 'href="/static/light.css"' in html
    css = _read_css()
    assert "margin-left: 0" in css or "margin-left:0" in css
    assert "margin-right: 0" in css or "margin-right:0" in css


def test_mobile_article_and_code_blocks_have_explicit_width_constraints(client):
    response = client.get("/posts/hello.html")

    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert 'href="/static/light.css"' in html
    css = _read_css()
    assert (
        "article," in css and ".article-header," in css and ".article-body {" in css
        and "width: 100%" in css and "max-width: 100%" in css and "min-width: 0" in css
    )
    assert "width: 100%;" in css and "max-width: 100%;" in css and "overflow-x: auto" in css


def test_mobile_responsive_contract_is_shared_by_content_pages(client):
    for path in ("/posts/hello.html", "/archives.html", "/topic/about.html"):
        response = client.get(path)

        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert 'href="/static/light.css"' in html
    css = _read_css()
    assert "Mobile readable responsive overrides" in css


def test_public_theme_exposes_professional_editorial_contract(client):
    response = client.get("/")

    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert 'href="/static/light.css"' in html
    css = _read_css()
    assert "Professional editorial polish" in css
    assert "--surface-paper" in css
    assert "--shadow-card-hover" in css
    assert ".article-summary" in css
    assert "text-wrap: balance" in css


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
    assert 'href="/static/light.css"' in html
    css = _read_css()
    assert ".site-header .container {" in css and "min-width: 0" in css
    assert ".site-nav {" in css and "min-width: 0" in css and "flex: 1" in css
    assert "overflow-x: auto" in css
    assert "scrollbar-width: none" in css
