from bs4 import BeautifulSoup

def extract_Images_From_Content(content):
    soup = BeautifulSoup(content, 'html.parser')
    img_tag = soup.find('img')
    if img_tag and 'src' in img_tag.attrs:
        return img_tag['src']
    return None
