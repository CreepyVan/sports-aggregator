"""
Module for finding Wikipedia, WhoScored, and ESPN news links related to football players.
"""
#pylint: disable=  unused-import,trailing-whitespace,line-too-long,broad-except,duplicate-code
from bs4 import BeautifulSoup as bs
from repository.browser import WebDriverWait, EC, By, init_driver
def find_wikipedia_link(name):
    """
    Finds the Wikipedia link for a football player's name.

    Args:
        name (str): The name of the football player.

    Returns:
        str: The Wikipedia link or an error message if not found.
    """
    query = '+'.join(name.split())
    search_url = f'https://www.google.com/search?q={query}+football+wikipedia'
    browser = init_driver()
    browser.get(search_url)
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.g')))
    
    soup = bs(browser.page_source, 'html.parser')
    link = None
    
    for item in soup.select('div.g a[href]'):
        try:
            link = item['href']
            if 'wikipedia.org' in link:
                link = link.split('&')[0]  # Clean up unnecessary parameters
                break
        except Exception as e:
            print(f"Exception: {e}")
    browser.quit()
    
    return link if link else f"No Wikipedia link found for {name}"


def find_stat_link(name):
    """
    Finds the statistics link for a football player's name on WhoScored.

    Args:
        name (str): The name of the football player.

    Returns:
        str: The WhoScored statistics link or an error message if not found.
    """
    query = '+'.join(name.split()) + '+stats'
    search_url = f'https://www.google.com/search?q={query}+whoscored'
    browser = init_driver()
    browser.get(search_url)
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.g')))
    
    soup = bs(browser.page_source, 'html.parser')
    link = None
    
    for item in soup.select('div.g a[href]'):
        try:
            link = item['href']
            if 'www.whoscored.com' in link:
                link = link.split('&')[0]  # Clean up unnecessary parameters
                break
        except Exception as e:
            print(f"Exception: {e}")
    browser.quit()
    
    return link if link else f"No WhoScored link found for {name}"


def find_news_link(name):
    """
    Finds the ESPN news link for a football player's name.

    Args:
        name (str): The name of the football player.

    Returns:
        str: The ESPN news link or an empty string if not found.
    """
    query = '+'.join(name.split())
    search_url = f'https://www.google.com/search?q={query}+espn.in+news'
    browser = init_driver()
    browser.get(search_url)
    WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.g')))
    
    soup = bs(browser.page_source, 'html.parser')
    link = None
    
    for item in soup.select('div.g a[href]'):
        try:
            link = item['href']
            if ('www.espn.in/football/player' in link or 'www.espn.com/soccer/player' in link) and '/story/' not in link:
                link = link.split('&')[0]  # Clean up unnecessary parameters
                break
        except Exception as e:
            print(f"Exception: {e}")
    browser.quit()
    
    return link if link else ''
