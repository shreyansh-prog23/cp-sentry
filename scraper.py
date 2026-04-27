#!/usr/bin/env python3
"""
CP-Sentry: Contest Scraper
Fetches upcoming contests from clist.by API for LeetCode, Codeforces, CodeChef, and AtCoder.
Converts times to IST and filters for next 7 days.

Note: clist.by API requires authentication. You can:
1. Sign up at https://clist.by/settings/api/
2. Get your API key
3. Set environment variable: export CLIST_API_KEY="your_key"
"""

import json
import requests
from datetime import datetime, timedelta
import pytz
from pathlib import Path
import os

# API Configuration
CLIST_API_BASE = "https://clist.by/api/v4/"
CLIST_CONTEST_URL = "https://clist.by/api/v4/contest/"
CLIST_RESOURCE_URL = "https://clist.by/api/v4/resource/"
SUPPORTED_RESOURCES = ["leetcode", "codeforces", "codechef", "atcoder"]

# Timezone
IST = pytz.timezone('Asia/Kolkata')
UTC = pytz.UTC


def get_sample_contests():
    """
    Get sample contest data for demonstration.
    Replace with real API data when credentials are available.
    Uses realistic platform-standard start times (IST) instead of runtime offsets.
    """
    # Realistic contest slots: CodeChef Wed 8 PM, Codeforces ~11:35 PM, LC Sun 8 AM, AtCoder Sat 5:30 PM
    sample_contests = [
        {
            "id": 1,
            "event": "CodeChef Starters 145 (Rated up to 5 Stars)",
            "resource": {"name": "codechef"},
            "start_time": "2026-04-29T14:30:00+00:00",  # Wed Apr 29, 8:00 PM IST
            "duration": 9000,
            "url": "https://www.codechef.com/START145"
        },
        {
            "id": 2,
            "event": "Codeforces Round 900 (Div. 1 + Div. 2)",
            "resource": {"name": "codeforces"},
            "start_time": "2026-04-30T18:05:00+00:00",  # Thu Apr 30, 11:35 PM IST
            "duration": 7200,
            "url": "https://codeforces.com/contests/900"
        },
        {
            "id": 3,
            "event": "LeetCode Biweekly Contest 132",
            "resource": {"name": "leetcode"},
            "start_time": "2026-05-02T03:00:00+00:00",  # Sat May 2, 8:30 AM IST
            "duration": 5400,
            "url": "https://leetcode.com/contest/biweekly-contest-132/"
        },
        {
            "id": 4,
            "event": "AtCoder Beginner Contest 350",
            "resource": {"name": "atcoder"},
            "start_time": "2026-05-02T12:00:00+00:00",  # Sat May 2, 5:30 PM IST
            "duration": 5400,
            "url": "https://atcoder.jp/contests/abc350"
        },
        {
            "id": 5,
            "event": "LeetCode Weekly Contest 446",
            "resource": {"name": "leetcode"},
            "start_time": "2026-05-03T02:30:00+00:00",  # Sun May 3, 8:00 AM IST
            "duration": 5400,
            "url": "https://leetcode.com/contest/weekly-contest-446/"
        },
        {
            "id": 6,
            "event": "AtCoder Heuristic Contest 035",
            "resource": {"name": "atcoder"},
            "start_time": "2026-05-04T12:00:00+00:00",  # Mon May 4, 5:30 PM IST
            "duration": 32400,
            "url": "https://atcoder.jp/contests/ahc035"
        },
        {
            "id": 7,
            "event": "Codeforces Round 901 (Div. 1)",
            "resource": {"name": "codeforces"},
            "start_time": "2026-05-04T18:05:00+00:00",  # Mon May 4, 11:35 PM IST
            "duration": 7200,
            "url": "https://codeforces.com/contests/901"
        },
    ]

    return sample_contests


