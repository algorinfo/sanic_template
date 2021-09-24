import click
from changeme.conf import Config
from changeme.db.nosync import AsyncSQL
from changeme.blog.models import Article, Category
from changeme.utils.http import sync2async

cfg = Config()


@click.group()
def cli():
    """
    wrapper
    """
    pass

@click.command()
@click.option('--sql', "-s",
              default=cfg.ASQL,
              help="SQL Database")
@click.argument('action', type=click.Choice(['createall', 'dropall']))
@sync2async
async def db(sql, action):
    """ Create or Drop all the tables in database
    """
    sql = AsyncSQL(cfg.ASQL)
    await sql.init()
    if action == "createall":
        await sql.create_all()
    elif action == "dropall":
        await sql.drop_all()
        
cli.add_command(db)

if __name__ == "__main__":
    cli()
