"""
Basic FastApi application that handles a single incoming request.
"""

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def index():
    return {"msg": "working"}
