# pylint: disable=trailing-whitespace ,import-error, broad-except,line-too-long,too-many-locals,raise-missing-from,redefined-builtin
import asyncio
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from scrapper.scrapper_team import (
    scrape_fixtures, scrape_stats, scrape_players,
    scrape_name_image, scrape_news
)
from db_model.models import models
from db_model.schemas import schema
from scrapper.finder import find_team_link, team_player_link, team_news_link
from db_model.database.database import get_db
from fuzzywuzzy import fuzz
from apscheduler.schedulers.background import BackgroundScheduler

router = APIRouter(
    tags=['teams'],
    prefix='/teams'
)

def is_similar(name1: str, name2: str, threshold: int = 65) -> bool:
    """
    Check if two team names are similar based on a fuzzy matching threshold.

    Args:
        name1 (str): First team name.
        name2 (str): Second team name.
        threshold (int): Similarity threshold.

    Returns:
        bool: True if the similarity ratio is above the threshold, False otherwise.
    """
    return fuzz.ratio(name1.lower(), name2.lower()) >= threshold

def get_most_similar_teams(teams, team_name: str, threshold: int = 60):
    """
    Get teams with names similar to the provided team name based on a fuzzy matching threshold.

    Args:
        teams (list): List of team objects.
        team_name (str): Team name to match against.
        threshold (int): Similarity threshold.

    Returns:
        list: List of teams with similar names.
    """
    most_similar_teams = [
        team for team in teams if fuzz.ratio(team.team_name.lower(), team_name.lower()) >= threshold
    ]
    return most_similar_teams

async def update_team_data(db: Session, team_name: str):
    """
    Update team data including fixtures, stats, players, and news.

    Args:
        db (Session): Database session.
        team_name (str): Name of the team to update.

    Raises:
        HTTPException: If the team is not found.
    """
    team = db.query(models.Team).filter(models.Team.team_name == team_name).first()
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")

    link = find_team_link(team_name)

    # Update fixtures
    fixtures = scrape_fixtures(link)
    if fixtures:
        db.query(models.MatchFixtures).filter(models.MatchFixtures.team_id == team.id).delete()
        for fixture in fixtures:
            db_fixture = models.MatchFixtures(**fixture, team_id=team.id)
            db.add(db_fixture)
        db.commit()

    # Update stats
    stats = scrape_stats(link)
    if stats:
        db.query(models.TeamStats).filter(models.TeamStats.team_id == team.id).delete()
        for stat in stats:
            db_stat = models.TeamStats(**stat, team_id=team.id)
            db.add(db_stat)
        db.commit()

    # Update players
    player_link = team_player_link(team_name)
    players = scrape_players(player_link)
    if players:
        db.query(models.TeamPlayers).filter(models.TeamPlayers.team_id == team.id).delete()
        for player in players:
            db_player = models.TeamPlayers(**player, team_id=team.id)
            db.add(db_player)
        db.commit()

    # Update news
    news_link = team_news_link(team_name)
    try:
        news_items = await scrape_news(news_link)
        if news_items:
            similar_teams = get_most_similar_teams(db.query(models.Team_News).all(), team_name)
            if similar_teams:
                db.query(models.Team_News).filter(
                    models.Team_News.team_name.in_([team.team_name for team in similar_teams])
                ).delete()
                db.commit()
                for item in news_items:
                    db_news = models.Team_News(**item, team_name=team_name)
                    db.add(db_news)
                db.commit()
    except Exception as e:
        print(f"Error scraping news: {e}")

def update_team_data_background(team_name: str, db: Session):
    """
    Update team data in the background.

    Args:
        team_name (str): Name of the team to update.
        db (Session): Database session.
    """
    loop = asyncio.get_event_loop()
    loop.run_in_executor(None, lambda: asyncio.run(update_team_data(db, team_name)))

scheduler = BackgroundScheduler()
scheduler.add_job(lambda: asyncio.run(update_all_team_data()), 'interval', hours=0.125)

async def update_all_team_data():
    """
    Update data for all teams.

    Returns:
        None
    """
    db = next(get_db())
    teams = db.query(models.Team).all()
    for team in teams:
        update_team_data_background(team.team_name, db)

@router.on_event("startup")
async def startup_event():
    """
    Event handler for the application startup event.
    """
    scheduler.start()

@router.on_event("shutdown")
async def shutdown_event():
    """
    Event handler for the application shutdown event.
    """
    scheduler.shutdown()

