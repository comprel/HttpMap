
from core.route import url
from controller.example.example import Example

add_route = [
    url("/api/v1/example", Example())
]

