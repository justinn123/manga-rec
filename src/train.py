import os
import pandas as pd
from surprise import Dataset, Reader
from surprise.model_selection import train_test_split
from surprise import KNNBasic, accuracy


# path to dataset file

df = pd.read_csv('../data/updated_manga_data.csv', encoding = 'Latin-1')

df_exploded = df.assign(Genres=df['Genres'].str.split(', ')).explode('Genres')

df_surprise = df_exploded[['Genres', 'Title', 'Rating']]

df_surprise = df_surprise.rename(columns={'Genres': 'user_id', 'Title': 'item_id', 'Rating': 'rating'})

reader = Reader(rating_scale=(1, 10))

data = Dataset.load_from_df(df_surprise[['user_id', 'item_id', 'rating']], reader)

trainset, testset = train_test_split(data, test_size=0.25)

# Use an item-based collaborative filtering algorithm
algo = KNNBasic(sim_options={'user_based': False})  # Set user_based to False for item-based

# Train the algorithm on the training set
algo.fit(trainset)

# Get the inner id of the item (manga) you are interested in
item_inner_id = algo.trainset.to_inner_iid('One Piece')  # Replace 'Manga1' with the title you're interested in

# Find the k nearest neighbors (k similar manga titles)
k = 5  # Number of recommendations
neighbors = algo.get_neighbors(item_inner_id, k=k)

# Convert inner ids back to raw ids (titles) to get the recommendations
recommended_titles = [algo.trainset.to_raw_iid(inner_id) for inner_id in neighbors]

print("Recommended Manga Titles:")
for title in recommended_titles:
    print(title)
