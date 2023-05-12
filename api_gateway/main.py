from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from app.api.v1 import router

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

# Add the router responsible for all /api/ endpoint requests
app.include_router(router)
# Include redirection router in the main app
