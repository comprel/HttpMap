from core.route import url
from controller.access.access import AccessHandler
from controller.access.access_history import AccessHistoryHandler


add_route = [
    url("/api/v1/access", AccessHandler()),
    url("/api/v1/accessHistory", AccessHistoryHandler()),
]
