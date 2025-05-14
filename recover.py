#!/usr/bin/env python3
import os
import sqlite3
import shutil
import tempfile
import argparse
from datetime import datetime, timedelta

def get_browser_paths():
    """Returns possible paths for Chrome and Vivaldi data directories."""
    home = os.path.expanduser("~")
    
    return {
        "chrome": [
            os.path.join(home, ".config/google-chrome/Default/"),
            os.path.join(home, ".var/app/com.google.Chrome/config/google-chrome/Default/")
        ],
        "vivaldi": [
            os.path.join(home, ".config/vivaldi/Default/"),
            os.path.join(home, ".var/app/com.vivaldi.Vivaldi/config/vivaldi/Default/")
        ]
    }

def find_valid_browser_path(browser_paths):
    """Finds the first valid browser data directory that contains a History file."""
    for path in browser_paths:
        history_path = os.path.join(path, "History")
        if os.path.exists(history_path):
            return path, history_path
    return None, None

def recover_browser_tabs(browser_type=None, days=1):
    """Recover tabs from Chrome or Vivaldi browser."""
    browser_paths = get_browser_paths()
    browsers_to_check = []
    
    if browser_type:
        if browser_type.lower() in browser_paths:
            browsers_to_check = [(browser_type, browser_paths[browser_type.lower()])]
        else:
            print(f"Unknown browser type: {browser_type}")
            return
    else:
        browsers_to_check = browser_paths.items()
    
    found_any = False
    
    for browser_name, paths in browsers_to_check:
        browser_dir, history_db = find_valid_browser_path(paths)
        
        if not browser_dir or not history_db:
            print(f"No valid {browser_name.title()} data directory found.")
            continue
            
        print(f"\n=== Recovering tabs from {browser_name.title()} ===")
        print(f"Using database at: {history_db}")
        found_any = True
        
        # Check session files
        session_files = ["Current Session", "Current Tabs", "Last Session", "Last Tabs"]
        print("\nSession files found:")
        for file_name in session_files:
            file_path = os.path.join(browser_dir, file_name)
            if os.path.exists(file_path):
                print(f"- {file_name} ({os.path.getsize(file_path)} bytes)")
        
        # Create a temporary copy of the database as it might be locked
        temp_dir = tempfile.mkdtemp()
        temp_history = os.path.join(temp_dir, "History")
        
        try:
            # Copy the database to temp location
            shutil.copy2(history_db, temp_history)
            
            # Connect to the database
            conn = sqlite3.connect(temp_history)
            cursor = conn.cursor()
            
            # Get recent URLs
            time_threshold = int((datetime.now() - timedelta(days=days)).timestamp() * 1000000)
            
            # Query the database for recent tabs
            cursor.execute("""
                SELECT url, title, last_visit_time 
                FROM urls 
                WHERE last_visit_time > ? 
                ORDER BY last_visit_time DESC
                LIMIT 100
            """, (time_threshold,))
            
            results = cursor.fetchall()
            
            if not results:
                print(f"\nNo {browser_name} tabs found in the last {days} day(s).")
            else:
                print(f"\nFound {len(results)} recently visited URLs in {browser_name.title()}:")
                for i, (url, title, timestamp) in enumerate(results, 1):
                    visit_time = datetime.fromtimestamp(timestamp / 1000000)
                    print(f"{i}. [{visit_time}] {title}")
                    print(f"   URL: {url}")
                    print()
                
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            # Clean up
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
    
    if not found_any:
        print("No browser data found. Make sure Chrome or Vivaldi is installed and has been used.")

def main():
    parser = argparse.ArgumentParser(description="Recover tabs from Chrome and Vivaldi browsers")
    parser.add_argument("--browser", choices=["chrome", "vivaldi"], 
                        help="Specify browser to recover tabs from (chrome or vivaldi). Default: both")
    parser.add_argument("--days", type=int, default=1, 
                        help="Number of days to look back for tabs (default: 1)")
    
    args = parser.parse_args()
    
    recover_browser_tabs(args.browser, args.days)

if __name__ == "__main__":
    main()