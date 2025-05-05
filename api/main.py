from fastapi import FastAPI
from app.routes import csv_analyzer

app = FastAPI()

app.include_router(csv_analyzer.router)