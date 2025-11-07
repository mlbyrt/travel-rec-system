"""
Yelp Fusion API Client
Handles all interactions with Yelp API
"""

import requests
import pandas as pd

class YelpClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.yelp.com/v3"
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}'
        })
        self.call_count = 0
    
    def search_businesses(self, lat: float, lng: float, term: str, 
                         limit: int = 20) -> pd.DataFrame:
        """
        Search for businesses by coordinates and term
        
        Args:
            lat: Latitude
            lng: Longitude
            term: Search term (e.g., "museums", "restaurants")
            limit: Max results (max 50 per call, but we use 20 to match Google)
            
        Returns:
            DataFrame with business information
        """
        url = f"{self.base_url}/businesses/search"
        
        params = {
            'latitude': lat,
            'longitude': lng,
            'term': term,
            'limit': min(limit, 50),
            'radius': 10000  # 10km radius
        }
        
        try:
            response = self.session.get(url, params=params)
            self.call_count += 1
            response.raise_for_status()
            
            data = response.json()
            businesses = self._parse_businesses_response(data)
            
            return pd.DataFrame(businesses)
            
        except requests.exceptions.RequestException as e:
            print(f"Yelp API Error: {e}")
            return pd.DataFrame()
    
    def _parse_businesses_response(self, data: dict) -> list:
        """Parse API response into list of business dictionaries"""
        businesses = []
        
        for biz in data.get('businesses', []):
            businesses.append({
                'place_id': biz.get('id', ''),
                'name': biz.get('name', ''),
                'address': ', '.join(biz.get('location', {}).get('display_address', [])),
                'latitude': biz.get('coordinates', {}).get('latitude'),
                'longitude': biz.get('coordinates', {}).get('longitude'),
                'rating': biz.get('rating'),
                'review_count': biz.get('review_count', 0),
                'price_level': self._normalize_price(biz.get('price', '')),
                'categories': ','.join([cat['title'] for cat in biz.get('categories', [])]),
                'phone': biz.get('phone', ''),
                'yelp_url': biz.get('url', ''),
                'image_url': biz.get('image_url', ''),
                'source': 'yelp'
            })
        
        return businesses
    
    def _normalize_price(self, price_str: str) -> int:
        """
        Convert Yelp's $ symbols to 0-4 scale
        """
        if not price_str:
            return 0
        return len(price_str)  # $=1, $$=2, $$$=3, $$$$=4
    
    def get_call_count(self) -> int:
        """Return number of API calls made"""
        return self.call_count