We have three datasets:

MovieLens which contains four files
movies.dat
ratings.dat
users.dat
README

so for our model we will use movies, ratings and users files from this dataset and accordingly perfrom data understanding and cleaning.

Another dataset is Movies dataset which has seven files

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

third dataset is Anime, it has six files

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

================================================================

Dataset: Anime (anime-dataset-2023)
-------------------------------------

Step 1 – Understand Dataset Structure
Objective

Understand the overall structure of the anime dataset before examining individual columns.

Code
anime.info()
Output Summary
Attribute	Value
Total Rows	24,905
Total Columns	24
Memory Usage	~4.6 MB
Columns
Column	Data Type	Non-Null Count
anime_id	int64	24,905
Name	str	24,905
English name	str	24,905
Other name	str	24,905
Score	str	24,905
Genres	str	24,905
Synopsis	str	24,905
Type	str	24,905
Episodes	str	24,905
Aired	str	24,905
Premiered	str	24,905
Status	str	24,905
Producers	str	24,905
Licensors	str	24,905
Studios	str	24,905
Source	str	24,905
Duration	str	24,905
Rating	str	24,905
Rank	str	24,905
Popularity	int64	24,905
Favorites	int64	24,905
Scored By	str	24,905
Members	int64	24,905
Image URL	str	24,905
Findings
The dataset contains 24,905 anime records and 24 columns.
No missing values are reported by info().
Most columns are stored as strings.
Four columns are stored as numeric values:
anime_id
Popularity
Favorites
Members
Several columns that appear numeric are currently stored as strings and may require datatype validation later:
Score
Episodes
Rank
Scored By
Content Categories

The dataset contains multiple types of information:

Identification
anime_id
Name
English name
Other name
Content Metadata
Genres
Synopsis
Type
Source
Studios
Producers
Licensors
Release Information
Aired
Premiered
Status
Popularity & Community Metrics
Score
Rank
Popularity
Favorites
Scored By
Members
Additional Attributes
Episodes
Duration
Rating
Image URL
Important Observation

This dataset is significantly richer than the movie metadata dataset because it combines:

Anime metadata
Genre information
Synopsis information
Production information
Community popularity metrics
Ranking information

within a single table.

Conclusion

The dataset appears to be a comprehensive anime catalog containing both content-based features and popularity-based features.

It is expected to serve as the primary metadata source for the anime recommendation domain.

----------------------------------------------------------------

Step 2 – Understand Sample Records (anime-dataset-2023)
Objective

Inspect sample records to understand what each row represents and how the dataset attributes are structured.

Code
anime.head()
Findings

The sample records show that each row represents a single anime title and contains:

Identification information
Content metadata
Production information
Release information
Community ratings and popularity metrics
Media assets

Example anime records include:

Cowboy Bebop
Cowboy Bebop: The Movie
Trigun
Witch Hunter Robin
Beet the Vandel Buster
Column Understanding
anime_id

Examples:

1
5
6
7
8
Unique anime identifier.
Expected to serve as the primary key.
Name / English name / Other name

Example:

Name         : Cowboy Bebop
English name : Cowboy Bebop
Other name   : カウボーイビバップ

Provides multilingual naming information.

Potential uses:

Search functionality
User-facing display
Cross-language matching
Genres

Examples:

Action, Award Winning, Sci-Fi
Action, Adventure, Sci-Fi
Adventure, Fantasy, Supernatural

Observation:

Stored as comma-separated values.
An anime can belong to multiple genres.

Potential use:

Content-based recommendation features.
Genre filtering and analytics.
Synopsis

Example:

Crime is timeless. By the year 2071...

Observation:

Long-form textual description.
Rich source for NLP-based feature extraction.

Potential use:

TF-IDF features
Embeddings
Semantic similarity
Type

Examples:

TV
Movie

Potential categories:

TV
Movie
OVA
ONA
Special
Music

Potential use:

User preference modeling.
Recommendation filtering.
Episodes

Examples:

26
1
52

Observation:

Appears numeric but is currently stored as string/object.

May require datatype conversion during preprocessing.

Production Information

Examples:

Studios   : Sunrise
Studios   : Bones
Studios   : Madhouse

Source    : Original
Source    : Manga

Potential use:

Studio-based recommendations.
Source-material analysis.
Community Metrics

Examples:

Score      : 8.75
Rank       : 41
Popularity : 43
Favorites  : 78,525
Members    : 1,771,505

