"""

Main module for FastAPI application.
"""
#pylint: disable=  unused-import,trailing-whitespace,line-too-long,import-error
import random  # Standard library import
from sqlalchemy.orm import session  # Third-party import
from fastapi import FastAPI, Depends  # Third-party import
from db_model.models import models  # First-party import
from db_model.schemas import schema  # First-party import
from db_model.database.database import engine, get_db  # First-party import
from app.routers import player, teams  # First-party import

app = FastAPI()

models.Base.metadata.create_all(engine)

app.include_router(player.router)
app.include_router(teams.router)

@app.get('/news')
def get_news(db: session = Depends(get_db)):
    """
    Endpoint to fetch news from the database.
    """
    team_news = db.query(models.Team_News).all()
    news = []
    for index in random.sample(range(0, len(team_news)), 15):
        news.append(schema.Team_News.from_orm(team_news[index]))
    return news
