import sys
import logging

from logging import handlers
from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from . import models
from app.endpoints import api
from .db.database import engine_uconnect

models.Base.metadata.create_all(bind=engine_uconnect)

app = FastAPI(
    title="uConnect Main",
    openapi_url=None
)

app_uconnect = FastAPI(
    title="uConnect",
    description="Proyecto de Tesis uConnect APP",
    version="0.1.0"
)

app.mount("/uconnect/api", app_uconnect)


log = logging.getLogger('')
log.setLevel(logging.DEBUG)
format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

ch = logging.StreamHandler(sys.stdout)
ch.setFormatter(format)
log.addHandler(ch)

# get root logger
logger = logging.getLogger(__name__)

async def log_requests(request: Request):

    body = None
    # try if body came in the body
    try:
        body = await request.json()
    except Exception:
        body = None
    # print(body)
    message = f"method={request.method};path={request.url}"
    if body is not None:
        message += f";body={body}"
    request_msg = f"Request:[{message}]"
    logger.info(request_msg)

origins = [
    "*",
]

# import endpoints
app_uconnect.include_router(api, dependencies=[Depends(log_requests)])

app_uconnect.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
