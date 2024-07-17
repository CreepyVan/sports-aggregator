# pylint: disable=trailing-whitespace , broad-except,line-too-long,import-error
from urllib.parse import unquote
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from db_model.database.database import get_db
from app import schema
from app import models
from scrapper.scrapper import scrape_player_data, scrape_player_stats, scrape_player_news, scrape_player_name

router = APIRouter(
    tags=['player'],
    prefix='/player'
)

@router.post('/{player_name}', status_code=status.HTTP_201_CREATED)
def create_player(player_name: str, db: Session = Depends(get_db)):
    """
    Create a new player entry in the database.

    Args:
        player_name (str): The name of the player to be added.
        db (Session): The database session.

    Raises:
        HTTPException: If player data is not found.

    Returns:
        dict: Player data.
    """
    # Scraping player data and stats
    player_data = scrape_player_data(player_name)
    player_stats = scrape_player_stats(player_name)
    
    if not player_data:
        raise HTTPException(status_code=404, detail="Player not found")
    
    # Create new player entry in the database
    new_player = models.Player(**player_data.dict())
    db.add(new_player)
    db.commit()
    db.refresh(new_player)
    
    # Add player stats to the database
    for stat in player_stats:
        new_stat = models.Stats(**stat.dict(), player_id=new_player.id)
        db.add(new_stat)
    
    db.commit()
    
    return player_data

@router.get('/{player_name}', response_model=schema.ShowPlayer, status_code=status.HTTP_200_OK)
def get_player(player_name: str, db: Session = Depends(get_db)):
    """
    Get a player's information by name.

    Args:
        player_name (str): The name of the player.
        db (Session): The database session.

    Raises:
        HTTPException: If player data is not found.

    Returns:
        schema.ShowPlayer: Player data, stats, and news.
    """
    # Decode player name from URL path
    decoded_player_name = unquote(player_name)
    
    # Scrape player name and soup
    player_name, soup = scrape_player_name(decoded_player_name)
    
    if not player_name:
        raise HTTPException(status_code=404, detail="Player not found")
    
    # Query player from database
    player = db.query(models.Player).filter(models.Player.name == player_name).first()
    
    if player:
        # Prepare player stats
        player_stats = [
            schema.ShowStats(
                tournament=str(stat.tournament),
                apps=str(stat.apps),
                goals=str(stat.goals),
                assists=str(stat.assists),
                yellow=str(stat.yellow),
                red=str(stat.red),
                motm=str(stat.motm),
                rating=str(stat.rating),
            )
            for stat in player.stats
        ]
        
        # Scrape player news
        player_news = scrape_player_news(player_name)
        
        # Prepare response with player data, stats, and news
        player_data = schema.ShowPlayer(
            name=player.name,
            country=player.country,
            height=player.height,
            positions=player.positions,
            age=player.age,
            shirt_no=str(player.shirt_no),
            player_img=player.player_img,
            club_img=player.club_img,
            stats=player_stats,
            news=player_news,
        )
        
        return player_data
    
    # If player not found in database, create new entry
    player_data = scrape_player_data(soup)
    player_stats = scrape_player_stats(player_name)
    player_news = scrape_player_news(player_name)
    
    new_player = models.Player(**player_data.dict())
    db.add(new_player)
    db.commit()
    db.refresh(new_player)
    
    # Add player stats to the database
    for stat in player_stats:
        new_stat = models.Stats(**stat.dict(), player_id=new_player.id)
        db.add(new_stat)
    
    db.commit()
    
    # Prepare stats for response
    player_stats_response = [
        schema.ShowStats(
            tournament=str(stat.tournament),
            apps=str(stat.apps),
            goals=str(stat.goals),
            assists=str(stat.assists),
            yellow=str(stat.yellow),
            red=str(stat.red),
            motm=str(stat.motm),
            rating=str(stat.rating),
        )
        for stat in player_stats
    ]
    
    # Prepare news for response
    player_news_response = [
        schema.NewsBase(
            news_img=str(news.news_img),
            news_link=str(news.news_link),
            news_title=str(news.news_title),
        )
        for news in player_news
    ]
    
    # Prepare response with newly created player data, stats, and news
    show_data = schema.ShowPlayer(
        name=new_player.name,
        country=new_player.country,
        height=new_player.height,
        positions=new_player.positions,
        age=new_player.age,
        shirt_no=str(new_player.shirt_no),
        player_img=new_player.player_img,
        club_img=new_player.club_img,
        stats=player_stats_response,
        news=player_news_response,
    )
    
    return show_data
