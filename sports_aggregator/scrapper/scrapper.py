"""
Module for scraping football player data from various sources.
"""
#pylint: disable=  unused-import,trailing-whitespace,line-too-long,broad-except,duplicate-code,import-error
from urllib.parse import unquote
import time
import re
from selenium import webdriver
from bs4 import BeautifulSoup as bs
from db_model.schemas import schema
from repository.browser import init_driver
from .search import find_stat_link, find_wikipedia_link, find_news_link

def remove_square_brackets(content):
    """
    Removes square brackets and extra whitespace from content.

    Args:
        content (str): The string from which to remove square brackets.

    Returns:
        str: The cleaned content.
    """
    pattern = r"\[.*?\]"
    return re.sub(pattern, "", content)

def scrape_player_data(soup):
    """
    Scrapes basic player data from a Wikipedia page.

    Args:
        soup (BeautifulSoup): The BeautifulSoup object of the player's Wikipedia page.

    Returns:
        schema.Playerbase: Player information structured according to schema.
    """
    try:
        name = remove_square_brackets(soup.find('td', class_="infobox-data nickname").text.strip().replace('\n', ''))
        country = remove_square_brackets(soup.find('td', class_="infobox-data birthplace").text.strip().replace('\n', ''))
        height = remove_square_brackets(soup.find_all('td', class_="infobox-data")[3].text.strip().replace('\n', ''))
        position = remove_square_brackets(soup.find('td', class_="infobox-data role").text.strip().replace('\n', ''))
        
        try:
            age = remove_square_brackets(soup.find('span', class_="noprint ForceAgeToShow").text.strip().replace('\n', ''))
        except:
            age = 'unknown'
        
        shirt_no = remove_square_brackets(soup.find_all('td', class_="infobox-data")[6].text.strip().replace('\n', ''))
        item = soup.find('td', class_="infobox-image")
        player_img = item.find('img', class_='mw-file-element').get('src').strip().replace('\n', '')
        club_img = ""
        
        try:
            browser = webdriver.Chrome()
            time.sleep(7)
            link = find_wikipedia_link(soup.find('td', class_="infobox-data org").text.strip().replace('\n', ''))
            browser.get(link)
            time.sleep(7)
            soup = bs(browser.page_source, "html.parser")
            item = soup.find('td', class_="infobox-image")
            club_img = item.find('img', class_='mw-file-element').get('src').strip().replace('\n', '')
            print(club_img, "link: ", link)
        except Exception as e:
            print(f"Error scraping club image: {e}")
        finally:
            browser.quit()
        
        player = schema.Playerbase(
            name=name, 
            positions=position, 
            age=age, 
            country=country, 
            height=height, 
            shirt_no=shirt_no, 
            player_img=player_img, 
            club_img=club_img
        )
        return player
    except Exception as e:
        print(f"Error scraping player data: {e}")

def scrape_player_stats(name):
    """
    Scrapes player statistics from a stats link.

    Args:
        name (str): The name of the player.

    Returns:
        list: A list of schema.StatsBase objects containing player statistics.
    """
    stats = []
    try:
        link = find_stat_link(name)
        browser = init_driver()
        link = unquote(unquote(link))
        browser.get(link)
        time.sleep(5)
        soup = bs(browser.page_source, "html.parser")
        table = soup.find('table', class_="grid with-centered-columns hover")
        rows = table.find_all('tr')
        
        for row in rows:
            cells = row.find_all('td')
            if len(cells) >= 12:
                stats.append(schema.StatsBase(
                    tournament=cells[0].text.strip().replace('\n', ''),
                    apps=cells[1].text.strip().replace('\n', ''),
                    goals=cells[3].text.strip().replace('\n', ''),
                    assists=cells[4].text.strip().replace('\n', ''),
                    yellow=cells[5].text.strip().replace('\n', ''),
                    red=cells[6].text.strip().replace('\n', ''),
                    motm=cells[10].text.strip().replace('\n', ''),
                    rating=cells[11].text.strip().replace('\n', ''),
                ))
    except Exception as e:
        print(f"Error scraping player stats: {e}")
    finally:
        browser.quit()
        return stats

def scrape_player_news(name):
    """
    Scrapes player-related news articles.

    Args:
        name (str): The name of the player.

    Returns:
        list: A list of schema.NewsBase objects containing player news articles.
    """
    try:
        link = find_news_link(name)
        browser = init_driver()
        browser.get(link)
        soup = bs(browser.page_source, "html.parser")
        link = soup.find('ul', class_='Nav__Secondary__Menu center flex items-center relative').find_all('li')[2].find('a').get('href')
        link = 'https://espn.in' + link
        link = unquote(unquote(link))

        browser.get(link)
        time.sleep(5)
        soup = bs(browser.page_source, "html.parser")
        articles = soup.find_all('article')
        news_items = []

        for article in articles:
            img = ""
            link = ""
            title = ""

            # Find image container and extract image source
            container = article.find('div', class_="Image__Wrapper aspect-ratio--child")
            if container:
                img_tag = container.find('img')
                if img_tag:
                    img = img_tag.get('src')

            # Find link container and extract link and title
            link_container = article.find('div', class_="ResponsiveWrapper")
            if link_container:
                link_tag = link_container.find('a')
                if link_tag:
                    link = 'https://www.espn.in' + link_tag.get('href')

                title_tag = link_container.find('h2', class_="contentItem__title")
                if title_tag:
                    title = title_tag.text.strip()

            news_items.append(schema.NewsBase(news_img=img, news_title=title, news_link=link))

        return news_items
    except Exception as e:
        print(f"Error scraping player news: {e}")
    finally:
        browser.quit()

def scrape_player_name(name):
    """
    Scrapes the official name of a player from Wikipedia.

    Args:
        name (str): The name of the player.

    Returns:
        str: The official name of the player.
    """
    try:
        link = find_wikipedia_link(name)
        time.sleep(7)
        link = unquote(unquote(link))
        browser = init_driver()
        browser.get(link)
        soup = bs(browser.page_source, "html.parser")
        name = remove_square_brackets(soup.find('td', class_="infobox-data nickname").text.strip().replace('\n', ''))
        return name, soup
    except Exception as e:
        print(f"Error scraping player name: {e}")
    finally:
        browser.quit()

def find_articles(name):
    """
    Finds news articles related to a player.

    Args:
        name (str): The name of the player.

    Returns:
        list: A list of news articles as HTML strings.
    """
    try:
        link = find_news_link(name)
        link = unquote(unquote(link))
        browser = init_driver()
        browser.get(link)
        time.sleep(5)
        soup = bs(browser.page_source, "html.parser")
        articles = soup.find_all('article')
        articles = [str(item) for item in articles]
    except Exception as e:
        print(f"Error finding articles: {e}")
    finally:
        browser.quit()
        return articles
