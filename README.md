# CP-Sentry 🔍

**Your Personal Competitive Programming Contest Tracker**

An autonomous agent that fetches upcoming programming contests, displays them in an elegant Streamlit dashboard, and monitors your LeetCode profile for rating changes.

---

## 📋 Features

- 🏆 **Contest Aggregation**: Fetches contests from LeetCode, Codeforces, CodeChef, and AtCoder
- 🌍 **IST Timezone**: All times automatically converted to Indian Standard Time (UTC+5:30)
- 📅 **Smart Filtering**: Shows only contests starting in the next 7 days
- 🎯 **Professional Dashboard**: Beautiful Streamlit UI with contest checklist and register buttons
- 📊 **Profile Monitoring**: Tracks LeetCode rating changes and logs them
- ⚙️ **Automation**: macOS LaunchAgent for weekly automatic updates
- 💾 **Local Storage**: JSON-based persistence for contests and ratings

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- macOS (for LaunchAgent automation)
- Internet connection

### Installation

1. **Navigate to the project directory**:
   ```bash
   cd /Users/shreyanshkrishna/Desktop/Contests
   ```

2. **Activate the virtual environment**:
   ```bash
   source venv/bin/activate
   ```

3. **Verify dependencies are installed**:
   ```bash
   pip list | grep -E "requests|pytz|streamlit|pandas"
   ```

---

## 📁 Project Structure

```
Contests/
├── venv/                          # Virtual environment
├── data/
│   ├── contests.json             # Fetched contests (auto-generated)
│   ├── ratings.log               # LeetCode rating changes (auto-generated)
│   ├── leetcode_state.json       # Previous LeetCode state (auto-generated)
│   ├── scraper.log               # Scraper execution logs
│   └── scraper_error.log         # Scraper error logs
├── scraper.py                     # Contest fetcher (clist.by API)
├── app.py                         # Streamlit dashboard
├── monitor.py                     # LeetCode profile monitor
├── com.cpsentry.scraper.plist    # macOS LaunchAgent configuration
├── install_launchagent.sh        # Installation script
└── README.md                      # This file
```

---

## 🛠️ Components

### 1. **scraper.py** - Contest Scraper
Fetches upcoming contests from the clist.by API.

**Usage**:
```bash
python3 scraper.py
```

**Output**: Saves contests to `data/contests.json`

**What it does**:
- Fetches contests from LeetCode, Codeforces, CodeChef, AtCoder
- Converts all times to IST (UTC+5:30)
- Filters for contests in the next 7 days
- Saves structured JSON with contest details

---

### 2. **app.py** - Streamlit Dashboard
Beautiful web interface to view and manage contests.

**Usage**:
```bash
streamlit run app.py
```

**Features**:
- Display all upcoming contests in the next 7 days
- Filter by platform (LeetCode, Codeforces, CodeChef, AtCoder)
- One-click "Register" buttons linking to contest pages
- Contest duration and timing in IST
- Recent LeetCode rating changes
- Auto-refresh capability

---

### 3. **monitor.py** - LeetCode Monitor
Tracks your LeetCode profile for rating changes and improvements.

**Usage**:
```bash
export LEETCODE_USERNAME="your_username"
python3 monitor.py
```

**Features**:
- Fetches current LeetCode profile data
- Compares with previous state
- Logs rating changes and new problems solved
- Saves profile baseline for future comparisons

**Note**: Current implementation uses LeetCode's GraphQL API. Some features may require authentication for full access.

---

### 4. **Automation - macOS LaunchAgent**
Automatically runs the scraper every Monday at midnight.

**Installation**:
```bash
chmod +x install_launchagent.sh
./install_launchagent.sh
```

**What it does**:
- Installs a LaunchAgent that runs `scraper.py` automatically
- Scheduled for every Monday at 00:00 (midnight)
- Logs output to `data/scraper.log`
- Runs in the background without user intervention

**Manual LaunchAgent Management**:
```bash
# Check if LaunchAgent is loaded
launchctl list | grep com.cpsentry.scraper

# View LaunchAgent status
launchctl list com.cpsentry.scraper

# Unload LaunchAgent
launchctl unload ~/Library/LaunchAgents/com.cpsentry.scraper.plist

# Reload LaunchAgent
launchctl load ~/Library/LaunchAgents/com.cpsentry.scraper.plist
```

---

## 🕐 Timezone Configuration

All times are displayed in **IST (Indian Standard Time, UTC+5:30)**.

### Adjusting LaunchAgent Timing

