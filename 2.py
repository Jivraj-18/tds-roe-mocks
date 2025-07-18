#!/usr/bin/env python3
# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "requests>=2.25.0",
# ]
# ///
"""
Stack Overflow Tag Analysis Script

This script mimics the JavaScript validation logic to find the tag with the highest 
combined common question count with two randomly selected tags.

Uses the Stack Exchange API v2.3 tags/{tags}/related endpoint.

Author: Tag Analysis Script
Date: 2025-07-18
"""

import requests
import sys
import hashlib
import random
from typing import Dict, List, Tuple, Optional
from time import sleep

# Stack Exchange API base URL
API_BASE_URL = "https://api.stackexchange.com/2.3"
SITE = "stackoverflow"

# Predefined tags list from JavaScript
TAGS_LIST = [
    "javascript", "python", "java", "php", "android", "html", "jquery", "css", "ios", "sql",
    "mysql", "r", "reactjs", "node.js", "arrays", "c", "json", "ruby-on-rails", "sql-server",
    "swift", "django", "angular", "objective-c", "excel", "pandas", "angularjs", "regex",
    "typescript", "ruby", "linux", "ajax", "iphone", "vba", "xml", "laravel", "spring",
    "database", "wordpress", "string", "flutter", "postgresql", "mongodb", "wpf", "windows",
    "amazon-web-services"
]

def seeded_random_selection(seed_string: str) -> Tuple[str, str]:
    """
    Simulate the JavaScript seeded random selection.
    Uses a hash of the seed string to initialize Python's random module.
    """
    # Create a hash of the seed string to get a numeric seed
    seed_hash = hashlib.md5(seed_string.encode()).hexdigest()
    seed_int = int(seed_hash[:8], 16)  # Use first 8 hex chars as seed
    
    # Initialize random with the seed
    random.seed(seed_int)
    
    # Shuffle the tags list and select first 2
    shuffled_tags = TAGS_LIST.copy()
    random.shuffle(shuffled_tags)
    
    return shuffled_tags[0], shuffled_tags[1]

def get_related_tags(tag: str, pagesize: int = 20) -> List[Dict]:
    """
    Get related tags for a given tag using the Stack Exchange API.
    
    Args:
        tag: The tag to find related tags for
        pagesize: Number of results to return (default 20 to match JavaScript)
    
    Returns:
        List of dictionaries containing related tag information
    """
    url = f"{API_BASE_URL}/tags/{tag}/related"
    
    params = {
        'site': SITE,
        'pagesize': pagesize
    }
    
    try:
        print(f"Fetching related tags for '{tag}'...")
        response = requests.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        if 'items' in data:
            print(f"Found {len(data['items'])} related tags for '{tag}'")
            return data['items']
        else:
            print(f"No related tags found for '{tag}'")
            return []
            
    except requests.exceptions.RequestException as e:
        print(f"Error fetching related tags for '{tag}': {e}")
        return []
    except Exception as e:
        print(f"Unexpected error: {e}")
        return []

def process_related_tags(tag1_data: List[Dict], tag2_data: List[Dict], exclude_tags: List[str]) -> str:
    """
    Process related tags data to find the tag with highest combined common question count.
    This mimics the JavaScript logic exactly.
    
    Args:
        tag1_data: List of tag dictionaries from first API response
        tag2_data: List of tag dictionaries from second API response
        exclude_tags: List of tags to exclude from the result
    
    Returns:
        The tag name with the highest combined count
    """
    combined_counts = {}
    
    # Process first tag's related tags
    for tag in tag1_data:
        tag_name = tag.get('name', '')
        count = tag.get('count', 0)
        if tag_name:
            combined_counts[tag_name] = combined_counts.get(tag_name, 0) + count
    
    # Process second tag's related tags
    for tag in tag2_data:
        tag_name = tag.get('name', '')
        count = tag.get('count', 0)
        if tag_name:
            combined_counts[tag_name] = combined_counts.get(tag_name, 0) + count
    
    # Sort by combined count (descending) and find first tag not in exclude list
    sorted_tags = sorted(combined_counts.items(), key=lambda x: x[1], reverse=True)
    
    for tag_name, count in sorted_tags:
        if tag_name not in exclude_tags:
            print(f"Best tag: {tag_name} with combined count: {count}")
            return tag_name
    
    return ""

def main():
    """
    Main function to analyze Stack Overflow tags using the JavaScript validation logic.
    """
    print("Stack Overflow Tag Analysis (JavaScript-compatible)")
    print("=" * 55)
    
    # Check if command line arguments are provided
    if len(sys.argv) == 3:
        tag1 = sys.argv[1].lower()
        tag2 = sys.argv[2].lower()
        print(f"Using command line arguments: {tag1} and {tag2}")
    elif len(sys.argv) == 1:
        # Default behavior - test both combinations
        print("No arguments provided. Testing both combinations...")
        
        # Test angular and swift
        print("\nTEST: angular and swift")
        print("=" * 30)
        
        angular_related = get_related_tags('angular')
        sleep(0.1)
        swift_related = get_related_tags('swift')
        
        angular_swift_best = process_related_tags(angular_related, swift_related, ['angular', 'swift'])
        print(f"Best tag for angular + swift: {angular_swift_best}")
        
        # Test r and database
        print(f"\nTEST: r and database")
        print("=" * 30)
        
        r_related = get_related_tags('r')
        sleep(0.1)
        database_related = get_related_tags('database')
        
        r_database_best = process_related_tags(r_related, database_related, ['r', 'database'])
        print(f"Best tag for r + database: {r_database_best}")
        
        return
    else:
        print("Usage: python 2.py [tag1] [tag2]")
        print("Example: python 2.py r database")
        print("Example: python 2.py angular swift")
        print("If no arguments provided, will test both angular+swift and r+database")
        return
    
    # Analyze the specified tags
    print(f"\nAnalyzing tags: {tag1} and {tag2}")
    print("=" * 55)
    
    # Fetch related tags for both specified tags
    tag1_related = get_related_tags(tag1)
    sleep(0.1)
    tag2_related = get_related_tags(tag2)
    
    # Process the data to find the best combined tag
    best_tag = process_related_tags(tag1_related, tag2_related, [tag1, tag2])
    
    print(f"\n" + "=" * 55)
    print("FINAL RESULT")
    print("=" * 55)
    print(f"Tags analyzed: {tag1} and {tag2}")
    print(f"Best combined tag: {best_tag}")

if __name__ == "__main__":
    main()
