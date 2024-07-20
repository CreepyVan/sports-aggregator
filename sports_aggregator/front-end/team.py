# pylint: disable=unused-import, trailing-whitespace, line-too-long,duplicate-code,bare-except
import asyncio
import aiohttp
import streamlit as st
from conversion import get_base64_image, default_image_path

BASE_URL = "https://sports-aggregator.onrender.com"

async def get_news(team_name: str):
    """
    Fetch news for a specific team from the API.

    Args:
        team_name (str): The name of the team.

    Returns:
        list: A list of news articles for the team.

    Raises:
        Exception: If an unexpected error occurs while fetching news.
    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{BASE_URL}/teams/news/{team_name}") as response:
                response.raise_for_status()
                return await response.json()
    except aiohttp.ClientResponseError as e:
        if e:
            return None
        raise
    except Exception as e:
        st.error(f"An unexpected error occurred while fetching news: {e}")

async def add_news(team_name: str):
    """
    Add news for a specific team to the database via the API.

    Args:
        team_name (str): The name of the team.

    Returns:
        list: A list of added news articles for the team.
    """
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{BASE_URL}/teams/news/{team_name}") as response:
            response.raise_for_status()
            return await response.json()

async def add_team(team_name: str):
    """
    Add a team to the database via the API.

    Args:
        team_name (str): The name of the team.

    Returns:
        dict: The added team's information.
    """
    async with aiohttp.ClientSession() as session:
        st.write("post")
        async with session.post(f"{BASE_URL}/teams/{team_name}") as response:
            print("hi")
            response.raise_for_status()
            return await response.json()

async def get_team(team_name: str):
    """
    Fetch a team's data from the API.

    Args:
        team_name (str): The name of the team.

    Returns:
        dict: The team's information.

    Raises:
        Exception: If an unexpected error occurs while fetching team data.
    """
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f"{BASE_URL}/teams/{team_name}") as response:
                
                response.raise_for_status()
                return await response.json()
        except aiohttp.ClientResponseError as e:
            if e:
                return None
            raise
        except Exception as e:
            st.error(f"An unexpected error occurred while fetching team data: {e}")

async def add_fixtures(team_name: str, id: int):
    """
    Add fixtures for a specific team to the database via the API.

    Args:
        team_name (str): The name of the team.
        id (int): The team's ID.

    Returns:
        list: A list of added fixtures for the team.
    """
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{BASE_URL}/teams/fixtures/{id}/{team_name}") as response:
            response.raise_for_status()
            return await response.json()

async def add_stats(team_name: str, id: int):
    """
    Add stats for a specific team to the database via the API.

    Args:
        team_name (str): The name of the team.
        id (int): The team's ID.

    Returns:
        list: A list of added stats for the team.
    """
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{BASE_URL}/teams/stats/{id}/{team_name}") as response:
            response.raise_for_status()
            return await response.json()

async def add_players(team_name: str, id: int):
    """
    Add players for a specific team to the database via the API.

    Args:
        team_name (str): The name of the team.
        id (int): The team's ID.

    Returns:
        list: A list of added players for the team.
    """
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{BASE_URL}/teams/players/{id}/{team_name}") as response:
            response.raise_for_status()
            return await response.json()

async def display_team_news(team_news, team_name):
    """
    Display team news in a Streamlit app.

    Args:
        team_news (list): A list of news articles for the team.
        team_name (str): The name of the team.
    """
    try:
        if team_news is None:
            team_news = await add_news(team_name)
        with tab_2:
            st.markdown("""
