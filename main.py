from fastapi import FastAPI
import logging
from database import init_db
from strawberry.fastapi import GraphQLRouter
from graphql_schema import schema

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def lifespan(app: FastAPI):
    try:
        await init_db()
        logger.info("Database Initialized Successfully")
    except Exception as e:
        logger.error(f"Failed to initialize the database: {e}")
        raise
    yield

app = FastAPI(lifespan=lifespan)
graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")
