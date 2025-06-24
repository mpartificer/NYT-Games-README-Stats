# NYT Crossword Stats Tracker

Automatically track and display your New York Times crossword statistics on your GitHub profile README! This project uses GitHub Actions to fetch your stats daily and update your profile with beautiful, formatted statistics.

## ✨ Features

- 🔄 **Automated Updates**: Runs daily via GitHub Actions
- 🧩 **Crossword Stats**: Current streak, longest streak, solve rate, average times, and daily performance breakdown
- 🎨 **Beautiful Formatting**: Emoji-rich markdown tables
- 🔒 **Secure**: Uses GitHub secrets for sensitive data

## 🚀 Quick Setup

### 1. Fork This Repository

Click the "Fork" button at the top of this page to create your own copy.

### 2. Get Your NYT User ID

**Option A: Use the Helper Script (Recommended)**

1. **Clone this repository** to your local machine
2. **Install dependencies**: `pip install -r requirements.txt`
3. **Run the helper script**: `python find_user_id.py`
4. **Enter your NYT cookie** when prompted
5. **Wait for the script** to find your user ID automatically

**Option B: Manual Discovery**

1. **Open your browser's Developer Tools** (F12)
2. **Go to the Network tab**
3. **Visit** [NYT Crossword](https://www.nytimes.com/crosswords)
4. **Look for API calls** to endpoints like:
   - `stats-and-streaks.json`
   - `puzzle/daily/stats.json`
5. **Find your user ID** in the URL (it's a number like `245290511`)

### 3. Get Your NYT Cookie

1. **Log into** [NYT Crossword](https://www.nytimes.com/crosswords)
2. **Open Developer Tools** (F12) → Application/Storage tab
3. **Find the Cookie section**
4. **Copy the entire cookie string** (it's very long, starts with things like `nyt-a=...`)

### 4. Create a GitHub Personal Access Token

1. **Go to** [GitHub Settings → Developer settings → Personal access tokens](https://github.com/settings/tokens)
2. **Click "Generate new token (classic)"**
3. **Select scopes:**
   - ✅ `repo` (Full control of private repositories)
   - ✅ `workflow` (Update GitHub Action workflows)
4. **Copy the generated token** (you won't see it again!)

### 5. Set Up GitHub Secrets

In your forked repository:

1. **Go to Settings → Secrets and variables → Actions**
2. **Add these repository secrets:**

| Secret Name             | Value                                            |
| ----------------------- | ------------------------------------------------ |
| `NYT_COOKIE`            | Your NYT cookie string                           |
| `NYT_USER_ID`           | Your NYT user ID number                          |
| `PERSONAL_ACCESS_TOKEN` | Your GitHub personal access token                |
| `PROFILE_REPOSITORY`    | Your username/username (e.g., `johndoe/johndoe`) |

### 6. Update Your Profile README

In your profile repository (`username/username`):

1. **Add these markers** to your README.md:

```markdown
<!-- NYT_STATS_START -->
<!-- NYT_STATS_END -->
```

2. **The stats will automatically appear between these markers**

### 7. Test the Workflow

1. **Go to Actions tab** in your forked repository
2. **Click "Update NYT Stats"** workflow
3. **Click "Run workflow"** → "Run workflow"
4. **Check the logs** to ensure everything works

## 🔧 Customization

### Update Frequency

Edit `.github/workflows/update_nyt_stats.yml`:

```yaml
schedule:
  - cron: "0 9 * * *" # Daily at 9 AM UTC
```

### Customize the Formatting

Edit `nyt_stats.py` in the `format_stats_markdown()` function to:

- Change emojis
- Modify table layouts
- Add/remove statistics

## 🛠️ Troubleshooting

### "Token not supplied" Error

- Ensure `PERSONAL_ACCESS_TOKEN` is set in repository secrets
- Verify the token has the correct permissions

### "403 Forbidden" Error

- Check that `PERSONAL_ACCESS_TOKEN` has `repo` scope
- Verify `PROFILE_REPOSITORY` is correct format (`username/username`)

### "NYT_USER_ID not found" Error

- Double-check your user ID discovery process
- Try the alternative method mentioned above

### Stats Not Updating

- Check GitHub Actions logs for errors
- Verify your NYT cookie is still valid (they expire)
- Ensure your profile README has the required markers

## 🔒 Security Notes

- ✅ **Secure**: All sensitive data stored in GitHub secrets
- ✅ **No hardcoded credentials**: Everything configurable
- ✅ **Minimal permissions**: Token only needs repo access
- ⚠️ **Cookie expiration**: NYT cookies expire periodically
- ⚠️ **Token security**: Keep your personal access token private

## 📝 License

This project is open source. Feel free to fork, modify, and share!

## 🤝 Contributing

Found a bug or have an improvement? Open an issue or submit a pull request!

---

**Happy puzzling! 🧩✨**

<!-- NYT_STATS_START -->

## 🧩 My NYT Puzzle Stats

> _Hey there! 👋 I built this automated tracker to monitor my NYT puzzle progress and connect with fellow puzzle enthusiasts. It updates daily with fresh stats from my solving adventures!_

_Last updated: 2025-06-24 20:34:00_

### 🎯 Crossword

| Statistic          | Value   |
| ------------------ | ------- |
| 🔥 Current Streak  | 1       |
| 🏆 Max Streak      | 5       |
| ✅ Total Solved    | 236     |
| 🎲 Total Attempted | 876     |
| 📊 Solve Rate      | 26.9%   |
| ⏱️ Average Time    | 46m 21s |

#### 📅 Daily Performance

| Day       | Best Time | Average Time | Solved | Current Streak |
| --------- | --------- | ------------ | ------ | -------------- |
| Monday    | 4m 17s    | 9m 11s       | 137    | 🔥 1           |
| Tuesday   | 5m 44s    | 13m 45s      | 66     | 🔥 1           |
| Wednesday | 9m 26s    | 21m 30s      | 21     | ❄️ 0           |
| Thursday  | 19m 13s   | 46m 21s      | 3      | ❄️ 0           |
| Friday    | 21m 26s   | 30m 51s      | 6      | ❄️ 0           |
| Saturday  | 28m 28s   | 30m 54s      | 2      | ❄️ 0           |
| Sunday    | 40m 22s   | 40m 22s      | 1      | ❄️ 0           |

<!-- NYT_STATS_END -->
