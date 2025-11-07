from config.api_keys import GOOGLE_MAPS_API_KEY, YELP_API_KEY
from src.api.google_client import GooglePlacesClient
from src.api.yelp_client import YelpClient

# Test Google
print("Testing Google Client...")
google = GooglePlacesClient(GOOGLE_MAPS_API_KEY)
results = google.search_places(42.3601, -71.0589, "museums", 5)
print(f"✅ Google returned {len(results)} results")

# Test Yelp
print("\nTesting Yelp Client...")
yelp = YelpClient(YELP_API_KEY)
results = yelp.search_businesses(42.3601, -71.0589, "museums", 5)
print(f"✅ Yelp returned {len(results)} results")

print("\n✅ Both clients working!")