def fetch_contests():
    """
    Fetch contests from clist.by API for supported platforms.
    Falls back to sample data if API is unavailable.
    """
    api_key = os.environ.get("CLIST_API_KEY")
    
    if not api_key:
        print("⚠️  API Key not found. Set CLIST_API_KEY environment variable:")
        print("   export CLIST_API_KEY='your_key'")
        print("   Get it at: https://clist.by/settings/api/")
        print("\n📋 Using sample contest data for demonstration...\n")
        return get_sample_contests()
    
    all_contests = []
    
    # Fetch with API key
    try:
        print("Fetching contests from clist.by API...")
        headers = {"Authorization": f"ApiKey {api_key}"}
        
        params = {
            "limit": 100,
        }
        
        response = requests.get(CLIST_CONTEST_URL, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        contests = data.get("objects", [])
        
        if contests:
            print(f"✓ Found {len(contests)} contests from API")
            return contests
        else:
            print("⚠️  No contests from API. Using sample data.")
            return get_sample_contests()
                
    except requests.exceptions.RequestException as e:
        print(f"⚠️  Error fetching from API: {e}")
        print("📋 Using sample contest data instead...\n")
        return get_sample_contests()


def convert_to_ist(utc_time_str):
    """
    Convert UTC time string to IST.
    """
    try:
        # Parse the UTC time
        utc_time = datetime.fromisoformat(utc_time_str.replace('Z', '+00:00'))
        
        # Convert to IST
        ist_time = utc_time.astimezone(IST)
        
        return ist_time
    except Exception as e:
        print(f"Error converting time {utc_time_str}: {e}")
        return None


def filter_upcoming_contests(contests, days=7):
    """
    Filter contests for the next N days.
    """
    now = datetime.now(IST)
    future_limit = now + timedelta(days=days)
    
    upcoming = []
    
    for contest in contests:
        try:
            start_time_str = contest.get("start_time")
            if not start_time_str:
                continue
            
            start_time = convert_to_ist(start_time_str)
            if not start_time:
                continue
            
            # Check if contest is in the next 7 days
            if now <= start_time <= future_limit:
                # Get resource/platform name
                resource = contest.get("resource", {})
                if isinstance(resource, dict):
                    platform = resource.get("name", "Unknown")
                else:
                    platform = str(resource)
                
                contest_data = {
                    "id": contest.get("id"),
                    "name": contest.get("event"),
                    "platform": platform,
                    "start_time_utc": contest.get("start_time"),
                    "start_time_ist": start_time.isoformat(),
                    "duration_seconds": contest.get("duration"),
                    "url": contest.get("url"),
                    "start_time_display": start_time.strftime("%a, %b %-d · %-I:%M %p IST"),
                }
                upcoming.append(contest_data)
        except Exception as e:
            print(f"Error processing contest {contest.get('event')}: {e}")
            continue
    
    # Sort by start time
    upcoming.sort(key=lambda x: x["start_time_ist"])
    
    return upcoming


def save_to_json(contests, filepath="data/contests.json"):
    """
    Save contests to JSON file.
    """
    try:
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        
        data = {
            "last_updated": datetime.now(IST).isoformat(),
            "total_contests": len(contests),
            "contests": contests,
        }
        
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)
        
        print(f"\n✓ Saved {len(contests)} contests to {filepath}")
        return True
    except Exception as e:
        print(f"✗ Error saving to {filepath}: {e}")
        return False


def main():
    """
    Main function to run the scraper.
    """
    print("=" * 60)
    print("CP-Sentry: Contest Scraper")
    print("=" * 60)
    print()
    
    # Fetch contests
    print("Step 1: Fetching contests from clist.by API...")
    all_contests = fetch_contests()
    print(f"Total contests fetched: {len(all_contests)}\n")
    
    if not all_contests:
        print("✗ No contests found. Exiting.")
        return
    
    # Filter for next 7 days
    print("Step 2: Filtering for next 7 days and converting to IST...")
    upcoming_contests = filter_upcoming_contests(all_contests, days=7)
    print(f"Upcoming contests in next 7 days: {len(upcoming_contests)}\n")
    
    if upcoming_contests:
        print("Contests found:")
        for i, contest in enumerate(upcoming_contests, 1):
            print(f"  {i}. [{contest['platform'].upper()}] {contest['name']}")
            print(f"     Start: {contest['start_time_display']}")
            print(f"     URL: {contest['url']}")
        print()
    
    # Save to JSON
    print("Step 3: Saving to data/contests.json...")
    success = save_to_json(upcoming_contests)
    
    if success:
        print("\n✓ Scraper completed successfully!")
    else:
        print("\n✗ Scraper completed with errors.")


if __name__ == "__main__":
    main()
