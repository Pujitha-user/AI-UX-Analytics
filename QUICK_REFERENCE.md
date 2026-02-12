# DataHarvesterPro - Quick Reference Guide

## 🚀 Running the Project

### Step 1: Start Flask Server
```bash
cd c:\DataHarvesterPro
C:/DataHarvesterPro/.venv/Scripts/python.exe main.py
```

The server will start on `http://localhost:5000`

### Step 2: Open in Browser
Navigate to: **http://localhost:5000**

### Step 3: Access Dashboard
Use one of these demo keys:
- `demo`
- `test`  
- `admin`

## 📋 Testing Everything

### Run Comprehensive Tests
```bash
C:/DataHarvesterPro/.venv/Scripts/python.exe test_app.py
```

**Expected Result**: All 8 test categories should PASS (100%)

### Test Results Information
- **TEST 1**: Landing Page ✅
- **TEST 2**: Authentication ✅
- **TEST 3**: Dashboard ✅
- **TEST 4**: API Endpoints ✅
- **TEST 5**: Tracking Endpoint ✅
- **TEST 6**: Tracking Script ✅
- **TEST 7**: Static Files ✅
- **TEST 8**: Logout ✅

## 🎯 Button Click Testing Guide

### Landing Page (`http://localhost:5000`)

**Button 1**: "Access Dashboard"
- **Input**: Enter "demo" in the text field
- **Action**: Click the button
- **Expected**: Redirects to dashboard and shows analytics
- **Status**: ✅ WORKING

### Dashboard (`http://localhost:5000/dashboard`)

After authenticating, you'll see these buttons in the sidebar:

**Button 1**: "Overview" (Sidebar)
- **Action**: Click to view main analytics stats
- **Functions Called**:
  - `setupNavigation()` - Handles navigation
  - `setupCharts()` - Creates Chart.js charts
  - `loadHeatmapData()` - Fetches heatmap data
  - `loadScrollData()` - Fetches scroll analytics
  - `loadSuggestions()` - Fetches AI suggestions
- **Data Shows**: Total events, unique sessions, event types chart, timeline chart
- **Status**: ✅ WORKING

**Button 2**: "Heatmaps" (Sidebar)
- **Action**: Click to switch to heatmap view
- **Functions Called**:
  - `loadHeatmapData()` - Fetches `/api/heatmap-data`
  - `renderHeatmap()` - Draws canvas visualization
- **Data Shows**: Click clusters, intensity visualization, click statistics
- **Status**: ✅ WORKING

**Button 3**: "Scroll Analysis" (Sidebar)
- **Action**: Click to view scroll behavior
- **Functions Called**:
  - `loadScrollData()` - Fetches `/api/scroll-data`
  - `renderScrollAnalytics()` - Creates scroll chart
- **Data Shows**: Scroll depth percentage, bounce rate, scroll distribution
- **Status**: ✅ WORKING

**Button 4**: "AI Suggestions" (Sidebar)
- **Action**: Click to view AI recommendations
- **Functions Called**:
  - `loadSuggestions()` - Fetches `/api/suggestions`
  - `renderSuggestions()` - Displays suggestion cards
- **Data Shows**: Priority levels, descriptions, actionable tips
- **Status**: ✅ WORKING

**Button 5**: "Export Data" (Sidebar)
- **Action**: Click to export analytics as JSON
- **Functions Called**:
  - `exportData()` - Fetches `/api/export-data`
  - Creates and downloads JSON file
- **Download**: `ux-analytics-data-[DATE].json`
- **Status**: ✅ WORKING

**Button 6**: "Refresh" (Top Right)
- **Action**: Click the refresh icon button
- **Function Called**: `refreshData()`
- **Effect**: Reloads page with latest data, shows spinner
- **Status**: ✅ WORKING

**Button 7**: "Copy Script" (In demo/setup section)
- **Action**: Click to copy tracking script tag
- **Function Called**: `copyToClipboard()`
- **Effect**: Copies to clipboard, shows "Copied" confirmation
- **Status**: ✅ WORKING

**Button 8**: "Logout" (Bottom of Sidebar)
- **Action**: Click to logout
- **Function Called**: Redirects to `/logout`
- **Effect**: Clears session, redirects to landing page
- **Status**: ✅ WORKING

## 📊 API Endpoints Reference

All endpoints require authentication (except `/api/track` which is public).

### 1. `/api/track` (POST) - Track User Events
```
POST /api/track
Content-Type: application/json

{
  "event_type": "click",
  "x": 100,
  "y": 200,
  "element_type": "button",
  "url": "http://example.com",
  "timestamp": "2026-02-12T17:00:00",
  "session_id": "sess_[ID]"
}

Response: {"status": "success"}
Status: 200
```