If you want the scraper to run at a different time, edit `com.cpsentry.scraper.plist`:

```xml
<key>StartCalendarInterval</key>
<array>
    <dict>
        <key>Weekday</key>
        <integer>1</integer>      <!-- 1 = Monday, 2 = Tuesday, etc. -->
        <key>Hour</key>
        <integer>0</integer>       <!-- Hour (0-23) -->
        <key>Minute</key>
        <integer>0</integer>       <!-- Minute (0-59) -->
    </dict>
</array>
```

**Timezone Conversions**:
- 00:00 IST = 18:30 UTC (previous day)
- 00:00 IST = 13:30 EST (previous day)
- 00:00 IST = 10:30 PST (previous day)

After editing, reload the LaunchAgent:
```bash
launchctl unload ~/Library/LaunchAgents/com.cpsentry.scraper.plist
launchctl load ~/Library/LaunchAgents/com.cpsentry.scraper.plist
```

---

## 📊 Data Files

### contests.json
```json
{
  "last_updated": "2026-04-28T12:30:45.123456+05:30",
  "total_contests": 5,
  "contests": [
    {
      "id": 12345,
      "name": "Contest Name",
      "platform": "codeforces",
      "start_time_utc": "2026-05-01T10:00:00Z",
      "start_time_ist": "2026-05-01T15:30:00+05:30",
      "start_time_display": "2026-05-01 15:30:00 IST",
      "duration_seconds": 7200,
      "url": "https://..."
    }
  ]
}
```

### ratings.log
```
[2026-04-28 12:30:45 IST] Baseline profile established for username
[2026-05-05 12:30:45 IST] Change detected: Ranking improved by 50 positions: 1000 → 950
[2026-05-05 12:30:45 IST] Change detected: Solved 3 new problem(s): 250 → 253
```

---

## 🔍 API Integration

### clist.by API
- **Endpoint**: `https://clist.by/api/v4/contests/`
- **Free tier**: Available without authentication
- **Rate limit**: ~60 requests per hour
- **Documentation**: https://clist.by/api/v4/

### LeetCode API
- **GraphQL Endpoint**: `https://leetcode.com/graphql/`
- **Note**: Some queries may require authentication
- **Alternative**: Use official LeetCode API when available

---

## 🐛 Troubleshooting

### Scraper returns no contests
- Check internet connection
- Verify clist.by API is accessible
- Try running manually: `python3 scraper.py`

### Streamlit app not loading
- Ensure app.py is in the same directory as data/
- Check if `data/contests.json` exists
- Run scraper first: `python3 scraper.py`

### LaunchAgent not running
- Check if it's loaded: `launchctl list | grep com.cpsentry.scraper`
- Review logs: `tail -f data/scraper.log`
- Verify plist file permissions: `ls -la ~/Library/LaunchAgents/`

### LeetCode monitor not working
- Set username: `export LEETCODE_USERNAME="your_username"`
- Check GraphQL endpoint accessibility
- Review API response: `python3 monitor.py`

---

## 📝 Usage Examples

### Run everything manually
```bash
# 1. Fetch contests
python3 scraper.py

# 2. Launch dashboard
streamlit run app.py

# 3. Monitor LeetCode (optional)
export LEETCODE_USERNAME="your_username"
python3 monitor.py
```

### Automate on macOS
```bash
# Install LaunchAgent for weekly runs
./install_launchagent.sh

# Or manually:
cp com.cpsentry.scraper.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.cpsentry.scraper.plist
```

### Check what's scheduled
```bash
launchctl list com.cpsentry.scraper
```

---

## 🔐 Privacy & Security

- **Local-only**: All data stored locally in the `data/` directory
- **No authentication**: Uses only public APIs
- **No data sharing**: No information sent to external services except API calls
- **Environment variables**: Use for sensitive data like LeetCode username

---

## 🤝 Contributing

Feel free to extend CP-Sentry with:
- Additional contest platforms
- Email notifications
- Slack/Discord integration
- Contest recommendations
- Performance analytics

---

## 📄 License

This project is provided as-is for personal use.

---

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review log files in `data/`
3. Verify API accessibility
4. Check your internet connection

---

## 🎯 Next Steps

1. **First run**: `python3 scraper.py`
2. **View dashboard**: `streamlit run app.py`
3. **Monitor LeetCode**: `python3 monitor.py` (with username)
4. **Automate**: `./install_launchagent.sh`
5. **Subscribe**: Let CP-Sentry run automatically every Monday!

---

**CP-Sentry v1.0** | Built for competitive programmers ✨
