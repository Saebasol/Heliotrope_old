from sanic import Blueprint
from sanic.response import json

from Heliotrope.utils.checker.check import authorized
from Heliotrope.utils.database import user_register

register = Blueprint("register", url_prefix="/register")


@register.route(
    "/",
    methods=["POST"],
)
@authorized()
async def api_register(request):
    user_id = request.json.get("user_id")
    check = request.json.get("check")
    if not user_id or check is None:
        return json({"status": 400, "message": "bad_request"}, 400)

    result = await user_register(user_id, check)

    return result
