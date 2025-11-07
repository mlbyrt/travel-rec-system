"""
Demo Recommendations
Test the recommendation engine
"""

from src.recommender.recommendation_engine import RecommendationEngine

def main():
    print("\n" + "="*70)
    print(" " * 20 + "TRAVEL RECOMMENDATION DEMO")
    print("="*70)
    
    # Example 1: Boston - Cultural & Food, Moderate Budget, 3 days
    print("\n" + "🟦" * 35)
    print("EXAMPLE 1: Boston Cultural Food Tour")
    print("🟦" * 35)
    
    engine_boston = RecommendationEngine('boston')
    
    # Get top 10 recommendations
    recs = engine_boston.get_recommendations(
        categories=['food', 'cultural'],
        budget_level=2,  # Moderate
        num_days=3,
        top_n=10
    )
    
    engine_boston.print_recommendations(recs)
    
    # Get top 5 famous places
    print("\n" + "="*60)
    print("🏆 TOP 5 MOST FAMOUS PLACES IN BOSTON")
    print("="*60)
    
    famous = engine_boston.get_top_famous_places(5)
    for idx, (_, place) in enumerate(famous.iterrows(), 1):
        print(f"\n{idx}. {place['name']}")
        print(f"   ⭐ {place['rating']:.1f} ({int(place['review_count']):,} reviews)")
        print(f"   🏷️ {place['category']}")
    
    # Create 3-day itinerary
    print("\n" + "="*60)
    itinerary = engine_boston.create_itinerary(
        categories=['food', 'cultural', 'nightlife'],
        budget_level=2,
        num_days=3
    )
    engine_boston.print_itinerary(itinerary)
    
    # Example 2: Miami - Beach & Nightlife, Comfortable Budget, 2 days
    print("\n\n" + "🟨" * 35)
    print("EXAMPLE 2: Miami Beach & Nightlife")
    print("🟨" * 35)
    
    engine_miami = RecommendationEngine('miami')
    
    recs_miami = engine_miami.get_recommendations(
        categories=['nightlife', 'food'],
        budget_level=3,  # Comfortable
        num_days=2,
        top_n=8
    )
    
    engine_miami.print_recommendations(recs_miami)
    
    # Statistics
    print("\n" + "="*70)
    print("📊 DATASET STATISTICS")
    print("="*70)
    
    boston_stats = engine_boston.get_statistics()
    miami_stats = engine_miami.get_statistics()
    
    print(f"\n🟦 BOSTON:")
    print(f"   Total places: {boston_stats['total_places']}")
    print(f"   Avg rating: {boston_stats['avg_rating']:.2f}")
    print(f"   Total reviews: {boston_stats['total_reviews']:,}")
    
    print(f"\n🟨 MIAMI:")
    print(f"   Total places: {miami_stats['total_places']}")
    print(f"   Avg rating: {miami_stats['avg_rating']:.2f}")
    print(f"   Total reviews: {miami_stats['total_reviews']:,}")
    
    print("\n" + "="*70)
    print("✅ Demo complete! Your recommendation system is working!")
    print("="*70)

if __name__ == "__main__":
    main()