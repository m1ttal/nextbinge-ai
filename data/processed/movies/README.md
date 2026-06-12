We have three datasets:

First dataset is Movies dataset which has seven files

movies_metadata
credits
keywords
links
links_small
ratings
ratings_small

and we will use:

movies_metadata
credits
keywords
links
ratings

Second dataset is Anime, it has six files

anime-dataset-2023
users-details-2023
users-score-2023
anime-filtered
user-filtered
final_animedataset

and we will use:

anime-dataset-2023
users-details-2023
users-score-2023

last dataset is TVshows, contains

TMDB_tv_dataset_v3


=================================================================

Recommendation Pipeline

Uses:

source_item_id
title
overview
genres
belongs_to_collection
production_companies
production_countries
vote_average
vote_count


Dashboard

Uses:

title
release_date
runtime
language
popularity
budget
revenue
vote_average
vote_count
poster_path
genres


movies_metadata.csv
-------------------
Original rows: 45,466

Cleaning performed:
- Selected 16 required columns
- Removed 3 invalid TMDB IDs
- Removed 30 duplicate TMDB IDs
- Filled missing overview with ""
- Filled missing belongs_to_collection with ""
- Converted:
    - id -> int
    - popularity -> numeric
    - budget -> numeric
    - release_date -> datetime
- Dropped 3 rows with missing title
- Filled small missing values:
    - language -> "unknown"
    - popularity -> 0
    - vote_average -> 0
    - vote_count -> 0
    - revenue -> 0
    - production_companies -> ""
    - production_countries -> ""
- Added domain = "movie"

Final rows: 45,430


Dataset: Movies (movies_metadata)
--------------------------------------------

Step 1: Dataset Structure

Displayed dataset information:

movies_metadata.info()

Result:

Rows    : 45,466
Columns : 24

Key Columns:

adult
belongs_to_collection
budget
genres
homepage
id
imdb_id
original_language
original_title
overview
popularity
poster_path
production_companies
production_countries
release_date
revenue
runtime
spoken_languages
status
tagline
title
video
vote_average
vote_count

Observation:

The dataset contains 45,466 records and 24 columns.
Several columns contain missing values.
Missing values are especially common in:
belongs_to_collection
homepage
tagline
overview
poster_path
runtime
Most columns are stored as strings.
revenue, runtime, vote_average, and vote_count are numeric.
The dataset occupies approximately 8.3 MB of memory.

Important Observation:

id is stored as a string (str) rather than an integer.
budget is stored as a string (str) rather than a numeric type.
popularity is stored as a string (str) rather than a numeric type.

These columns may require datatype validation during the data cleaning phase.

Conclusion:

movies_metadata is a content-rich movie dataset containing
movie descriptions, genres, popularity metrics, release information,
and production details.

The dataset contains several missing values and potential datatype issues
that will need to be addressed during cleaning.

-------------------------------------------------------------

Step 2: Understand Dataset Content (Modeling Columns)

Displayed the key columns that are expected to be used for recommendation modeling:

movies_metadata[
    [
        "id",
        "title",
        "genres",
        "overview",
        "vote_average",
        "vote_count",
        "release_date",
        "original_language"
    ]
].head()

Columns Examined:

id
title
genres
overview
vote_average
vote_count
release_date
original_language

Observation:

id represents the TMDB movie identifier.
title contains the movie name.
genres contains genre information for the movie.
overview contains the movie synopsis or description.
vote_average contains the average community rating.
vote_count contains the total number of ratings received.
release_date contains the movie release date.
original_language contains the original language code of the movie.

Example Record:

Movie              : Toy Story
TMDB ID            : 862
Genres             : Animation, Comedy, Family
Vote Average       : 7.7
Vote Count         : 5415
Release Date       : 1995-10-30
Original Language  : en

Important Observations:

Genres are not stored as simple text values.

Instead, they are stored as a string representation
of a list of dictionaries.

Example:

[{'id': 16, 'name': 'Animation'},
 {'id': 35, 'name': 'Comedy'},
 {'id': 10751, 'name': 'Family'}]
Overview contains rich textual descriptions
that can later be used for content-based recommendations.
Release dates appear to follow the YYYY-MM-DD format.
Original language is stored using language codes
such as en (English).

Conclusion:

