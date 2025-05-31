import json
import logging
from datetime import datetime, timedelta
from collections import defaultdict, Counter
import math

class UXAnalyzer:
    """AI-powered UX analysis engine for generating insights and suggestions"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def generate_heatmap_data(self, tracking_data):
        """Generate heatmap data from click events"""
        try:
            heatmap_points = []
            click_events = [d for d in tracking_data if d.get('event_type') == 'click']
            
            # Group clicks by coordinates
            click_clusters = defaultdict(int)
            for event in click_events:
                x = int(event.get('x', 0))
                y = int(event.get('y', 0))
                # Cluster nearby clicks (within 20px radius)
                cluster_key = (x // 20 * 20, y // 20 * 20)
                click_clusters[cluster_key] += 1
            
            # Convert to heatmap format
            max_intensity = max(click_clusters.values()) if click_clusters else 1
            for (x, y), count in click_clusters.items():
                intensity = min(count / max_intensity, 1.0)
                heatmap_points.append({
                    'x': x,
                    'y': y,
                    'intensity': intensity,
                    'count': count
                })
            
            return {
                'points': heatmap_points,
                'total_clicks': len(click_events),
                'clusters': len(heatmap_points)
            }
            
        except Exception as e:
            self.logger.error(f"Error generating heatmap data: {str(e)}")
            return {'points': [], 'total_clicks': 0, 'clusters': 0}
    
    def analyze_scroll_behavior(self, tracking_data):
        """Analyze scroll depth and patterns"""
        try:
            scroll_events = [d for d in tracking_data if d.get('event_type') == 'scroll']
            
            if not scroll_events:
                return {
                    'average_depth': 0,
                    'max_depth': 0,
                    'depth_distribution': [],
                    'bounce_rate': 100
                }
            
            # Calculate scroll depths
            scroll_depths = []
            max_scroll_per_session = defaultdict(int)
            
            for event in scroll_events:
                depth = event.get('scroll_depth', 0)
                session_id = event.get('session_id', 'unknown')
                scroll_depths.append(depth)
                max_scroll_per_session[session_id] = max(max_scroll_per_session[session_id], depth)
            
            # Calculate metrics
            average_depth = sum(scroll_depths) / len(scroll_depths) if scroll_depths else 0
            max_depth = max(scroll_depths) if scroll_depths else 0
            
            # Depth distribution (in 10% buckets)
            depth_buckets = [0] * 10
            for depth in scroll_depths:
                bucket = min(int(depth / 10), 9)
                depth_buckets[bucket] += 1
            
            # Calculate bounce rate (sessions with < 25% scroll)
            low_engagement_sessions = sum(1 for depth in max_scroll_per_session.values() if depth < 25)
            total_sessions = len(max_scroll_per_session)
            bounce_rate = (low_engagement_sessions / total_sessions * 100) if total_sessions else 0
            
            return {
                'average_depth': round(average_depth, 2),
                'max_depth': max_depth,
                'depth_distribution': depth_buckets,
                'bounce_rate': round(bounce_rate, 2),
                'total_scroll_events': len(scroll_events)
            }
            
        except Exception as e:
            self.logger.error(f"Error analyzing scroll behavior: {str(e)}")
            return {
                'average_depth': 0,
                'max_depth': 0,
                'depth_distribution': [],
                'bounce_rate': 100
            }
    
    def generate_suggestions(self, tracking_data):
        """Generate AI-powered UX improvement suggestions"""
        try:
            suggestions = []
            
            # Analyze click patterns
            click_analysis = self._analyze_click_patterns(tracking_data)
            suggestions.extend(click_analysis)
            
            # Analyze scroll behavior
            scroll_analysis = self._analyze_scroll_suggestions(tracking_data)
            suggestions.extend(scroll_analysis)
            
            # Analyze user flow
            flow_analysis = self._analyze_user_flow(tracking_data)
            suggestions.extend(flow_analysis)
            
            # Analyze engagement metrics
            engagement_analysis = self._analyze_engagement(tracking_data)
            suggestions.extend(engagement_analysis)
            
            return suggestions[:10]  # Return top 10 suggestions
            
        except Exception as e:
            self.logger.error(f"Error generating suggestions: {str(e)}")
            return []
    
    def _analyze_click_patterns(self, tracking_data):
        """Analyze click patterns for suggestions"""
        suggestions = []
        click_events = [d for d in tracking_data if d.get('event_type') == 'click']
        
        if not click_events:
            return suggestions
        
        # Analyze click distribution
        click_positions = [(d.get('x', 0), d.get('y', 0)) for d in click_events]
        click_elements = [d.get('element_type', 'unknown') for d in click_events]
        
        # Low click areas
        if len(click_events) < 10:
            suggestions.append({
                'type': 'click_optimization',
                'priority': 'high',
                'title': 'Low Click Engagement',
                'description': 'Very few clicks detected. Consider making CTAs more prominent.',
                'actionable_tips': [
                    'Increase button sizes and contrast',
                    'Use more compelling call-to-action text',
                    'Position important buttons above the fold'
                ]
            })
        
        # Button click analysis
        button_clicks = [d for d in click_events if d.get('element_type') == 'button']
        if len(button_clicks) / len(click_events) < 0.3:
            suggestions.append({
                'type': 'button_optimization',
                'priority': 'medium',
                'title': 'Low Button Interaction',
                'description': 'Users are not clicking buttons frequently. Improve button design.',
                'actionable_tips': [
                    'Make buttons more visually distinct',
                    'Use contrasting colors for primary actions',
                    'Add hover effects to improve interactivity'
                ]
            })
        
        return suggestions
    
    def _analyze_scroll_suggestions(self, tracking_data):
        """Generate scroll-based suggestions"""
        suggestions = []
        scroll_analysis = self.analyze_scroll_behavior(tracking_data)
        
        # Low scroll depth
        if scroll_analysis['average_depth'] < 30:
            suggestions.append({
                'type': 'content_optimization',
                'priority': 'high',
                'title': 'Low Scroll Engagement',
                'description': f'Average scroll depth is only {scroll_analysis["average_depth"]}%. Users are not engaging with content below the fold.',
                'actionable_tips': [
                    'Move important content higher up the page',
                    'Reduce content length and focus on key information',
                    'Add visual breaks and scanning elements'
                ]
            })
        
        # High bounce rate
        if scroll_analysis['bounce_rate'] > 70:
            suggestions.append({
                'type': 'engagement_optimization',
                'priority': 'high',
                'title': 'High Bounce Rate',
                'description': f'{scroll_analysis["bounce_rate"]}% of users barely scroll. Improve initial content engagement.',
                'actionable_tips': [
                    'Strengthen your headline and value proposition',
                    'Add compelling visuals above the fold',
                    'Reduce loading times and improve performance'
                ]
            })
        
        return suggestions
    
    def _analyze_user_flow(self, tracking_data):
        """Analyze user flow patterns"""
        suggestions = []
        
        # Group events by session
        sessions = defaultdict(list)
        for event in tracking_data:
            session_id = event.get('session_id', 'unknown')
            sessions[session_id].append(event)
        
        # Analyze session patterns
        short_sessions = 0
        for session_events in sessions.values():
            if len(session_events) < 3:
                short_sessions += 1
        
        if short_sessions / len(sessions) > 0.5:
            suggestions.append({
                'type': 'user_flow',
                'priority': 'medium',
                'title': 'Short User Sessions',
                'description': 'Many users have very short sessions with minimal interaction.',
                'actionable_tips': [
                    'Improve page loading speed',
                    'Clarify your value proposition immediately',
                    'Add interactive elements to encourage engagement'
                ]
            })
        
        return suggestions
    
    def _analyze_engagement(self, tracking_data):
        """Analyze overall engagement metrics"""
        suggestions = []
        
        # Calculate events per session
        sessions = defaultdict(int)
        for event in tracking_data:
            session_id = event.get('session_id', 'unknown')
            sessions[session_id] += 1
        
        if sessions:
            avg_events_per_session = sum(sessions.values()) / len(sessions)
            
            if avg_events_per_session < 5:
                suggestions.append({
                    'type': 'engagement',
                    'priority': 'medium',
                    'title': 'Low User Engagement',
                    'description': f'Users generate only {avg_events_per_session:.1f} events per session on average.',
                    'actionable_tips': [
                        'Add more interactive elements',
                        'Improve content relevance and quality',
                        'Optimize user interface for better usability'
                    ]
                })
        
        return suggestions
    
    def get_analytics_summary(self, tracking_data):
        """Get overall analytics summary"""
        try:
            total_events = len(tracking_data)
            
            # Count unique sessions
            unique_sessions = len(set(d.get('session_id', 'unknown') for d in tracking_data))
            
            # Event type distribution
            event_types = Counter(d.get('event_type', 'unknown') for d in tracking_data)
            
            # Calculate time range
            timestamps = [d.get('timestamp') for d in tracking_data if d.get('timestamp')]
            time_range = None
            if timestamps:
                try:
                    parsed_times = [datetime.fromisoformat(ts.replace('Z', '+00:00')) for ts in timestamps]
                    earliest = min(parsed_times)
                    latest = max(parsed_times)
                    time_range = {
                        'start': earliest.isoformat(),
                        'end': latest.isoformat(),
                        'duration_hours': (latest - earliest).total_seconds() / 3600
                    }
                except:
                    pass
            
            return {
                'total_events': total_events,
                'unique_sessions': unique_sessions,
                'event_types': dict(event_types),
                'events_per_session': round(total_events / unique_sessions, 2) if unique_sessions else 0,
                'time_range': time_range
            }
            
        except Exception as e:
            self.logger.error(f"Error getting analytics summary: {str(e)}")
            return {
                'total_events': 0,
                'unique_sessions': 0,
                'event_types': {},
                'events_per_session': 0,
                'time_range': None
            }
