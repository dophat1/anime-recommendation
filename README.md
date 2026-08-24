# Anime Recommendation

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

jupyter notebook "Anime Recommend.ipynb"
```

Run the cells top to bottom; the last cell prompts for your favorite anime titles and which algorithm to use.

To scrape a fresh dataset instead of using the included one: `python scrape.py` (takes a while — it's rate-limited and paginated against the live Jikan API).

## Limitations / next steps

- Purely content-based on genre + popularity metadata — no synopsis/plot text, no user rating history, so it can't capture "similar vibe, different genre tags."
- No formal evaluation of recommendation quality (no held-out relevance judgments) — recommendations are only as good as genre-overlap intuition suggests, not validated against a metric.
- Genre input titles are case-sensitive exact matches against the dataset.
