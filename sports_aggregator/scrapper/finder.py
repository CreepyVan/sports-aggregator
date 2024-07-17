"""
Module for finding links related to football teams and players using web scraping.
"""
#pylint: disable=  unused-import,trailing-whitespace,line-too-long,duplicate-code
from bs4 import BeautifulSoup as bs
from repository.browser import init_driver, WebDriverWait, EC, By

def find_team_link(name):
    """
    Finds and returns the WhoScored link for a given team name.
    
    Args:
        name (str): The name of the football team.
    
    Returns:
        str: The WhoScored link for the team if found, otherwise an error message.
    """
    driver = init_driver()
    try:
        query = '+'.join(name.split()) + '+stats'
        search_url = f'https://www.google.com/search?q={query}+football+details+whoscored.com'
        driver.get(search_url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.g')))
        soup = bs(driver.page_source, 'html.parser')
        link = None
        for item in soup.select('div.g a[href]'):
            try:
                link = item['href']
                if 'www.whoscored.com' in link:
                    link = link.split('&')[0]  # Clean up unnecessary parameters
                    break
            except KeyError as e:
                print(f"KeyError: {e}")
            except Exception as e:
                print(f"Exception: {e}")
        return link if link else f"No WhoScored link found for {name}"
    finally:
        driver.quit()

def team_player_link(name):
    """
    Finds and returns the Transfermarkt link for a given team player name.
    
    Args:
        name (str): The name of the football team player.
    
    Returns:
        str: The Transfermarkt link for the player if found, otherwise None.
    """
    driver = init_driver()
    try:
        query = '+'.join(name.split()) + '+stats'
        search_url = f'https://www.google.com/search?q={query}+transfermarkt.co.in+club+profile/'
        driver.get(search_url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.g')))
        soup = bs(driver.page_source, 'html.parser')
        link = None
        for item in soup.select('div.g a[href]'):
            try:
                link = item['href']
                if 'www.transfermarkt.co.in' in link:
                    link = link.split('&')[0]  # Clean up unnecessary parameters
                    break
            except KeyError as e:
                print(f"KeyError: {e}")
            except Exception as e:
                print(f"Exception: {e}")
        return link
    finally:
        driver.quit()

def team_news_link(team_name):
    """
    Finds and returns the ESPN link for current football news related to a team.
    
    Args:
        team_name (str): The name of the football team.
    
    Returns:
        str: The ESPN link for current team news if found, otherwise an empty string.
    """
    query = '+'.join(team_name.split())
    search_url = f'https://www.google.com/search?q={query}+espn.com+football+current+news'
    browser = init_driver()
    try:
        browser.get(search_url) 
        WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.g')))
        soup = bs(browser.page_source, 'html.parser')
        link = None
        for item in soup.select('div.g a[href]'):
            try:
                link = item['href']
                if (link.startswith('https://www.espn.in/football/') or 
                    link.startswith('https://www.espn.com/soccer/')) and '/story/' not in link:
                    link = link.split('&')[0]  # Clean up unnecessary parameters
                    break
            except KeyError as e:
                print(f"KeyError: {e}")
            except Exception as e:
                print(f"Exception: {e}")
            print(link)
        return link if link else ''
    finally:
        browser.quit()
