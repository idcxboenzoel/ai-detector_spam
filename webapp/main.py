from fastapi import FastAPI, Request
from webapp.views import router

app = FastAPI()
app.include_router(router)