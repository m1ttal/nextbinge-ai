# Multi-Domain Recommendation System - Schema Design

## Overview

This project uses a unified schema across multiple domains:

* Movies
* Anime
* TV Shows

Each domain is transformed into a common data model before recommendation algorithms are applied.

---

# Core Tables

## dim_items

Master table containing item-level information.

| Column                | Data Type | Description                                                 |
| --------------------- | --------- | ----------------------------------------------------------- |
| item_id               | Integer   | Internal unique item identifier                             |
| source_item_id        | String    | Original source identifier (TMDB ID, Anime ID, TV ID, etc.) |
| domain                | String    | movie / anime / tv                                          |
| title                 | String    | Item title                                                  |
| description              | String    | Item description or synopsis                                |
| release_date          | Date      | Release date                                                |
| runtime               | Float     | Duration in minutes                                         |
| language     | String    | Original language                                           |
| popularity            | Float     | Popularity score from source                                |
| vote_average          | Float     | Average rating                                              |
| vote_count            | Integer   | Number of votes                                             |
| belongs_to_collection | String    | Franchise or collection name                                |
| production_companies  | String    | Production companies                                        |
| production_countries  | String    | Production countries                                        |
| budget                | Float     | Budget amount                                               |
| revenue               | Float     | Revenue amount                                              |
| poster_path           | String    | Poster image path                                           |

Primary Key:

* item_id

---

## dim_users

Master user table.

| Column  | Data Type | Description              |
| ------- | --------- | ------------------------ |
| user_id | Integer   | Internal user identifier |

Primary Key:

* user_id

---

# Interaction Tables

## fact_interactions

Stores user-item interactions.

| Column    | Data Type | Description              |
| --------- | --------- | ------------------------ |
| user_id   | Integer   | User identifier          |
| item_id   | Integer   | Internal item identifier |
| rating    | Float     | User rating              |
| timestamp | Integer   | Interaction timestamp    |

Primary Key:

* (user_id, item_id)

Foreign Keys:

* user_id → dim_users.user_id
* item_id → dim_items.item_id

---

# Metadata Tables

## item_genres

Stores item-to-genre relationships.

| Column  | Data Type | Description              |
| ------- | --------- | ------------------------ |
| item_id | Integer   | Internal item identifier |
| genre   | String    | Genre name               |

Examples:

* Action
* Comedy
* Drama
* Fantasy

Foreign Key:

* item_id → dim_items.item_id

---

## item_keywords

Stores item keywords/tags.

| Column  | Data Type | Description              |
| ------- | --------- | ------------------------ |
| item_id | Integer   | Internal item identifier |
| keyword | String    | Keyword/tag              |

Examples:

* space travel
* friendship
* detective

Foreign Key:

* item_id → dim_items.item_id

---

## item_cast

Stores cast information.

| Column  | Data Type | Description              |
| ------- | --------- | ------------------------ |
| item_id | Integer   | Internal item identifier |
| actor   | String    | Actor name               |

Examples:

* Tom Hanks
* Leonardo DiCaprio

Foreign Key:

* item_id → dim_items.item_id

---

## item_directors

Stores director information.

| Column   | Data Type | Description              |
| -------- | --------- | ------------------------ |
| item_id  | Integer   | Internal item identifier |
| director | String    | Director name            |

Examples:

* Steven Spielberg
* Christopher Nolan

Foreign Key:

* item_id → dim_items.item_id

---

# Identifier Strategy

## item_id

System-generated identifier.

Purpose:

* Internal joins
* Model training
* Cross-domain integration

Examples:

| item_id | domain |
| ------- | ------ |
| 1       | movie  |
| 2       | movie  |
| 50001   | anime  |
| 100001  | tv     |

---

## source_item_id

Original identifier from source datasets.

Examples:

| domain | source_item_id |
| ------ | -------------- |
| movie  | TMDB ID        |
| anime  | Anime ID       |
| tv     | TV Show ID     |

Purpose:

* Traceability
* Data refresh
* Source reconciliation

---

# Recommendation Features

Content-Based Features:

* title
* description
* genres
* keywords
* cast
* directors
* collection

Collaborative Features:

* ratings
* user interactions

Popularity Features:

* vote_average
* vote_count
* popularity

Dashboard Features:

* title
* release_date
* runtime
* popularity
* budget
* revenue
* vote_average
* vote_count
* poster_path

---

# Storage Format

Processed datasets are stored in Parquet format.

Directory Structure:

data/
├── processed/
│   ├── movies/
│   ├── anime/
│   └── tv/
