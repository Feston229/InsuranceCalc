import asyncio
import logging

import typer
import uvicorn

from insurance_calc.gunicorn_runner import GunicornApplication
from insurance_calc.log import configure_logging
from insurance_calc.pre_start import db_deploy
from insurance_calc.settings import settings

cli = typer.Typer()


@cli.command()
def deploy() -> None:
    """Create initial data for the application."""

    configure_logging()
    asyncio.run(db_deploy())
    logging.info("Initial data created")


@cli.command()
def run() -> None:
    """Entrypoint of the application."""

    if settings.environment == "kubernetes" or settings.reload:
        uvicorn.run(
            "insurance_calc.web.application:get_app",
            host=settings.host,
            port=settings.port,
            reload=settings.reload,
            log_level=settings.log_level.value.lower(),
            factory=True,
        )
    else:
        # We choose gunicorn only if reload
        # option is not used, because reload
        # feature doesn't work with gunicorn workers.
        GunicornApplication(
            "insurance_calc.web.application:get_app",
            host=settings.host,
            port=settings.port,
            workers=settings.workers_count,
            factory=True,
            accesslog="-",
            loglevel=settings.log_level.value.lower(),
            access_log_format='%r "-" %s "-" %Tf',  # noqa: WPS323
        ).run()


if __name__ == "__main__":
    cli()
