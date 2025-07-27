from fastapi import APIRouter
import time

router = APIRouter()
_start = time.time()

@router.get("/health/live")
def liveness():
    return {"status": "alive", "uptime_sec": time.time() - _start}

@router.get("/health/ready")
def readiness():
    # placeholder for DB checks or other lightweight verifications
    return {"status": "ready"}
