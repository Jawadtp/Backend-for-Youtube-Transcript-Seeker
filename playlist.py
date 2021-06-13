from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi

import os
from dotenv import load_dotenv

load_dotenv()

def search_playlist(id, searchTerm):
    result={}
    result['messages'] = []
    result['titles'] = []
    api_key = os.getenv('API_KEY')
    nextPageToken = None
    youtube_service = build('youtube', 'v3', developerKey = api_key)

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
                break
            videoName = videoDetails['items'][0]['snippet']['title']
            try:
                transcripts[videoName] = YouTubeTranscriptApi.get_transcript(item['contentDetails']['videoId'])
                result['messages'].append(f'Found transcript for {videoName}')
                result['titles'].append((videoName, videoDetails['items'][0]['id']))
            except:
                result['messages'].append(f'Transcript for video:"{videoName}" is disabled')

        if not nextPageToken:
            break

    count = 0
    for title in transcripts.keys():
        result[title] = {}
        for line  in transcripts[title]:
            if(searchTerm.lower() in line['text'].lower()):
                time = int(line['start'])
                hours = time//(60*60)
                minutes = (time//60)%60
                seconds = time%60
                result[title][str(time)] = (f"({hours:02d}:{minutes:02d}:{seconds:02d})", f"-> \"...{line['text']}...\"\n")
                count += 1

    if count == 0 :
        result['messages'].append("No matches found :(")

    youtube_service.close()
    return result