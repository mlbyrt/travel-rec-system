"""
Google Places API Client
Handles all interactions with Google Places API (New)
"""

import requests
import pandas as pd
from typing import Optional

class GooglePlacesClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://places.googleapis.com/v1/places"
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'X-Goog-Api-Key': api_key,
            'X-Goog-FieldMask': (
                'places.id,'
                'places.displayName,'
                'places.formattedAddress,'
                'places.location,'
                'places.rating,'
                'places.userRatingCount,'
                'places.priceLevel,'
                'places.types,'
                'places.websiteUri,'
                'places.googleMapsUri'
            )
        })
        self.call_count = 0
    
    def search_places(self, lat: float, lng: float, keyword: str, 
                     max_results: int = 20) -> pd.DataFrame:
        """
        Search for places near a location by keyword
        
        Args:
            lat: Latitude
            lng: Longitude
            keyword: Search keyword (e.g., "museums", "restaurants")
            max_results: Maximum results (max 20 per call)
            
        Returns:
            DataFrame with place information
        """
        url = f"{self.base_url}:searchText"
        
        payload = {
            "textQuery": f"{keyword} near {lat},{lng}",
            "maxResultCount": min(max_results, 20),
            "locationBias": {
                "circle": {
                    "center": {
                        "latitude": lat,
                        "longitude": lng
                    },
                    "radius": 10000
                }
            }
        }
        
        try:
            response = self.session.post(url, json=payload)
            self.call_count += 1
            response.raise_for_status()
            
            data = response.json()
            places = self._parse_places_response(data)
            
            return pd.DataFrame(places)
            
        except requests.exceptions.RequestException as e:
            print(f"Google API Error: {e}")
            return pd.DataFrame()
    
    def _parse_places_response(self, data: dict) -> list:
        """Parse API response into list of place dictionaries"""
        places = []
        
        for place in data.get('places', []):
            places.append({
                'place_id': place.get('id', ''),
                'name': place.get('displayName', {}).get('text', ''),
                'address': place.get('formattedAddress', ''),
                'latitude': place.get('location', {}).get('latitude'),
                'longitude': place.get('location', {}).get('longitude'),
                'rating': place.get('rating'),
                'review_count': place.get('userRatingCount', 0),
                'price_level': self._normalize_price_level(place.get('priceLevel')),
                'types': ','.join(place.get('types', [])),
                'website': place.get('websiteUri', ''),
                'google_maps_url': place.get('googleMapsUri', ''),
                'source': 'google'
            })
        
        return places
    
    def _normalize_price_level(self, price_str: str) -> int:
        """
        Convert Google's price level string to 0-4 scale
        """
        if not price_str:
            return 0
        
        price_map = {
            'PRICE_LEVEL_FREE': 0,
            'PRICE_LEVEL_INEXPENSIVE': 1,
            'PRICE_LEVEL_MODERATE': 2,
            'PRICE_LEVEL_EXPENSIVE': 3,
            'PRICE_LEVEL_VERY_EXPENSIVE': 4,
            'PRICE_LEVEL_UNSPECIFIED': 0
        }
        
        return price_map.get(price_str, 0)
    
    def get_call_count(self) -> int:
        """Return number of API calls made"""
        return self.call_count