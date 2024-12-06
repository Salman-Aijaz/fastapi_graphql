import os
import ssl
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Configure SSL context
ssl_context = ssl.create_default_context(cafile=None)  # Add a CA file if needed

# Create async engine with SSL options
engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    connect_args={"ssl": ssl_context},  # Add SSL context here
    pool_size=10,  # Size of the connection pool
    max_overflow=20,  # Number of connections beyond pool_size
    pool_timeout=30,  # Timeout for pool
    pool_recycle=3600  # Recycle connections every hour
)

async def init_db():
    try:
        async with engine.begin() as conn:
            # Create tables
            await conn.run_sync(SQLModel.metadata.create_all)
            logger.info("Tables created successfully")
    except Exception as e:
        logger.error(f"Error in initializing the database: {e}")
        raise

async def get_db():
    try:
        async with AsyncSession(engine) as session:
            yield session
    except Exception as e:
        logger.error(f"Error during database session: {e}")
        raise
