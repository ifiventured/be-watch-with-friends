# main.py assembles the API by registering each router so its endpoints are available on the server
# creats fastapi application object
from fastapi import FastAPI
# imports routers to define endpoints
from app.api.routes import health, auth, groups
from app.api.routes import watchlist

#mounts each router onto the app
# registration so the app knows what exists
app = FastAPI(title="Watch With Friends API")
# include_router is how the app is told which endpoint groups actually exist
app.include_router(health.router, prefix="/api")
app.include_router(auth.router, prefix="/api")
app.include_router(groups.router, prefix="/api")
app.include_router(watchlist.router, prefix="/api")

# for the server to know which url paths exist + which functions shoukld run when urls are hit
