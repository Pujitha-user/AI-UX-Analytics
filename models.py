from app import db
from datetime import datetime
import json

class TrackingEvent(db.Model):
    """Model for storing user tracking events"""
    __tablename__ = 'tracking_events'
    
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100), nullable=False, index=True)
    event_type = db.Column(db.String(50), nullable=False, index=True)
    url = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, index=True)
    
    # Position data
    x = db.Column(db.Float)
    y = db.Column(db.Float)
    
    # Scroll data
    scroll_depth = db.Column(db.Float)
    scroll_top = db.Column(db.Float)
    document_height = db.Column(db.Float)
    
    # Element data
    element_type = db.Column(db.String(50))
    element_text = db.Column(db.Text)
    element_id = db.Column(db.String(200))
    element_class = db.Column(db.Text)
    
    # Browser/viewport data
    viewport_width = db.Column(db.Integer)
    viewport_height = db.Column(db.Integer)
    user_agent = db.Column(db.Text)
    referrer = db.Column(db.Text)
    
    # Page data
    page_title = db.Column(db.Text)
    
    # Additional data stored as JSON
    additional_data = db.Column(db.Text)  # JSON string for any extra data
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert tracking event to dictionary"""
        data = {
            'id': self.id,
            'session_id': self.session_id,
            'event_type': self.event_type,
            'url': self.url,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'x': self.x,
            'y': self.y,
            'scroll_depth': self.scroll_depth,
            'scroll_top': self.scroll_top,
            'document_height': self.document_height,
            'element_type': self.element_type,
            'element_text': self.element_text,
            'element_id': self.element_id,
            'element_class': self.element_class,
            'viewport_width': self.viewport_width,
            'viewport_height': self.viewport_height,
            'user_agent': self.user_agent,
            'referrer': self.referrer,
            'page_title': self.page_title
        }
        
        # Add additional data if present
        if self.additional_data:
            try:
                additional = json.loads(self.additional_data)
                data.update(additional)
            except (json.JSONDecodeError, TypeError):
                pass
                
        return data
    
    @classmethod
    def from_dict(cls, data):
        """Create tracking event from dictionary"""
        # Extract known fields
        known_fields = {
            'session_id', 'event_type', 'url', 'x', 'y', 'scroll_depth',
            'scroll_top', 'document_height', 'element_type', 'element_text',
            'element_id', 'element_class', 'viewport_width', 'viewport_height',
            'user_agent', 'referrer', 'page_title'
        }
        
        # Handle timestamp
        timestamp = data.get('timestamp')
        if isinstance(timestamp, str):
            try:
                timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            except (ValueError, AttributeError):
                timestamp = datetime.utcnow()
        elif not isinstance(timestamp, datetime):
            timestamp = datetime.utcnow()
        
        # Extract additional data
        additional_data = {}
        for key, value in data.items():
            if key not in known_fields and key != 'timestamp':
                additional_data[key] = value
        
        return cls(
            session_id=data.get('session_id', ''),
            event_type=data.get('event_type', ''),
            url=data.get('url', ''),
            timestamp=timestamp,
            x=data.get('x'),
            y=data.get('y'),
            scroll_depth=data.get('scroll_depth'),
            scroll_top=data.get('scroll_top'),
            document_height=data.get('document_height'),
            element_type=data.get('element_type'),
            element_text=data.get('element_text'),
            element_id=data.get('element_id'),
            element_class=data.get('element_class'),
            viewport_width=data.get('viewport_width'),
            viewport_height=data.get('viewport_height'),
            user_agent=data.get('user_agent'),
            referrer=data.get('referrer'),
            page_title=data.get('page_title'),
            additional_data=json.dumps(additional_data) if additional_data else None
        )

class AnalyticsSession(db.Model):
    """Model for tracking user sessions"""
    __tablename__ = 'analytics_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100), unique=True, nullable=False, index=True)
    first_seen = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    last_seen = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    event_count = db.Column(db.Integer, default=0)
    pages_visited = db.Column(db.Integer, default=0)
    
    # Session metadata
    user_agent = db.Column(db.Text)
    initial_referrer = db.Column(db.Text)
    initial_url = db.Column(db.Text)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert session to dictionary"""
        return {
            'id': self.id,
            'session_id': self.session_id,
            'first_seen': self.first_seen.isoformat() if self.first_seen else None,
            'last_seen': self.last_seen.isoformat() if self.last_seen else None,
            'event_count': self.event_count,
            'pages_visited': self.pages_visited,
            'user_agent': self.user_agent,
            'initial_referrer': self.initial_referrer,
            'initial_url': self.initial_url,
            'duration_seconds': (self.last_seen - self.first_seen).total_seconds() if self.last_seen and self.first_seen else 0
        }