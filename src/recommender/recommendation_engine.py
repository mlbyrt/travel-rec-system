"""
Recommendation Engine
Generates personalized travel recommendations
"""

import pandas as pd
from pathlib import Path
from config.config import CITIES, BUDGET_TIERS, PROCESSED_DATA_DIR

class RecommendationEngine:
    def __init__(self, city_name: str):
        """
        Initialize recommendation engine for a city
        
        Args:
            city_name: 'boston' or 'miami'
        """
        self.city_name = city_name
        self.city_config = CITIES[city_name]
        
        # Load processed data
        data_file = Path(PROCESSED_DATA_DIR) / f"{city_name}_places.parquet"
        if not data_file.exists():
            raise FileNotFoundError(
                f"No data found for {city_name}. Run collect_data.py first!"
            )
        
        self.places_df = pd.read_parquet(data_file)
        print(f"✅ Loaded {len(self.places_df)} places for {self.city_config['display_name']}")
    
    def get_recommendations(self, categories: list, budget_level: int, 
                           num_days: int, top_n: int = 20) -> pd.DataFrame:
        """
        Get personalized recommendations
        
        Args:
            categories: List of category preferences (e.g., ['food', 'cultural'])
            budget_level: 1-4 (Budget to Luxury)
            num_days: Number of days for the trip
            top_n: Number of recommendations to return
            
        Returns:
            DataFrame with top recommendations
        """
        print("\n" + "="*60)
        print("🎯 GENERATING RECOMMENDATIONS")
        print("="*60)
        print(f"City: {self.city_config['display_name']}")
        print(f"Categories: {', '.join(categories)}")
        print(f"Budget: {BUDGET_TIERS[budget_level]['name']} ({BUDGET_TIERS[budget_level]['range']})")
        print(f"Duration: {num_days} days")
        
        # Filter by categories
        filtered = self.places_df[self.places_df['category'].isin(categories)].copy()
        print(f"\n📍 Found {len(filtered)} places in selected categories")
        
        # Filter by budget
        filtered = self._filter_by_budget(filtered, budget_level)
        print(f"💰 After budget filter: {len(filtered)} places")
        
        if filtered.empty:
            print("❌ No places match your criteria!")
            return pd.DataFrame()
        
        # Calculate scores
        filtered = self._calculate_scores(filtered)
        
        # Sort by score
        recommendations = filtered.nlargest(top_n, 'score')
        
        return recommendations
    
    def get_top_famous_places(self, top_n: int = 5) -> pd.DataFrame:
        """
        Get the most famous/popular places regardless of category
        Based on review count and ratings
        
        Args:
            top_n: Number of places to return
            
        Returns:
            DataFrame with top famous places
        """
        df = self.places_df.copy()
        
        # Calculate fame score (heavily weight review count)
        df['fame_score'] = (
            df['rating'].fillna(0) * 0.3 +
            (df['review_count'].fillna(0) / 100) * 0.7  # Normalize reviews
        )
        
        top_places = df.nlargest(top_n, 'fame_score')
        
        return top_places
    
    def create_itinerary(self, categories: list, budget_level: int, 
                        num_days: int) -> dict:
        """
        Create a day-by-day itinerary
        
        Args:
            categories: List of category preferences
            budget_level: 1-4
            num_days: Number of days
            
        Returns:
            Dictionary with day-by-day recommendations
        """
        # Get recommendations
        all_recs = self.get_recommendations(
            categories, budget_level, num_days, 
            top_n=num_days * 5  # ~5 places per day
        )
        
        if all_recs.empty:
            return {}
        
        # Distribute across days
        places_per_day = len(all_recs) // num_days
        
        itinerary = {}
        for day in range(1, num_days + 1):
            start_idx = (day - 1) * places_per_day
            end_idx = start_idx + places_per_day if day < num_days else len(all_recs)
            
            day_places = all_recs.iloc[start_idx:end_idx]
            itinerary[f"Day {day}"] = day_places
        
        return itinerary
    
    def _filter_by_budget(self, df: pd.DataFrame, budget_level: int) -> pd.DataFrame:
        """Filter places by budget level"""
        # Include places at or below budget level, or places with no price data (0)
        return df[
            (df['price_estimate'] <= budget_level) | 
            (df['price_estimate'] == 0)
        ]
    
    def _calculate_scores(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calculate recommendation score for each place
        Score = weighted combination of rating and popularity
        """
        # Normalize review counts (log scale to handle wide range)
        import numpy as np
        df['review_score'] = np.log1p(df['review_count'].fillna(0))
        max_review_score = df['review_score'].max()
        if max_review_score > 0:
            df['review_score'] = df['review_score'] / max_review_score
        
        # Calculate final score
        df['score'] = (
            df['rating'].fillna(0) * 0.7 +      # 70% weight on rating
            df['review_score'] * 0.3            # 30% weight on popularity
        )
        
        return df
    
    def print_recommendations(self, recommendations: pd.DataFrame):
        """Pretty print recommendations"""
        print("\n" + "="*60)
        print("🌟 TOP RECOMMENDATIONS")
        print("="*60)
        
        for idx, (_, place) in enumerate(recommendations.iterrows(), 1):
            rating_display = f"{place['rating']:.1f}⭐" if pd.notna(place['rating']) else "No rating"
            price_display = '$' * int(place['price_estimate']) if place['price_estimate'] > 0 else 'Free/Unknown'
            
            print(f"\n{idx}. {place['name']}")
            print(f"   📍 {place['address']}")
            print(f"   ⭐ {rating_display} ({int(place['review_count']):,} reviews)")
            print(f"   💰 {price_display}")
            print(f"   🏷️  {place['category']}")
            print(f"   🔗 {place.get('google_maps_url', place.get('yelp_url', 'N/A'))}")
            print(f"   📊 Score: {place['score']:.2f}")
    
    def print_itinerary(self, itinerary: dict):
        """Pretty print day-by-day itinerary"""
        print("\n" + "="*60)
        print("📅 YOUR PERSONALIZED ITINERARY")
        print("="*60)
        
        for day_name, places in itinerary.items():
            print(f"\n{'='*60}")
            print(f"📆 {day_name.upper()}")
            print(f"{'='*60}")
            
            for idx, (_, place) in enumerate(places.iterrows(), 1):
                rating_display = f"{place['rating']:.1f}⭐" if pd.notna(place['rating']) else "No rating"
                price_display = '$' * int(place['price_estimate']) if place['price_estimate'] > 0 else 'Free'
                
                print(f"\n  {idx}. {place['name']}")
                print(f"      📍 {place['address'][:50]}...")
                print(f"      ⭐ {rating_display} | 💰 {price_display} | 🏷️ {place['category']}")
    
    def get_statistics(self) -> dict:
        """Get dataset statistics"""
        return {
            'total_places': len(self.places_df),
            'by_category': self.places_df['category'].value_counts().to_dict(),
            'by_source': self.places_df['source'].value_counts().to_dict(),
            'avg_rating': self.places_df['rating'].mean(),
            'total_reviews': self.places_df['review_count'].sum(),
            'price_coverage': (self.places_df['price_level'] > 0).sum() / len(self.places_df) * 100
        }