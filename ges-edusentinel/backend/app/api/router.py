from fastapi import APIRouter
from .auth import router as auth
from .org import router as org
from .academics import router as academics
from .submissions import router as submissions
from .analytics import router as analytics
from .reports import router as reports

router = APIRouter(prefix="/api")
router.include_router(auth, tags=["auth"])
router.include_router(org, tags=["org"])
router.include_router(academics, tags=["academics"])
router.include_router(submissions, tags=["submissions"])
router.include_router(analytics, tags=["analytics"])
router.include_router(reports, tags=["reports"])
