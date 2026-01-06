import time
import random
from fastapi import FastAPI, HTTPException

from tracelens.middleware.track import TraceLensMiddleware
from tracelens.core.config.model import TraceLensConfig
from tracelens.api.show import show

# -------------------------------
# CONFIG
# -------------------------------
config = TraceLensConfig(
    enabled=True,
    slow_request_threshold_ms=300,  # anything over 0.3s is "slow"
    enable_dashboard=False,         # optional
)

# -------------------------------
# FASTAPI APP
# -------------------------------
app = FastAPI(title="Tracelens Demo")

# Add Tracelens middleware
app.add_middleware(TraceLensMiddleware, config=config)


# -------------------------------
# ENDPOINTS
# -------------------------------
@app.get("/fast")
def fast_endpoint():
    return {"status": "fast"}


@app.get("/slow")
def slow_endpoint():
    # Simulate a slow request
    time.sleep(random.uniform(0.4, 0.7))
    return {"status": "slow"}


@app.get("/error")
def error_endpoint():
    # Simulate an error
    raise HTTPException(status_code=500, detail="Simulated error")


@app.get("/show_logs")
def show_logs_endpoint():
    # Allow user to read current logs using tracelens.show()
    return show(raw=True)
