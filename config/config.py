"""
Project Configuration
Settings for cities, categories, and API parameters
"""

# City configurations with coordinates
CITIES = {
    "boston": {
        "display_name": "Boston, MA",
        "coordinates": {"lat": 42.3601, "lng": -71.0589},
        "radius": 15000  # 15km search radius
    },
    "miami": {
        "display_name": "Miami, FL",
        "coordinates": {"lat": 25.7617, "lng": -80.1918},
        "radius": 15000
    }
}

# Travel categories and their search keywords
CATEGORY_KEYWORDS = {
    "leisure": ["spa", "beach", "resort", "relaxation", "massage"],
    "adventure": ["hiking", "water sports", "kayaking", "adventure tour", "snorkeling"],
    "physical_activity": ["gym", "yoga studio", "fitness", "cycling", "running trail"],
    "nightlife": ["bar", "nightclub", "lounge", "live music", "dance club"],
    "cultural": ["museum", "art gallery", "theater", "historical site", "cultural center"],
    "food": ["restaurant", "cafe", "food tour", "brunch", "dining"],
    "nature": ["park", "botanical garden", "nature reserve", "beach", "hiking trail"],
    "shopping": ["shopping mall", "market", "boutique", "shopping district"],
    "family": ["zoo", "aquarium", "children's museum", "family activities", "amusement park"]
}

# Default price levels by category (1-4 scale, 0 = free/unknown)
# Used when real price data is not available
DEFAULT_PRICE_BY_CATEGORY = {
    "food": None,           # Will use Yelp's actual price data
    "nightlife": None,      # Will use Yelp's actual price data
    "cultural": 2,          # Museums typically $15-30
    "adventure": 3,         # Tours/activities typically $50-100
    "nature": 1,            # Parks/trails often free or low cost
    "leisure": 2,           # Spas/resorts vary, default moderate
    "physical_activity": 2, # Gyms/classes $15-30
    "shopping": 2,          # Varies widely
    "family": 2             # Kid activities $15-40
}

# Budget tier definitions (price per person per day)
BUDGET_TIERS = {
    1: {"name": "Budget", "range": "$0-50/day", "description": "Free attractions, affordable dining"},
    2: {"name": "Moderate", "range": "$50-150/day", "description": "Mix of activities, mid-range dining"},
    3: {"name": "Comfortable", "range": "$150-300/day", "description": "Most attractions, nice restaurants"},
    4: {"name": "Luxury", "range": "$300+/day", "description": "Premium experiences, fine dining"}
}

# API endpoints
GOOGLE_PLACES_BASE_URL = "https://places.googleapis.com/v1/places"
YELP_BASE_URL = "https://api.yelp.com/v3"

# Cache settings
CACHE_DIR = "data/raw/cache"
CACHE_EXPIRY_DAYS = 30

# Data collection settings
MAX_RESULTS_PER_QUERY = 20  # Max for Google Places (New) API
RESULTS_PER_CATEGORY = 20   # How many places to fetch per category

# Processed data directory
PROCESSED_DATA_DIR = "data/processed"