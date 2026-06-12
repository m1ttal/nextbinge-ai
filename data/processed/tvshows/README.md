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

=================================================================

Dataset: TV Shows (TMDB_tv_dataset_v3)
-------------------------------------------

Step 1 – Understand Dataset Structure
Objective

Understand the overall structure, size, data types, and completeness of the TV Shows dataset before performing further analysis.

Code
tvshows.info()
Output Summary
Attribute	Value
Total Rows	168,639
Total Columns	29
Memory Usage	~35.1 MB
Column Overview
Column	Non-Null Count	Data Type
id	168,639	int64
name	168,634	str
number_of_seasons	168,639	int64
number_of_episodes	168,639	int64
original_language	168,639	str
vote_count	168,639	int64
vote_average	168,639	float64
overview	93,333	str
adult	168,639	bool
backdrop_path	77,780	str
first_air_date	136,903	str
last_air_date	138,735	str
homepage	50,998	str
in_production	168,639	bool
original_name	168,634	str
popularity	168,639	float64
poster_path	108,737	str
type	168,639	str
status	168,639	str
tagline	5,330	str
genres	99,713	str
created_by	36,496	str
languages	110,050	str
networks	97,589	str
origin_country	137,609	str
spoken_languages	109,280	str
production_companies	59,342	str
production_countries	77,511	str
episode_run_time	168,639	int64
Findings
Dataset Size

The dataset contains:

168,639 TV shows
29 columns

This makes it significantly larger than:

MovieLens Movies (3,883)
TMDB Movies Metadata (45,466)
Anime Dataset (24,905)
Identifier Column
id

appears to be the unique TMDB TV Show identifier.

It is expected to serve as the primary key of the dataset.

Content Metadata

The dataset contains rich descriptive information:

name
original_name
overview
genres
original_language
languages
spoken_languages

These attributes are highly valuable for:

Content-based recommendations
Search functionality
Similarity calculations
Popularity & Community Metrics
vote_average
vote_count
popularity

These metrics represent audience engagement and ratings.

Potential uses:

Popularity-based recommendations
Ranking algorithms
Hybrid recommendation systems
TV-Specific Attributes

Unlike movie datasets, this dataset contains television-specific information:

number_of_seasons
number_of_episodes
episode_run_time
status
in_production
first_air_date
last_air_date

These attributes can support:

Series-length preferences
Active vs completed show filtering
Runtime-based recommendations
Production Information
created_by
networks
production_companies
production_countries
origin_country

Potential uses:

Network-based recommendations
Creator-based recommendations
Dashboard filtering
Media Assets
poster_path
backdrop_path
homepage
tagline

Useful primarily for:

Dashboarding
Front-end display

Not typically used for recommendation modeling.

Missing Value Observation

Several columns contain substantial missing values.

High Missingness
Column	Missing Count
tagline	~163,309
created_by	~132,143
homepage	~117,641
production_companies	~109,297
backdrop_path	~90,859
production_countries	~91,128
overview	~75,306
genres	~68,926
Moderate Missingness
Column	Missing Count
first_air_date	~31,736
last_air_date	~29,904
origin_country	~31,030
networks	~71,050
languages	~58,589
Important Observation

Unlike the Anime dataset, this dataset contains real null values rather than placeholder values such as "UNKNOWN".

Missing-value handling will therefore be an important part of the cleaning phase.

Preliminary Conclusion

The dataset appears to be a comprehensive TV-show metadata repository containing:

Content information
Language information
Popularity metrics
Production details
Runtime and season statistics

It is expected to serve as the primary metadata source for the TV Shows recommendation domain.

---------------------------------------------------------------

Step 2 – Understand Dataset Content
Objective

Inspect sample records to understand what each row represents and how the TV show attributes are structured.

Code
tvshows.head()
Findings

The sample records show that each row represents a single TV show and contains:

Identification information
Content metadata
Popularity metrics
Production information
Broadcasting details
Runtime and season statistics

Example TV Shows:

Game of Thrones
Money Heist
Stranger Things
The Walking Dead
Lucifer
Column Understanding
id

Examples:

1399
71446
66732
1402
63174

TMDB TV Show identifier.

Expected to serve as the primary key.

Potential use:

Dataset joins
Recommendation output
Dashboard navigation
name

Examples:

Game of Thrones
Money Heist
Stranger Things

TV show title displayed to users.

Potential use:

Search
Recommendation display
Dashboard presentation
original_name

Examples:

Game of Thrones
La Casa de Papel

Original title of the TV show.

Potential use:

Internationalization
Multilingual search
overview

Example:

Seven noble families fight for control...

Long-form plot description.

Observation:

Rich textual information suitable for NLP processing.

Potential use:

TF-IDF
Embeddings
Semantic similarity
Content-based recommendation
genres

Examples:

Sci-Fi & Fantasy, Drama, Action & Adventure

Crime, Drama

Drama, Sci-Fi & Fantasy, Mystery

