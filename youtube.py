
# Test Case 1: https://www.youtube.com/watch?v=WPjsDVS_trI

# import sys
# import json
# import datetime

import re
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi

def playlist(id,searchTerm):

    result=[]
    api_key = 'YOUR-API-KEY-HERE'
    nextPageToken = None
    youtube_service = build('youtube','v3',developerKey = api_key)
    
    # js = json.dumps(playlistResult,indent = 4) 
    # print(js)

    # List of transcripts
    transcripts = dict()

    while True:

        playlistItemsRequest = youtube_service.playlistItems().list(part='contentDetails',
        playlistId=id,
        maxResults = 50,
        pageToken = nextPageToken)
        playlistResult = playlistItemsRequest.execute()
        
        nextPageToken = playlistResult.get('nextPageToken')

        for item in playlistResult['items']:
            # print(item['id'])
        
            # print(item['contentDetails']['videoId'])
            videoNameRequest = youtube_service.videos().list(
            part="snippet",id=item['contentDetails']['videoId'])
            videoDetails = videoNameRequest.execute()
            videoName = videoDetails['items'][0]['snippet']['title']
            try:
                transcripts[videoName] = YouTubeTranscriptApi.get_transcript(item['contentDetails']['videoId'])
            except:
                print(f'\nTranscript for video:"{videoName}" is disabled\n')
                pass
        if not nextPageToken:
            break
            
        

    #for title in transcripts: print(title)
    
    for title in transcripts:    
        for line  in transcripts[title]:
            if(searchTerm in line['text']):
                hours = int(line['start'])//(60*60)
                minutes = (int(line['start'])//60)%60
                seconds = int(line['start'])%60
                x=f"{title}\n({hours}:{minutes}:{seconds})-> \"...{line['text']}...\""
                result.append(x)
             #   print(f"{title}\n({hours}:{minutes}:{seconds})-> \"...{line['text']}...\"")
    youtube_service.close()
    return result

def video(id,searchTerm):
    
    count = 0
    result=[]
    api_key = 'AIzaSyAHHa0_Bdkydw53FaUj5jG5oKQVkkCa_m8'
    youtube_service = build('youtube','v3',developerKey = api_key)
    videoNameRequest = youtube_service.videos().list(
    part="snippet,contentDetails",id=id)
    videoDetails = videoNameRequest.execute()
    title = videoDetails['items'][0]['snippet']['title']
    try:
        transcript = YouTubeTranscriptApi.get_transcript(id)
        print(f'Found transcript for video ->\n{title}\n')
    except:
        print("Transcripts disabled for this video")
    for line  in transcript:
            if(searchTerm in line['text']):
                hours = int(line['start'])//(60*60)
                minutes = (int(line['start'])//60)%60
                seconds = int(line['start'])%60
                temp = f"({hours}:{minutes}:{seconds})-> \"...{line['text']}...\"\n"
             #   print(f"({hours}:{minutes}:{seconds})-> \"...{line['text']}...\"\n")
                result.append(temp)
                count += 1
    if count == 0 : print("No matches found :(\n")
    youtube_service.close()
    return result

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
        return url[url.find('.be')+3:],0
    else:
        return None,None

def main(url,searchTerm = None):
    print('\n################ Yoogle ###################')

    result = []
    extracted_id,n = parse(url)
    if not extracted_id: 
        print("Invalid URL")
        return None
    if n == 1:
        result=playlist(extracted_id,searchTerm)
    else:
        result=video(extracted_id,searchTerm)
    return result

'''
url = input("Paste the url: ")
searchTerm = input("Word/Sentence to be searched: ")
main(url,searchTerm)    
'''




