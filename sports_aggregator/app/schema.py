#pylint: disable= trailing-whitespaces,line-too-long
from typing import List
from pydantic import BaseModel, ConfigDict

class StatsBase(BaseModel):
    """
    Base model for player statistics.
    
    Attributes:
        tournament (str): Name of the tournament.
        apps (str): Number of appearances.
        goals (str): Number of goals.
        assists (str): Number of assists.
        yellow (str): Number of yellow cards.
        red (str): Number of red cards.
        motm (str): Number of Man of the Match awards.
        rating (str): Player rating.
    """
    tournament: str
    apps: str
    goals: str
    assists: str
    yellow: str
    red: str
    motm: str
    rating: str
    model_config = ConfigDict(from_attributes=True)

class ShowStats(BaseModel):
    """
    Model for displaying player statistics.
    
    Attributes:
        tournament (str): Name of the tournament.
        apps (str): Number of appearances.
        goals (str): Number of goals.
        assists (str): Number of assists.
        yellow (str): Number of yellow cards.
        red (str): Number of red cards.
        motm (str): Number of Man of the Match awards.
        rating (str): Player rating.
    """
    tournament: str
    apps: str
    goals: str
    assists: str
    yellow: str
    red: str
    motm: str
    rating: str
    model_config = ConfigDict(from_attributes=True)

class Playerbase(BaseModel):
    """
    Base model for player information.
    
    Attributes:
        name (str): Player's name.
        country (str): Player's country.
        height (str): Player's height.
        positions (str): Player's positions.
        age (str): Player's age.
        shirt_no (str): Player's shirt number.
        player_img (str): URL to the player's image.
        club_img (str): URL to the player's club image.
    """
    name: str
    country: str
    height: str
    positions: str
    age: str
    shirt_no: str
    player_img: str
    club_img: str 
    model_config = ConfigDict(from_attributes=True)

class NewsBase(BaseModel):
    """
    Base model for news information.
    
    Attributes:
        news_img (str): URL to the news image.
        news_title (str): Title of the news.
        news_link (str): URL to the news link.
    """
    news_img: str
    news_title: str
    news_link: str
    model_config = ConfigDict(from_attributes=True)

class ShowBase(NewsBase):
    """
    Model for displaying news with player name.
    
    Attributes:
        news_player (str): Name of the player related to the news.
    """
    news_player: str

class ShowPlayer(BaseModel):
    """
    Model for displaying player information along with statistics and news.
    
    Attributes:
        name (str): Player's name.
        country (str): Player's country.
        height (str): Player's height.
        positions (str): Player's positions.
        age (str): Player's age.
        shirt_no (str): Player's shirt number.
        player_img (str): URL to the player's image.
        club_img (str): URL to the player's club image.
        stats (List[ShowStats]): List of player statistics.
        news (List[NewsBase]): List of news related to the player.
    """
    name: str
    country: str
    height: str
    positions: str
    age: str
    shirt_no: str
    player_img: str
    club_img: str
    stats: List[ShowStats]
    news: List[NewsBase]
    model_config = ConfigDict(from_attributes=True)

class MatchFixtures(BaseModel):
    """
    Model for match fixtures.
    
    Attributes:
        league (str): Name of the league.
        date (str): Date of the match.
        home (str): Home team.
        result (str): Match result.
        away (str): Away team.
    """
    league: str
    date: str
    home: str
    result: str
    away: str
    model_config = ConfigDict(from_attributes=True)

class TeamStats(BaseModel):
    """
    Model for team statistics.
    
    Attributes:
        tournament (str): Name of the tournament.
        goals (str): Number of goals.
        shots_pg (str): Shots per game.
        poss (str): Possession percentage.
        passes (str): Number of passes.
        rating (str): Team rating.
    """
    tournament: str
    goals: str
    shots_pg: str
    poss: str
    passes: str
    rating: str
    model_config = ConfigDict(from_attributes=True)

class TeamPlayers(BaseModel):
    """
    Model for team players.
    
    Attributes:
        name (str): Player's name.
        img (str): URL to the player's image.
        dob (str): Date of birth.
        nat (str): Nationality.
        market_value (str): Market value.
    """
    name: str
    img: str
    dob: str
    nat: str
    market_value: str
    model_config = ConfigDict(from_attributes=True)

class Team(BaseModel):
    """
    Model for team information.
    
    Attributes:
        team_name (str): Team's name.
        team_img (str): URL to the team's image.
        fixtures (List[MatchFixtures]): List of match fixtures.
        stats (List[TeamStats]): List of team statistics.
        players (List[TeamPlayers]): List of team players.
        id (int): Team ID.
    """
    team_name: str
    team_img: str
    fixtures: List[MatchFixtures]
    stats: List[TeamStats]
    players: List[TeamPlayers]
    id: int
    model_config = ConfigDict(from_attributes=True)

class shteam(BaseModel):
    """
    Model for simplified team information.
    
    Attributes:
        team_name (str): Team's name.
        team_img (str): URL to the team's image.
        id (int): Team ID.
    """
    team_name: str
    team_img: str
    id: int
    model_config = ConfigDict(from_attributes=True)

class Team_News(BaseModel):
    """
    Model for team news.
    
    Attributes:
        news_img (str): URL to the news image.
        news_link (str): URL to the news link.
        news_title (str): Title of the news.
    """
    news_img: str
    news_link: str
    news_title: str
    model_config = ConfigDict(from_attributes=True)
