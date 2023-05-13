from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from app.api import router
from fastapi.middleware.cors import CORSMiddleware

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
# Add the router responsible for all /api/ endpoint requests
app.include_router(router)
# Include redirection router in the main app
