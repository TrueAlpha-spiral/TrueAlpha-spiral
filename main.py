from fastapi import FastAPI
from watchdog_endpoints import router as watchdog_router

app = FastAPI(title="TrueAlpha Service")
app.include_router(watchdog_router, prefix="/watchdog", tags=["watchdog"])


@app.get("/")
async def root():
    return {"message": "TrueAlpha API"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
