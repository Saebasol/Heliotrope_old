from sanic import Blueprint
from sanic.response import json
from Heliotrope.utils.hitomi import hitomi
from Heliotrope.utils.checker.check import authorized

integrated = Blueprint("hitomi_integrated", url_prefix="/integrated")


@integrated.route("/<index>")
@authorized()
async def hitomi_integrated(request, index: int):
    json_ = await hitomi.integrated_info(index)
    return json(json_)
