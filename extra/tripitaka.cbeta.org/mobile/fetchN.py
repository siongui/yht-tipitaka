# Requirements
# $ pip install requests beautifulsoup4

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs

def get_query_dict(url: str) -> dict:
    # Parse the URL
    parsed_url = urlparse(url)

    # Extract the raw query string
    query_string = parsed_url.query

    # Convert query string to dictionary
    query_dict = parse_qs(query_string)

    return query_dict


def fetch_and_save_page(url: str) -> list:
    """
    Fetches a webpage, saves its HTML to a file, and returns all href links.

    Args:
        url (str): The URL to fetch.
        output_file (str): The local filename to save the HTML content.

    Returns:
        list: A list of href links found in the page.
    """
    try:
        response = requests.get(url)

        if response.status_code == 200:
            html_content = response.text

            links = []
            output_file = 'index.html'

            # Parse HTML and extract hrefs
            soup = BeautifulSoup(html_content, 'html.parser')

            # find all tags with href
            for a in soup.find_all('a', href=True):
                old_href = a['href']

                query_dict = get_query_dict(old_href)
                #print("Parsed query string:", query_dict)
                if 'index' in query_dict:
                    print(query_dict['index'])
                    a['href'] = query_dict['index'][0] + '/'

                links.append(old_href)

            # Save HTML to file
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(str(soup))
            print(f"✅ Page saved to: {output_file}")

            print(f"🔗 Found {len(links)} links.")
            return links
        else:
            print(f"❌ Failed to fetch page. Status code: {response.status_code}")
            return []

    except Exception as e:
        print(f"⚠️ Error: {e}")
        return []

# Example usage
if __name__ == "__main__":
    url = 'https://tripitaka.cbeta.org/mobile/index.php?index=N'
    hrefs = fetch_and_save_page(url)

    # Print the links
    #for href in hrefs:
    #    print(href)

