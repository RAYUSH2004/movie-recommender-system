import pandas as pd

# Load the dataset
csv_file = "movies_tmdb.csv"  # Ensure this is the correct path
tmdb_df = pd.read_csv(csv_file)

# Rename columns to match expected names
tmdb_df.rename(columns={"tmdb_id": "id", "poster": "poster_path"}, inplace=True)

# Ensure ID is treated as a string for matching
tmdb_df["id"] = tmdb_df["id"].astype(str)

# Function to get poster path
def get_poster_path(tmdb_id):
    movie = tmdb_df[tmdb_df["id"] == str(tmdb_id)]
    if movie.empty:
        print(f"No movie found with TMDb ID: {tmdb_id}")
        return None
    return movie["poster_path"].values[0]

# Fetch poster function
def fetch_poster(tmdb_id):
    poster_path = get_poster_path(tmdb_id)
    if poster_path:
        return poster_path  # If poster_path is a complete URL, return it
    else:
        return "Poster not available"
