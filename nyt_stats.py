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

def get_nyt_stats(cookie):
    """
    Fetch NYT puzzle stats using user's cookie
    """
    headers = {
        'Cookie': cookie,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    print(f"Using cookie: {cookie[:50]}..." if len(cookie) > 50 else f"Using cookie: {cookie}")
    
    # First, try to discover the user ID
    print("Attempting to discover user ID...")
    discover_user_id(cookie)
    
    # Try to get crossword stats - using the correct endpoint
    crossword_stats = {}
    try:
        print("Fetching crossword stats...")
        # Note: You'll need to replace 245290511 with your actual user ID
        crossword_response = requests.get('https://www.nytimes.com/svc/crosswords/v3/245290511/stats-and-streaks.json?date_start=1988-01-01&start_on_monday=true', headers=headers)
        print(f"Crossword response status: {crossword_response.status_code}")
        if crossword_response.status_code == 200:
            crossword_stats = crossword_response.json()
            print(f"Crossword stats received: {crossword_stats}")
        else:
            print(f"Crossword response text: {crossword_response.text[:200]}...")
    except Exception as e:
        print(f"Error fetching crossword stats: {e}")
    
    # Try to get Wordle and Spelling Bee stats - using the correct endpoint
    wordle_stats = {}
    spelling_bee_stats = {}
    try:
        print("Fetching Wordle and Spelling Bee stats...")
        # Note: You'll need to replace 2329 with the current puzzle ID
        games_response = requests.get('https://www.nytimes.com/svc/games/state/wordleV2/latests?puzzle_ids=2329', headers=headers)
        print(f"Games response status: {games_response.status_code}")
        if games_response.status_code == 200:
            games_data = games_response.json()
            print(f"Games stats received: {games_data}")
            
            # Extract Wordle stats if available
            if 'wordle' in games_data:
                wordle_stats = games_data['wordle']
            
            # Extract Spelling Bee stats if available
            if 'spellingBee' in games_data:
                spelling_bee_stats = games_data['spellingBee']
        else:
            print(f"Games response text: {games_response.text[:200]}...")
    except Exception as e:
        print(f"Error fetching games stats: {e}")
    
    result = {
        "crossword": crossword_stats,
        "wordle": wordle_stats,
        "spelling_bee": spelling_bee_stats,
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    print(f"Final stats object: {result}")
    return result

def format_stats_markdown(stats):
    """
    Format the stats as a nice markdown table for GitHub README
    """
    print(f"Formatting stats: {stats}")
    
    markdown = "## 🧩 My NYT Puzzle Stats\n\n"
    markdown += f"*Last updated: {stats['last_updated']}*\n\n"
    
    # Format Crossword stats - updated for new API structure
    if stats['crossword'] and 'results' in stats['crossword']:
        cw_results = stats['crossword']['results']
        if 'stats' in cw_results and 'streaks' in cw_results:
            cw_stats = cw_results['stats']
            cw_streaks = cw_results['streaks']
            print(f"Processing crossword stats: {cw_stats}")
            print(f"Processing crossword streaks: {cw_streaks}")
            
            markdown += "### Crossword\n\n"
            markdown += "| Statistic | Value |\n"
            markdown += "|-----------|-------|\n"
            
            if 'current_streak' in cw_streaks:
                markdown += f"| Current Streak | {cw_streaks['current_streak']} |\n"
            if 'longest_streak' in cw_streaks:
                markdown += f"| Max Streak | {cw_streaks['longest_streak']} |\n"
            if 'puzzles_solved' in cw_stats:
                markdown += f"| Total Solved | {cw_stats['puzzles_solved']} |\n"
            if 'puzzles_attempted' in cw_stats:
                markdown += f"| Total Attempted | {cw_stats['puzzles_attempted']} |\n"
            if 'solve_rate' in cw_stats:
                solve_rate_pct = round(cw_stats['solve_rate'] * 100, 1)
                markdown += f"| Solve Rate | {solve_rate_pct}% |\n"
            if 'longest_avg_time' in cw_stats:
                avg_time = int(cw_stats['longest_avg_time'])
                minutes = avg_time // 60
                seconds = avg_time % 60
                markdown += f"| Average Time | {minutes}m {seconds}s |\n"
            
            markdown += "\n"
        else:
            print("No crossword stats or streaks found in results")
    else:
        print("No crossword stats found or invalid format")
    
    # Format Wordle stats - updated for new API structure
    if stats['wordle']:
        w_stats = stats['wordle']
        print(f"Processing Wordle stats: {w_stats}")
        markdown += "### Wordle\n\n"
        markdown += "| Statistic | Value |\n"
        markdown += "|-----------|-------|\n"
        
        # Adjust these field names based on the actual API response structure
        if 'currentStreak' in w_stats:
            markdown += f"| Current Streak | {w_stats['currentStreak']} |\n"
        if 'maxStreak' in w_stats:
            markdown += f"| Max Streak | {w_stats['maxStreak']} |\n"
        if 'gamesPlayed' in w_stats:
            markdown += f"| Games Played | {w_stats['gamesPlayed']} |\n"
        if 'winPercentage' in w_stats:
            markdown += f"| Win Rate | {w_stats['winPercentage']}% |\n"
        if 'guesses' in w_stats:
            guesses_dist = w_stats['guesses']
            markdown += f"| Guess Distribution | 1: {guesses_dist.get('1', 0)}, 2: {guesses_dist.get('2', 0)}, "
            markdown += f"3: {guesses_dist.get('3', 0)}, 4: {guesses_dist.get('4', 0)}, "
            markdown += f"5: {guesses_dist.get('5', 0)}, 6: {guesses_dist.get('6', 0)} |\n"
        
        markdown += "\n"
    else:
        print("No Wordle stats found or invalid format")
    
    # Format Spelling Bee stats - updated for new API structure
    if stats['spelling_bee']:
        sb_stats = stats['spelling_bee']
        print(f"Processing Spelling Bee stats: {sb_stats}")
        markdown += "### Spelling Bee\n\n"
        markdown += "| Statistic | Value |\n"
        markdown += "|-----------|-------|\n"
        
        # Adjust these field names based on the actual API response structure
        if 'currentStreak' in sb_stats:
            markdown += f"| Current Streak | {sb_stats['currentStreak']} |\n"
        if 'maxStreak' in sb_stats:
            markdown += f"| Max Streak | {sb_stats['maxStreak']} |\n"
        if 'gamesPlayed' in sb_stats:
            markdown += f"| Games Played | {sb_stats['gamesPlayed']} |\n"
        if 'genius' in sb_stats:
            markdown += f"| Genius Achieved | {sb_stats['genius']} times |\n"
        if 'pangrams' in sb_stats:
            markdown += f"| Total Pangrams | {sb_stats['pangrams']} |\n"
    else:
        print("No Spelling Bee stats found or invalid format")
    
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
    
    # Get NYT cookie from environment variable
    nyt_cookie = os.environ.get('NYT_COOKIE')
    if not nyt_cookie:
        print("Error: NYT_COOKIE environment variable not set")
        return
    
    print("NYT_COOKIE environment variable found")
    
    # Fetch stats
    print("Fetching NYT stats...")
    stats = get_nyt_stats(nyt_cookie)
    
    # Format stats as markdown
    print("Formatting stats as markdown...")
    stats_markdown = format_stats_markdown(stats)
    
    # Update README
    print("Updating README...")
    update_readme(stats_markdown)
    
    print("GitHub README successfully updated with NYT puzzle stats!")

if __name__ == "__main__":
    main()