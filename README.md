# UX Analytics Pro - AI-Powered Website Optimization

A complete full-stack web application that tracks user interactions, generates heatmaps, analyzes scroll behavior, and provides AI-powered UX improvement suggestions.

##  Features

- **Real-time User Tracking**: Capture clicks, scrolls, mouse movements, and page views
- **Interactive Heatmaps**: Visualize user interaction patterns with beautiful heatmap overlays
- **Scroll Depth Analysis**: Understand how users consume your content
- **AI-Powered Suggestions**: Get actionable UX improvement recommendations
- **Professional Dashboard**: Clean, analytics-focused interface for viewing insights
- **Easy Integration**: Lightweight tracking script for any website
- **Data Export**: Download analytics data for further analysis

##  Technology Stack

### Backend
- **Flask**: Python web framework for API and web interface
- **scikit-learn**: Machine learning for user behavior analysis
- **NumPy**: Data processing and analysis
- **JSON**: File-based data storage (Replit-friendly)

### Frontend
- **HTML5 & CSS3**: Modern, responsive interface
- **Vanilla JavaScript**: Client-side functionality
- **Chart.js**: Interactive charts and graphs
- **Canvas API**: Heatmap visualization
- **Font Awesome**: Professional icons

### Tracking
- **Vanilla JavaScript**: Lightweight tracking script
- **XMLHttpRequest/Fetch API**: Real-time data transmission
- **Local Storage**: Session management

##  Project Structure

```
DataHarvesterPro/
├── app.py                      # Main Flask application
├── db_utils.py                 # Database operations
├── models.py                   # SQLAlchemy ORM models
├── ml_model.py                 # AI/ML analysis engine
├── utils.py                    # Utility functions
├── main.py                     # Entry point
├── requirements.txt            # Python dependencies
├── .env.example                # Environment variables template
├── .gitignore                  # Git ignore rules
│
├── templates/
│   ├── index.html              # Login/landing page
│   └── dashboard.html          # Analytics dashboard
│
├── static/
│   ├── css/
│   │   └── style.css           # Dashboard styling
│   ├── js/
│   │   ├── dashboard.js        # Dashboard functionality
│   │   └── tracking.js         # Tracking script for external sites
│   └── test_website.html       # Test HTML for tracking
│
├── data/
│   └── tracking_data.json      # Stored tracking events
│
└── Documentation/
    ├── README.md               # This file
    ├── HOW_TRACKING_WORKS.md   # Tracking system guide
    ├── PROJECT_SETUP_REPORT.md # Setup instructions
    └── QUICK_REFERENCE.md      # Quick start guide
```

##  Quick Start

### Prerequisites
- Python 3.10+
- pip or conda

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/Pujitha-user/AI-UX-Analytics.git
cd DataHarvesterPro
```

2. **Create virtual environment**
```bash
python -m venv .venv
source .venv/bin/activate      # On Windows: .venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env and set SESSION_SECRET if needed
```

5. **Run the application**
```bash
python app.py
```

The application will be available at `http://localhost:5000`

##  Authentication

### Default Demo Keys
- `demo` - Demo account
- `test` - Test account  
- `admin` - Admin account

Simply enter any of these keys on the login page to access the dashboard.

##  How It Works

### 1. **Tracking System**
- Lightweight JavaScript tracker captures user interactions
- Sends event data to Flask backend via `/api/track` endpoint
- Works on any website (not limited to demo/test/admin)

### 2. **Data Storage**
- Events stored in SQLite database (local.db)
- JSON-based analytics data
- User sessions tracked with Flask sessions

### 3. **Analytics Dashboard**
- Real-time visualization of user interactions
- Heatmap generation from click/scroll data
- Scroll depth analysis
- User behavior patterns

### 4. **AI-Powered Insights**
- scikit-learn analyzes behavioral patterns
- Generates actionable UX improvement suggestions
- Identifies high-value interaction zones

### 5. **Report Generation**
- Download comprehensive analytics reports as HTML
- Includes charts, heatmaps, and recommendations
- PDF-ready formatting