Observation:

The dataset contains both:

User evaluation metrics
Popularity metrics

which can be useful for ranking and recommendation strategies.

Image URL

Example:

https://cdn.myanimelist.net/...

Provides image references for dashboard and UI development.

Key Observation

Unlike the TMDB datasets where metadata is distributed across multiple files:

movies_metadata
credits
keywords

the anime dataset already contains:

Titles
Genres
Synopsis
Production details
Popularity metrics
Ranking metrics
Images

within a single dataset.

This makes it a highly valuable source for both content-based recommendations and dashboard visualizations.

Conclusion

Each row appears to represent a single anime title enriched with descriptive, production, and popularity information.

The dataset contains several strong candidate features for recommendation modeling, particularly:

Genres
Synopsis
Type
Studios
Source
Score
Popularity
Favorites
Members

-----------------------------------------------------------------

Step 3 – Verify Granularity
Objective

Verify whether each row represents a unique anime and determine whether anime_id can serve as the primary key of the dataset.

Code
anime["anime_id"].nunique()
Result
24,905

Compared with dataset row count:

Total Rows      = 24,905
Unique anime_id = 24,905
Observation

The number of unique anime identifiers is equal to the total number of rows in the dataset.

This indicates that each anime appears exactly once within the dataset.

No duplicate anime identifiers were identified.

Granularity

The dataset follows the expected granularity:

One row = One anime

Each record contains metadata, production details, popularity metrics, and descriptive information for a single anime title.

Conclusion

The anime_id column uniquely identifies each anime record and can be considered the primary key of the dataset.

The dataset maintains a consistent granularity of one record per anime.

-----------------------------------------------------------------

Step 4 – Investigate Hidden Missing Values
Objective

Identify placeholder values that represent missing information but are stored as text rather than actual null values.

Code
anime.eq("Unknown").sum().sort_values(ascending=False)
Results
Column	Count of "Unknown"
Source	3,689
Duration	663
All other inspected columns	0
Findings
Source
Unknown values = 3,689

The source material for these anime titles is unavailable or unspecified.

Examples of known source values observed earlier:

Original
Manga
Light Novel
Visual Novel

Potential impact:

Reduces usefulness of source-based recommendations.
May require grouping into an "Unknown" category during preprocessing.
Duration
Unknown values = 663

Duration information is unavailable for a subset of anime records.

Examples of known values:

24 min per ep
1 hr 55 min
23 min per ep

Potential impact:

May affect duration-based filtering or recommendation features.
Can be treated as missing during preprocessing.
Observation

Despite the dataset reporting:

24,905 non-null values

in every column, hidden missing information exists in the form of placeholder text values.

The primary columns affected are:

Source
Duration
Data Quality Assessment
Issue	Count
Missing Source Information	3,689
Missing Duration Information	663

No significant hidden missing values were identified in:

Genres
Synopsis
Type
Episodes
Status
Studios
Rating
Rank
Popularity
Conclusion

The anime dataset is largely complete.

The only notable data-quality issues identified during the understanding phase are placeholder "Unknown" values in:

Source
Duration

These can be handled during the data cleaning phase without significantly affecting the overall usability of the dataset.

--------------------------------------------------------------

Step 5.1 – Validate Numeric-Like Column: Score

The Score column was stored as object despite containing decimal rating values.

A numeric conversion test revealed that 9,213 records could not be converted to numeric format.

Investigation showed that all invalid values were represented by the placeholder "UNKNOWN".

Findings:

Total Records      : 24,905
Numeric Scores     : 15,692
UNKNOWN Scores     : 9,213

Approximately 37% of anime titles do not have a community score.

Conclusion:

The Score column represents a numeric feature stored as text.
The placeholder value "UNKNOWN" should be treated as missing data during preprocessing, after which the column can be safely converted to float.

---

Step 5.2 – Validate Numeric-Like Column: Episodes
Findings

Episodes is stored as object but contains numeric values represented as text.

Top values:

1.0        11532
12.0        1919
2.0         1528
26.0        1201
...
UNKNOWN      611
Conversion Validation
pd.to_numeric(anime["Episodes"], errors="coerce").isna().sum()

Result:

611
Invalid Value Investigation
UNKNOWN    611
Data Quality Assessment
Metric	Value
Total Records	24,905
UNKNOWN Episodes	611
Missing %	~2.45%
Business Interpretation

These are likely:

Currently airing anime
Upcoming anime
Titles where episode count has not been finalized
Conclusion

