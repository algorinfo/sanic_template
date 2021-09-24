from functools import wraps
import asyncio
from sanic import Request

def parse_page_limit(request: Request, def_pg="1", def_lt="100"):
    strpage = request.args.get("page", [def_pg])
    strlimit = request.args.get("limit", [def_lt])
    page = int(strpage[0])
    limit = int(strlimit[0])

    return page, limit


def sync2async(f):
    """
    Decorator for async cmds
    from: https://github.com/pallets/click/issues/85
    """

    @wraps(f)
    def wrapper(*args, **kwargs):
        """
        Check if loop is running first.
        Because is used as decoretor, maybe this function is executed
        inside an async context.
        """
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None
        if loop and loop.is_running:
            return asyncio.ensure_future(f(*args, **kwargs))

        return asyncio.run(f(*args, **kwargs))

    return wrapper

