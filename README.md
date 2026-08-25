
# Anime Recommendation
<img width="800" height="450" alt="image" src="https://github.com/user-attachments/assets/df797346-3dd3-47c3-8f95-92f4b627d177" />
A content-based anime recommender: pick your favorite title(s) and get back visually/thematically similar anime, using genre and popularity features rather than user ratings (no collaborative filtering data available).

## Data

`scrape.py` pulls anime metadata from the [Jikan API](https://jikan.moe/) (an unofficial MyAnimeList API) — title, score, scored_by, rank, popularity, members, favorites, and genres — with retry logic and exponential backoff on rate limits (HTTP 429). Output goes to `output/anime_list_<timestamp>.{csv,json}`. A dataset is already included in `output/` so the notebook runs without re-scraping.

## Approach

`Anime Recommend.ipynb`:

1. **Cleaning** — fill missing genres/scores/members, basic EDA (score distribution, top-20 genre frequency).
2. **Feature engineering** — TF-IDF vectorize the genre string per title, scale numerical features (score, members), then combine them with `scipy.sparse.hstack`. Genres are weighted 2x relative to the numerical features, since genre similarity matters more than popularity for "is this anime like that one."
3. **Recommendation, two ways:**
   - `get_recommendations_multi(titles, n)` — k-nearest-neighbors (cosine distance) on the combined feature matrix. Supports multiple input titles by averaging their feature vectors first, so you can ask "something like both X and Y."
   - `draw_neighborhood_dendrogram(title, n)` — agglomerative hierarchical clustering on a title's nearest neighbors, plotted as a dendrogram, to see the similarity *structure* around a title rather than just a flat top-N list.
4. An interactive cell at the end lets you type favorite titles and pick which of the two approaches to use.

## Tech stack

Python, `requests`, pandas, NumPy, scikit-learn (`TfidfVectorizer`, `NearestNeighbors`, `AgglomerativeClustering`), SciPy (sparse matrices, hierarchical clustering), matplotlib/seaborn.

## Running it

```bash
git clone <this repo>
cd Anime_Recommendation

python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt

python scrape.py # Fetch data from the free Jikan API

jupyter notebook "Anime Recommend.ipynb" # For your analyzing and recommendations.
```

Run the cells top to bottom; the last cell prompts for your favorite anime titles and which algorithm to use.

To scrape a fresh dataset instead of using the included one: `python scrape.py` (takes a while — it's rate-limited and paginated against the live Jikan API).

## Limitations 

- Purely content-based on genre + popularity metadata — no synopsis/plot text, no user rating history, so it can't capture "similar vibe, different genre tags."
- No formal evaluation of recommendation quality (no held-out relevance judgments) — recommendations are only as good as genre-overlap intuition suggests, not validated against a metric.
- Genre input titles are case-sensitive exact matches against the dataset.

### Next steps

- Predict based on the similarities of the content of the film as well with NLP, not only genres and quantitative value. 
- Capture user rating history as part of predictions.

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