Episodes is fundamentally a numeric field.

Only "UNKNOWN" prevents conversion.

During cleaning:

anime["Episodes"] = pd.to_numeric(
    anime["Episodes"].replace("UNKNOWN", np.nan)
)

---

Step 5.3 – Validate Numeric-Like Column: Rank
Findings

Top values:

UNKNOWN    4612
0.0         187
7175.0        4
9618.0        4
...
Conversion Validation
pd.to_numeric(anime["Rank"], errors="coerce").isna().sum()

Result:

4612
Invalid Value Investigation
UNKNOWN    4612
Data Quality Assessment
Metric	Value
Total Records	24,905
UNKNOWN Rank	4,612
Missing %	~18.5%
Interesting Observation

Notice:

0.0    187

This deserves investigation before cleaning.

Run:

anime[anime["Rank"] == "0.0"][
    ["anime_id","Name","Score","Rank","Scored By"]
].head()

Questions:

Does Rank = 0 mean "unranked"?
Is it a placeholder?
Is it a valid ranking?

This should be investigated before deciding how to clean Rank.

Conclusion

Rank is a numeric field stored as text.

The only non-numeric value identified is:

UNKNOWN

However, the presence of rank value 0.0 requires further validation.

---

Step 5.4 – Validate Numeric-Like Column: Scored By
Findings

Top values:

UNKNOWN    9213
121.0        35
128.0        35
150.0        33
...
Conversion Validation
pd.to_numeric(anime["Scored By"], errors="coerce").isna().sum()

Result:

9213
Invalid Value Investigation
UNKNOWN    9213
Data Quality Assessment
Metric	Value
Total Records	24,905
UNKNOWN	9,213
Missing %	~37%
Important Observation

This matches exactly the number of missing Scores:

Column	UNKNOWN Count
Score	9,213
Scored By	9,213

This suggests a strong relationship:

If an anime has no score, it also has no users who scored it.

That is logically consistent.

Business Interpretation

Scored By likely represents:

Number of users who submitted a score.

When there are insufficient ratings:

Score = UNKNOWN
Scored By = UNKNOWN
Conclusion

Scored By is a numeric count field stored as text.

The placeholder "UNKNOWN" should be treated as missing data.

---

Step 5.5 – Investigate Rank Value 0.0

Objective

Determine whether rank value 0.0 represents a valid ranking position or a placeholder value.

Code

anime[anime["Rank"] == "0.0"][
    ["Score", "Scored By"]
].value_counts()

Result

Score    Scored By
UNKNOWN  UNKNOWN      187

Findings

All anime records with:

Rank = 0.0

also contain:

Score = UNKNOWN
Scored By = UNKNOWN

No scored or ranked anime were observed with a rank value of 0.0.

Conclusion

The value 0.0 does not represent a legitimate ranking position.

Instead, it appears to be a placeholder used for anime that have not received sufficient community ratings to obtain:

a score
a ranking
a scored-by count

During preprocessing, Rank = 0.0 should be treated similarly to a missing rank value.

-----------------------------------------------------------------

Step 6 – Identify Recommendation Modeling Columns

Objective

Identify the subset of attributes that are expected to contribute directly to recommendation generation and ranking.

Selected Recommendation Columns

anime_id
Name
English name
Genres
Synopsis
Type
Source
Studios
Score
Rank
Popularity
Favorites
Members
Scored By
Episodes

Rationale

These columns contain:

Anime identifiers
Content metadata
Genre information
Text descriptions
Production attributes
Community rating metrics
Popularity indicators
Episode-count information

Together, they provide the most relevant features for building content-based, popularity-based, and hybrid recommendation models.

================================================================

Dataset: Anime (users-details-2023)
---------------------------------------

Step 1 – Understand Dataset Structure
Objective

Understand the overall structure of the user details dataset before examining individual columns.

Code
anime_users.info()
Output Summary
Attribute	Value
Total Rows	731,290
Total Columns	16
Memory Usage	~89.3 MB
Columns
Column	Data Type	Non-Null Count
Mal ID	int64	731,290
Username	str	731,289
Gender	str	224,383
Birthday	str	168,068
Location	str	152,805
Joined	str	731,290
Days Watched	float64	731,282
Mean Score	float64	731,282
Watching	float64	731,282
Completed	float64	731,282
On Hold	float64	731,282
Dropped	float64	731,282
Plan to Watch	float64	731,282
Total Entries	float64	731,282
Rewatched	float64	731,282
Episodes Watched	float64	731,282
Findings
Dataset Size

