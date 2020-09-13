from sanic.response import json
from Heliotrope.utils.database import User


async def user_register(user_id):
    user_data = await User.get_or_none(user_id=user_id)
    if user_data:
        return json({"status": "already_register"}, 200)
    else:
        await User.create(user_id=user_id)
        return json({"status": "successfully"}, 201)