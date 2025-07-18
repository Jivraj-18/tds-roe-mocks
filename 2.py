
# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "requests",
# ]
# ///

import requests
import sys
from collections import defaultdict

def get_related_tags(tag, site="stackoverflow"):
    """Get tags related to a given tag from StackOverflow API."""
    url = f"https://api.stackexchange.com/2.3/tags/{tag}/related"
    params = {
        "site": site,
        "pagesize": 100  # Get more results to find the highest counts
    }
    
    try:
        resp = requests.get(url, params=params)
        resp.raise_for_status()
        data = resp.json()
        
        related = {}
        for item in data.get("items", []):
            related[item["name"]] = item["count"]
        
        return related
    except requests.RequestException as e:
        print(f"Error fetching data for tag '{tag}': {e}")
        return {}

def find_highest_combined_tag(tag1, tag2):
    """Find the tag with highest combined common question count with two given tags."""
    
    # Get related tags for both tags
    print(f"Fetching related tags for '{tag1}'...")
    tag1_related = get_related_tags(tag1)
    
    print(f"Fetching related tags for '{tag2}'...")
    tag2_related = get_related_tags(tag2)
    
    if not tag1_related or not tag2_related:
        print("Failed to fetch related tags")
        return None, None
    
    # Combine counts for each tag
    combined_counts = defaultdict(int)
    
    # Add tag1-related counts
    for tag, count in tag1_related.items():
        combined_counts[tag] += count
    
    # Add tag2-related counts
    for tag, count in tag2_related.items():
        combined_counts[tag] += count
    
    # Remove the original tags themselves from results
    if tag1 in combined_counts:
        del combined_counts[tag1]
    if tag2 in combined_counts:
        del combined_counts[tag2]
    
    if not combined_counts:
        return None, None
    
    # Find the tag with highest combined count
    max_tag = max(combined_counts, key=lambda t: combined_counts[t])
    max_count = combined_counts[max_tag]
    
    return max_tag, max_count

if __name__ == "__main__":
    # Check if correct number of arguments provided
    if len(sys.argv) != 3:
        print("Usage: python 2.py <tag1> <tag2>")
        print("Example: python 2.py angular swift")
        print("Example: python 2.py angular typescript")
        sys.exit(1)
    
    # Get tags from command line arguments
    tag1 = sys.argv[1]
    tag2 = sys.argv[2]
    
    print(f"Finding tag with highest combined common question count with '{tag1}' and '{tag2}'...")
    print("=" * 80)
    
    result_tag, result_count = find_highest_combined_tag(tag1, tag2)
    
    if result_tag:
        print(f"\nResult:")
        print(f"Tag: {result_tag}")
        print(f"Combined count: {result_count}")
        print(f"\nAnswer: {result_tag}")
    else:
        print("No result found.")