The dataset contains:

731,290 user records
16 columns

This is significantly larger than the anime metadata dataset and appears to contain user profile information and anime consumption statistics.

Identifier Column
Mal ID

appears to be the user identifier.

It will likely be used to connect this dataset with:

users-score-2023

during recommendation modeling.

User Profile Attributes
Username
Gender
Birthday
Location
Joined

These columns contain demographic and profile-related information.

User Activity Statistics
Days Watched
Mean Score
Watching
Completed
On Hold
Dropped
Plan to Watch
Total Entries
Rewatched
Episodes Watched

These columns summarize a user's anime viewing behavior and engagement level.

Examples:

Mean Score → Average rating given by the user
Completed → Number of completed anime
Watching → Number of currently watched anime
Episodes Watched → Total episodes consumed
Missing Value Observation

Several profile-related columns contain substantial missing values:

Column	Missing Values
Gender	~506,907
Birthday	~563,222
Location	~578,485

while:

Joined
Mal ID

appear complete.

Additional Observation

A group of activity-related columns share the same non-null count:

731,282

This suggests that:

731,290 - 731,282 = 8

records may be missing all activity statistics simultaneously.

This should be investigated later during the missing-value analysis phase.

Conclusion

The dataset appears to contain one record per MyAnimeList user, including:

User profile information
Demographic attributes
Anime viewing statistics
User scoring behavior

The dataset is expected to provide valuable user-level features for recommendation modeling and user profiling.

-----------------------------------------------------------------

Step 2 – Understand Dataset Content
Objective

Inspect sample records to understand what each row represents and how the dataset attributes are structured.

Code
anime_users.head()
Findings

The sample records show that each row contains information about an individual MyAnimeList user, including:

User profile information
Demographic attributes
Account information
Anime consumption statistics
User scoring behavior
Column Understanding
Mal ID

Examples:

1
3
4
9
18

Unique MyAnimeList user identifier.

Expected to be used for linking with:

users-score-2023
Username

Examples:

Xinil
Aokaado
Crystal
Arcane
Mad

User account name.

Potential use:

User identification
Dashboard display
Demographic Information
Gender

Examples:

Male
Female
NaN

Represents the user's self-reported gender.

Observation:

Many records contain missing values.

Birthday

Examples:

1985-03-04T00:00:00+00:00
NaN

Represents the user's birth date.

Observation:

Stored as a string in timestamp format.

Contains substantial missing values.

Location

Examples:

California
Oslo, Norway
Melbourne, Australia
NaN

Represents the user's self-reported location.

Observation:

Free-text location values rather than standardized countries or regions.

Contains substantial missing values.

Account Information
Joined

Examples:

2004-11-05T00:00:00+00:00
2004-11-11T00:00:00+00:00

Represents the date the user joined MyAnimeList.

Observation:

Stored as a timestamp string.

Potential use:

User tenure analysis
Community growth analysis
Viewing Statistics
Days Watched

Examples:

142.3
68.6
212.8

Represents the cumulative number of days spent watching anime.

Episodes Watched

Examples:

8458
4072
12781

Represents the total number of anime episodes watched by the user.

User Rating Information
Mean Score

Examples:

7.37
7.34
6.68
7.71

Represents the average rating assigned by the user across scored anime.

Potential use:

User rating behavior analysis
User preference profiling
Anime List Statistics
Watching

Number of anime currently being watched.

Completed

Number of anime completed.

On Hold

Number of anime placed on hold.

Dropped

Number of anime dropped.

Plan to Watch

Number of anime planned for future viewing.

Total Entries

Total number of anime list entries maintained by the user.

Rewatched

Number of anime rewatched by the user.

Key Observation

Unlike anime-dataset-2023, where each row represented:

One row = One anime

this dataset appears to represent:

One row = One user

Each record summarizes a user's anime viewing history and profile information rather than details about a specific anime.

The dataset therefore provides user-level features that can complement the user-anime interactions stored in users-score-2023.

----------------------------------------------------------------

Step 3 – Verify Granularity
Objective

Determine the level of detail represented by each row and identify the primary key of the dataset.

Code
len(anime_users)

Output:

731290
anime_users["Mal ID"].nunique()

Output:

731290
Findings
Metric	Value
Total Rows	731,290
Unique Mal ID	731,290

