"""Generate URL Preview

Title and Limited URL Content
"""
import os
import requests
import bs4

USERAGENT = os.getenv("USERAGENT", "Admins User Agent - Never Gonna Give You Up, Never Gonna Let You Down")

class InvalidUrlError(Exception):
    """Raise if fetching url fails."""
    pass

class FailedToGetPreviewError(Exception):
    """Raise if parsing url fails."""
    pass

blacklist = [
	'[document]',
	'noscript',
	'header',
	'html',
	'meta',
	'head', 
	'input',
	'script',
    'style',
    'table',
	# there may be more elements you don't want, such as "style", etc.
]

PREVIEW_LIMIT = 500

def get_preview(url: str) -> dict:
    """Get the preview of a url as dict with title and content string.
    Raise InvalidUrlError if fetching url fails.

    Arguments
    ---------
    url: str
        URL to get preview for
    
    Returns
    -------
    dict
        keys title and content for url preview
    """
    try:
        resp = requests.get(
            url,
            headers = {
                "User-Agent": USERAGENT
            }
        )
    except:
        raise InvalidUrlError()

    try:
        json_data = resp.json()
        return {
            "title": url,
            "text": str(json_data)
        }
    except:
        pass

    try:
        html = bs4.BeautifulSoup(resp.text, "lxml")
            
        page_text = ""

        for t in html.find_all(text=True):
            if t.parent.name not in blacklist:
                page_text += '{} '.format(t.strip())

        page_text = page_text[:PREVIEW_LIMIT]
        
        return {
            "title": html.title.text,
            "text": page_text
        }
    except:
        raise FailedToGetPreviewError()

        
