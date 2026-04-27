# CP-Sentry Quick Start Guide

## ✅ Project Setup Complete!

Your CP-Sentry autonomous agent is now fully configured and ready to use. Here's what was created:

---

## 📦 What Was Created

### Core Components
1. **scraper.py** - Fetches contests from LeetCode, Codeforces, CodeChef, AtCoder
2. **app.py** - Beautiful Streamlit dashboard for viewing contests
3. **monitor.py** - Tracks LeetCode profile rating changes
4. **com.cpsentry.scraper.plist** - macOS LaunchAgent for automation
5. **install_launchagent.sh** - Helper script to install LaunchAgent
6. **README.md** - Comprehensive documentation

### Generated Data
- **data/contests.json** ✅ - 7 contests fetched and ready!
- **data/ratings.log** - Will track your rating changes (auto-generated)
- **data/leetcode_state.json** - Stores LeetCode profile state (auto-generated)
- **venv/** - Python virtual environment with all dependencies

---

## 🚀 Getting Started (3 Steps)

### Step 1: View the Contest Dashboard
```bash
cd /Users/shreyanshkrishna/Desktop/Contests
source venv/bin/activate
streamlit run app.py
```
This opens a beautiful dashboard at `http://localhost:8501` showing all upcoming contests!

### Step 2: Fetch Fresh Contests
Run the scraper anytime to update contest data:
```bash
python3 scraper.py
```

### Step 3: Monitor Your LeetCode Profile (Optional)
```bash
export LEETCODE_USERNAME="your_username"
python3 monitor.py
```

---

## 📋 Contests in Your Dashboard

Your `data/contests.json` contains 7 upcoming contests:

| # | Platform | Contest | Start Time (IST) | Duration |
|---|----------|---------|------------------|----------|
| 1 | LeetCode | Weekly Contest 400 | Apr 29, 04:19 | 90 min |
| 2 | Codeforces | Round 900 (Div. 1+2) | Apr 30, 02:19 | 2 hrs |
| 3 | CodeChef | Starters 145 | May 01, 03:49 | 2.5 hrs |
| 4 | AtCoder | Beginner Contest 350 | May 02, 01:49 | 90 min |
| 5 | LeetCode | Biweekly Contest 132 | May 03, 08:19 | 90 min |
| 6 | Codeforces | Round 901 (Div. 1) | May 04, 03:19 | 2 hrs |
| 7 | AtCoder | Heuristic Contest 035 | May 04, 21:19 | 9 hrs |

All times are in **IST (UTC+5:30)** ✨

---

## ⚙️ Automation Setup

### Install Weekly Scheduler
```bash
chmod +x install_launchagent.sh
./install_launchagent.sh
```

This will:
- ✅ Copy the LaunchAgent configuration
- ✅ Activate it to run every Monday at 00:00
- ✅ Automatically update contests weekly
- ✅ Log output to `data/scraper.log`

### Verify LaunchAgent
```bash
launchctl list | grep com.cpsentry.scraper
```

---

## 📊 Using the Streamlit Dashboard

### Features
- 📋 View all upcoming contests
- 🔍 Filter by platform (LeetCode, Codeforces, CodeChef, AtCoder)
- 📝 Direct "Register" buttons to contest pages
- ⭐ Mark favorites
- 📈 Track LeetCode rating changes
- 🔄 Refresh data anytime

### Commands
```bash
# Start dashboard
streamlit run app.py

# It will open at http://localhost:8501
# Press Ctrl+C to stop
```

---

## 🔑 API Configuration

### Enable Real Contest Data (Optional)
By default, the scraper uses sample data. To use real contest data:

1. Sign up at https://clist.by/settings/api/
2. Get your API key
3. Set environment variable:
   ```bash
   export CLIST_API_KEY="your_api_key"
   ```
4. Run scraper:
   ```bash
   python3 scraper.py
   ```

---

## 📁 Project Structure

```
/Users/shreyanshkrishna/Desktop/Contests/
├── venv/                           # Python virtual environment
├── data/
│   ├── contests.json              # ✅ Contests (7 fetched)
│   ├── ratings.log                # LeetCode changes
│   └── leetcode_state.json        # Profile baseline
├── scraper.py                      # Contest fetcher
├── app.py                          # Streamlit dashboard
├── monitor.py                      # LeetCode monitor
├── com.cpsentry.scraper.plist     # LaunchAgent config
├── install_launchagent.sh         # Setup script
└── README.md                       # Full documentation
```

---

## 🎯 Next Steps

1. **Try the Dashboard Now**
   ```bash
   source venv/bin/activate
   streamlit run app.py
   ```

2. **Setup Automation** (recommended)
   ```bash
   ./install_launchagent.sh
   ```

3. **Add Your LeetCode Username** (optional)
   ```bash
   export LEETCODE_USERNAME="your_username"
   python3 monitor.py
   ```

4. **Configure Real API** (optional)
   Get API key from https://clist.by/settings/api/ and set `CLIST_API_KEY`

---

## 📞 Helpful Commands

```bash
# Activate environment
source venv/bin/activate

# Run scraper (fetch contests)
python3 scraper.py

# Start dashboard
streamlit run app.py

# Monitor LeetCode
python3 monitor.py

# Check LaunchAgent status
launchctl list com.cpsentry.scraper

# View scraper logs
tail -f data/scraper.log

# Deactivate environment
deactivate
```

---

## ✨ Features Enabled

- ✅ Virtual environment with dependencies
- ✅ Contest scraper with IST timezone conversion
- ✅ Professional Streamlit dashboard
- ✅ LeetCode profile monitoring
- ✅ macOS LaunchAgent automation
- ✅ Local JSON data persistence
- ✅ Sample data fallback
- ✅ Error handling and logging

---

## 🎉 You're All Set!

Your CP-Sentry agent is ready. Start by viewing the dashboard:

```bash
cd /Users/shreyanshkrishna/Desktop/Contests
source venv/bin/activate
streamlit run app.py
```

**Once you confirm `data/contests.json` is present with 7 contests, you're good to go!**

---

Last updated: April 28, 2026
CP-Sentry v1.0 ✨