Each record contains both content information
(genres, overview, language) and popularity information
(vote_average, vote_count).

These fields will form the primary metadata features
for building content-based and hybrid recommendation systems.

-------------------------------------------------------------

Step 3: Verify Granularity

Checked the number of unique movie IDs:

movies_metadata["id"].nunique()

Result:

45436

Compared with dataset row count:

Rows = 45466
Unique id = 45436

Observation:

The number of unique movie IDs is lower than the total number of rows.
Some movie IDs appear more than once in the dataset.

Difference:

Duplicate Records Based on id = 30

Conclusion:

One row is intended to represent one movie.

However, duplicate movie records are present in the dataset
and will need to be investigated during the data cleaning phase.

----------------------------------------------------------------

Step 4: Investigate Missing Values in Modeling Columns

From the dataset structure analysis, the following columns were identified as important for recommendation and dashboard development:

* id
* title
* genres
* overview
* release_date
* original_language
* vote_average
* vote_count

Using the missing value information obtained from `.info()`, sample records with missing values were inspected to understand whether the missing data represents normal data quality issues or potential dataset corruption.

---

4.1 Missing Title Investigation

Checked sample records where `title` is missing.

Observation:

The records with missing titles showed unusual patterns:

* Some rows contained valid movie IDs but missing titles.
* Some rows contained dates inside the `id` column instead of movie IDs.
* The `overview` column contained values such as "Released", which normally belong to another column.

Example:

id = 1997-08-20
title = NaN
overview = Released

Conclusion:

These records appear to have shifted column values and may represent corrupted rows rather than simple missing values.

---

4.2 Missing Overview Investigation

Checked sample records where `overview` is missing.

Observation:

Several movies have valid movie IDs and titles but no plot description.

Examples:

* Wings of Courage
* Roommates
* Happy Weekend
* The Superwife

Conclusion:

These appear to be legitimate movie records with missing descriptions rather than corrupted rows.

Impact:

Since overview is an important feature for content-based recommendation, these records may require special handling during preprocessing.

---

4.3 Missing Release Date Investigation

Checked sample records where `release_date` is missing.

Observation:

Movies such as:

* War Stories Our Mother Never Told Us
* Vermont Is for Lovers
* Jails, Hospitals & Hip-Hop
* Divine Intervention

have valid titles but missing release dates.

Conclusion:

These appear to be normal missing values and not data corruption issues.

Impact:

Release year may be useful for filtering, analytics, and dashboard visualizations.

---

4.4 Missing Original Language Investigation

Checked sample records where `original_language` is missing.

Observation:

Movies such as:

* Shadowing the Third Man
* Unfinished Sky
* 13 Fighting Men
* Lambchops
* Prince Bayaya

have valid movie information but missing language values.

Conclusion:

The missing language values appear to be isolated data quality issues.

Impact:

Language may be useful as a dashboard filter and recommendation attribute.

---

4.5 Missing Vote Information Investigation

Checked sample records where `vote_average` and `vote_count` are missing.

Observation:

The same rows that contained missing titles were also missing vote information.

Examples:

* id = 82663
* id = 1997-08-20
* id = 122662
* id = 2012-09-29
* id = 249260
* id = 2014-01-01

Conclusion:

The missing vote information is concentrated within the suspicious rows identified earlier and further supports the possibility of dataset corruption or column misalignment.

---

Overall Conclusion

The missing value investigation revealed two categories of issues:

1. Normal Missing Values

   * overview
   * release_date
   * original_language

2. Suspicious / Potentially Corrupted Records

   * missing title
   * missing vote_average
   * missing vote_count
   * invalid values appearing inside the id column

These suspicious records require further validation before the dataset can be cleaned and used for recommendation modeling or dashboard development.


------------------------------------------------------------------

Step 5: Validate Movie Identifier Column

Since the id column will later be used to join Movie Metadata with other datasets (Credits, Keywords, Links), its validity was verified.

Checked whether all values in the id column contain numeric movie IDs:

movies_metadata["id"].str.isnumeric().value_counts()

Result:

True     45463
False        3

Observation:

45,463 records contain valid numeric movie IDs.
3 records contain non-numeric values.
These 3 invalid IDs correspond to the corrupted rows identified in Step 4, where column values were shifted into incorrect positions.

Examples of invalid IDs:

1997-08-20
2012-09-29
2014-01-01

