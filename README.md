# 🌎 Travel Recommendation System

A travel recommendation system for Boston and Miami that provides personalized place recommendations based on user preferences, budget, and trip duration.

## Features

- **Personalized Recommendations**: Filter by categories (food, cultural, nightlife, etc.) and budget level
- **Smart Caching**: Efficient API response caching to minimize costs and improve performance
- **Multi-Source Data**: Combines data from Google Places API and Yelp Fusion API
- **Budget-Aware**: 4-tier budget system with intelligent price estimation
- **Top Famous Places**: Identifies the most popular attractions
- **Multi-Day Itineraries**: Automatically generates day-by-day travel plans
- **200+ Places**: Comprehensive dataset for Boston and Miami

## Technologies

- **Python 3.8+**
- **Pandas**: Data processing and analysis
- **Google Places API (New)**: Location and place data
- **Yelp Fusion API**: Reviews, ratings, and business information
- **Parquet**: Efficient data caching and storage

## Project Structure
```
travel-rec-system/
├── config/
│   ├── config.py              # Project settings and constants
│   └── api_keys.py            # API keys (not tracked in git)
├── src/
│   ├── api/
│   │   ├── google_client.py   # Google Places API wrapper
│   │   └── yelp_client.py     # Yelp API wrapper
│   ├── data/
│   │   ├── cache_manager.py   # Smart caching system
│   │   └── data_collector.py  # Data collection orchestrator
│   └── recommender/
│       └── recommendation_engine.py  # Recommendation logic
├── data/
│   ├── raw/cache/             # Cached API responses
│   └── processed/             # Processed datasets
├── notebooks/
│   └── 01_api_testing.ipynb   # API exploration notebook
├── collect_data.py            # Data collection script
├── demo_recommendations.py    # Demo script
└── requirements.txt           # Python dependencies
```

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Google Maps Platform API key ([Get one here](https://console.cloud.google.com/))
- Yelp Fusion API key ([Get one here](https://www.yelp.com/developers))

### Installation

1. **Clone the repository**
```bash
   git clone https://github.com/YOUR_USERNAME/travel-rec-system.git
   cd travel-rec-system
```

2. **Install dependencies**
```bash
   pip install -r requirements.txt
```

3. **Set up API keys**
   
   Create `config/api_keys.py`:
```python
   # config/api_keys.py
   GOOGLE_MAPS_API_KEY = "your_google_api_key_here"
   YELP_API_KEY = "your_yelp_api_key_here"
```

4. **Collect data**
```bash
   python collect_data.py
```
   
   This will fetch data for Boston and Miami (uses ~60 API calls, all cached for future use)

5. **Run the demo**
```bash
   python demo_recommendations.py
```

## Usage Examples

### Basic Recommendation
```python
from src.recommender.recommendation_engine import RecommendationEngine

# Initialize for a city
engine = RecommendationEngine('boston')

# Get recommendations
recommendations = engine.get_recommendations(
    categories=['food', 'cultural'],
    budget_level=2,  # Moderate budget
    num_days=3,
    top_n=10
)

# Display results
engine.print_recommendations(recommendations)
```

### Top Famous Places
```python
# Get the 5 most famous places
famous = engine.get_top_famous_places(5)
print(famous)
```

### Multi-Day Itinerary
```python
# Generate a 3-day itinerary
itinerary = engine.create_itinerary(
    categories=['food', 'cultural', 'nightlife'],
    budget_level=2,
    num_days=3
)

engine.print_itinerary(itinerary)
```

## Recommendation Algorithm

The system uses **content-based filtering** with a weighted scoring system:

- **Rating (70%)**: Quality of the place
- **Popularity (30%)**: Number of reviews (log-normalized)
```python
score = (rating * 0.7) + (log(review_count) / max_log * 0.3)
```

This ensures high-quality places are prioritized while still considering popularity.

## Budget Tiers

| Level | Name | Range | Description |
|-------|------|-------|-------------|
| 1 | Budget | $0-50/day | Free attractions, affordable dining |
| 2 | Moderate | $50-150/day | Mix of activities, mid-range dining |
| 3 | Comfortable | $150-300/day | Most attractions, nice restaurants |
| 4 | Luxury | $300+/day | Premium experiences, fine dining |

## Available Categories

- **leisure**: Spa, beach, resort, relaxation
- **adventure**: Hiking, water sports, outdoor activities
- **physical_activity**: Gym, yoga, fitness, cycling
- **nightlife**: Bars, clubs, live music
- **cultural**: Museums, theaters, art galleries
- **food**: Restaurants, cafes, food tours
- **nature**: Parks, gardens, trails
- **shopping**: Malls, markets, boutiques
- **family**: Zoo, aquarium, kid-friendly activities

## Supported Cities

- Boston, MA
- Miami, FL

## Future Enhancements

- [ ] Add more cities (NYC, SF, LA, etc.)
- [ ] Web UI with Streamlit
- [ ] Distance-based optimization for itineraries
- [ ] Review text analysis and sentiment scoring
- [ ] Map visualization of recommendations
- [ ] Export itineraries to PDF
- [ ] User preference learning over time
