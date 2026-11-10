from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.auth import router as auth_router
from app.api.users import router as users_router
from app.core.database import Base, engine
from app.core.exceptions import AuthError, handle_exceptions


@asynccontextmanager  # because FastAPI's lifespan function is an async context manager, we can use the @asynccontextmanager decorator to define a function that will be called when the application starts and stops.
async def lifespan(app: FastAPI):
    # Create the database tables
    Base.metadata.create_all(engine)
    yield


app = FastAPI(lifespan=lifespan)


app.include_router(auth_router)
app.include_router(users_router)
app.add_exception_handler(AuthError, handle_exceptions)
