# Source to Schema Mapping

## Movies Domain (TMDB Dataset)

Source Files:

* movies_metadata.csv
* keywords.csv
* credits.csv
* ratings.csv

---

# dim_items

Source: movies_metadata.csv

| Target Column         | Source Column         |
| --------------------- | --------------------- |
| source_item_id        | id                    |
| title                 | title                 |
| description           | overview              |
| release_date          | release_date          |
| runtime               | runtime               |
| language              | original_language     |
| popularity            | popularity            |
| vote_average          | vote_average          |
| vote_count            | vote_count            |
| belongs_to_collection | belongs_to_collection |
| production_companies  | production_companies  |
| production_countries  | production_countries  |
| budget                | budget                |
| revenue               | revenue               |
| poster_path           | poster_path           |
| domain                | constant = "movie"    |

Generated:

| Target Column | Logic                          |
| ------------- | ------------------------------ |
| item_id       | System-generated surrogate key |

---

# dim_users

Source: ratings.csv

| Target Column | Source Column |
| ------------- | ------------- |
| user_id       | userId        |

Transformation:

* Remove duplicates
* One record per unique user

---

# fact_interactions

Source: ratings.csv

| Target Column | Source Column        |
| ------------- | -------------------- |
| user_id       | userId               |
| rating        | rating               |
| timestamp     | timestamp            |
| item_id       | Lookup from item_map |

Transformation:

* Join ratings.movieId → links.movieId
* Resolve TMDB ID
* Join TMDB ID → item_map
* Replace source identifiers with item_id

---

# item_genres

Source: movies_metadata.csv

| Target Column | Source Column        |
| ------------- | -------------------- |
| item_id       | Lookup from item_map |
| genre         | genres.name          |

Transformation:

* Parse JSON-like genres field
* Explode into one row per genre

Example:

Movie:
Action, Adventure, Sci-Fi

Produces:

(item_id, Action)
(item_id, Adventure)
(item_id, Sci-Fi)

---

# item_keywords

Source: keywords.csv

| Target Column | Source Column        |
| ------------- | -------------------- |
| item_id       | Lookup from item_map |
| keyword       | keywords.name        |

Transformation:

* Parse keywords list
* Explode into one row per keyword

---

# item_cast

Source: credits.csv

| Target Column | Source Column        |
| ------------- | -------------------- |
| item_id       | Lookup from item_map |
| actor         | cast.name            |

Transformation:

* Parse cast list
* Explode into one row per actor

---

# item_directors

Source: credits.csv

| Target Column | Source Column                  |
| ------------- | ------------------------------ |
| item_id       | Lookup from item_map           |
| director      | crew.name where job='Director' |

Transformation:

* Parse crew list
* Filter Director records only
* Explode into one row per director

---

# item_map

Generated Table

Purpose:

Maps source identifiers to internal identifiers.

| Column         | Description                |
| -------------- | -------------------------- |
| item_id        | Internal system identifier |
| source_item_id | TMDB movie identifier      |
| domain         | movie                      |

Example:

| item_id | source_item_id | domain |
| ------- | -------------- | ------ |
| 1       | 862            | movie  |
| 2       | 8844           | movie  |
| 3       | 15602          | movie  |

---

# Data Quality Rules

Movies Metadata

* Remove invalid IDs
* Remove duplicate source_item_id values
* Fill missing overview with empty string
* Fill missing collection with empty string

Keywords

* Remove duplicate IDs
* Keep only records present in dim_items

Credits

* Remove duplicate IDs
* Keep only records present in dim_items

Ratings

* Keep only ratings that map to valid item_id values
* Preserve original ratings and timestamps

---

# Final Output Tables

data/processed/movies/

* dim_items.parquet
* dim_users.parquet
* fact_interactions.parquet
* item_genres.parquet
* item_keywords.parquet
* item_cast.parquet
* item_directors.parquet
