from flask import url_for


def test_non_admin_cannot_access_admin(authenticated_client):
    response = authenticated_client.get("/admin/", follow_redirects=False)

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/auth/login")


def test_admin_can_access_admin(admin_client):
    response = admin_client.get("/admin/")

    assert response.status_code == 200
    assert b"NumberGuesser Admin" in response.data
    assert b"Dashboard" in response.data
    assert b"User" in response.data
    assert b"Game" in response.data
    assert b"Guess" in response.data
    assert b"Feedback" in response.data
    assert b"adminuser" in response.data
    assert b"admin-sidebar__link is-active" in response.data


def test_admin_sidebar_highlights_active_model_view(admin_client, app):
    with app.test_request_context():
        user_admin_url = url_for("admin_users.index_view")

    response = admin_client.get(user_admin_url)

    assert response.status_code == 200
    assert b'admin-sidebar__link is-active"' in response.data
    assert b"Manage user records" in response.data
