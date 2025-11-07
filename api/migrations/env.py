from __future__ import annotations
import sys
from pathlib import Path
from logging.config import fileConfig
from alembic import context
from sqlalchemy import engine_from_config, pool
from dotenv import load_dotenv

# ✅ Ensure app/ is importable
BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(BASE_DIR / "app"))

# ✅ Load environment variables
load_dotenv(BASE_DIR / ".env")

# ✅ Import DB and models
from app.db import Base, DATABASE_URL
from app.models import Paper  # <-- ensure model is imported here

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata
config.set_main_option("sqlalchemy.url", DATABASE_URL)


def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
