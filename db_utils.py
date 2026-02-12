"""Database utility functions for tracking data"""

import logging
from datetime import datetime, timedelta
from sqlalchemy import func, desc
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger(__name__)

def validate_tracking_data(data):
    """Validate incoming tracking data"""
    if not isinstance(data, dict):
        return False
    
    required_fields = ['event_type', 'url']
    
    # Check if all required fields are present
    for field in required_fields:
        if field not in data:
            return False
    
    # Validate event type
    valid_event_types = ['click', 'scroll', 'mousemove', 'pageview', 'hover', 'page_hidden', 'page_visible', 'page_unload']
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
            if x is not None:
                float(x)
            if y is not None:
                float(y)
        except (ValueError, TypeError):
            return False
    
    # Validate scroll depth for scroll events
    if data.get('event_type') == 'scroll':
        try:
            scroll_depth = data.get('scroll_depth')
            if scroll_depth is not None:
                depth = float(scroll_depth)
                if depth < 0 or depth > 100:
                    return False
        except (ValueError, TypeError):
            return False
    
    return True

def save_tracking_event(db, TrackingEvent, AnalyticsSession, data):
    """Save tracking event to database"""
    try:
        # Create tracking event
        event = TrackingEvent.from_dict(data)
        db.session.add(event)
        
        # Update or create session
        session_id = data.get('session_id')
        if session_id:
            session = AnalyticsSession.query.filter_by(session_id=session_id).first()
            if not session:
                session = AnalyticsSession(
                    session_id=session_id,
                    user_agent=data.get('user_agent'),
                    initial_referrer=data.get('referrer'),
                    initial_url=data.get('url'),
                    event_count=0,
                    pages_visited=0
                )
                db.session.add(session)
            
            # Ensure event_count is not None
            if session.event_count is None:
                session.event_count = 0
            if session.pages_visited is None:
                session.pages_visited = 0
                
            session.last_seen = datetime.utcnow()
            session.event_count = session.event_count + 1
            
            # Count unique pages
            if data.get('event_type') == 'pageview':
                session.pages_visited = session.pages_visited + 1
        
        db.session.commit()
        return True
        
    except SQLAlchemyError as e:
        logger.error(f"Database error saving tracking event: {str(e)}")
        db.session.rollback()
        return False
    except Exception as e:
        logger.error(f"Error saving tracking event: {str(e)}")
        db.session.rollback()
        return False

def get_tracking_data(db, TrackingEvent, limit=None, days_back=None):
    """Get tracking data from database"""
    try:
        query = TrackingEvent.query
        
        # Filter by date if specified
        if days_back:
            cutoff_date = datetime.utcnow() - timedelta(days=days_back)
            query = query.filter(TrackingEvent.timestamp >= cutoff_date)
        
        # Apply limit if specified
        if limit:
            query = query.limit(limit)
        
        # Order by timestamp descending
        query = query.order_by(desc(TrackingEvent.timestamp))
        
        events = query.all()
        return [event.to_dict() for event in events]
        
    except SQLAlchemyError as e:
        logger.error(f"Database error loading tracking data: {str(e)}")
        return []
    except Exception as e:
        logger.error(f"Error loading tracking data: {str(e)}")
        return []

def get_analytics_summary(db, TrackingEvent, AnalyticsSession):
    """Get analytics summary from database"""
    try:
        # Get total events
        total_events = db.session.query(func.count(TrackingEvent.id)).scalar() or 0
        
        # Get unique sessions
        unique_sessions = db.session.query(func.count(AnalyticsSession.id)).scalar() or 0
        
        # Get event type distribution
        event_types = {}
        event_type_counts = db.session.query(
            TrackingEvent.event_type,
            func.count(TrackingEvent.id)
        ).group_by(TrackingEvent.event_type).all()
        
        for event_type, count in event_type_counts:
            event_types[event_type] = count
        
        # Calculate events per session
        events_per_session = round(total_events / unique_sessions, 2) if unique_sessions else 0
        
        # Get time range
        time_range = None
        earliest = db.session.query(func.min(TrackingEvent.timestamp)).scalar()
        latest = db.session.query(func.max(TrackingEvent.timestamp)).scalar()
        
        if earliest and latest:
            time_range = {
                'start': earliest.isoformat(),
                'end': latest.isoformat(),
                'duration_hours': (latest - earliest).total_seconds() / 3600
            }
        
        return {
            'total_events': total_events,
            'unique_sessions': unique_sessions,
            'event_types': event_types,
            'events_per_session': events_per_session,
            'time_range': time_range
        }
        
    except SQLAlchemyError as e:
        logger.error(f"Database error getting analytics summary: {str(e)}")
        return {
            'total_events': 0,
            'unique_sessions': 0,
            'event_types': {},
            'events_per_session': 0,
            'time_range': None
        }
    except Exception as e:
        logger.error(f"Error getting analytics summary: {str(e)}")
        return {
            'total_events': 0,
            'unique_sessions': 0,
            'event_types': {},
            'events_per_session': 0,
            'time_range': None
        }

def clean_old_data(db, TrackingEvent, AnalyticsSession, days_to_keep=30):
    """Clean tracking data older than specified days"""
    try:
        cutoff_date = datetime.utcnow() - timedelta(days=days_to_keep)
        
        # Delete old tracking events
        deleted_events = db.session.query(TrackingEvent).filter(
            TrackingEvent.timestamp < cutoff_date
        ).delete()
        
        # Delete old sessions that have no events
        deleted_sessions = db.session.query(AnalyticsSession).filter(
            AnalyticsSession.last_seen < cutoff_date
        ).delete()
        
        db.session.commit()
        
        logger.info(f"Cleaned {deleted_events} old events and {deleted_sessions} old sessions")
        return True
        
    except SQLAlchemyError as e:
        logger.error(f"Database error cleaning old data: {str(e)}")
        db.session.rollback()
        return False
    except Exception as e:
        logger.error(f"Error cleaning old data: {str(e)}")
        db.session.rollback()
        return False

def get_export_data(db, TrackingEvent, AnalyticsSession):
    """Get all data for export"""
    try:
        # Get all tracking events
        events = get_tracking_data(db, TrackingEvent, limit=None)
        
        # Get all sessions
        sessions = AnalyticsSession.query.all()
        session_data = [session.to_dict() for session in sessions]
        
        return {
            'events': events,
            'sessions': session_data,
            'exported_at': datetime.utcnow().isoformat(),
            'total_events': len(events),
            'total_sessions': len(session_data)
        }
        
    except SQLAlchemyError as e:
        logger.error(f"Database error getting export data: {str(e)}")
        return {
            'events': [],
            'sessions': [],
            'exported_at': datetime.utcnow().isoformat(),
            'total_events': 0,
            'total_sessions': 0
        }
    except Exception as e:
        logger.error(f"Error getting export data: {str(e)}")
        return {
            'events': [],
            'sessions': [],
            'exported_at': datetime.utcnow().isoformat(),
            'total_events': 0,
            'total_sessions': 0
        }