Since:

Total Rows = Unique Mal ID

there are no duplicate user identifiers.

Granularity Determination

The dataset granularity is:

One row = One unique MyAnimeList user

Each record represents a single user's profile and aggregated anime consumption statistics.

Primary Key
Mal ID

acts as the primary key because:

Every record has a unique value.
No duplicates were observed.
It uniquely identifies a user.
Relationship with Other Datasets

This dataset is expected to connect with the user-anime interaction dataset (users-score-2023) through:

Mal ID

allowing user profile information to be linked with individual anime ratings.

Conclusion

The dataset has a user-level granularity with:

Primary Key: Mal ID
Granularity: One row per user
Duplicate Users: None detected

--------------------------------------------------------------

Step 4 – Investigate Missing Value Anomalies
Issue A – Missing Username

A single record was identified with a missing username.

Affected Records: 1

The corresponding user identifier (Mal ID) remains available, allowing the record to remain uniquely identifiable.

Issue B – Missing Activity Statistics

Eight records were identified where all anime activity metrics were simultaneously missing.

Affected columns:

Days Watched
Mean Score
Watching
Completed
On Hold
Dropped
Plan to Watch
Total Entries
Rewatched
Episodes Watched

Profile information such as username, gender, birthday, location, and join date remained available for most of these records.

Interpretation

The user profile exists, but anime activity statistics were unavailable during data collection. Possible causes include:

Deleted accounts
Closed accounts
Private profiles
Data extraction failures
Impact
Affected Records: 8
Affected Percentage:
8 / 731,290 ≈ 0.0011%

The impact on analysis and recommendation modeling is negligible.

----------------------------------------------------------------

Selected Recommendation Columns – users-details-2023

The following columns were identified as potentially useful for recommendation modeling:

Mal ID
Mean Score
Days Watched
Watching
Completed
On Hold
Dropped
Plan to Watch
Total Entries
Rewatched
Episodes Watched

These attributes capture user engagement, consumption patterns, and rating behavior, which can support user profiling and hybrid recommendation approaches.

The following columns were retained primarily for dashboarding and descriptive analysis:

Username
Gender
Birthday
Location
Joined

=================================================================

Dataset: users-score-2023
----------------------------

Step 1 – Understand Dataset Structure
Objective

Understand the overall structure, size, data types, and completeness of the user-anime interaction dataset before performing further analysis.

Code
anime_scores.info(show_counts=True)
Output Summary
Metric	Value
Total Rows	24,325,191
Total Columns	5
Memory Usage	~927.9 MB
Column Overview
Column	Non-Null Count	Data Type
user_id	24,325,191	int64
Username	24,324,959	str
anime_id	24,325,191	int64
Anime Title	24,325,191	str
rating	24,325,191	int64
Initial Findings
Dataset Size

The dataset contains:

24,325,191 records
5 columns

This makes it the largest dataset analyzed so far and indicates that it stores detailed user-anime interactions rather than anime metadata or user profile information.

Identifier Columns

The dataset contains two identifier fields:

user_id
anime_id

These appear to represent:

A unique user
A unique anime

Further granularity validation will determine whether the combination of these two columns uniquely identifies each record.

Interaction Information

The dataset contains:

user_id
anime_id
rating

which suggests that each record captures a user's rating for a specific anime.

This structure is commonly used for:

User-Based Collaborative Filtering
Item-Based Collaborative Filtering
Matrix Factorization
SVD
ALS
Hybrid Recommendation Systems
Data Completeness

All critical recommendation fields are fully populated:

Column	Missing Values
user_id	0
anime_id	0
rating	0
Anime Title	0

Only the Username column contains missing values.

Missing Usernames = 232

Since user_id is available for all records, the missing usernames are not expected to impact recommendation modeling.

Data Type Assessment

All columns appear to have appropriate data types:

Column	Expected Type	Actual Type
user_id	Integer	int64
anime_id	Integer	int64
rating	Integer	int64
Username	Text	str
Anime Title	Text	str

No datatype inconsistencies were identified during the initial structure analysis.

Conclusion

The users-score-2023 dataset is a large-scale user-anime interaction dataset containing over 24 million records. It includes user identifiers, anime identifiers, anime titles, and user ratings, making it the primary dataset for collaborative filtering and recommendation modeling.

A minor data quality issue was identified:

Username: 232 missing values

All recommendation-critical fields (user_id, anime_id, and rating) are complete.