<style>
.news-box {
    border: 1px solid #e6e6e6;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    padding: 16px;
    margin: 20px;
    width: 100%;
    background-color: #ffffff;
}
.news-box:hover {
    transform: scale(1.05); /* Slightly enlarge the box on hover */
}
.news-box img {  
    border-radius: 10px;
}
.news-title {
    font-size: 18px;
    font-weight: bold;
    margin-top: 8px;
}
</style>
""", unsafe_allow_html=True)

            # Display team name
            st.header(team_name)

            # Display news with styling
            col_1, col_2 = st.columns(2)
            col = [col_1, col_2]

            for news in team_news:
                with col[0]:
                    news_img = get_base64_image(default_image_path) if not news['news_img'] else news['news_img']

                    try:
                        news_title = news['news_title']
                        news_link = news['news_link']
                    except:
                        news_title = 'News not found'
                        news_link = '#'

                    # Display news box
                    st.markdown(f"""
                        <div class="news-box">
                            <img src="{news_img}" width="100%">
                            <div class="news-title" style="font-size: larger;">
                                <a href="{news_link}" target="_blank" style="text-decoration: none">{news_title}</a>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    col.append(col.pop(0))
    except Exception as e:
        st.error(f"An error occurred while displaying team news: {e}")

async def display_team_data(team_info, team_name):
    """
    Display team data in a Streamlit app.

    Args:
        team_info (dict): The team's information.
        team_name (str): The name of the team.
    """
    try:
        if team_info is None:
            st.write("Team data not found, scraping data...")
            team_data = await add_team(team_name)
            team_id = team_data['id']
            fixtures_task = add_fixtures(team_name, team_id)
            stats_task = add_stats(team_name, team_id)
            players_task = add_players(team_name, team_id)
            await asyncio.gather(fixtures_task, stats_task, players_task)
            team_info = await get_team(team_name)
            fixtures = team_info['fixtures']
            stats = team_info['stats']
            players = team_info['players']
        else:
            fixtures = team_info['fixtures']
            stats = team_info['stats']
            players = team_info['players']

        # Display results
        with tab_1:
            st.write("## Team Info")
            st.markdown(f"![Team Image]({team_info['team_img']})")

            st.write("## Fixtures")
            st.table(fixtures)  # Ensure fixtures is defined and initialized

            st.write("## Stats")
            st.table(stats)

            st.write("## Players")
            st.markdown("""
                <style>
                    table {
                        width: 100%;
                        border-collapse: collapse;
                    }
                    th, td {
                        border: 1px solid black;
                        padding: 5px;
                        text-align: left;
                        width: 20%; /* Equal width for each column */
                        white-space: nowrap;
                        box-sizing: border-box;
                    }
                    th {
                        background-color: #f2f2f2;
                    }
                    .index {
                        background-color: #f2f2f2;
                        width: 5%; /* Smaller index column */
                        font-weight: bolder;
                    }
                    td img {
                        width: 50px; /* Smaller images */
                        height: auto;
                    }
                </style>
                <table>
            """, unsafe_allow_html=True)

            for idx, player in enumerate(players, start=1):
                st.markdown(f"""
                    <tr>
                        <td class="index">{idx}</td>
                        <td><img src="{player['img']}"></td>
                        <td>{player['name']}</td>
                        <td>{player['dob']}</td>
                        <td><img src="{player['nat']}" width="25"></td>
                        <td>{player['market_value']}</td>
                    </tr>
                """, unsafe_allow_html=True)

            st.markdown("</table>", unsafe_allow_html=True)

    except asyncio.TimeoutError:
        st.error("Timeout occurred while fetching data.")
    except aiohttp.ClientError as e:
        st.error(f"HTTP Error: {e}")
    except Exception as e:
        st.error(f"An error occurred while displaying team data: {e}")

async def get_news_data(team_name):
    """
    Fetch team information and news concurrently.

    Args:
        team_name (str): The name of the team.

    Returns:
        tuple: A tuple containing the team's information and news.
    """
    team_info = await get_team(team_name)
    team_news = await get_news(team_name)
    return team_info, team_news

async def display_info(team_name):
    """
    Display team information and news in a Streamlit app.

    Args:
        team_name (str): The name of the team.
    """
    team_info, team_news = await get_news_data(team_name)
    await display_team_data(team_info, team_name)
    await display_team_news(team_news, team_name)

# Streamlit App
def teams():
    """
    Streamlit app for displaying team data and news.
    """
    st.title("Team Data Application")
    st.write('Stats')
    team_name = st.text_input("Enter Team Name:")
    global tab_1, tab_2
    tab_1, tab_2 = st.tabs(['stats', 'news'])
    if team_name:
        with st.spinner("Fetching data..."):
            asyncio.run(display_info(team_name))
