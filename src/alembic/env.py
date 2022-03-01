import logging
import re
from logging.config import fileConfig
from typing import Any, Callable, Dict, Mapping

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

import authserver.db.models
import authserver.settings
import snacksbar.products.db.models
import snacksbar.settings
from alembic import context

USE_TWOPHASE = False

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

fileConfig(config.config_file_name)
logger = logging.getLogger("alembic.env")

DB_NAMES = re.split(r",\s*", config.get_main_option("databases"))
target_metadata = {
    "snacksbar": snacksbar.products.db.models.Base.metadata,
    "authserver": authserver.db.models.Base.metadata,
}
url_registry: Mapping[str, Callable[[], str]] = {
    "snacksbar": lambda: snacksbar.settings.APISettings.from_cache().SNACKSBAR_DB_URL,
    "authserver": lambda: authserver.settings.APISettings.from_cache().AUTHSERVER_DB_URL,
}


def url_factory(name) -> str:
    return url_registry[name]()


def engine_factory(name) -> Engine:
    return create_engine(url_factory(name))


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    # for the --sql use case, run migrations for each URL into
    # individual files.

    engines: Dict[str, Dict[str, Any]] = {}
    for name in DB_NAMES:
        rec = {"url": url_factory(name)}
        engines[name] = rec

    for name, rec in engines.items():
        logger.info("Migrating database %s" % name)
        file_ = "%s.sql" % name
        logger.info("Writing output to %s" % file_)
        with open(file_, "w") as buffer:
            context.configure(
                url=rec["url"],
                output_buffer=buffer,
                target_metadata=target_metadata[name],
                literal_binds=True,
                dialect_opts={"paramstyle": "named"},
            )
            with context.begin_transaction():
                context.run_migrations(engine_name=name)


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    # for the direct-to-DB use case, start a transaction on all
    # engines, then run all migrations, then commit all transactions.

    engines: Dict[str, Dict[str, Any]] = {}
    for name in DB_NAMES:
        rec = {"engine": engine_factory(name)}
        engines[name] = rec

    for name, rec in engines.items():
        engine = rec["engine"]
        rec["connection"] = conn = engine.connect()

        if USE_TWOPHASE:
            rec["transaction"] = conn.begin_twophase()
        else:
            rec["transaction"] = conn.begin()

    try:
        for name, rec in engines.items():
            logger.info("Migrating database %s" % name)
            context.configure(
                connection=rec["connection"],
                upgrade_token="%s_upgrades" % name,
                downgrade_token="%s_downgrades" % name,
                target_metadata=target_metadata[name],
            )
            context.run_migrations(engine_name=name)

        if USE_TWOPHASE:
            for rec in engines.values():
                rec["transaction"].prepare()

        for rec in engines.values():
            rec["transaction"].commit()
    except Exception as err:
        for rec in engines.values():
            rec["transaction"].rollback()
        raise err
    finally:
        for rec in engines.values():
            rec["connection"].close()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
