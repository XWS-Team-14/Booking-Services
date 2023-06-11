from fastapi import FastAPI, Request, Header
from fastapi.responses import ORJSONResponse
from app.api import router
import http.client
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from app.config import get_yaml_config
import logging_loki

config = get_yaml_config().get("loki")
url = config.get("url")
service = config.get("service")

try:
    conn = http.client.HTTPConnection(url)
    conn.request("GET", "/ready")
    r2 = conn.getresponse()
except Exception as e:
    logger.info(f"{e}")
else:
    handler = logging_loki.LokiHandler(
        url="http://" + url + "/loki/api/v1/push",
        tags={"service": service},
        version="1",
    )
    logger.add(
        handler,
        format="{time} | {level} | {message}",
    )


app = FastAPI(
    debug=True,
    title="Booking Server",
    version="1.00",
    description="Fastapi tester",
    # Set current documentation specs to v1
    default_response_class=ORJSONResponse,
    license_info={
        "name": "GNU General Public License v3.0",
        "url": "https://www.gnu.org/licenses/gpl-3.0.en.html",
    },
)
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_clients_and_requests(request: Request, call_next):
    response = await call_next(request)

    logger.remove()
    handler_middlewere = logging_loki.LokiHandler(
        url="http://" + url + "/loki/api/v1/push",
        tags={
            "service" : service,
            "status_code": response.status_code,
            "client_address": request.client.host,
            "user_agent": request.headers["user-agent"],
            "endpoint": request.url.path,
        },
        version="1",
    )
    middlewere = logger.add(
        handler_middlewere,
        format="{time} | {level} | {message}",
    )
    logger.info(
        str(response.status_code)
        + " | "
        + request.client.host
        + " | "
        + request.headers["user-agent"],
        
    )
    logger.remove(middlewere)
    return response


# Add the router responsible for all /api/ endpoint requests
app.include_router(router)
# Include redirection router in the main app
