import json
import os
import logging
from datetime import datetime

def load_tracking_data():
    """Load tracking data from JSON file"""
    try:
        with open('data/tracking_data.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        logging.error("Invalid JSON in tracking_data.json")
        return []
    except Exception as e:
        logging.error(f"Error loading tracking data: {str(e)}")
        return []

def save_tracking_data(data):
    """Save tracking data to JSON file"""
    try:
        # Ensure data directory exists
        os.makedirs('data', exist_ok=True)
        
        with open('data/tracking_data.json', 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        logging.error(f"Error saving tracking data: {str(e)}")
        return False

def validate_tracking_data(data):
    """Validate incoming tracking data"""
    if not isinstance(data, dict):
        return False
    
    required_fields = ['event_type', 'url', 'timestamp']
    
    # Check if all required fields are present
    for field in required_fields:
        if field not in data:
            return False
    
    # Validate event type
    valid_event_types = ['click', 'scroll', 'mousemove', 'pageview', 'hover']
    if data.get('event_type') not in valid_event_types:
        return False
    
    # Validate URL format
    url = data.get('url', '')
    if not url or not isinstance(url, str):
        return False
    
    # Validate coordinates for position-based events
    if data.get('event_type') in ['click', 'mousemove', 'hover']:
        try:
            x = data.get('x')
            y = data.get('y')
            if x is None or y is None:
                return False
            float(x)  # Check if convertible to number
            float(y)
        except (ValueError, TypeError):
            return False
    
    # Validate scroll depth for scroll events
    if data.get('event_type') == 'scroll':
        try:
            scroll_depth = data.get('scroll_depth')
            if scroll_depth is None:
                return False
            depth = float(scroll_depth)
            if depth < 0 or depth > 100:
                return False
        except (ValueError, TypeError):
            return False
    
    return True

def format_timestamp(timestamp_str):
    """Format timestamp for display"""
    try:
        dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    except:
        return timestamp_str

def calculate_session_duration(events):
    """Calculate session duration from events"""
    try:
        timestamps = [e.get('timestamp') for e in events if e.get('timestamp')]
        if len(timestamps) < 2:
            return 0
        
        parsed_times = [datetime.fromisoformat(ts.replace('Z', '+00:00')) for ts in timestamps]
        duration = max(parsed_times) - min(parsed_times)
        return duration.total_seconds()
    except:
        return 0

def clean_old_data(days_to_keep=30):
    """Clean tracking data older than specified days"""
    try:
        data = load_tracking_data()
        if not data:
            return True
        
        cutoff_date = datetime.utcnow() - timedelta(days=days_to_keep)
        
        filtered_data = []
        for event in data:
            try:
                event_time = datetime.fromisoformat(event.get('timestamp', '').replace('Z', '+00:00'))
                if event_time > cutoff_date:
                    filtered_data.append(event)
            except:
                # Keep events with invalid timestamps for safety
                filtered_data.append(event)
        
        return save_tracking_data(filtered_data)
    except Exception as e:
        logging.error(f"Error cleaning old data: {str(e)}")
        return False

def get_data_statistics():
    """Get basic statistics about tracking data"""
    try:
        data = load_tracking_data()
        
        if not data:
            return {
                'total_events': 0,
                'unique_sessions': 0,
                'date_range': None,
                'file_size': 0
            }
        
        # Count unique sessions
        unique_sessions = len(set(e.get('session_id', 'unknown') for e in data))
        
        # Calculate date range
        timestamps = [e.get('timestamp') for e in data if e.get('timestamp')]
        date_range = None
        if timestamps:
            try:
                parsed_times = [datetime.fromisoformat(ts.replace('Z', '+00:00')) for ts in timestamps]
                earliest = min(parsed_times)
                latest = max(parsed_times)
                date_range = {
                    'earliest': earliest.isoformat(),
                    'latest': latest.isoformat()
                }
            except:
                pass
        
        # Get file size
        file_size = 0
        try:
            file_size = os.path.getsize('data/tracking_data.json')
        except:
            pass
        
        return {
            'total_events': len(data),
            'unique_sessions': unique_sessions,
            'date_range': date_range,
            'file_size': file_size
        }
        
    except Exception as e:
        logging.error(f"Error getting data statistics: {str(e)}")
        return {
            'total_events': 0,
            'unique_sessions': 0,
            'date_range': None,
            'file_size': 0
        }
