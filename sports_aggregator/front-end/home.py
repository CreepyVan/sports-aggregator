#pylint: disable=  unused-import,,trailing-whitespace,line-too-long
import streamlit as st
import requests
from conversion import get_base64_image, default_image_path

def get_news():
    """
    Fetch news data from the API.

    Returns:
        list: A list of news articles.
    """
    try:
        news_list = requests.get("https://sports-aggregator.onrender.com/news")
        news_list.raise_for_status()
        return news_list.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching news: {e}")
        return []

def home():
    """
    Streamlit app homepage displaying sports news.
    """
    st.title("Sports Stats and Scores Aggregator")
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

    for news in get_news():
        news_img = get_base64_image(default_image_path) if not news['news_img'] else news['news_img']
        
        news_title = news.get('news_title', 'News not found')
        news_link = news.get('news_link', '#')

        # Display news box
        st.markdown(f"""
        <div class="news-box">
            <img src="{news_img}" width="100%">
            <div class="news-title" style="font-size: larger;">
                <a href="{news_link}" target="_blank" style="text-decoration: none">{news_title}</a>
            </div>
        </div>
        """, unsafe_allow_html=True)
