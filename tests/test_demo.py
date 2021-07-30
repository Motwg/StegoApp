def test_get_demo(client):
    route = '/demo'
    rv = client.get(route)
    assert rv.status_code == 200
