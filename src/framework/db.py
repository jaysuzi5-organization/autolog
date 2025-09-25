"""
Database Initialization and Session Management

This module provides:
- A global SQLAlchemy `Base` class for ORM models.
- Database initialization logic that supports both production and testing environments.
- A dependency function for FastAPI routes to get a database session.

Environment Variables for Production:
    POSTGRES_USER     - PostgreSQL username
    POSTGRES_PASSWORD - PostgreSQL password
    POSTGRES_HOST     - Hostname or IP address of the database server
    POSTGRES_PORT     - Database port (default: 5432)
    POSTGRES_DB       - Database name
    DB_POOL_SIZE      - SQLAlchemy pool size (default: 10)
    DB_MAX_OVERFLOW   - Max overflow connections beyond pool_size (default: 20)
    DB_POOL_RECYCLE   - Connection lifetime in seconds before recycling (default: 3600)

Environment Variables for Testing:
    DATABASE_URL - Full SQLAlchemy database URL (e.g., sqlite:///./test.db)

"""

import os
import importlib.util
from sqlalchemy.orm import  sessionmaker
from sqlalchemy import create_engine
import logging

logger = logging.getLogger(__name__)

class Database:
    # Accept Base as an argument during initialization
    def __init__(self, base, model_paths: str = None, database_url: str = None):
        self._base = base
        self._engine = None
        self._set_engine(database_url)
        self._session = sessionmaker(bind=self._engine)
        self.model_paths = model_paths if model_paths is not None else []

        # If models dynamically
        self._import_models()
        self._base.metadata.create_all(self._engine)

    def get_session(self):
        return self._session()

    def _set_engine(self, database_url: str):
        if not database_url:
            required_keys = {
                "POSTGRES_USER": None,
                "POSTGRES_PASSWORD": None,
                "POSTGRES_HOST": None,
                "POSTGRES_PORT": None,
                "POSTGRES_DB": None
            }

            missing_vars = []
            for key in required_keys:
                value = os.getenv(key)
                if not value:
                    missing_vars.append(key)
                required_keys[key] = value

            if missing_vars:
                raise EnvironmentError(
                    f"Missing required environment variables: {', '.join(missing_vars)}"
                )

            database_url = (
                f"postgresql+psycopg2://{required_keys['POSTGRES_USER']}:"
                f"{required_keys['POSTGRES_PASSWORD']}@"
                f"{required_keys['POSTGRES_HOST']}:"
                f"{required_keys['POSTGRES_PORT']}/"
                f"{required_keys['POSTGRES_DB']}"
            )
        self.engine = create_engine(database_url)


    def _import_models(self):
        """
        Dynamically imports all Python files from the specified model paths
        to ensure all Base-derived models are registered.
        This method uses the Base instance provided during Database initialization.
        """
        if not self.model_paths:
            return
        for model_dir_path in self.model_paths:
            # For simplicity, we assume model_dir_path is directly importable or an absolute path
            if not os.path.isdir(model_dir_path):
                print(f"Warning: Model path '{model_dir_path}' not found. Skipping dynamic load.")
                continue
            for filename in os.listdir(model_dir_path):
                if filename.endswith(".py") and filename != "__init__.py":
                    module_name = filename[:-3] # Remove .py extension
                    module_full_path = os.path.join(model_dir_path, filename)
                    try:
                        # Construct a unique module name to avoid conflicts if same filename exists elsewhere
                        spec = importlib.util.spec_from_file_location(f"dynamic_model_{module_name}", module_full_path)
                        if spec is not None:
                            module = importlib.util.module_from_spec(spec)
                            spec.loader.exec_module(module)
                    except Exception as e:
                        print(f"Error importing model module {filename} from {model_dir_path}: {e}")
