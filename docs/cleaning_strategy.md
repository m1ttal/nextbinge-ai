# Multi-Domain Recommendation System - Cleaning Strategy

## Purpose

This document defines the data cleaning and preprocessing rules for the Movie domain datasets before loading them into the unified recommendation schema.

The objective is to ensure:

* Data quality
* Consistent identifiers
* Reliable recommendation inputs
* Future compatibility with Anime and TV Show datasets

---

# Cleaning Principles

The following principles apply to all datasets:

1. Preserve original identifiers whenever possible.
2. Remove duplicate records that create ambiguity.
3. Standardize data types.
4. Retain only columns required for recommendation, analytics, or dashboarding.
5. Store missing values as NULL/NaN rather than using placeholder values.
6. Generate item_id only after successful dataset integration.

---

# DATASET 1: users_ml

Target Table:

dim_users

## Cleaning Rules

### Remove Duplicates

* Verify userId uniqueness.
* Remove duplicate user records if found.

### Data Type Validation

| Column     | Expected Type |
| ---------- | ------------- |
| userId     | Integer       |
| gender     | String        |
| age        | Integer       |
| occupation | Integer       |
| zipCode    | String        |

### Missing Values

* Check all columns for missing values.
* Investigate missing userId records.
* Preserve rows unless userId is missing.

### Standardization

* Trim whitespace.
* Standardize gender values if required.

---

# DATASET 2: ratings_ml

Target Table:

fact_interactions

## Cleaning Rules

### Remove Duplicates

Check for duplicate combinations:

(userId, movieId)

If duplicates exist:

* Keep the most recent rating based on timestamp.
* Document the number of removed records.

### Data Type Validation

| Column    | Expected Type |
| --------- | ------------- |
| userId    | Integer       |
| movieId   | Integer       |
| rating    | Float         |
| timestamp | Integer       |

### Rating Validation

Ensure ratings fall within the expected range.

Example:

0.5 – 5.0

Remove invalid ratings if found.

### Timestamp Handling

Convert timestamps into datetime format during preprocessing if required.

---

# DATASET 3: movies_ml

Target Table:

dim_items
item_genres

## Cleaning Rules

### Remove Duplicates

Verify movieId uniqueness.

### Title Standardization

* Trim whitespace.
* Preserve original title formatting.

### Genre Processing

MovieLens stores genres as:

Action|Adventure|Sci-Fi

Split into individual genres.

Generate records for:

item_genres

Example:

| item_id | genre     |
| ------- | --------- |
| 1       | Action    |
| 1       | Adventure |
| 1       | Sci-Fi    |

### Unknown Genres

Handle:

(no genres listed)

as NULL or a designated Unknown category.

---

# DATASET 4: links

Purpose:

MovieLens ↔ TMDB Integration

## Cleaning Rules

### Data Type Validation

| Column  | Expected Type |
| ------- | ------------- |
| movieId | Integer       |
| imdbId  | Integer       |
| tmdbId  | Integer       |

### Missing Values

Investigate:

* Missing tmdbId
* Missing imdbId

### Duplicate Validation

Check:

movieId uniqueness

Check:

tmdbId uniqueness

Document any conflicts before integration.

### Integration Validation

Verify:

movieId exists in movies_ml

before integration.

---

# DATASET 5: movies_metadata

Target Table:

dim_items

## Cleaning Rules

### Remove Corrupted Records

Remove records where:

id is not numeric

### Remove Duplicate TMDB IDs

Keep a single record per tmdb_id.

Document removed records.

### Data Type Conversion

Convert:

| Column       |
| ------------ |
| budget       |
| revenue      |
| popularity   |
| runtime      |
| vote_average |
| vote_count   |

to numeric formats.

### Date Conversion

Convert:

release_date

to datetime.

### Missing Values

Assess missing values for:

* overview
* runtime
* release_date
* language

Preserve rows where possible.

### Column Retention

Retain only columns mapped to the schema.

---

# DATASET 6: Keywords

Target Table:

item_keywords

## Cleaning Rules

### Remove Duplicate Records

Verify:

tmdb_id uniqueness

before expansion.

### Parse Keyword Structures

Convert JSON-like arrays into rows.

Example:

[
{"id": 931, "name": "jealousy"},
{"id": 4290, "name": "toy"}
]

becomes:

| item_id | keyword  |
| ------- | -------- |
| 1       | jealousy |
| 1       | toy      |

### Standardization

* Convert keywords to lowercase.
* Trim whitespace.
* Remove empty keywords.

---

# DATASET 7: Credits

Target Table:

item_people

## Cleaning Rules

### Remove Duplicate Records

Verify:

tmdb_id uniqueness

before expansion.

### Parse Cast

Extract:

* Actor Name

### Parse Crew

Extract:

* Director
* Writer (optional)
* Producer (optional)

### Standardization

* Trim whitespace.
* Remove empty names.

### Role Filtering

Retain only roles useful for recommendation.

Recommended:

* Actor
* Director

---

# Integration Validation

Before creating dim_items:

Validate:

movies_ml
↔ links
↔ movies_metadata

using:

movieId
and
tmdbId

Checks:

1. Every movieId maps correctly.
2. Every tmdbId joins correctly.
3. No duplicate item mappings exist.
4. No orphaned records remain after integration.

---

# item_id Generation Strategy

item_id is generated only after:

1. Cleaning is complete.
2. Integration is complete.
3. dim_items is finalized.

Rules:

* item_id must be unique.
* item_id must remain stable across future processing runs.
* item_id becomes the canonical identifier used throughout the recommendation system.

---

# Output Tables

After cleaning and integration:

* dim_users
* dim_items
* fact_interactions
* item_genres
* item_keywords
* item_people

These tables become the foundation for:

* Collaborative Filtering
* Content-Based Filtering
* Hybrid Recommendation
* Cross-Domain Recommendation

