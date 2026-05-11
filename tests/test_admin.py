def test_non_admin_cannot_access_admin(authenticated_client):
    response = authenticated_client.get("/admin/", follow_redirects=False)

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/auth/login")


def test_admin_can_access_admin(admin_client):
    response = admin_client.get("/admin/")

    assert response.status_code == 200
    assert b"NumberGuesser Admin" in response.data
