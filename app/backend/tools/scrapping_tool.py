import requests
import bs4
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from io import BytesIO
from PIL import Image
import pandas as pd

class ScrapTool:

    def visit_url(self, website_url):
        
        content = requests.get(website_url,timeout=60).content
        
        #lxml is apparently faster than other settings.
        soup = BeautifulSoup(content, "lxml")
        result = {
            "website_url": website_url,
            "website_name": self.get_website_name(website_url),
            "website_text": self.get_html_title_tag(soup)+self.get_html_meta_tags(soup)+self.get_html_heading_tags(soup)+
                                                               self.get_text_content(soup)
        }
        return pd.Series(result)
    def get_html_title_tag(self,soup):
        
        return '. '.join(soup.title.contents)
    
    def get_website_name(self,website_url):
        
        return "".join(urlparse(website_url).netloc.split(".")[-2])
    
    def get_html_meta_tags(self,soup):
        '''Returns the text content of <meta> tags related to keywords and description from a webpage'''
        tags = soup.find_all(lambda tag: (tag.name=="meta") & (tag.has_attr('name') & (tag.has_attr('content'))))
        content = [str(tag["content"]) for tag in tags if tag["name"] in ['keywords','description']]
        return ' '.join(content)
    
    def get_html_heading_tags(self,soup):
        '''returns the text content of heading tags. The assumption is that headings might contain relatively important text.'''
        tags = soup.find_all(["h1","h2","h3","h4","h5","h6"])
        content = [" ".join(tag.stripped_strings) for tag in tags]
        return ' '.join(content)
    
    def get_text_content(self,soup):
        '''returns the text content of the whole page with some exception to tags. See tags_to_ignore.'''
        tags_to_ignore = ['style', 'script', 'head', 'title', 'meta', '[document]',"h1","h2","h3","h4","h5","h6","noscript"]
        tags = soup.find_all(text=True)
        result = []
        for tag in tags:
            stripped_tag = tag.strip()
            if tag.parent.name not in tags_to_ignore\
                and isinstance(tag, bs4.element.Comment)==False\
                and not stripped_tag.isnumeric()\
                and len(stripped_tag)>0:
                result.append(stripped_tag)
        return ' '.join(result)
    
    def extract_data(self, website_url):
        """
        Visits a URL and extracts text content and a preview image.
        Returns a dictionary containing 'text' and 'image_bytes' (or None).
        """
        try:
            content = requests.get(website_url, timeout=60).content
            soup = BeautifulSoup(content, "lxml")
            text = self._get_combined_text(soup)
            image_bytes = self._get_preview_image_bytes(soup, website_url)
            return {"text": text, "image_bytes": image_bytes}
        except requests.exceptions.RequestException as e:
            return {"error": f"Error fetching URL: {e}"}
        except Exception as e:
            return {"error": f"An unexpected error occurred during extraction: {e}"}

    def _get_preview_image_bytes(self, soup, website_url):
        """Attempts to find, download, and resize a preview image; returns bytes."""
        parsed_url = urlparse(website_url)
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

        # Look for og:image
        og_image = soup.find("meta", property="og:image")
        if og_image and og_image.get("content"):
            image_url = self._make_absolute_url(og_image["content"], base_url)
            return self._download_and_resize_image(image_url)

        # Look for favicon
        favicon = soup.find("link", rel="icon")
        if favicon and favicon.get("href"):
            image_url = self._make_absolute_url(favicon["href"], base_url)
            return self._download_and_resize_image(image_url)

        # Fallback to first reasonable image
        images = soup.find_all("img")
        for img in images:
            if img.get("src"):
                image_url = self._make_absolute_url(img["src"], base_url)
                image_bytes = self._download_and_resize_image(image_url)
                if image_bytes:  # Return the first successful one
                    return image_bytes
        return None

    def _download_and_resize_image(self, image_url):
        """Downloads and resizes an image; returns bytes or None."""
        try:
            response = requests.get(image_url, stream=True, timeout=10)
            response.raise_for_status()
            image = Image.open(BytesIO(response.content))
            image.thumbnail((200, 200))
            buffered = BytesIO()
            image.save(buffered, format="JPEG")
            return buffered.getvalue()
        except requests.exceptions.RequestException:
            return None
        except Exception:
            return None

    def _make_absolute_url(self, url, base_url):
        """Ensures a URL is absolute."""
        if not urlparse(url).netloc:
            return urljoin(base_url, url)
        return url

    def _get_combined_text(self, soup):
        """Extracts and combines relevant text content from the page."""
        title = soup.title.string if soup.title else ""
        metas = [meta.get('content', '') for meta in soup.find_all('meta', attrs={'name': ['description', 'keywords']})]
        headings = [h.get_text(strip=True) for h in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])]
        body_text_parts = [p.get_text(strip=True) for p in soup.find_all('p')]
        body_text = " ".join(body_text_parts)

        return f"{title}. {' '.join(metas)}. {' '.join(headings)}. {body_text}"