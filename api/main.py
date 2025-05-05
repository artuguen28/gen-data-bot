from fastapi import FastAPI
from routes import csv_loader, ask_question

app = FastAPI()

app.include_router(csv_loader.router)
app.include_router(ask_question.router)