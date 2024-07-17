# pylint: disable=unused-import, trailing-whitespace, line-too-long,duplicate-code
import streamlit as st
import pandas as pd
import requests
from conversion import default_image_path, get_base64_image

def players():
    """
    Displays player stats and news using Streamlit.
    
    The function allows the user to input a player's name and fetches the player's stats and news from an API. 
    It then displays the player's stats in a tabular format and news articles with images and titles.
    """
    st.title("Player Stats")

    player_name = st.text_input(placeholder="Enter player name", label="*")
    tab_1, tab_2 = st.tabs(['Stats', 'News'])

    if player_name:
        try:
            response = requests.get(f'http://127.0.0.1:8000/player/{player_name}')
        except Exception as e:
            raise e

        if response.status_code == 200:
            player_data = response.json()

            with tab_1:
                col1, col2 = st.columns(2)
                with col1:
                    st.title(player_data['name'])
                    st.write(f"Name: {player_data['name']}")
                    st.write(f"Country: {player_data['country']}")
                    st.write(f"Height: {player_data['height']}")
                    st.write(f"Position: {player_data['positions']}")
                    st.write(f"Age: {player_data['age']}")
                    st.write(f"Shirt Number: {player_data['shirt_no']}")
                    st.write("Stats:")
                    stats_df = pd.DataFrame(player_data['stats'])
                    st.dataframe(stats_df.style.set_properties(**{'text-align': 'center'}))

                with col2:
                    player_data['player_img'] = "https:" + player_data['player_img']
                    player_data['club_img'] = "https:" + player_data['club_img']
                    st.image(player_data['player_img'], caption='Player Image')
                    try:
                        st.image(player_data['club_img'], caption='Club Image')
                    except:
                        st.write("Club image not found")

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

                st.header(player_data['name'])

                col_1, col_2 = st.columns(2)
                col = [col_1, col_2]

                for news in player_data['news']:
                    with col[0]:
                        news_img = get_base64_image(default_image_path) if not news['news_img'] else news['news_img']
                        try:
                            news_title = news['news_title']
                            news_link = news['news_link']
                        except:
                            news_title = 'News not found'
                            news_link = '#'

                        st.markdown(f"""
                            <div class="news-box">
                                <img src="{news_img}" width="100%">
                                <div class="news-title" style="font-size: larger;">
                                    <a href="{news_link}" target="_blank" style="text-decoration: none">{news_title}</a>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                        col.append(col.pop(0))
        else:
            st.write('Player not found')
