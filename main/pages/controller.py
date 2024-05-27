from googleapiclient.discovery import build
import pandas as pd

"""benim_api_key = 'AIzaSyCXMRgjhpkL_pShQTuj3AsQN8_QwqWADQk'"""
api_key='AIzaSyCWlmmXqgrPLGIRimpMHT62Mxr7fqO-l04'
youtube = build('youtube', 'v3', developerKey=api_key)

def get_id(search_query):
    try:
        #print("sen buraya giriyor musun",search_query)
        search_response = youtube.search().list(
        q=search_query,
        part='id',
        maxResults=1,
        type='video'
        ).execute()

        #print("response",search_response)
        video_id = search_response['items'][0]['id']['videoId']
        #print("sonuç",video_id)
        return video_id
    except Exception as e:
        #print("Hata Mesajı:", e)
        return None