-----------------------------------------------------------------

Step 2 – Understand Dataset Content
Objective

Inspect sample records to understand what each row represents and how the interaction data is structured.

Code
anime_scores.head()
Findings

The sample records show multiple entries for the same user:

user_id	Username	anime_id	Anime Title	rating
1	Xinil	21	One Piece	9
1	Xinil	48	.hack//Sign	7
1	Xinil	320	A Kite	5
1	Xinil	49	Aa! Megami-sama!	8
1	Xinil	304	Aa! Megami-sama! Movie	8

This indicates that a user can appear multiple times, with each record corresponding to a different anime.

Column Understanding
user_id

Example:

1

Unique identifier of the user who provided the rating.

Expected to link with:

users-details-2023

through the user identifier.

Username

Example:

Xinil

Username associated with the user account.

Observation:

This information is duplicated across multiple rows for the same user.

anime_id

Examples:

21
48
320
49
304

Unique identifier of the anime being rated.

Expected to link with:

anime-dataset-2023

through the anime identifier.

Anime Title

Examples:

One Piece
.hack//Sign
A Kite
Aa! Megami-sama!
Aa! Megami-sama! Movie

Human-readable anime title corresponding to the anime identifier.

Observation:

This information is duplicated across multiple user ratings for the same anime.

rating

Examples:

9
7
5
8
8

Represents the rating assigned by a user to a specific anime.

Initial observation suggests an integer rating scale.

The exact rating range will be validated during later analysis.

Dataset Role in the Recommendation System

This dataset acts as the interaction dataset connecting users and anime.

Conceptually:

User  ── rates ──► Anime

Each row captures one rating interaction between:

user_id
anime_id

along with the rating value assigned by the user.

Preliminary Granularity Assessment

The sample records suggest:

One row = One user's rating for one anime

However, this must be formally validated by checking whether the combination:

(user_id, anime_id)

is unique across the dataset.

Relationship with Other Datasets
Dataset	Join Column
users-details-2023	user_id (Mal ID equivalent)
anime-dataset-2023	anime_id

This dataset serves as the bridge between user information and anime metadata.

Conclusion

The dataset contains user-anime rating interactions and appears to be the primary source for collaborative filtering and recommendation modeling.

-----------------------------------------------------------------

Step 3 – Verify Granularity
Objective

Determine the level of detail represented by each row and identify the key that uniquely defines a user-anime interaction.

Code
anime_scores[["user_id", "anime_id"]].duplicated().sum()
Output
0
Findings

No duplicate combinations of:

(user_id, anime_id)

were found in the dataset.

This means that:

A user appears multiple times.
An anime appears multiple times.
A specific user can rate multiple anime.
A specific anime can be rated by multiple users.
A user rates a particular anime at most once.
Granularity Determination

The dataset granularity is:

One row = One user-anime rating interaction

Each record represents a unique rating assigned by a user to a specific anime.

Composite Primary Key

Neither column is unique individually:

user_id
anime_id

However, the combination:

(user_id, anime_id)

uniquely identifies every record.

Therefore, the interaction table has a composite key:

(user_id, anime_id)
Recommendation Modeling Significance

This structure is ideal for recommendation systems because it forms a user-item interaction matrix:

User	Anime	Rating
U1	A1	9
U1	A2	7
U2	A1	8
U3	A5	10

which can be transformed into:

            Anime1  Anime2  Anime3 ...
User1         9       7       ...
User2         8       ...
User3                 ...     10

This matrix serves as the foundation for:

Collaborative Filtering
Matrix Factorization
SVD
ALS
Hybrid Recommendation Models
Conclusion

The dataset has:

Granularity: One row per user-anime rating
Composite Key: (user_id, anime_id)
Duplicate Interactions: None

This confirms that the interac

----------------------------------------------------------------

Step 4 – Investigate Data Quality Observations
Issue A – Missing Username

A total of 232 records contained missing usernames.

Investigation revealed that all affected records belong to a single user:

user_id = 20930

The same missing username was also observed in the users-details-2023 dataset, indicating a source-data issue rather than a processing error.

Since the user identifier remains available, the impact on recommendation modeling is negligible.

Issue B – Rating Scale Validation

The rating distribution contains only values between:

1 and 10

No placeholder or invalid values such as:

0
-1
UNKNOWN
NaN

were identified.

This confirms that the rating column contains valid explicit user ratings and is suitable for collaborative filtering and matrix factorization techniques.

