import requests
import json
import time
import csv
import os
from datetime import datetime
from typing import List, Dict, Optional

class JikanScraper:
    def __init__(self, base_url: str = "https://api.jikan.moe/v4/anime"):
        self.base_url = base_url
        self.session = requests.Session()
        
    def scrape_page(self, page: int, max_retries: int = 3) -> Optional[List[Dict]]:
        """
        Scrape a single page with retry logic
        """
        for attempt in range(max_retries):
            try:
                url = f"{self.base_url}?page={page}"
                response = self.session.get(url, timeout=10)
                
                if response.status_code == 429:
                    wait_time = 2 ** attempt  # Exponential backoff
                    print(f"Rate limited. Waiting {wait_time} seconds...")
                    time.sleep(wait_time)
                    continue
                    
                response.raise_for_status()
                data = response.json()
                
                return self._extract_anime_data(data, page)
                
            except requests.exceptions.RequestException as e:
                print(f"Attempt {attempt + 1} failed for page {page}: {e}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
                else:
                    print(f"Failed to scrape page {page} after {max_retries} attempts")
                    return None
                    
        return None
    
    def _extract_anime_data(self, api_response: Dict, page: int) -> List[Dict]:
        """
        Extract required fields from API response
        """
        scraped_data = []
        
        for index, anime in enumerate(api_response.get('data', [])):
            # Get default title
            default_title = next(
                (title['title'] for title in anime.get('titles', []) 
                 if title.get('type') == 'Default'),
                anime.get('title')
            )
            
            # --- KEY CHANGE HERE ---
            # Extract genres and join them into a single string immediately
            genre_list = [genre['name'] for genre in anime.get('genres', [])]
            genres_string = ", ".join(genre_list) 
            
            # Calculate new reset ID (sequential from 1)
            reset_id = (page - 1) * 25 + index + 1
            
            anime_info = {
                'id': reset_id,
                'title': default_title,
                'score': anime.get('score'),
                'scored_by': anime.get('scored_by'),
                'rank': anime.get('rank'),
                'popularity': anime.get('popularity'),
                'members': anime.get('members'),
                'favorites': anime.get('favorites'),
                'genres': genres_string,  # Stored as "Action, Comedy" in one cell
            }
            
            scraped_data.append(anime_info)
        
        return scraped_data
    
    def scrape_range(self, start_page: int, end_page: int, delay: float = 0.5) -> List[Dict]:
        """
        Scrape a range of pages
        """
        all_data = []
        
        for page in range(start_page, end_page + 1):
            print(f"Scraping page {page}/{end_page}...")
            
            page_data = self.scrape_page(page)
            if page_data:
                all_data.extend(page_data)
                print(f"  ✓ Found {len(page_data)} anime")
            else:
                print(f"  ✗ Failed to scrape page {page}")
            
            # Rate limiting
            if page < end_page:
                time.sleep(delay)
        
        return all_data

def save_to_csv(data: List[Dict], filename: str):
    """Save data to CSV with single genres column"""
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        # Define field order
        fieldnames = ['id', 'title', 'score', 'scored_by', 'rank', 
                      'popularity', 'members', 'favorites', 'genres']
        
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    print(f"💾 CSV saved: {filename}")

def save_to_json(data: List[Dict], filename: str):
    """Save data to JSON"""
    with open(filename, 'w', encoding='utf-8') as jsonfile:
        json.dump(data, jsonfile, indent=2, ensure_ascii=False)
    print(f"💾 JSON saved: {filename}")

def display_sample_data(data: List[Dict], sample_size: int = 3):
    """
    Display sample data 
    """
    print(f"\n📝 SAMPLE DATA (first {sample_size} records):")
    print("=" * 60)
    
    for i, anime in enumerate(data[:sample_size]):
        print(f"\n🎬 Sample #{i + 1}:")
        print(f"   ID: {anime['id']}")
        print(f"   Title: {anime['title'][:60]}..." if len(anime['title']) > 60 else f"   Title: {anime['title']}")
        print(f"   Score: {anime['score']}")
        print(f"   Genres: {anime['genres']}") # Simply prints the string now

def main():
    """
    Main function
    """
    print("🚀 Jikan MAL API Scraper - Single Column Genres")
    print("=" * 60)
    
    # Initialize scraper
    scraper = JikanScraper()
    
    # Configuration
    START_PAGE = 1
    END_PAGE = 1180  # Reduced for testing, change back to 200 if needed
    DELAY_BETWEEN_REQUESTS = 0.5
    
    print(f"Scraping pages {START_PAGE} to {END_PAGE}")
    
    start_time = time.time()
    
    # Scrape data
    all_anime_data = scraper.scrape_range(START_PAGE, END_PAGE, DELAY_BETWEEN_REQUESTS)
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    if all_anime_data:
        print("\n" + "=" * 60)
        print("📊 SCRAPING COMPLETED")
        print(f"Total anime scraped: {len(all_anime_data)}")
        print(f"Time elapsed: {elapsed_time:.2f} seconds")
        
        # Create output directory
        os.makedirs('output', exist_ok=True)
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_filename = f"output/anime_list_{timestamp}.csv"
        json_filename = f"output/anime_list_{timestamp}.json"
        
        # Save files
        save_to_csv(all_anime_data, csv_filename)
        save_to_json(all_anime_data, json_filename)
        
        # Display sample
        display_sample_data(all_anime_data, sample_size=3)
        
    else:
        print("❌ No data was scraped. Please check your connection or API status.")

if __name__ == "__main__":
    main()