Conclusion:

The id column is valid for the vast majority of records.

However, 3 corrupted rows must be removed before using id as a joining key with other datasets.

-----------------------------------------------------------------

Step 6 – Duplicate Movie ID Analysis

A duplicate-ID investigation was performed after discovering that the number of unique movie IDs (45,436) was lower than the total number of rows (45,466). Using duplicated(keep=False), 59 rows associated with duplicate IDs were identified.

Inspection of key columns (title, genres, overview, release_date, vote_average, vote_count, original_language) showed that duplicate IDs correspond to the same movie repeated multiple times. Most duplicated rows were completely identical, while a few contained only minor differences such as a one-vote variation in vote_count.

Since duplicate IDs do not represent distinct movies, keeping a single record per movie ID is appropriate for both recommendation modeling and dashboard reporting.

================================================================

Dataset: Movies (credits)
-------------------------------------------

Step 1 – Understand Dataset Structure (credits.csv)
Objective

Understand the overall structure of the credits dataset before examining individual columns.

Code
credits.info()
Output Summary
Attribute	Value
Total Rows	45,476
Total Columns	3
Memory Usage	~1.0 MB
Columns
Column	Data Type	Non-Null Count
cast	object (string)	45,476
crew	object (string)	45,476
id	int64	45,476
Findings
The dataset contains 45,476 records.
There are only 3 columns, making this a compact dataset.
No missing values are present in any column.
id is already stored as a numeric field (int64).
Both cast and crew are stored as strings and likely contain structured JSON-like data that will need to be interpreted later.
Since every row contains an id, cast, and crew, the dataset appears complete at a structural level.
Observation for Future Use

The dataset is expected to provide:

Cast information (actors, actresses, characters)
Crew information (director, producer, writer, etc.)
Movie identifier (id) for merging with movies_metadata

-----------------------------------------------------------------

Step 2 – Understand Sample Records (credits.csv)
Objective

Inspect sample rows to understand what each record represents and how the important columns are structured.

Code
credits.head()
Findings

The sample records show that:

Each row represents one movie.
The id column appears to be the movie identifier and matches IDs seen in movies_metadata (e.g., 862 = Toy Story, 8844 = Jumanji).
The cast column contains a list of dictionaries describing actors and the characters they played.
The crew column contains a list of dictionaries describing crew members and their roles (Director, Producer, Writer, etc.).
Column Understanding
id

Example:

862
8844
15602
Numeric movie identifier.
Expected to be used later for merging with movies_metadata.
cast

Example structure:

[
    {
        'cast_id': 14,
        'character': 'Woody (voice)',
        'name': 'Tom Hanks',
        ...
    }
]

Contains information such as:

Actor name
Character name
Cast order
Gender
Cast identifier

Potential future use:

Top-billed actors
Cast-based recommendations
Dashboard movie details
crew

Example structure:

[
    {
        'credit_id': '...',
        'department': 'Directing',
        'job': 'Director',
        'name': 'John Lasseter',
        ...
    }
]

Contains information such as:

Crew member name
Department
Job role
Credit identifier

Potential future use:

Director-based recommendations
Writer-based recommendations
Dashboard movie details
Key Observation

Although cast and crew are displayed as strings, they actually contain JSON-like lists of dictionaries.

This means the columns are structured data embedded inside text and will need special handling during the cleaning phase.

---------------------------------------------------------------

Step 3 – Verify Granularity
Objective

Verify whether each row represents a unique movie and determine if the id column can be used as the primary key for the dataset.

Code
credits["id"].nunique()
Result
45,432

Compared with dataset row count:

Total Rows = 45,476
Unique id  = 45,432
Observation

The number of unique movie IDs is lower than the total number of rows.

Difference:

45,476 − 45,432 = 44

This indicates that duplicate movie IDs are present in the dataset.

Since the id column represents the movie identifier, multiple rows exist for some movies.

Conclusion

The intended granularity of the dataset is:

One row = One movie

However, duplicate movie IDs are present and require further investigation.

At this stage, the id column cannot yet be confirmed as a unique primary key.

A duplicate-ID analysis will be performed in a later step to determine whether the duplicate records represent:

Exact duplicate rows
Multiple versions of the same movie record
Data quality issues

---------------------------------------------------------------

Step 4 – Duplicate Movie ID Analysis
Objective

