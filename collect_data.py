"""
Data Collection Script
Run this to collect data for Boston and Miami
"""

from src.data.data_collector import DataCollector

def main():
    print("\n" + "="*70)
    print(" " * 15 + "TRAVEL REC SYSTEM - DATA COLLECTION")
    print("="*70)
    
    collector = DataCollector()
    
    # Choose which cities and categories to collect
    # Start with a subset to test, then expand
    
    # Option 1: Collect ALL categories for a city (many API calls!)
    # boston_data = collector.collect_city_data('boston')
    
    # Option 2: Collect specific categories (recommended for testing)
    test_categories = ['food', 'cultural', 'nightlife']
    
    print("\n🎯 STRATEGY: Collecting limited categories first to test")
    print(f"   Categories: {test_categories}")
    print(f"   This will make ~{len(test_categories) * 5 * 2} API calls per city")
    print(f"   (2 APIs × 5 keywords/category × {len(test_categories)} categories)")
    
    input("\nPress Enter to continue or Ctrl+C to cancel...")
    
    # Collect Boston data
    print("\n" + "🟦" * 35)
    boston_data = collector.collect_city_data('boston', categories=test_categories)
    
    # Collect Miami data
    print("\n" + "🟨" * 35)
    miami_data = collector.collect_city_data('miami', categories=test_categories)
    
    # Final summary
    print("\n" + "="*70)
    print("🎉 DATA COLLECTION COMPLETE!")
    print("="*70)
    
    stats = collector.get_usage_stats()
    print(f"\n📊 TOTAL API USAGE:")
    print(f"   Google Places: {stats['google_calls']} calls")
    print(f"   Yelp: {stats['yelp_calls']} calls")
    print(f"   Total API calls: {stats['total_calls']}")
    print(f"\n   Free tier remaining (Google): {10000 - stats['google_calls']:,} calls")
    print(f"   Free tier remaining (Yelp): {5000 - stats['yelp_calls']:,} calls/day")
    
    print(f"\n💾 DATA SAVED TO:")
    print(f"   data/processed/boston_places.parquet")
    print(f"   data/processed/boston_places.csv")
    print(f"   data/processed/miami_places.parquet")
    print(f"   data/processed/miami_places.csv")
    
    print("\n✅ Next steps:")
    print("   1. Inspect the CSV files to see your data")
    print("   2. Run this script again - should use cache (0 new API calls!)")
    print("   3. Ready to build recommendation engine!")
    
    print("\n" + "="*70)

if __name__ == "__main__":
    main()
    