import re
from video import search_video
from playlist import search_playlist

def parse(url):
    if url.find('list') != -1:
        #parse for list
        exp = "list=([a-zA-Z0-9-_]+)&?"
        return re.findall(exp,url)[0],1
    elif url.find('v=') != -1:
        # parse for videoID
        if url.find('&') != -1:
            return url[url.find('v=')+2:url.find('&')+1],0
        else:
            return url[url.find('v=')+2:],0        
    elif '.be' in url:
        return url[url.find('.be')+4:],0
    else:
        return None,None

def main(url,searchTerm = None):
    print('\n################ Yoogle ###################')
    extracted_id,n = parse(url)
    if not extracted_id: 
        print("Invalid URL")
        return ['Invalid URL']
    if n == 1:
        return search_playlist(extracted_id,searchTerm)
    else:
        return search_video(extracted_id,searchTerm)

'''
url = input("Paste the url: ")
searchTerm = input("Word/Sentence to be searched: ")
main(url,searchTerm)    
'''