##  API Endpoints

### Authentication
- `POST /login` - Authenticate with demo key

### Tracking
- `POST /api/track` - Submit tracking events (public API)
- `GET /api/track-data` - Retrieve tracking data

### Analytics
- `GET /api/analytics` - Get analytics summary
- `POST /api/generate-report` - Generate analytics report

### Pages
- `GET /` - Landing/login page
- `GET /dashboard` - Analytics dashboard

## 📈 Integration Example

To track interactions on your website, add this script:

```html
<script src="http://localhost:5000/static/js/tracking.js"></script>
<script>
  InitializeTracking('http://localhost:5000/api/track');
</script>
```

The tracker captures:
- Page views
- User clicks (with coordinates)
- Scroll depth
- Mouse movements
- Session duration

##  Testing

Run the comprehensive test suite:

```bash
python test_app.py
```

Test categories:
-  Landing page rendering
-  Authentication flow
-  Dashboard access
-  API endpoints
-  Tracking functionality
-  Static file serving
-  Logout functionality
-  Data persistence

All 43 tests passing with 100% success rate.

##  Database Schema

### TrackingEvent
- `id`: Primary key
- `url`: Website URL being tracked
- `event_type`: Type of event (click, scroll, etc.)
- `event_data`: JSON event details
- `timestamp`: Event timestamp
- `session_id`: Associated session

### AnalyticsSession
- `id`: Primary key
- `session_key`: Demo/test/admin key
- `created_at`: Session creation time
- `last_accessed`: Last access time
- `event_count`: Total events in session
- `pages_visited`: Unique pages visited

##  Environment Variables

Create `.env` file from `.env.example`:

```
SESSION_SECRET=your-secret-key-here
DATABASE_URL=sqlite:///local.db
```

##  Documentation

- **[HOW_TRACKING_WORKS.md](HOW_TRACKING_WORKS.md)** - Detailed tracking system guide
- **[PROJECT_SETUP_REPORT.md](PROJECT_SETUP_REPORT.md)** - Complete setup documentation
- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - Quick start reference
- **[COMPLETION_REPORT.md](COMPLETION_REPORT.md)** - Project completion summary

##  Key Features Explained

### Real-time Tracking
- Non-blocking tracking requests
- Works across different domains (CORS enabled)
- Batches events for performance

### Heatmap Generation
- Visual representation of click locations
- Scroll depth heatmaps
- Canvas-based rendering

### AI Suggestions
- Pattern recognition from user behavior
- Machine learning-based recommendations
- Actionable insights for UX improvement

### Report Generation
- Professional HTML reports
- Downloadable analytics data
- Chart and visualization export

##  Troubleshooting

**Dashboard not loading after login?**
- Clear browser cache and cookies
- Check if Flask server is running
- Verify SESSION_SECRET is set

**Tracking events not recorded?**
- Ensure tracking script is included on page
- Check browser console for errors
- Verify `/api/track` endpoint is accessible

**Report generation fails?**
- Ensure you have at least one tracked event
- Check browser console for errors
- Verify localStorage has sufficient space

##  Dependencies

- Flask 3.1.2 - Web framework
- SQLAlchemy 3.1.1 - ORM
- scikit-learn 1.6.1 - ML/AI
- Requests - HTTP library
- Werkzeug - WSGI toolkit
- Email-validator - Email validation
- Gunicorn - Production WSGI server

See `requirements.txt` for complete list with versions.

##  Deployment

### Local Development
```bash
python app.py
```

### Production (using Gunicorn)
```bash
gunicorn --bind 0.0.0.0:5000 app:app
```

### Environment Setup
1. Set `SESSION_SECRET` environment variable
2. Set `DATABASE_URL` for PostgreSQL if needed
3. Set `FLASK_ENV=production`

##  License

This project is open source and available under the MIT License.

##  Author

Created as an AI-powered UX Analytics platform for website optimization and user behavior analysis.

##  Contributing

Contributions are welcome! Please feel free to submit a Pull Request.


