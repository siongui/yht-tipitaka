import os
from bs4 import BeautifulSoup

def remove_style(file_path: str, soup):
    print(f'found in {file_path}')

    for link in soup.find_all('link'):
        #print(link)
        link.decompose()  # Completely remove the element

    for script in soup.find_all('script'):
        print(script)
        script.decompose()  # Completely remove the element

    # Save the updated HTML back to the same file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(str(soup))


def find_elements_with_id(root_dir, target_id='cbeta_tripitaka'):

    # Walk through all subdirectories
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename == "index.html":
                file_path = os.path.join(dirpath, filename)
                try:
                    isRemove = False
                    with open(file_path, 'r', encoding='utf-8') as f:
                        soup = BeautifulSoup(f, 'html.parser')

                    elements = soup.find_all('div', id=target_id)
                    if len(elements) > 0:
                        isRemove = True

                    if isRemove:
                        remove_style(file_path, soup)

                except Exception as e:
                    print(f"Error reading {file_path}: {e}")


# Example usage
if __name__ == "__main__":
    root_folder = "."  # 🔁 Replace with your actual path
    find_elements_with_id(root_folder)

