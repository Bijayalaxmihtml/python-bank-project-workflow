import sys
import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool, create_engine
from alembic import context
from dotenv import load_dotenv

# Adjust sys.path to import your models module if it's outside this directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models import Base  # Import your SQLAlchemy models' Base here

# Load environment variables from .env file in project root
load_dotenv()

config = context.config

# Setup logging according to alembic.ini config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Target metadata for 'autogenerate' support in migrations
target_metadata = Base.metadata

def get_db_url() -> str:
    """
    Get the database URL from environment variable or alembic.ini config.
    """
    url = os.getenv("DATABASE_URL")
    if url is None:
        url = config.get_main_option("sqlalchemy.url")
    if not url:
        raise RuntimeError("Database URL not found. Set DATABASE_URL environment variable or sqlalchemy.url in alembic.ini.")
    return url

def run_migrations_offline() -> None:
    """
    Run migrations in 'offline' mode, using only the URL.
    """
    url = get_db_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """
    Run migrations in 'online' mode, creating an Engine and connection.
    """
    url = get_db_url()
    connectable = create_engine(url, poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
