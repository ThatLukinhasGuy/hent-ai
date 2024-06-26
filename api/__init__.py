from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import routers
from .utils import configure_error_handlers
from .responses import PrettyJSONResponse

app = FastAPI(default_response_class=PrettyJSONResponse, docs_url=None)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

for router in routers:
    app.include_router(router)

for exc, handler in configure_error_handlers().items():
    app.add_exception_handler(exc, handler)