Observation:

Unlike TMDB Movies where genres were stored as JSON-like dictionaries, TV genres are already stored as readable comma-separated text.

Potential use:

Genre-based filtering
Content similarity
User preference modeling
original_language

Examples:

en
es

Language code of the original production.

Examples:

en = English
es = Spanish

Potential use:

Language-based filtering
User preference matching
vote_average

Examples:

8.442
8.257
8.624

Average community rating.

Potential use:

Popularity ranking
Hybrid recommendation scoring
vote_count

Examples:

21857
17836
16161

Number of user votes.

Observation:

Shows with high vote averages and high vote counts are generally more reliable candidates for recommendation.

Potential use:

Bayesian ranking
Confidence weighting
popularity

TMDB popularity score.

Potential use:

Trending recommendations
Popularity-based ranking
TV-Specific Attributes
number_of_seasons

Examples:

8
3
4
11
6

Represents total seasons.

Potential use:

Length preference modeling
Filtering short vs long series
number_of_episodes

Examples:

73
41
34
177
93

Represents total episodes.

Potential use:

Viewing commitment recommendations
User preference analysis
episode_run_time

Examples:

70
42
45

Represents average runtime in minutes.

Interesting observation:

Some highly popular shows display:

episode_run_time = 0

Example:

Game of Thrones
Stranger Things

This requires investigation because runtime should normally be positive.

Potential data-quality check for later.

Production Information
created_by

Examples:

David Benioff, D.B. Weiss
Álex Pina
Matt Duffer, Ross Duffer

Observation:

Already stored as readable text.

Potential use:

Creator-based similarity
Dashboard details
networks

Examples:

HBO
Netflix
AMC
FOX

Potential use:

Network-based recommendations
Analytics
production_companies

Examples:

Revolution Sun Studios
Vancouver Media
AMC Studios
Warner Bros. Television

Potential use:

Advanced content similarity
Dashboard display
Country & Language Information
origin_country

Examples:

US
ES

Country where the show originated.

Potential use:

Regional recommendations
Dashboard filters
spoken_languages

Examples:

English
Español

Human-readable language values.

Potential use:

User preference matching
Status Information
status

Typical values likely include:

Ended
Returning Series
Canceled

Potential use:

Filtering active vs completed shows
in_production

Boolean field:

True
False

Indicates whether new episodes are still being produced.

Potential use:

Ongoing show recommendations
Key Observation

Unlike the Movies domain, where information was spread across:

movies_metadata
credits
keywords

the TV Shows dataset already combines:

Metadata
Genres
Overviews
Creator information
Network information
Popularity metrics
Runtime information

into a single table.

This makes it structurally much closer to the Anime dataset than to the Movie dataset.

Recommendation-Relevant Columns (Initial Selection)

These are the strongest candidates for recommendation modeling:

id
name
genres
overview
original_language
vote_average
vote_count
popularity
number_of_seasons
number_of_episodes
episode_run_time
status
in_production
created_by
networks
origin_country

---------------------------------------------------------------

Step 3 – Verify Granularity
Objective

Determine whether each row represents a unique TV show and whether the id column can serve as the primary key.

Code
tvshows["id"].nunique()
Result
Unique id = 164,705

Compared with:

Total Rows = 168,639
Observation

The number of unique TV show IDs is lower than the total number of rows.

168,639 - 164,705 = 3,934

This indicates that duplicate TV show IDs are present in the dataset.

Metric	Value
Total Rows	168,639
Unique IDs	164,705
Duplicate Rows	3,934
Preliminary Interpretation

The intended granularity appears to be:

One row = One TV Show

because the dataset contains attributes such as:

name
overview
genres
vote_average
number_of_seasons
number_of_episodes

which describe a TV show rather than an episode or season.

However, duplicate IDs suggest that some TV shows appear multiple times.

Conclusion

At this stage:

id cannot yet be considered a unique primary key.

Further investigation is required to determine whether duplicate IDs represent:

Exact duplicate records
Different versions of the same TV show record
Data collection duplicates
Legitimate records with conflicting information

---------------------------------------------------------------

Step 4 - Duplicate TV Show IDs

The dataset contains duplicate TV show identifiers.

Investigation revealed that duplicate IDs are not exact copies. Instead, multiple records for the same TV show contain different levels of metadata completeness.

Examples include differences in:

genres
homepage
poster_path
production_companies
popularity
last_air_date

This suggests the dataset contains multiple snapshots of the same TMDB record collected at different times.

For recommendation modeling, duplicate TV show IDs should be consolidated by retaining the most complete record for each id.

----------------------------------------------------------------

For the final recommendation engine, I would keep:

id
name
genres
overview
original_language
vote_average
vote_count
popularity
number_of_seasons
number_of_episodes
episode_run_time
status
in_production
created_by
networks
origin_country

For dashboard/UI only:

poster_path
backdrop_path
homepage
tagline
production_companies
production_countries
spoken_languages
languages