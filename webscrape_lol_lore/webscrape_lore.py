# Third Party
from bs4 import BeautifulSoup
import requests
import re

# First Party
from utils.utils import (
    read_file_into_array,
    save_string_to_file,
)
from utils.webscrape_utils import scroll_page_down

base_url = 'https://universe.leagueoflegends.com/en_US/story'
champion_list_url = 'champion.list'

champion_list = read_file_into_array(champion_list_url)


def cleanup_string(input_str):
    """ Remove anything that is not a letter or number (including spaces)."""
    return re.sub('[^A-Za-z0-9]+', '', input_str)

def preprocess_champion_name(champion_name):
    """
    Pre-process champion name.
    Useful for passing as URL.
    """
    return cleanup_string(champion_name).lower()

def get_content_from_URL(url, page_type):
    """Returns content from URL."""
    text = None
    if page_type == 'bio':
        response = requests.get(url)
        text = response.text
    elif page_type == 'story':
        text = scroll_page_down(url)
    else:
        raise NotImplementedError

    return scrape_content(text, page_type)

def construct_query_url(base_url, champion, page_type):
    """Constructs the query URL."""
    if page_type == 'bio':
        return f"{base_url}/champion/{champion}"
    # page_type == 'story'
    if champion == 'ahri':
        # Special case for AHRI as her URL is different.
        return f"{base_url}/{champion}-color"
    return f"{base_url}/{champion}-color-story"

def construct_save_filepath(champion, page_type):
    """
    Constructs the save URL.

    datasets/raw
    - champion
        - bio
        - story
    """
    return f"datasets/raw/{champion}/{page_type}"

def scrape_content(text, page_type):
    """
    Scrapes LOL webpages.

    @last_updated: 01/20/2024
    """
    soup = BeautifulSoup(text, 'html.parser')
    if page_type == 'bio':
        content = soup.find('meta', {'name': 'description'})['content']
    elif page_type == 'story':
        lines: list = soup.findAll('p', {'class': 'p_1_sJ'})
        lines_text = [line.text for line in lines]
        content = "\n".join(lines_text)
    return content

def main():
    # Iterate over all champion list.
    # Save to datasets.
    for raw_champion in champion_list:
        champion = preprocess_champion_name(raw_champion)
        for page_type in ['bio', 'story']:
            print(f"Querying champion={champion} for page_type={page_type}")
            query_url = construct_query_url(base_url, champion, page_type)
            content = get_content_from_URL(query_url, page_type)
            save_filepath = construct_save_filepath(champion, page_type)
            print(f"Save filepath: {save_filepath}")
            save_string_to_file(content, save_filepath)

        
if __name__ == '__main__':
    main()