### 2. `/api/heatmap-data` (GET) - Get Click Heatmap Data
```
GET /api/heatmap-data

Response: {
  "points": [
    {"x": 100, "y": 200, "intensity": 0.8, "count": 5},
    ...
  ],
  "total_clicks": 42,
  "clusters": 8
}
Status: 200
```

### 3. `/api/scroll-data` (GET) - Get Scroll Analytics
```
GET /api/scroll-data

Response: {
  "average_depth": 65.5,
  "max_depth": 100,
  "bounce_rate": 15.3,
  "depth_distribution": [0, 2, 3, 5, ...]
}
Status: 200
```

### 4. `/api/suggestions` (GET) - Get AI Suggestions
```
GET /api/suggestions

Response: {
  "suggestions": [
    {
      "title": "Improve Button Visibility",
      "description": "...",
      "priority": "high",
      "actionable_tips": ["...", "..."]
    },
    ...
  ]
}
Status: 200
```

### 5. `/api/export-data` (GET) - Export All Data
```
GET /api/export-data

Response: {
  "total_events": 156,
  "unique_sessions": 12,
  "events": [...],
  "sessions": [...]
}
Status: 200
```

## 🔧 Troubleshooting

### Issue: "Connection refused" on localhost:5000
**Solution**: Make sure Flask server is running
```bash
C:/DataHarvesterPro/.venv/Scripts/python.exe main.py
```

### Issue: Database locked error
**Solution**: Delete `local.db` and restart
```bash
rm c:\DataHarvesterPro\local.db
C:/DataHarvesterPro/.venv/Scripts/python.exe main.py
```

### Issue: Port 5000 already in use
**Solution**: Kill the process or use a different port
```bash
# Find process on port 5000
netstat -ano | findstr :5000

# Kill the process (replace PID with actual ID)
taskkill /PID [PID] /F
```

### Issue: Module not found errors
**Solution**: Reinstall dependencies
```bash
C:/DataHarvesterPro/.venv/Scripts/python.exe -m pip install -r requirements.txt
```

## 📝 Function Call Flow

### When Dashboard Loads
1. `initializeDashboard(analytics)` - Main initialization
2. `setupNavigation()` - Sets up sidebar buttons
3. `setupCharts()` - Initializes Chart.js charts
4. `loadHeatmapData()` - Loads `/api/heatmap-data`
5. `loadScrollData()` - Loads `/api/scroll-data`
6. `loadSuggestions()` - Loads `/api/suggestions`
7. Auto-refresh set for every 30 seconds

### When Navigation Button Clicked
1. `setupNavigation()` event listener triggered
2. Button gets `active` class
3. Corresponding section gets `active` class
4. Other sections hidden
5. Data for that section already loaded

### When Tracking Script Runs (In Browser)
1. `init()` - Generates session ID
2. `setupEventListeners()` - Attaches listeners
3. Event occurs (click, scroll, etc.)
4. Handler called (handleClick, handleScroll, etc.)
5. `sendEvent()` - Posts to `/api/track`
6. Server saves event to database

## 💾 Database Schema

### tracking_events table
- id (Integer, PK)
- session_id (String)
- event_type (String): click, scroll, hover, pageview, mousemove, etc.
- url (Text)
- x, y (Float): Click coordinates
- scroll_depth, scroll_top, document_height (Float)
- element_type, element_text, element_id, element_class (String)
- viewport_width, viewport_height (Integer)
- user_agent, referrer, page_title (Text)
- timestamp (DateTime)

### analytics_sessions table
- id (Integer, PK)
- session_id (String, Unique)
- first_seen, last_seen (DateTime)
- event_count (Integer)
- pages_visited (Integer)
- user_agent, initial_referrer, initial_url (Text)

## 🎓 How to Integrate Tracking

To integrate the tracking script into your website:

1. Copy the tracking script code from `/tracking-script` endpoint
2. Add to your HTML before closing `</body>` tag:
   ```html
   <script src="http://localhost:5000/tracking-script"></script>
   ```
3. The tracking automatically starts collecting user interactions
4. Check dashboard to see real-time data

## 📞 Support Files

- **Setup Report**: PROJECT_SETUP_REPORT.md
- **Test Results**: test_results.txt
- **Test Script**: test_app.py
- **Documentation**: README.md

---
**Last Updated**: 2026-02-12
**Status**: ✅ All Systems Operational
