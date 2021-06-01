import time, threading
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi

import os
from dotenv import load_dotenv

load_dotenv()



def search_playlist_1(id,searchTerm):
    result=[]
    api_key = os.getenv('API_KEY')
    nextPageToken = None
    youtube_service = build('youtube','v3',developerKey = api_key)

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
            
            videoNameRequest = youtube_service.videos().list(
            part="snippet",id=item['contentDetails']['videoId'])
            videoDetails = videoNameRequest.execute()

            if ('error' in videoDetails.keys() or len(videoDetails.get('items')) == 0 ):
                youtube_service.close()
                return result
            videoName = videoDetails['items'][0]['snippet']['title']
            try:
                transcripts[videoName] = YouTubeTranscriptApi.get_transcript(item['contentDetails']['videoId'])
                print(f'Found transcript for {videoName}')
                result.append(f'Found transcript for {videoName}')
            except:
                print(f'Transcript for video:"{videoName}" is disabled')
                result.append(f'Transcript for video:"{videoName}" is disabled')
                
        if not nextPageToken:
            break
            
    count = 0
    for title in transcripts:    
        for line  in transcripts[title]:
            if(searchTerm.lower() in line['text'].lower()):
                hours = int(line['start'])//(60*60)
                minutes = (int(line['start'])//60)%60
                seconds = int(line['start'])%60
             #   print(f"\n{title}\n({hours}:{minutes}:{seconds})-> \"...{line['text']}...\"")
                result.append(f"\n{title}\n({hours}:{minutes}:{seconds})-> \"...{line['text']}...\"")
                count += 1

    if count == 0 : 
        print("No matches found :(")
        result.append("No matches found :(")

    youtube_service.close()
    return result

def loadingAnimation(process) :
    while process.is_alive():
        chars = "/—\|" 
        for char in chars:
            print('Fetching Transcripts '+char, end='\r')
            time.sleep(.1)

def search_playlist(id,searchTerm):
        
    return search_playlist_1(id, searchTerm)