#!/usr/bin/env python3
"""
NYT User ID Discovery Tool

This script helps you find your NYT user ID by testing common endpoints
and showing you which one returns your personal data.
"""

import requests
import sys
import os

def test_user_id(cookie, user_id):
    """Test if a user ID returns valid crossword stats"""
    headers = {
        'Cookie': cookie,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    url = f'https://www.nytimes.com/svc/crosswords/v3/{user_id}/stats-and-streaks.json?date_start=1988-01-01&start_on_monday=true'
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if 'results' in data and 'stats' in data['results']:
                stats = data['results']['stats']
                if 'puzzles_solved' in stats and stats['puzzles_solved'] > 0:
                    return True, stats
        return False, None
    except Exception as e:
        return False, None

def main():
    print("🔍 NYT User ID Discovery Tool")
    print("=" * 40)
    
    # Get cookie from user
    cookie = input("Enter your NYT cookie: ").strip()
    if not cookie:
        print("❌ No cookie provided. Exiting.")
        return
    
    print("\n🔍 Testing common user ID patterns...")
    print("This may take a few minutes...\n")
    
    # Test common patterns
    test_ids = []
    
    # Add some common starting numbers
    for base in [245, 246, 247, 248, 249, 250]:
        for suffix in range(100000, 999999, 10000):
            test_ids.append(f"{base}{suffix}")
    
    # Add some random ranges that might be common
    for i in range(245000000, 245999999, 100000):
        test_ids.append(str(i))
    
    found_ids = []
    
    for i, user_id in enumerate(test_ids):
        if i % 10 == 0:
            print(f"Testing ID {i+1}/{len(test_ids)}: {user_id}")
        
        is_valid, stats = test_user_id(cookie, user_id)
        if is_valid:
            found_ids.append((user_id, stats))
            print(f"✅ Found valid user ID: {user_id}")
            print(f"   Puzzles solved: {stats.get('puzzles_solved', 'N/A')}")
            print(f"   Solve rate: {stats.get('solve_rate', 'N/A')}")
            print()
    
    if found_ids:
        print("🎉 Success! Found valid user ID(s):")
        for user_id, stats in found_ids:
            print(f"   User ID: {user_id}")
            print(f"   Puzzles solved: {stats.get('puzzles_solved', 'N/A')}")
            print(f"   Solve rate: {stats.get('solve_rate', 'N/A')}")
            print()
        
        if len(found_ids) == 1:
            print(f"📋 Use this user ID in your GitHub secrets: {found_ids[0][0]}")
        else:
            print("📋 Multiple IDs found. Use the one with the most puzzles solved.")
    else:
        print("❌ No valid user IDs found in the tested range.")
        print("\n💡 Try these manual methods:")
        print("1. Open browser dev tools (F12) → Network tab")
        print("2. Visit nytimes.com/crosswords")
        print("3. Look for API calls to 'stats-and-streaks.json'")
        print("4. Your user ID will be in the URL")

if __name__ == "__main__":
    main() 