import os
import json
import logging
from datetime import datetime, timedelta
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from ml_model import UXAnalyzer

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production-12345")

# Session configuration
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_COOKIE_SECURE'] = False  # Set to True in production with HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# Configure database
database_url = os.environ.get("DATABASE_URL")
if not database_url:
   # Use SQLite for local development
   database_url = "sqlite:///local.db"

app.config["SQLALCHEMY_DATABASE_URI"] = database_url

app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

# Initialize UX analyzer
ux_analyzer = UXAnalyzer()

# Import database utilities and models
from db_utils import (
    validate_tracking_data, save_tracking_event, get_tracking_data,
    get_analytics_summary, get_export_data
)

@app.route('/')
def index():
    """Landing page with login/demo access"""
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    """Main dashboard for viewing analytics"""
    if 'authenticated' not in session:
        return redirect(url_for('index'))
    
    # Import models
    from models import TrackingEvent, AnalyticsSession
    
    # Get analytics summary from database
    analytics_summary = get_analytics_summary(db, TrackingEvent, AnalyticsSession)
    
    return render_template('dashboard.html', 
                         analytics=analytics_summary,
                         total_sessions=analytics_summary['unique_sessions'])

@app.route('/authenticate', methods=['POST'])
def authenticate():
    """Simple authentication for demo purposes"""
    demo_key = request.form.get('demo_key', '')
    if demo_key.lower() in ['demo', 'test', 'admin']:
        session['authenticated'] = True
        return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('index') + '?error=invalid_key')

@app.route('/api/track', methods=['POST'])
def track_data():
    """Endpoint to receive tracking data from embedded script"""
    try:
        data = request.get_json()
        
        if not validate_tracking_data(data):
            return jsonify({'error': 'Invalid tracking data'}), 400
        
        # Add timestamp if not present
        if 'timestamp' not in data:
            data['timestamp'] = datetime.utcnow().isoformat()
        
        # Ensure session_id is present
        if 'session_id' not in data:
            data['session_id'] = 'unknown'
        
        # Import models
        from models import TrackingEvent, AnalyticsSession
        
        # Save to database
        if save_tracking_event(db, TrackingEvent, AnalyticsSession, data):
            logging.info(f"Tracked event: {data.get('event_type')} from {data.get('url')}")
            return jsonify({'status': 'success'})
        else:
            logging.error(f"Failed to save tracking event: {data}")
            return jsonify({'error': 'Failed to save tracking data'}), 500
        
    except Exception as e:
        logging.error(f"Error tracking data: {str(e)}", exc_info=True)
        return jsonify({'error': f'Failed to track data: {str(e)}'}), 500

@app.route('/api/heatmap-data')
def get_heatmap_data():
    """Get heatmap data for visualization"""
    if 'authenticated' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        from models import TrackingEvent, AnalyticsSession
        tracking_data = get_tracking_data(db, TrackingEvent)
        heatmap_data = ux_analyzer.generate_heatmap_data(tracking_data)
        return jsonify(heatmap_data)
    except Exception as e:
        logging.error(f"Error generating heatmap data: {str(e)}")
        return jsonify({'error': 'Failed to generate heatmap data'}), 500

@app.route('/api/scroll-data')
def get_scroll_data():
    """Get scroll depth analysis data"""
    if 'authenticated' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        from models import TrackingEvent, AnalyticsSession
        tracking_data = get_tracking_data(db, TrackingEvent)
        scroll_data = ux_analyzer.analyze_scroll_behavior(tracking_data)
        return jsonify(scroll_data)
    except Exception as e:
        logging.error(f"Error analyzing scroll data: {str(e)}")
        return jsonify({'error': 'Failed to analyze scroll data'}), 500

@app.route('/api/suggestions')
def get_ux_suggestions():
    """Get AI-powered UX improvement suggestions"""
    if 'authenticated' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        from models import TrackingEvent, AnalyticsSession
        tracking_data = get_tracking_data(db, TrackingEvent)
        suggestions = ux_analyzer.generate_suggestions(tracking_data)
        return jsonify({'suggestions': suggestions})
    except Exception as e:
        logging.error(f"Error generating suggestions: {str(e)}")
        return jsonify({'error': 'Failed to generate suggestions'}), 500

@app.route('/api/export-data')
def export_data():
    """Export tracking data as JSON"""
    if 'authenticated' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        from models import TrackingEvent, AnalyticsSession
        export_data = get_export_data(db, TrackingEvent, AnalyticsSession)
        return jsonify(export_data)
    except Exception as e:
        logging.error(f"Error exporting data: {str(e)}")
        return jsonify({'error': 'Failed to export data'}), 500

@app.route('/tracking-script')
def get_tracking_script():
    """Serve the tracking script for embedding"""
    with open('static/js/tracking.js', 'r') as f:
        script_content = f.read()
    
    # Replace placeholder with actual API endpoint
    api_endpoint = request.url_root + 'api/track'
    script_content = script_content.replace('{{API_ENDPOINT}}', api_endpoint)
    
    response = app.response_class(
        response=script_content,
        status=200,
        mimetype='application/javascript'
    )
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.route('/api/generate-report')
def generate_report():
    """Generate a comprehensive analytics report"""
    if 'authenticated' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        from models import TrackingEvent, AnalyticsSession
        
        # Gather all data for the report
        export_data = get_export_data(db, TrackingEvent, AnalyticsSession)
        tracking_data = get_tracking_data(db, TrackingEvent)
        heatmap_data = ux_analyzer.generate_heatmap_data(tracking_data)
        scroll_data = ux_analyzer.analyze_scroll_behavior(tracking_data)
        suggestions = ux_analyzer.generate_suggestions(tracking_data)
        
        report_data = {
            'export_data': export_data,
            'heatmap_data': heatmap_data,
            'scroll_data': scroll_data,
            'suggestions': suggestions,
            'generated_at': datetime.utcnow().isoformat()
        }
        
        return jsonify(report_data)
    except Exception as e:
        logging.error(f"Error generating report: {str(e)}")
        return jsonify({'error': 'Failed to generate report'}), 500

@app.route('/test-website')
def test_website():
    """Serve the test website for demo purposes"""
    """with open('test_website.html', 'r') as f:
        return f.read()"""
    return app.send_static_file('test_website.html')


@app.route('/logout')
def logout():
    """Logout and clear session"""
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Initialize database tables
    with app.app_context():
        from models import TrackingEvent, AnalyticsSession
        db.create_all()
    
    app.run(host='0.0.0.0', port=5000, debug=True)
