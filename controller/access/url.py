from core.route import url
from controller.access.access import AccessHandler


add_route = [
    url("/api/v1/access", AccessHandler()),
]
