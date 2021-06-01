import threading,time
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi

import os
from dotenv import load_dotenv

load_dotenv()


def search_video_1(id,searchTerm):
    result=[]
    count = 0
    api_key = os.getenv('API_KEY')
    youtube_service = build('youtube','v3',developerKey = api_key)
    videoNameRequest = youtube_service.videos().list(
    part="snippet,contentDetails",id=id)
    videoDetails = videoNameRequest.execute()
    
    if ('error' in videoDetails.keys() or len(videoDetails.get('items')) == 0 ):
        print("Invalid video ID")
        result.append("\nInvalid Video ID")
        youtube_service.close()
        return result
    

    title = videoDetails['items'][0]['snippet']['title']
    try:
        transcript = YouTubeTranscriptApi.get_transcript(id)
        print(f'Found transcript for video ->\n{title}\n')
        result.append(f'Found transcript for video ->\n{title}\n')
    except:
        print("Transcripts are disabled for this video")
        result.append("Transcripts are disabled for this video")
        youtube_service.close()
        return result

    for line  in transcript:
            if(searchTerm.lower() in line['text'].lower()):
                hours = int(line['start'])//(60*60)
                minutes = (int(line['start'])//60)%60
                seconds = int(line['start'])%60
           #     print(f"({hours}:{minutes}:{seconds})-> \"...{line['text']}...\"\n")
                result.append(f"({hours}:{minutes}:{seconds})-> \"...{line['text']}...\"\n")
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
            print('Fetching Transcripts '+char, end='\r',flush=True)
            time.sleep(.1)
            

def search_video(id,searchTerm):
    '''
    loading_process = threading.Thread(target=search_video_1, args=(id,searchTerm))
    loading_process.start()

    loadingAnimation(loading_process)
    loading_process.join()
    '''
    return search_video_1(id,searchTerm)