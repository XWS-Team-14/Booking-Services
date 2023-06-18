from fastapi import APIRouter

from .auth import router as auth_router
from .accommodation import router as accommodation_router
from .user import router as user_router
from .availability import router as availability_router
from .reservation import router as reservation_router
from .search import router as search_router
from .notification import router as notification_router
from .orchestartor import router as orchestrator_router
from .accommodation_recomendator import router as accommodation_recomender_router
from .orchestrator import router as orchestrator_router
from .flights import router as flights_router
from ...config import get_yaml_config
from .review import  router as review_router

config = get_yaml_config().get("app")
router = APIRouter(prefix=f"/{config.get('api_prefix')}")
router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
router.include_router(user_router, prefix="/user", tags=["User management"])
router.include_router(availability_router, prefix="/avail", tags=["Availability"])
router.include_router(reservation_router, prefix="/reservation", tags=["Reservation"])
router.include_router(search_router, prefix="/search", tags=["Search"])
router.include_router(accommodation_router, prefix="/accommodation", tags=["Accommodation"])
router.include_router(notification_router, prefix="/notification", tags=["Notification"])
router.include_router(review_router, prefix="/review", tags=["Review"])
router.include_router(orchestrator_router, prefix="/orchestrator", tags=["Orchestrator"])
router.include_router(accommodation_recomender_router, prefix="/accommodation_recomender", tags=["Accommodation_recomender"])
router.include_router(flights_router, prefix="/flights", tags=["Flights"])