Investigate the duplicate movie IDs identified during the granularity check and determine whether they represent:

Exact duplicate records
Multiple versions of the same movie
Legitimate distinct records
Data quality issues
Code
credits[credits["id"].duplicated(keep=False)].sort_values("id")
Observation

The duplicate-ID investigation revealed multiple movie IDs appearing more than once.

Sample duplicate IDs:

3057
4912
5511
8767
9755
...

Inspection of the duplicate records showed that:

The duplicated rows share the same movie ID.
Cast information is identical or highly similar.
Crew information is identical or highly similar.
No evidence was found that the duplicated IDs represent different movies.

Example:

Movie ID = 3057

Record 1:
Cast = The Creature, ...
Crew = ...

Record 2:
Cast = The Creature, ...
Crew = ...

Result:
Both records represent the same movie.

Similar patterns were observed for other duplicate IDs.

Findings

The duplicate records appear to be repeated entries of the same movie rather than unique movie records.

The duplication does not introduce new cast or crew information.

Therefore, the duplicate rows do not increase the informational value of the dataset.

Impact on Granularity

The intended granularity of the credits dataset remains:

One row = One movie

However, duplicate movie IDs violate this granularity requirement.

Conclusion

Duplicate movie IDs are present within the credits dataset.

Based on manual inspection, the duplicates appear to represent repeated records of the same movie rather than distinct entities.

These duplicate records should be further validated during the data-cleaning phase, and retaining a single record per movie ID is expected to be sufficient for recommendation modeling and dashboard development.

=================================================================

Dataset: Movies (keywords)
-----------------------------

Step 1 – Understand Dataset Structure
Objective

Understand the overall structure of the keywords dataset before examining individual columns.

Code
keywords.info()
Output Summary
Attribute	Value
Total Rows	46,419
Total Columns	2
Memory Usage	~725 KB
Columns
Column	Data Type	Non-Null Count
id	int64	46,419
keywords	object (string)	46,419
Findings
The dataset contains 46,419 records and 2 columns.
No missing values are present in either column.
The id column is stored as an integer (int64).
The keywords column is stored as a string (object).
The dataset is compact and occupies approximately 725 KB of memory.
Every record contains both a movie identifier and associated keyword information.
Observation for Future Use

The dataset is expected to provide:

Movie identifier (id) for merging with other movie datasets.
Descriptive keywords associated with each movie.
Additional content information that can improve content-based recommendations.
Search and filtering capabilities for dashboards and analytics.
Preliminary Understanding of Columns
id
Numeric movie identifier.
Expected to match the movie IDs present in:
movies_metadata
credits
links
keywords
Stores movie-related keywords.
Likely contains structured JSON-like data represented as text.
Expected to describe themes, topics, locations, events, characters, or concepts associated with a movie.

Potential future use:

Content-based recommendation features.
Similarity calculations between movies.
Keyword-based search and filtering.

-----------------------------------------------------------------

Step 2 – Understand Sample Records (keywords.csv)
Objective

Inspect sample records to understand what each row represents and how the keywords column is structured.

Code
keywords.head()
Findings

The sample records show that:

Each row contains a movie identifier (id) and a corresponding set of keywords.
The movie IDs match those observed in other movie datasets such as:
movies_metadata
credits
The keywords column contains a list of dictionaries represented as a string.
Each dictionary contains:
a keyword identifier (id)
a keyword name (name)
Column Understanding
id

Examples:

862
8844
15602
31357
11862
Numeric movie identifier.
Expected to be used for merging with:
movies_metadata
credits
links
keywords

Example structure:

[
    {'id': 931, 'name': 'jealousy'},
    {'id': 4290, 'name': 'toy'},
    {'id': 5202, 'name': 'boy'},
    ...
]

Contains descriptive concepts associated with a movie, such as:

Themes
Topics
Objects
Events
Relationships
Story elements

Examples from the sample records:

jealousy
toy
board game
fishing
based on novel
baby
Potential Future Use

The keywords column can be used for:

Content-based recommendation systems
Movie similarity calculations
Feature engineering
Search and filtering functionality
Enhancing hybrid recommendation models
Key Observation

Although the keywords column is displayed as a string, it actually contains structured JSON-like data stored as text.

Example:

[
    {'id': 931, 'name': 'jealousy'},
    {'id': 4290, 'name': 'toy'}
]

Therefore, the column will require parsing during the preprocessing phase before it can be used for modeling.

Conclusion

Each record links a movie to a collection of descriptive keywords.

These keywords provide rich content information that can complement genres, overviews, cast, and crew data when building content-based and hybrid recommendation systems.

----------------------------------------------------------------

Step 3 – Verify Granularity
Objective

Verify whether each row represents a unique movie and determine whether the id column can serve as the primary key of the dataset.

Code
keywords["id"].nunique()
Result
45,432

Compared with dataset row count:

Total Rows = 46,419
Unique id  = 45,432
Observation

The number of unique movie IDs is lower than the total number of rows.

Difference:

46,419 − 45,432 = 987

This indicates that duplicate movie IDs exist within the dataset.

Since id represents the movie identifier, the expected granularity is:

One row = One movie

However, some movie IDs appear more than once.

Conclusion

The intended granularity of the dataset is one record per movie.

However, duplicate movie IDs are present in the dataset, preventing id from being a unique primary key at this stage.

Further investigation is required to determine whether these duplicate records represent:

Exact duplicate rows
Additional keyword information for the same movie
Data quality issues

----------------------------------------------------------------

Step 4 – Duplicate Movie ID Analysis
Objective

Investigate the duplicate movie IDs identified during the granularity check and determine whether they represent distinct movies or repeated records of the same movie.

Code
keywords[keywords["id"].duplicated(keep=False)].sort_values("id")
Observation

A sample of duplicate movie IDs was inspected.

Examples:

Movie ID	Observation
1998	Same keyword list appears in both records
3025	Same keyword list appears in both records
3692	Same keyword list appears in both records
4459	Same keyword list appears in both records
4709	Both records contain an empty keyword list ([])

Sample duplicate records:

id = 1998
keywords = identical

id = 3025
keywords = identical

id = 4709
keywords = []
keywords = []
Findings

The duplicate records contain the same movie identifier and identical keyword information.

No evidence was found that duplicate IDs contain additional or conflicting keyword data.

The duplicates therefore appear to represent repeated records of the same movie rather than separate movie entities.

Impact on Granularity

The intended granularity of the dataset remains:

One row = One movie

However, duplicate movie IDs violate this granularity requirement.

Conclusion

Duplicate movie IDs are present within the keywords dataset.

Based on manual inspection, the duplicates appear to be repeated copies of the same movie records and do not contribute additional keyword information.

Retaining a single record per movie ID is expected to be sufficient for recommendation modeling and dashboard development.

================================================================

Dataset: Movies (links)
-------------------------

Step 1 – Understand Dataset Structure
Objective

Understand the overall structure of the links dataset before examining individual columns.

Code
links.info()
Output Summary
Attribute	Value
Total Rows	45,843
Total Columns	3
Memory Usage	~1.0 MB
Columns
Column	Data Type	Non-Null Count
movieId	int64	45,843
imdbId	int64	45,843
tmdbId	float64	45,624
Findings
The dataset contains 45,843 records and 3 columns.
movieId and imdbId have no missing values.
tmdbId contains missing values.
All identifier columns are numeric.
The dataset primarily serves as a mapping table between different movie databases.
Column Understanding
movieId
MovieLens movie identifier.
Used to connect with MovieLens datasets.
imdbId
IMDb movie identifier.
Used to reference movies in IMDb.
tmdbId
TMDB movie identifier.
Used to connect with:
movies_metadata
credits
keywords
Important Observation

Unlike previous datasets, this dataset does not contain movie attributes or user interactions.

Its primary purpose is data integration and cross-dataset mapping.

Conclusion

The links dataset acts as a bridge between MovieLens, IMDb, and TMDB movie identifiers and will play an important role when integrating information from multiple movie datasets.

-----------------------------------------------------------------

Step 2 – Understand Sample Records (links.csv)
Objective

Inspect sample records to understand what each row represents and how the different movie identifiers are related.

Code
links.head()
Findings

The sample records show that each row contains identifiers for the same movie across three different movie databases.

Sample Records:

movieId	imdbId	tmdbId
1	114709	862
2	113497	8844
3	113228	15602
4	114885	31357
5	113041	11862
Column Understanding
movieId

Examples:

