
import pandas as pd
from  .user_based import prepare_dataset
import numpy as np
#Class for Item similarity based Recommender System model
class user_similarity_recommender_py():
    def __init__(self):
        self.train_data = None
        self.user_id = None
        self.item_id = None
        self.cooccurence_matrix = None
        self.songs_dict = None
        self.rev_songs_dict = None
        self.item_similarity_recommendations = None

    #Get unique items (songs) corresponding to a given user
    def get_user_items(self, user):
        user_data = self.train_data[self.train_data[self.user_id] == user]
        user_items = list(user_data[self.item_id].unique())

        return user_items

    #Get unique users for a given item (song)
    def get_item_users(self, item):
        item_data = self.train_data[self.train_data[self.item_id] == item]
        item_users = set(item_data[self.user_id].unique())

        return item_users

    #Get unique items (songs) in the training data
    def get_all_items_train_data(self):
        all_items = list(self.train_data[self.item_id].unique())

        return all_items

    #Construct cooccurence matrix
    def construct_cooccurence_matrix(self, user_songs, all_songs):

        ####################################
        #Get users for all songs in user_songs.
        ####################################
        user_songs_users = []
        for i in range(0, len(user_songs)):
            user_songs_users.append(self.get_item_users(user_songs[i]))
        ###############################################
        #Initialize the item cooccurence matrix of size
        #len(user_songs) X len(songs)
        ###############################################
        cooccurence_matrix = np.matrix(np.zeros(shape=(len(user_songs), len(all_songs))), float)

        #############################################################
        #Calculate similarity between user songs and all unique songs
        #in the training data
        #############################################################
        for i in range(0,len(all_songs)):
            #Calculate unique listeners (users) of song (item) i
            songs_i_data = self.train_data[self.train_data[self.item_id] == all_songs[i]]
            users_i = set(songs_i_data[self.user_id].unique())

            for j in range(0,len(user_songs)):

                #Get unique listeners (users) of song (item) j
                users_j = user_songs_users[j]

                #Calculate intersection of listeners of songs i and j
                users_intersection = users_i.intersection(users_j)

                #Calculate cooccurence_matrix[i,j] as Jaccard Index
                if len(users_intersection) != 0:
                    #Calculate union of listeners of songs i and j
                    users_union = users_i.union(users_j)

                    cooccurence_matrix[j,i] = float(len(users_intersection))/float(len(users_union))
                else:
                    cooccurence_matrix[j,i] = 0


        return cooccurence_matrix


    #Use the cooccurence matrix to make top recommendations
    def generate_top_recommendations(self, user, cooccurence_matrix, all_songs, user_songs,recommendation_number):
        print("Non zero values in cooccurence_matrix :%d" % np.count_nonzero(cooccurence_matrix))

        #Calculate a weighted average of the scores in cooccurence matrix for all user songs.
        user_sim_scores = cooccurence_matrix.sum(axis=0)/float(cooccurence_matrix.shape[0])
        user_sim_scores = np.array(user_sim_scores)[0].tolist()

        #Sort the indices of user_sim_scores based upon their value
        #Also maintain the corresponding score
        sort_index = sorted(((e,i) for i,e in enumerate(list(user_sim_scores))), reverse=True)

        #Create a dataframe from the following
        columns = ['user_id', 'song', 'score', 'rank']
        #index = np.arange(1) # array of numbers for the number of samples
        df = pd.DataFrame(columns=columns)

        #Fill the dataframe with top 10 item based recommendations
        rank = 1
        for i in range(0,len(sort_index)):
            if ~np.isnan(sort_index[i][0]) and all_songs[sort_index[i][1]] not in user_songs and rank <= recommendation_number:
                df.loc[len(df)]=[user,all_songs[sort_index[i][1]],sort_index[i][0],rank]
                rank = rank+1

        #Handle the case where there are no recommendations
        if df.shape[0] == 0:
            print("The current user has no songs for training user similarity based recommendation model.")
            return -1
        else:
            return df

    #Create the item similarity based recommender system model
    def create(self, train_data, user_id, item_id):
        self.train_data = train_data
        self.user_id = user_id
        self.item_id = item_id

    #Use the item similarity based recommender system model to
    #make recommendations
    def recommend(self, user,recommendation_number):

        ########################################
        #A. Get all unique songs for this user
        ########################################
        user_songs = self.get_user_items(user)

        #print("No. of unique songs for the user: %d" % len(user_songs))

        ######################################################
        #B. Get all unique items (songs) in the training data
        ######################################################
        all_songs = self.get_all_items_train_data()

        #print("no. of unique songs in the training set: %d" % len(all_songs))

        ###############################################
        #C. Construct item cooccurence matrix of size
        #len(user_songs) X len(songs)
        ###############################################
        cooccurence_matrix = self.construct_cooccurence_matrix(user_songs, all_songs)

        #print(cooccurence_matrix.shape)

        #######################################################
        #D. Use the cooccurence matrix to make recommendations
        #######################################################
        df_recommendations = self.generate_top_recommendations(user, cooccurence_matrix, all_songs, user_songs,recommendation_number)

        return df_recommendations

    #Get similar items to given items
    def get_similar_items(self, item_list,recommendation_number):

        user_songs = item_list

        ######################################################
        #B. Get all unique items (songs) in the training data
        ######################################################
        all_songs = self.get_all_items_train_data()

        print("no. of unique songs in the training set: %d" % len(all_songs))

        ###############################################
        #C. Construct item cooccurence matrix of size
        #len(user_songs) X len(songs)
        ###############################################
        cooccurence_matrix = self.construct_cooccurence_matrix(user_songs, all_songs)

        #######################################################
        #D. Use the cooccurence matrix to make recommendations
        #######################################################
        user = ""
        df_recommendations = self.generate_top_recommendations(user, cooccurence_matrix, all_songs, user_songs,recommendation_number)

        return df_recommendations
    

def create_popularity_recommendation(train_data,recommendation_number):
    train_data_grouped = train_data.groupby(['music_id']).agg({'listener_id': 'count'}).reset_index()
    train_data_grouped.rename(columns={'listener_id': 'score'}, inplace=True)
    train_data_sort = train_data_grouped.sort_values(['score', 'music_id'], ascending=[0, 1])
    train_data_sort['Rank'] = train_data_sort.score.rank(ascending=0, method='first')
    popularity_recommendations = train_data_sort.head(recommendation_number)


    return popularity_recommendations['music_id'].tolist()    

def user_based_recommendation(user_id,recommendation_number):
    is_model =user_similarity_recommender_py()
    #print("çalışıyor msun")
    user_song_list=prepare_dataset()
    #print("çalışıyor msun 2")
    is_model.create(user_song_list, 'user', 'title')
    #print("çalışıyor msun 3")
    result=is_model.recommend(user_id,recommendation_number)
    print(result)
    result_filtered = result[['song', 'user_id']]
    return result_filtered