@router.post('/fixtures/{id}/{team_name}', status_code=status.HTTP_201_CREATED)
def add_fixtures(team_name: str, id: int, db: Session = Depends(get_db)):
    """
    Add fixtures for a team.

    Args:
        team_name (str): Name of the team.
        id (int): Team ID.
        db (Session): Database session.

    Raises:
        HTTPException: If fixtures are not found.

    Returns:
        list: List of added fixtures.
    """
    link = find_team_link(team_name)
    fixtures = scrape_fixtures(link)
    
    if not fixtures:
        raise HTTPException(status_code=404, detail="Fixtures not found")
    
    tasks = []
    for fixture in fixtures:
        db_fixture = models.MatchFixtures(**fixture, team_id=id)
        db.add(db_fixture)
        tasks.append(db_fixture)

    db.commit()
    return [schema.MatchFixtures.from_orm(item) for item in tasks]

@router.post('/players/{id}/{team_name}', status_code=status.HTTP_201_CREATED)
def add_players(team_name: str, id: int, db: Session = Depends(get_db)):
    """
    Add players for a team.

    Args:
        team_name (str): Name of the team.
        id (int): Team ID.
        db (Session): Database session.

    Raises:
        HTTPException: If players are not found.

    Returns:
        list: List of added players.
    """
    link = team_player_link(team_name)
    players = scrape_players(link)
    
    if not players:
        raise HTTPException(status_code=404, detail="Players not found")
    
    tasks = []
    for player in players:
        db_player = models.TeamPlayers(**player, team_id=id)
        db.add(db_player)
        tasks.append(db_player)

    db.commit()
    return [schema.TeamPlayers.from_orm(item) for item in tasks]

@router.post('/stats/{id}/{team_name}', status_code=status.HTTP_201_CREATED)
def add_stats(team_name: str, id: int, db: Session = Depends(get_db)):
    """
    Add stats for a team.

    Args:
        team_name (str): Name of the team.
        id (int): Team ID.
        db (Session): Database session.

    Raises:
        HTTPException: If stats are not found.

    Returns:
        list: List of added stats.
    """
    link = find_team_link(team_name)
    stats = scrape_stats(link)
    
    if not stats:
        raise HTTPException(status_code=404, detail="Stats not found")
    
    tasks = []
    for stat in stats:
        db_stat = models.TeamStats(**stat, team_id=id)
        db.add(db_stat)
        tasks.append(db_stat)

    db.commit()
    return [schema.TeamStats.from_orm(item) for item in tasks]

@router.post('/{team_name}', status_code=status.HTTP_201_CREATED)
def add_team(team_name: str, db: Session = Depends(get_db)):
    """
    Add a team.

    Args:
        team_name (str): Name of the team.
        db (Session): Database session.

    Returns:
        schema.Team: Added team object.
    """
    link = find_team_link(team_name)
    team_data = scrape_name_image(link)
    db_team = models.Team(**team_data)
    db.add(db_team)
    db.commit()
    return schema.Team.from_orm(db_team)

@router.get('/{team_name}')
def get_team(team_name: str, db: Session = Depends(get_db)):
    """
    Get a team by name.

    Args:
        team_name (str): Name of the team.
        db (Session): Database session.

    Raises:
        HTTPException: If team is not found.

    Returns:
        schema.Team: Team object.
    """
    teams = db.query(models.Team).all()
    for team in teams:
        if is_similar(team.team_name, team_name):
            return schema.Team.from_orm(team)
    raise HTTPException(status_code=404, detail="Team not found")

@router.post('/news/{team_name}')
async def add_news(team_name: str, db: Session = Depends(get_db)):
    """
    Add news for a team.

    Args:
        team_name (str): Name of the team.
        db (Session): Database session.

    Raises:
        HTTPException: If news is not found.

    Returns:
        list: List of added news items.
    """
    link = team_news_link(team_name)
    print(link)
    try:
        news = []
        news_items = await scrape_news(link)
        print(news_items)
        for item in news_items:
            db_news = models.Team_News(**item, team_name=team_name)
            db.add(db_news)
            news.append(schema.Team_News.from_orm(item))
        db.commit()
        return news
    except:
        raise HTTPException(status_code=404, detail="News not found")

@router.get('/news/{team_name}')
def get_news(team_name: str, db: Session = Depends(get_db)):
    """
    Get news for a team by name.

    Args:
        team_name (str): Name of the team.
        db (Session): Database session.

    Raises:
        HTTPException: If no news is found for the team.

    Returns:
        list: List of news items for the team.
    """
    teams = get_most_similar_teams(db.query(models.Team_News).all(), team_name)
    if not teams:
        raise HTTPException(status_code=404, detail="No news found for this team")
    return [schema.Team_News.from_orm(item) for item in teams]
