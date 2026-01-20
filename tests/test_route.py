from acbrightspace.route import Route


def test_route_init_without_parameters():
    route = Route("GET", "/api/users")
    assert route.method == "GET"
    assert route.path == "/api/users"
    assert route.url == "https://brightspace.algonquincollege.com/api/users"


def test_route_init_with_parameters():
    route = Route("POST", "/api/users/{user_id}", user_id=123)
    assert route.method == "POST"
    assert route.path == "/api/users/{user_id}"
    assert route.url == "https://brightspace.algonquincollege.com/api/users/123"


def test_route_init_with_multiple_parameters():
    route = Route(
        "PUT",
        "/api/users/{user_id}/courses/{course_id}",
        user_id=123,
        course_id=456,
    )
    assert route.method == "PUT"
    assert (
        route.url
        == "https://brightspace.algonquincollege.com/api/users/123/courses/456"
    )


def test_route_with_different_http_methods():
    methods = ["GET", "POST", "PUT", "DELETE", "PATCH"]
    for method in methods:
        route = Route(method, "/api/test")
        assert route.method == method
