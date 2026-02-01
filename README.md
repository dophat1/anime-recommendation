# anime-recommendation
Find your next favourite anime that you will love 
<img width="800" height="450" alt="image" src="https://github.com/user-attachments/assets/df797346-3dd3-47c3-8f95-92f4b627d177" />

# Management summary
The goal of the project is recommending anime (Japanese Animation film) according to the favourite one of users with the help of machine learning algorithms.

The data was scraped from https://api.jikan.moe/v4/anime.

The data was scraped until: 16.12.2025

The data field consists of:

- title: Anime title
- score: the score given by the community
- scored_by: number of people who rates the anime
- rank: the rank of the anime in the whole list
- popularity: Popularity of anime (smaller number means higher popularity)
- members: The number of member of the website, who add the anime to their list
- favourites: The number of member of the website, who add the anime to their FAVOURITE list

## Models used
For the recommendation the project used 2 models:

- K-nearest neighbors
- Hierarchical clustering
## Program usage
Step 1: Run the cell, then prompt your favourite anime inside (If you have a list, please seperate them by comma).

Step 2: Choose the algorithm you want to use. The best is KNN for finding your favourite, it accepts a list of anime. Prompt 'k' for knn.

*Notes: Choose hierarchical clustering for a map of how close one is the closest to your favourite (note that it accepts only 1 anime). Prompt 'h' for hierarchical clustering. Or both if you want <3 

Step 3: Wait for the result and enjoy your next favorite anime !

# Overall:

Comedy is the most popular genre among all, so it is a good news if you are fond of hilarious stories.

Fantasy is the second popular genre.

The problem after watching such a good anime and desperately need for a new one that similar is largly solved by this model. Since there is no metrics to evaluate the goodness of the models for unsupervised ML model (from my knowledge only), I will give my personal opinion with experience that those recommendations are excellent.
