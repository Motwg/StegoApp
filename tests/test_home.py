def test_main_route_status_code(client):
    route = '/'
    rv = client.get(route)
    assert rv.status_code == 200
