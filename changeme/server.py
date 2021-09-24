from contextvars import ContextVar

from sanic import Sanic
from sanic_openapi import openapi2_blueprint

from changeme.conf import Config
from changeme.db.nosync import AsyncSQL
from changeme.home import views as home
from changeme.blog import views as blog
from changeme.blog import rest as blogapi
from changeme.utils import templates

cfg = Config()
render: templates.Render = templates.Render("changeme", "templates")
db = AsyncSQL(str(cfg.ASQL))

app = Sanic("changeme")
render.init_app(app)
app.ctx.db = db

_base_model_session_ctx = ContextVar("session")


@app.listener("before_server_start")
async def startserver(current_app, loop):
    await current_app.ctx.db.init()


@app.listener("after_server_stop")
async def shutdown(current_app, loop):
    await current_app.ctx.db.engine.dispose()


@app.middleware("request")
async def inject_session(request):
    request.ctx.session = app.ctx.db.sessionmaker()
    request.ctx.dbconn = db.engine
    request.ctx.session_ctx_token = _base_model_session_ctx.set(
        request.ctx.session)


app.blueprint(blogapi.bp)
app.blueprint(openapi2_blueprint)
app.blueprint(home.bp)
app.blueprint(blog.bp)
