#pylint: disable=  unused-import,,trailing-whitespace,line-too-long ,missing-docstring         
import streamlit as st
import home 
import player
import team


 
st.set_page_config(layout='wide') 
# Injecht custom CSS to increase the tab name size
default_image_path = r"C:\Users\Rishin Prageet\OneDrive\Desktop\intern\sports_aggregator\images\default-image.jpg"
st.markdown(
    """
    <style> 
    div[class*="st-emotion-cache-qgowjl e1nzilvr4"] p {
        font-size: 20px;
        font-weight: bold;
    }
    </style>
    """, 
    unsafe_allow_html=True
) 


def home_main():
    home.home()

def team_():
    team.teams()
    

def players():
    player.players()

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'home'


# Sidebar navigation
with st.sidebar:
    st.header("Menu")
    home_b=st.button("🏡 Home", use_container_width=True)
        
    team_b=st.button("⚽ Teams", use_container_width=True)
        
    player_b=st.button("⛹️‍♀️Player", use_container_width=True)
    
    if home_b:
        st.session_state.page = 'home'
    if team_b:
        st.session_state.page = 'teams'
    if player_b:
        st.session_state.page = 'player'

# Page content
if st.session_state.page == 'home':
    home_main()
elif st.session_state.page == 'teams':
    team_()
elif st.session_state.page == 'player':
    players()

 

    