1
2
3
4
5
MovieLens movie identifier.
Corresponds to movies in:
movies_ml
ratings_ml
imdbId

Examples:

114709
113497
113228
114885
113041
IMDb movie identifier.
Used to reference movies in the IMDb database.
Provides an external identifier for movie lookups.
tmdbId

Examples:

862
8844
15602
31357
11862
TMDB movie identifier.
Matches IDs found in:
movies_metadata
credits
keywords

Example:

movieId = 1
tmdbId  = 862

Movie ID 862 corresponds to Toy Story, which also appears in the TMDB datasets.

Key Observation

The links dataset does not contain movie attributes such as:

title
genres
ratings
keywords
cast
crew

Instead, it serves as a lookup table that maps movies across different movie databases.

Conclusion

Each record represents a mapping between:

MovieLens ID ↔ IMDb ID ↔ TMDB ID

This dataset will be essential when integrating MovieLens user-rating data with TMDB movie metadata, keywords, and credits information.

-----------------------------------------------------------------

Step 3 – Verify Granularity
Objective

Verify whether each row represents a unique movie mapping and determine whether movieId can serve as the primary key of the dataset.

Code
links["movieId"].nunique()
Result
45,843

Compared with dataset row count:

Total Rows = 45,843
Unique movieId = 45,843
Observation

The number of unique MovieLens movie IDs is equal to the total number of rows in the dataset.

This indicates that each MovieLens movie appears exactly once within the links dataset.

Conclusion

The granularity of the dataset is:

One row = One movie mapping

The movieId column uniquely identifies each record and can be considered the primary key of the dataset.

No duplicate MovieLens movie mappings were identified.

---

Since tmdbId will be used to connect MovieLens data with TMDB datasets (movies_metadata, credits, and keywords), its uniqueness was also examined.

Code

links["tmdbId"].nunique()

Result

45,594

Compared with non-null TMDB IDs:

Non-null tmdbId = 45,624
Unique tmdbId   = 45,594

Observation

The number of unique TMDB IDs is slightly lower than the number of non-null TMDB IDs.

Difference:

45,624 − 45,594 = 30

This indicates that some TMDB identifiers appear more than once within the dataset.

Conclusion

While movieId remains unique and defines the granularity of the links dataset, the tmdbId column contains a small number of duplicate values and will require further investigation during the data integration phase.

----------------------------------------------------------------

Step 4 – Investigate Missing Values and Identifier Consistency

Objective

Investigate missing values and identifier uniqueness issues that may affect dataset integration.

Missing Value Analysis

From the dataset structure analysis:

Column	Non-Null Count
movieId	45,843
imdbId	45,843
tmdbId	45,624

Observation:

Missing tmdbId values = 45,843 - 45,624 = 219

Sample records with missing tmdbId values were inspected.

Findings:

movieId remains populated.
imdbId remains populated.
Only the tmdbId value is missing.

Example:

movieId = 107623
imdbId  = 2928078
tmdbId  = NaN

Conclusion:

The records appear to be valid movie mappings that lack a corresponding TMDB identifier rather than corrupted records.

TMDB Identifier Consistency Analysis

Since tmdbId will be used to join MovieLens data with:

movies_metadata
credits
keywords

its uniqueness was examined.

Code:

links["tmdbId"].nunique()

Result:

Unique tmdbId = 45,594
Non-null tmdbId = 45,624

Difference:

45,624 - 45,594 = 30

Observation:

A small number of TMDB identifiers appear multiple times within the dataset.

Sample duplicate mappings:

movieId = 6003   → tmdbId = 4912
movieId = 144606 → tmdbId = 4912

movieId = 27136  → tmdbId = 5511
movieId = 7587   → tmdbId = 5511

Findings:

The duplicate values occur when multiple MovieLens movie IDs map to the same TMDB movie identifier.

Conclusion:

The duplication originates from the mapping relationship between MovieLens and TMDB rather than from duplicated TMDB movie records.

These mappings will require validation during the data integration phase to avoid unintended duplication after joins.

Overall Conclusion

The links dataset is structurally complete and provides the bridge between MovieLens and TMDB datasets.

However:

219 records have missing tmdbId values.
30 TMDB identifiers are associated with more than one MovieLens movie.

These issues should be considered during the data cleaning and integration phases.

==============================================================

Ratings section will be added later