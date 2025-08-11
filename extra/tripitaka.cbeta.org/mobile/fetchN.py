# Requirements
# $ pip install requests beautifulsoup4

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
import os

base_url = 'https://tripitaka.cbeta.org/mobile/index.php'
isDone = {}


def get_query_string_index(url: str) -> str:
    # Parse the URL
    parsed_url = urlparse(url)

    # Extract the raw query string
    query_string = parsed_url.query

    # Convert query string to dictionary
    query_dict = parse_qs(query_string)

    if 'index' not in query_dict:
        return None

    return query_dict['index'][0]


def fetch_and_save_page(url: str) -> list:
    try:
        response = requests.get(url)

        if response.status_code == 200:
            html_content = response.text

            indexes = []

            # Parse HTML and extract hrefs
            soup = BeautifulSoup(html_content, 'html.parser')

            # find a tags with href
            for a in soup.find_all('a', href=True):
                idx = get_query_string_index(a['href'])
                #print(idx)

                if idx is None:
                    a['href'] = base_url
                else:
                    a['href'] = f"../{idx}/"
                    indexes.append(idx)

            folder_path = get_query_string_index(url)
            output_file = folder_path + '/index.html'
            # Create the folder if it doesn't exist
            os.makedirs(folder_path, exist_ok=True)
            # Save HTML to file
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            print(f"✅ Page saved to: {output_file}")

            print(f"🔗 Return {len(indexes)} indexes.")
            return indexes
        else:
            print(f"❌ Failed to fetch page. Status code: {response.status_code}")
            return []

    except Exception as e:
        print(f"⚠️ Error: {e}")
        return []


def recursive_fetch(index: str):
    indexes = fetch_and_save_page(base_url + f'?index={index}')
    isDone[index] = True

    for index in indexes:
        if index not in isDone:
            recursive_fetch(index)


# Example usage
if __name__ == "__main__":
    recursive_fetch('N')

