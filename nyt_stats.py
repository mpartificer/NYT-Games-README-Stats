# nyt_stats.py
import os
import json
import requests
from datetime import datetime
import re

def discover_user_id(cookie):
    """
    Try to discover the user ID from NYT API responses
    """
    headers = {
        'Cookie': cookie,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # Try a few common endpoints that might reveal the user ID
    endpoints_to_try = [
        'https://www.nytimes.com/svc/crosswords/v3/puzzle/daily/stats.json',
        'https://www.nytimes.com/svc/crosswords/v3/puzzle/mini/stats.json',
        'https://www.nytimes.com/svc/games/state/wordleV2/latests'
    ]
    
    for endpoint in endpoints_to_try:
        try:
            print(f"Trying endpoint: {endpoint}")
            response = requests.get(endpoint, headers=headers)
            print(f"Response status: {response.status_code}")
            if response.status_code == 200:
                print(f"Response: {response.text[:500]}...")
            elif response.status_code == 404:
                print("404 - endpoint not found")
            else:
                print(f"Response: {response.text[:200]}...")
        except Exception as e:
            print(f"Error: {e}")
        print("---")

def get_nyt_stats(cookie, user_id):
    """
    Fetch NYT crossword stats using user's cookie and user ID
    """
    headers = {
        'Cookie': cookie,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    print(f"Using cookie: {cookie[:50]}..." if len(cookie) > 50 else f"Using cookie: {cookie}")
    print(f"Using user ID: {user_id}")
    
    # First, try to discover the user ID
    print("Attempting to discover user ID...")
    discover_user_id(cookie)
    
    # Get crossword stats
    crossword_stats = {}
    try:
        print("Fetching crossword stats...")
        # Use the provided user ID
        crossword_response = requests.get(f'https://www.nytimes.com/svc/crosswords/v3/{user_id}/stats-and-streaks.json?date_start=1988-01-01&start_on_monday=true', headers=headers)
        print(f"Crossword response status: {crossword_response.status_code}")
        if crossword_response.status_code == 200:
            crossword_stats = crossword_response.json()
            print(f"Crossword stats received: {crossword_stats}")
        else:
            print(f"Crossword response text: {crossword_response.text[:200]}...")
    except Exception as e:
        print(f"Error fetching crossword stats: {e}")
    
    result = {
        "crossword": crossword_stats,
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    print(f"Final stats object: {result}")
    return result

def format_stats_markdown(stats):
    """
    Format the crossword stats as a nice markdown table for GitHub README
    """
    print(f"Formatting stats: {stats}")
    
    markdown = "## 🧩 My New York Times Crossword Stats\n\n"
    markdown += f"*Last updated: {stats['last_updated']}*\n\n"
    
    # Format Crossword stats - updated for new API structure
    if stats['crossword'] and 'results' in stats['crossword']:
        cw_results = stats['crossword']['results']
        if 'stats' in cw_results and 'streaks' in cw_results:
            cw_stats = cw_results['stats']
            cw_streaks = cw_results['streaks']
            print(f"Processing crossword stats: {cw_stats}")
            print(f"Processing crossword streaks: {cw_streaks}")
            
            markdown += "### 🎯 Crossword\n\n"
            markdown += "| Statistic | Value |\n"
            markdown += "|-----------|-------|\n"
            
            if 'current_streak' in cw_streaks:
                markdown += f"| 🔥 Current Streak | {cw_streaks['current_streak']} |\n"
            if 'longest_streak' in cw_streaks:
                markdown += f"| 🏆 Max Streak | {cw_streaks['longest_streak']} |\n"
            if 'puzzles_solved' in cw_stats:
                markdown += f"| ✅ Total Solved | {cw_stats['puzzles_solved']} |\n"
            if 'puzzles_attempted' in cw_stats:
                markdown += f"| 🎲 Total Attempted | {cw_stats['puzzles_attempted']} |\n"
            if 'solve_rate' in cw_stats:
                solve_rate_pct = round(cw_stats['solve_rate'] * 100, 1)
                markdown += f"| 📊 Solve Rate | {solve_rate_pct}% |\n"
            if 'longest_avg_time' in cw_stats:
                avg_time = int(cw_stats['longest_avg_time'])
                minutes = avg_time // 60
                seconds = avg_time % 60
                markdown += f"| ⏱️ Average Time | {minutes}m {seconds}s |\n"
            
            markdown += "\n"
            
            # Add daily stats breakdown
            if 'stats_by_day' in cw_stats:
                markdown += "#### 📅 Daily Performance\n\n"
                markdown += "| Day | Best Time | Average Time | Solved | Current Streak |\n"
                markdown += "|-----|-----------|--------------|--------|----------------|\n"
                
                # Note: stats_by_day[0] = Monday, stats_by_day[1] = Tuesday, etc.
                # Note: vertical_streaks[0] = Sunday, vertical_streaks[1] = Monday, etc.
                days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                
                for i, day_stats in enumerate(cw_stats['stats_by_day']):
                    if i < len(days):
                        day_name = days[i]
                        best_time = day_stats.get('best_time', 0)
                        avg_time = day_stats.get('avg_time', 0)
                        solved = day_stats.get('avg_denominator', 0)
                        
                        # Get streak for this day
                        # stats_by_day[i] corresponds to vertical_streaks[i + 1] for Monday-Saturday
                        # For Sunday (stats_by_day[6]), we need vertical_streaks[0]
                        streak_length = 0
                        if 'vertical_streaks' in cw_streaks:
                            if i == 6:  # Sunday is at index 6 in stats_by_day, but index 0 in vertical_streaks
                                if len(cw_streaks['vertical_streaks']) > 0:
                                    streak_length = cw_streaks['vertical_streaks'][0].get('length', 0)
                            else:  # Monday-Saturday: stats_by_day[i] = vertical_streaks[i + 1]
                                if i + 1 < len(cw_streaks['vertical_streaks']):
                                    streak_length = cw_streaks['vertical_streaks'][i + 1].get('length', 0)
                        
                        # Format times
                        best_min = best_time // 60
                        best_sec = best_time % 60
                        avg_min = avg_time // 60
                        avg_sec = avg_time % 60
                        
                        # Format streak with emoji
                        streak_emoji = "🔥" if streak_length > 0 else "❄️"
                        streak_display = f"{streak_emoji} {streak_length}"
                        
                        markdown += f"| {day_name} | {best_min}m {best_sec}s | {avg_min}m {avg_sec}s | {solved} | {streak_display} |\n"
                
                markdown += "\n"
            
        else:
            print("No crossword stats or streaks found in results")
    else:
        print("No crossword stats found or invalid format")
    
    print(f"Generated markdown: {markdown}")
    return markdown

def update_readme(stats_markdown):
    """
    Update the GitHub README.md with the new stats
    """
    # Path to your README file
    readme_path = 'README.md'
    
    # Read the current README
    with open(readme_path, 'r') as file:
        content = file.read()
    
    # Define start and end markers for the stats section
    start_marker = "<!-- NYT_STATS_START -->"
    end_marker = "<!-- NYT_STATS_END -->"
    
    # Check if markers exist, otherwise add them
    if start_marker not in content:
        content += f"\n\n{start_marker}\n{end_marker}\n"
    
    # Replace or insert stats between markers
    pattern = f"{start_marker}(.*?){end_marker}"
    replacement = f"{start_marker}\n{stats_markdown}\n{end_marker}"
    updated_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    # Write the updated README
    with open(readme_path, 'w') as file:
        file.write(updated_content)

def main():
    print("Starting NYT stats update...")
    
    # Get NYT cookie and user ID from environment variables
    nyt_cookie = os.environ.get('NYT_COOKIE')
    nyt_user_id = os.environ.get('NYT_USER_ID')
    
    if not nyt_cookie:
        print("Error: NYT_COOKIE environment variable not set")
        return
    
    if not nyt_user_id:
        print("Error: NYT_USER_ID environment variable not set")
        return
    
    print("NYT_COOKIE environment variable found")
    print(f"NYT_USER_ID environment variable found: {nyt_user_id}")
    
    # Fetch stats
    print("Fetching NYT stats...")
    stats = get_nyt_stats(nyt_cookie, nyt_user_id)
    
    # Format stats as markdown
    print("Formatting stats as markdown...")
    stats_markdown = format_stats_markdown(stats)
    
    # Update README
    print("Updating README...")
    update_readme(stats_markdown)
    
    print("GitHub README successfully updated with NYT crossword stats!")

if __name__ == "__main__":
    main()