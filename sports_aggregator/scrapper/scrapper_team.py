"""
Module for scraping football data from various websites.
"""
#pylint: disable=  unused-import,trailing-whitespace,line-too-long,broad-except,duplicate-code
from bs4 import BeautifulSoup as bs
from repository.browser import init_driver, WebDriverWait, EC, By
import asyncio
import time
def scrape_fixtures(link):
    """
    Scrapes fixture data from a given link.
    
    Args:
        link (str): The URL of the fixtures page.
    
    Returns:
        list: A list of dictionaries containing fixture details.
    """
    driver = init_driver()
    try:
        driver.get(link)
        time.sleep(4)  # Allow time for page to load
        soup = bs(driver.page_source, "html.parser")
        table_body = soup.find('div', class_="fixture divtable")
        rows = table_body.find_all('div', class_="divtable-row item alt")
        fixtures = []
        for row in rows:
            # Extracting fixture details
            league = row.find('div', class_="col12-lg-1 col12-m-1 col12-s-1 col12-xs-1 tournament divtable-data").text
            date = row.find('div', class_="col12-lg-1 col12-m-1 col12-s-0 col12-xs-0 date fourth-col-date divtable-data").text
            home = row.find_all('div', class_="team")[0].text
            away = row.find_all('div', class_="team")[1].text
            result = row.find('div', class_="col12-lg-1 col12-m-1 col12-s-0 col12-xs-0 divtable-data result").text
            fixtures.append({"league": league, "date": date, "home": home, "away": away, "result": result})
        return fixtures
    finally:
        driver.quit()
def scrape_stats(link):
    """
    Scrapes team stats from a given link.
    
    Args:
        link (str): The URL of the team stats page.
    
    Returns:
        list: A list of dictionaries containing team stats.
    """
    driver = init_driver()
    try:
        driver.get(link)
        time.sleep(4)  # Allow time for page to load
        soup = bs(driver.page_source, "html.parser")
        
        tbody = soup.find('tbody', id="top-team-stats-summary-content")
        rows = tbody.find_all('tr')
        stats = []
        for row in rows:
            # Extracting team stats
            data = row.find_all('td')
            stat = {
                'tournament': data[0].text,
                'apps': data[1].text,
                'goals': data[2].text,
                'shots_pg': data[3].text,
                'poss': data[5].text,
                'passes': data[6].text,
                'rating': data[8].text
            }
            stats.append(stat)
        return stats
    finally:
        driver.quit()
def scrape_players(link):
    """
    Scrapes player data from a given link.
    
    Args:
        link (str): The URL of the players page.
    
    Returns:
        list: A list of dictionaries containing player details.
    """
    driver = init_driver()
    try:
        driver.get(link)
        try:
            # Handling cookie consent if present
            wait = WebDriverWait(driver, 7)
            iframe_xpath = '//iframe[@id="sp_message_iframe_953765"]'
            iframe = wait.until(EC.presence_of_element_located((By.XPATH, iframe_xpath)))
            driver.switch_to.frame(iframe)
            button_xpath = '//*[contains(@class, "message-component") and contains(@class, "message-button") and contains(@class, "no-children") and contains(@class, "focusable") and contains(@class, "accept-all") and contains(@class, "sp_choice_type_11") and contains(@class, "first-focusable-el")]'
            accept_button = wait.until(EC.element_to_be_clickable((By.XPATH, button_xpath)))
            accept_button.click()
            driver.switch_to.default_content()
        except:
            pass
        time.sleep(5)  # Allow time for page to load after handling consent
        soup = bs(driver.page_source, "html.parser")
        div = soup.find('div', class_='responsive-table')
        rows = div.find_all('tr', class_='odd') + div.find_all('tr', class_='even')
        team_players = []
        for row in rows:
            try:
                # Extracting player details
                data = row.find_all('td')
                dob = row.find_all('td', class_="zentriert")[1].text
                market_value = row.find('td', class_="rechts hauptlink").text
                img = data[1].find_all('td')[0].find('img').get('data-src') or data[1].find_all('td')[0].find('img').get('src')
                player = {
                    'img': img,
                    'name': data[1].find_all('td')[1].find('a').text.strip().strip('\n'),
                    'dob': dob,
                    'nat': data[6].find('img').get('src'),
                    'market_value': market_value
                }
                team_players.append(player)
            except Exception as e:
                print(f"Error scraping player data: {e}")
                raise Exception("Error scraping player data")
        
        return team_players
    finally:
        driver.quit()
def scrape_name_image(link):
    """
    Scrapes team name and image from a given link.
    
    Args:
        link (str): The URL of the team page.
    
    Returns:
        dict: A dictionary containing team name and image.
    """
    driver = init_driver()
    try:
        driver.get(link)
        time.sleep(4)  # Allow time for page to load
        soup = bs(driver.page_source, "html.parser")
        team_name = soup.find('span', class_="team-header-name").text.strip()
        team_img = soup.find('img', class_='team-emblem').get('src')
        return {"team_name": team_name, "team_img": team_img}
    finally:
        driver.quit()
async def scrape_news(link):
    """
    Asynchronously scrapes news articles from a given link.
    
    Args:
        link (str): The URL of the news page.
    
    Returns:
        list: A list of dictionaries containing news article details.
    """
    try:
        browser = init_driver()
        browser.get(link)
        print(link)
        await asyncio.sleep(2)  # Wait for the page to load
        soup = bs(browser.page_source, "html.parser")
        articles = soup.find_all('article')
        news_items = []
        for article in articles:
            img = ""
            link = ""
            title = ""
            # Extracting image, link, and title
            container = article.find('div', class_="Image__Wrapper aspect-ratio--child")
            if container:
                img_tag = container.find('img')
                if img_tag:
                    img = img_tag.get('src')
            link_container = article.find('div', class_="ResponsiveWrapper")
            if link_container:
                link_tag = link_container.find('a')
                if link_tag:
                    link = 'https://www.espn.in' + link_tag.get('href')
                title_tag = link_container.find('h2', class_="contentItem__title")
                if title_tag:
                    title = title_tag.text.strip()
            news_items.append({"news_img": img, "news_link": link, "news_title": title})
        browser.quit()
        return news_items
    except Exception as e:
        print(f"An error occurred: {e}")
        browser.quit()
        return []
