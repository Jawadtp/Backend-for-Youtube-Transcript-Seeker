import threading, time
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi

import os
from dotenv import load_dotenv

load_dotenv()


def search_video(id, searchTerm):
    result={}
    result['messages'] = []
    result['id'] = str(id)
    count = 0
    api_key = os.getenv('API_KEY')
    youtube_service = build('youtube', 'v3', developerKey = api_key)
    videoNameRequest = youtube_service.videos().list(
    part="snippet,contentDetails",id=id)
    videoDetails = videoNameRequest.execute()

    if ('error' in videoDetails.keys() or len(videoDetails.get('items')) == 0 ):
        result['messages'].append("\nInvalid Video ID")
        youtube_service.close()
        return result


    title = videoDetails['items'][0]['snippet']['title']
    result['titles'] = [(title, id)]
    result[title] = {}
    try:
        transcript = YouTubeTranscriptApi.get_transcript(id)
        result['messages'].append(f'Found transcript for video ->\n{title}\n')
    except:
        result['messages'].append("Transcripts are disabled for this video")
        youtube_service.close()
        return result

    for line  in transcript:
        if(searchTerm.lower() in line['text'].lower()):
            time = int(line['start'])
            hours = time//(60*60)
            minutes = (time//60)%60
            seconds = time%60
            result[title][str(time)] = (f"({hours:02d}:{minutes:02d}:{seconds:02d})", "-> \"...{line['text']}...\"\n")
            count += 1
    if count == 0 :
        result['messages'].append("No matches found :(")
    youtube_service.close()
    return result


def loadingAnimation(process) :
    while process.is_alive():
        chars = "/—\|"
        for char in chars:
            print('Fetching Transcripts '+char, end='\r', flush=True)
            time.sleep(.1)