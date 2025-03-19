from bs4 import BeautifulSoup
import sys

# Parse the HTML with Beautiful Soup
with open(sys.argv[1]) as f:
    soup = BeautifulSoup(f, 'html.parser')

    # Find all anchor tags and extract their href attributes
    links = []
    for a_tag in soup.find_all('a'):
        href = a_tag.get('href')
        if href:
            links.append(href)

    # Print all links
    print(f"# Found {len(links)} links:")
    for link in links:
        print(f'https://www.archives.gov{link}')
