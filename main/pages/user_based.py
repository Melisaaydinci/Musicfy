from listening.models import MusicListening
from music.models import Music
import pandas as pd

def prepare_dataset():
 
    musics_df = pd.DataFrame(list(Music.objects.values()))
    listenings_df = pd.DataFrame(list(MusicListening.objects.values()))
    merged_df = pd.merge(listenings_df,musics_df,left_on='music_id', right_on='id', how='inner')
    print(merged_df)
    merged_df.drop(['id_x', 'id_y','youtube_id'], axis=1, inplace=True)
    merged_df = merged_df.rename(columns={'listener_id': 'user', 'music_id': 'song','listen_count':'play_count'})
    print(merged_df.head())
    return merged_df
 

