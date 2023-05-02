def test_home_page(client):
    response = client.get("/")
    assert b"CyberTraining" in response.data
    assert b"Home" in response.data
    assert b"Log In" in response.data
    assert b"Register" in response.data
