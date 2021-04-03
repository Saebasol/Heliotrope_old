import os
from asyncio.events import AbstractEventLoop

import sentry_sdk
from aiohttp.client import ClientSession
from sanic import Sanic
from sanic_cors import CORS
from sentry_sdk.integrations.sanic import SanicIntegration
from tortoise.contrib.sanic import register_tortoise

import heliotrope
from heliotrope.routes import heliotrope_routes
from heliotrope.utils.requester import HitomiRequester
from heliotrope.mirroring import Mirroring
from heliotrope.utils.typed import Heliotrope

heliotrope_app = Sanic("heliotrope")
CORS(heliotrope_app, origins=["https://doujinshiman.ga"])
heliotrope_app.blueprint(heliotrope_routes)

if not os.environ.get("BYPASS"):
    heliotrope_app.config.DB_URL = os.environ["DB_URL"]
    heliotrope_app.config.HIYOBOT_SECRET = os.environ["HIYOBOT_SECRET"]
    if not os.environ.get("IS_TEST"):
        heliotrope_app.config.SENTRY_DSN = os.environ["SENTRY_DSN"]
        heliotrope_app.config.FORWARDED_SECRET = os.environ["FORWARDED_SECRET"]
        sentry_sdk.init(
            dsn=heliotrope_app.config.SENTRY_DSN,
            integrations=[SanicIntegration()],
            release=f"heliotrope@{heliotrope.__version__}",
        )

    register_tortoise(
        heliotrope_app,
        db_url=heliotrope_app.config.DB_URL,
        modules={
            "models": [
                "heliotrope.database.models.hitomi",
                "heliotrope.database.models.requestcount",
            ]
        },
        generate_schemas=True,
    )


@heliotrope_app.before_server_start
async def start(heliotrope: Heliotrope, loop: AbstractEventLoop):
    hitomi_session = ClientSession(loop=loop)
    mirroring_manager_session = ClientSession(loop=loop)
    heliotrope.ctx.hitomi_requester = HitomiRequester(hitomi_session)
    heliotrope.ctx.mirroring_manager = Mirroring(mirroring_manager_session)
    heliotrope.add_task(heliotrope.ctx.mirroring_manager.mirroring_task(3600))


@heliotrope_app.after_server_stop
async def stop(heliotrope: Heliotrope, loop: AbstractEventLoop):
    await heliotrope.ctx.hitomi_requester.session.close()
    await heliotrope.ctx.mirroring_manager.session.close()
