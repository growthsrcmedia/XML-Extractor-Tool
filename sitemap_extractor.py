#!/usr/bin/env python3
"""
XML Sitemap -> HTML URL Extractor (CSV Tool)

A lightweight command-line tool that extracts HTML page URLs from XML sitemaps.
Supports sitemap indexes and recursively follows nested sitemaps.

Usage:
    python sitemap_extractor.py <sitemap_url>
    
Example:
    python sitemap_extractor.py https://example.com/sitemap.xml

Output:
    sitemap_urls.csv - CSV file with a single column 'URL' containing all HTML URLs
"""

import sys
import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urlparse
import time
from typing import Set, List


# Configuration
REQUEST_TIMEOUT = 10  # seconds
REQUEST_DELAY = 0.5   # seconds between requests to be respectful
MAX_RETRIES = 3


def is_html_url(url: str) -> bool:
    """
    Check if a URL points to an HTML page.
    Filters out images, PDFs, videos, XML, and other non-HTML resources.
    """
    # Parse URL to get path
    parsed = urlparse(url)
    path = parsed.path.lower()
    
    # Non-HTML extensions to exclude
    non_html_extensions = {
        '.jpg', '.jpeg', '.png', '.gif', '.svg', '.webp', '.ico',  # Images
        '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',  # Documents
        '.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm',  # Videos
        '.mp3', '.wav', '.ogg', '.flac',  # Audio
        '.xml', '.rss', '.atom',  # XML feeds
        '.zip', '.rar', '.tar', '.gz',  # Archives
        '.css', '.js', '.json',  # Assets
        '.txt', '.csv',  # Text files
    }
    
    # Check if URL ends with a non-HTML extension
    for ext in non_html_extensions:
        if path.endswith(ext):
            return False
    
    # URLs without extensions or with .html/.htm are considered HTML
    # Also include URLs with query parameters or fragments
    if not path or path.endswith('/') or path.endswith('.html') or path.endswith('.htm'):
        return True
    
    # If there's no extension, assume it's HTML (common for modern websites)
    if '.' not in path.split('/')[-1]:
        return True
    
    # Default: include if not explicitly excluded
    return True


def fetch_sitemap(url: str) -> BeautifulSoup:
    """
    Fetch and parse an XML sitemap from a URL.
    Includes retry logic and error handling.
    """
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.get(url, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            
            # Parse XML
            soup = BeautifulSoup(response.content, 'xml')
            return soup
            
        except requests.exceptions.RequestException as e:
            if attempt < MAX_RETRIES - 1:
                print(f"Warning: Failed to fetch {url} (attempt {attempt + 1}/{MAX_RETRIES}). Retrying...")
                time.sleep(REQUEST_DELAY * (attempt + 1))  # Exponential backoff
            else:
                print(f"Error: Failed to fetch {url} after {MAX_RETRIES} attempts: {e}")
                raise
    
    raise Exception(f"Failed to fetch sitemap: {url}")


def is_sitemap_index(soup: BeautifulSoup) -> bool:
    """
    Check if the parsed XML is a sitemap index (contains <sitemap> tags)
    or a URL set (contains <url> tags).
    """
    # Sitemap index contains <sitemap> elements
    if soup.find('sitemap'):
        return True
    
    # URL set contains <url> elements
    if soup.find('url'):
        return False
    
    # If neither found, assume it's a URL set (most common case)
    return False


def extract_sitemap_urls(soup: BeautifulSoup) -> List[str]:
    """
    Extract sitemap URLs from a sitemap index.
    Returns a list of sitemap URLs to process.
    """
    sitemap_urls = []
    sitemap_tags = soup.find_all('sitemap')
    
    for sitemap_tag in sitemap_tags:
        loc_tag = sitemap_tag.find('loc')
        if loc_tag and loc_tag.text:
            sitemap_urls.append(loc_tag.text.strip())
    
    return sitemap_urls


def extract_page_urls(soup: BeautifulSoup) -> List[str]:
    """
    Extract page URLs from a URL set sitemap.
    Returns a list of HTML page URLs.
    """
    page_urls = []
    url_tags = soup.find_all('url')
    
    for url_tag in url_tags:
        loc_tag = url_tag.find('loc')
        if loc_tag and loc_tag.text:
            url = loc_tag.text.strip()
            # Only include HTML URLs
            if is_html_url(url):
                page_urls.append(url)
    
    return page_urls


def process_sitemap(url: str, visited: Set[str], all_urls: Set[str]) -> None:
    """
    Recursively process a sitemap URL.
    Handles both sitemap indexes and URL sets.
    
    Args:
        url: The sitemap URL to process
        visited: Set of already visited sitemap URLs (to prevent infinite loops)
        all_urls: Set to collect all HTML page URLs
    """
    # Prevent infinite loops
    if url in visited:
        return
    
    visited.add(url)
    print(f"Processing: {url}")
    
    try:
        # Fetch and parse sitemap
        soup = fetch_sitemap(url)
        
        # Small delay to be respectful to the server
        time.sleep(REQUEST_DELAY)
        
        # Check if it's a sitemap index or URL set
        if is_sitemap_index(soup):
            print(f"  -> Detected sitemap index, following child sitemaps...")
            child_sitemaps = extract_sitemap_urls(soup)
            print(f"  -> Found {len(child_sitemaps)} child sitemap(s)")
            
            # Recursively process each child sitemap
            for child_url in child_sitemaps:
                process_sitemap(child_url, visited, all_urls)
        else:
            print(f"  -> Detected URL set, extracting HTML URLs...")
            page_urls = extract_page_urls(soup)
            print(f"  -> Found {len(page_urls)} HTML URL(s)")
            
            # Add URLs to the collection (set automatically handles duplicates)
            all_urls.update(page_urls)
            
    except Exception as e:
        print(f"  X Error processing {url}: {e}")


def main():
    """
    Main function to run the sitemap extractor.
    """
    # Check command-line arguments
    if len(sys.argv) != 2:
        print("Usage: python sitemap_extractor.py <sitemap_url>")
        print("\nExample:")
        print("  python sitemap_extractor.py https://example.com/sitemap.xml")
        sys.exit(1)
    
    sitemap_url = sys.argv[1]
    
    print("=" * 60)
    print("XML Sitemap -> HTML URL Extractor")
    print("=" * 60)
    print(f"Starting extraction from: {sitemap_url}\n")
    
    # Track visited sitemaps and collected URLs
    visited_sitemaps: Set[str] = set()
    html_urls: Set[str] = set()
    
    # Process the sitemap recursively
    try:
        process_sitemap(sitemap_url, visited_sitemaps, html_urls)
    except KeyboardInterrupt:
        print("\n\nInterrupted by user. Saving progress...")
    except Exception as e:
        print(f"\n\nFatal error: {e}")
        sys.exit(1)
    
    # Convert to sorted list for consistent output
    sorted_urls = sorted(html_urls)
    
    # Create DataFrame and save to CSV
    df = pd.DataFrame({'URL': sorted_urls})
    output_file = 'sitemap_urls.csv'
    df.to_csv(output_file, index=False)
    
    # Print summary
    print("\n" + "=" * 60)
    print("Extraction Complete!")
    print("=" * 60)
    print(f"Total sitemaps processed: {len(visited_sitemaps)}")
    print(f"Total HTML URLs found: {len(html_urls)}")
    print(f"Output saved to: {output_file}")
    print("=" * 60)


if __name__ == '__main__':
    main()
