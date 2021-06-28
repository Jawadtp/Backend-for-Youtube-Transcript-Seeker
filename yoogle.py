import re
from video import search_video
from playlist import search_playlist

def parse(url):
    if 'list' in url:
        #parse for list
        exp = "list=([a-zA-Z0-9-_]+)&?"
        return re.findall(exp, url)[0], 1
    elif 'v=' in url:
        # parse for videoID
        if '&' in url:
            return url[url.find('v=')+2 : url.find('&')], 0
        else:
            return url[url.find('v=')+2:], 0
    elif '.be' in url:
        return url[url.find('.be')+4:], 0
    else:
        return None, None

def main(url,searchTerm = None):
    extracted_id, n = parse(url)
    if not extracted_id:
        return {'messages':  ['Invalid URL']}
    if n == 1:
        return search_playlist(extracted_id, searchTerm)
    else:
        return search_video(extracted_id, searchTerm)
