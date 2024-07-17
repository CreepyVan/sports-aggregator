"""
Module defining SQLAlchemy models for the application.
"""
#pylint: disable=  unused-import,trailing-whitespace,line-too-long
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db_model.database.database import Base

class Player(Base):
    """
    Player model representing players in the database.
    """
    __tablename__ = 'players'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    country = Column(String)
    height = Column(String)
    positions = Column(String)
    age = Column(Integer)
    shirt_no = Column(Integer)
    player_img = Column(String)
    club_img = Column(String)

    # Define relationships
    stats = relationship("Stats", back_populates="player")
    news = relationship("News", back_populates="player")

    def update_stats(self, stats_data):
        """
        Placeholder method to update player statistics.
        """
        pass

    def upload_image(self, image_data):
        """
        Placeholder method to upload player images.
        """
        pass


class Stats(Base):
    """
    Stats model representing statistics of players in tournaments.
    """
    __tablename__ = 'stats'

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey('players.id'))  # Foreign key to players table
    tournament = Column(String)
    apps = Column(String)
    goals = Column(String)
    assists = Column(String)
    yellow = Column(String)
    red = Column(String)
    motm = Column(String)
    rating = Column(String)

    # Define the relationship with Player table
    player = relationship("Player", back_populates="stats")

    def calculate_performance_rating(self):
        """
        Placeholder method to calculate player's performance rating.
        """
        pass


class News(Base):
    """
    News model representing news related to players.
    """
    __tablename__ = 'news'

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey('players.id'))
    news_img = Column(String)
    news_link = Column(String)
    news_title = Column(String)

    # Define the relationship with Player table
    player = relationship("Player", back_populates="news")

    def generate_news_summary(self):
        """
        Placeholder method to generate a summary of player news.
        """
        pass

class Team(Base):
    """Team model representing teams in the database."""
    __tablename__ = 'team'

    id = Column(Integer, primary_key=True, index=True)
    team_name = Column(String)
    team_img = Column(String)

    # Relationships
    fixtures = relationship("MatchFixtures", back_populates="team")
    stats = relationship("TeamStats", back_populates="team")
    players = relationship("TeamPlayers", back_populates="team")


class MatchFixtures(Base):
    """MatchFixtures model representing upcoming fixtures."""
    __tablename__ = 'fixtures'

    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, ForeignKey('team.id'))
    league = Column(String)
    date = Column(String)
    home = Column(String)
    result = Column(String)
    away = Column(String)

    # Relationship
    team = relationship("Team", back_populates="fixtures")


class TeamStats(Base):
    """TeamStats model representing team statistics."""
    __tablename__ = 'team_stats'

    id = Column(Integer, primary_key=True, index=True)
    tournament = Column(String)
    team_id = Column(Integer, ForeignKey('team.id'))
    apps = Column(String)
    goals = Column(String)
    shots_pg = Column(String)
    poss = Column(String)
    passes = Column(String)
    rating = Column(String)

    # Relationship
    team = relationship("Team", back_populates="stats")


class TeamPlayers(Base):
    """TeamPlayers model representing players in a team."""
    __tablename__ = 'team_player'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    img = Column(String)
    team_id = Column(Integer, ForeignKey('team.id'))
    dob = Column(String)
    nat = Column(String)
    market_value = Column(String)

    # Relationship
    team = relationship("Team", back_populates="players")


class Team_News(Base):
    """Team_News model representing news related to teams."""
    __tablename__ = 'Team_news'

    id = Column(Integer, primary_key=True, index=True)
    team_name = Column(String)
    news_img = Column(String)
    news_link = Column(String)
    news_title = Column(String)
