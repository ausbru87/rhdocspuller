import requests
from bs4 import BeautifulSoup

# URL of the main page
base_url = 'https://docs.redhat.com'
url = f'{base_url}/en/documentation/openshift_container_platform/4.16'

# Send GET request to the page
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Focus on the main content by targeting <main id="main-content">
main_content = soup.find('main', {'id': 'main-content'})

# Find all the category links within the main content area
links = main_content.find_all('a', href=True)

# Iterate over the links
for link in links:
    href = link['href']
    
    # Skip invalid or empty links
    if href.startswith('#') or 'javascript' in href:
        continue
    
    # Convert relative links to absolute
    if href.startswith('/'):
        href = base_url + href
    
    # Visit each valid link and extract PDFs
    try:
        subpage_response = requests.get(href)
        subpage_soup = BeautifulSoup(subpage_response.text, 'html.parser')
        
        # Find all PDF links in the subpage
        pdf_links = subpage_soup.find_all('a', href=lambda x: x and '.pdf' in x)
        for pdf_link in pdf_links:
            pdf_url = pdf_link['href']
            
            # Ensure PDF URLs are absolute and correctly formatted
            if pdf_url.startswith('/'):
                pdf_url = base_url + pdf_url
            
            pdf_name = pdf_url.split('/')[-1]
            
            # Download the PDF
            print(f"Downloading {pdf_name} from {pdf_url}")
            pdf_response = requests.get(pdf_url)
            with open(pdf_name, 'wb') as f:
                f.write(pdf_response.content)
            print(f"{pdf_name} downloaded successfully!")
    
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch {href}: {e}")

