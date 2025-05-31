/**
 * UX Analytics Pro - Website Tracking Script
 * Lightweight script to track user interactions and send data to analytics dashboard
 */

(function() {
    'use strict';
    
    // Configuration
    const CONFIG = {
        apiEndpoint: '{{API_ENDPOINT}}',
        sessionDuration: 30 * 60 * 1000, // 30 minutes
        throttleDelay: 100, // milliseconds
        maxEventsPerSession: 1000,
        debug: false
    };
    
    // State management
    let sessionId = null;
    let eventCount = 0;
    let isInitialized = false;
    let throttleTimer = null;
    let lastScrollTime = 0;
    let lastMouseMoveTime = 0;
    
    // Initialize tracking
    function init() {
        if (isInitialized) return;
        
        sessionId = generateSessionId();
        setupEventListeners();
        trackPageView();
        isInitialized = true;
        
        if (CONFIG.debug) {
            console.log('UX Analytics tracking initialized', { sessionId });
        }
    }
    
    // Generate unique session ID
    function generateSessionId() {
        return 'sess_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }
    
    // Setup event listeners
    function setupEventListeners() {
        // Click tracking
        document.addEventListener('click', handleClick, true);
        
        // Scroll tracking
        document.addEventListener('scroll', throttle(handleScroll, CONFIG.throttleDelay), true);
        
        // Mouse movement tracking (throttled)
        document.addEventListener('mousemove', throttle(handleMouseMove, 500), true);
        
        // Page visibility change
        document.addEventListener('visibilitychange', handleVisibilityChange);
        
        // Page unload
        window.addEventListener('beforeunload', handlePageUnload);
        
        // Hover tracking for interactive elements
        const interactiveElements = document.querySelectorAll('button, a, input, select, textarea, [onclick], [role="button"]');
        interactiveElements.forEach(element => {
            element.addEventListener('mouseenter', handleHover);
        });
    }
    
    // Handle click events
    function handleClick(event) {
        if (!shouldTrackEvent()) return;
        
        const element = event.target;
        const elementInfo = getElementInfo(element);
        
        const eventData = {
            event_type: 'click',
            x: event.clientX,
            y: event.clientY,
            element_type: elementInfo.type,
            element_text: elementInfo.text,
            element_id: elementInfo.id,
            element_class: elementInfo.className,
            url: window.location.href,
            timestamp: new Date().toISOString(),
            session_id: sessionId,
            viewport_width: window.innerWidth,
            viewport_height: window.innerHeight
        };
        
        sendEvent(eventData);
    }
    
    // Handle scroll events
    function handleScroll() {
        if (!shouldTrackEvent()) return;
        
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        const documentHeight = document.documentElement.scrollHeight;
        const viewportHeight = window.innerHeight;
        const scrollDepth = Math.round((scrollTop / (documentHeight - viewportHeight)) * 100);
        
        // Only track significant scroll changes
        const now = Date.now();
        if (now - lastScrollTime < 1000) return;
        lastScrollTime = now;
        
        const eventData = {
            event_type: 'scroll',
            scroll_depth: Math.min(scrollDepth, 100),
            scroll_top: scrollTop,
            document_height: documentHeight,
            viewport_height: viewportHeight,
            url: window.location.href,
            timestamp: new Date().toISOString(),
            session_id: sessionId
        };
        
        sendEvent(eventData);
    }
    
    // Handle mouse movement
    function handleMouseMove(event) {
        if (!shouldTrackEvent()) return;
        
        const now = Date.now();
        if (now - lastMouseMoveTime < 2000) return; // Only track every 2 seconds
        lastMouseMoveTime = now;
        
        const eventData = {
            event_type: 'mousemove',
            x: event.clientX,
            y: event.clientY,
            url: window.location.href,
            timestamp: new Date().toISOString(),
            session_id: sessionId
        };
        
        sendEvent(eventData);
    }
    
    // Handle hover events
    function handleHover(event) {
        if (!shouldTrackEvent()) return;
        
        const element = event.target;
        const elementInfo = getElementInfo(element);
        
        const eventData = {
            event_type: 'hover',
            x: event.clientX,
            y: event.clientY,
            element_type: elementInfo.type,
            element_text: elementInfo.text,
            element_id: elementInfo.id,
            element_class: elementInfo.className,
            url: window.location.href,
            timestamp: new Date().toISOString(),
            session_id: sessionId
        };
        
        sendEvent(eventData);
    }
    
    // Track initial page view
    function trackPageView() {
        const eventData = {
            event_type: 'pageview',
            url: window.location.href,
            referrer: document.referrer,
            title: document.title,
            timestamp: new Date().toISOString(),
            session_id: sessionId,
            viewport_width: window.innerWidth,
            viewport_height: window.innerHeight,
            user_agent: navigator.userAgent
        };
        
        sendEvent(eventData);
    }
    
    // Handle visibility change
    function handleVisibilityChange() {
        if (document.hidden) {
            // Page is hidden, user might be switching tabs
            sendEvent({
                event_type: 'page_hidden',
                url: window.location.href,
                timestamp: new Date().toISOString(),
                session_id: sessionId
            });
        } else {
            // Page is visible again
            sendEvent({
                event_type: 'page_visible',
                url: window.location.href,
                timestamp: new Date().toISOString(),
                session_id: sessionId
            });
        }
    }
    
    // Handle page unload
    function handlePageUnload() {
        const eventData = {
            event_type: 'page_unload',
            url: window.location.href,
            timestamp: new Date().toISOString(),
            session_id: sessionId,
            events_sent: eventCount
        };
        
        // Use sendBeacon for reliable delivery during page unload
        if (navigator.sendBeacon) {
            navigator.sendBeacon(CONFIG.apiEndpoint, JSON.stringify(eventData));
        }
    }
    
    // Extract element information
    function getElementInfo(element) {
        const tagName = element.tagName ? element.tagName.toLowerCase() : 'unknown';
        let elementType = tagName;
        
        // Determine more specific element type
        if (tagName === 'button') {
            elementType = 'button';
        } else if (tagName === 'a') {
            elementType = 'link';
        } else if (tagName === 'input') {
            elementType = element.type || 'input';
        } else if (element.getAttribute('role') === 'button') {
            elementType = 'button';
        } else if (element.onclick || element.getAttribute('onclick')) {
            elementType = 'clickable';
        }
        
        return {
            type: elementType,
            text: (element.textContent || element.value || element.alt || '').slice(0, 100),
            id: element.id || '',
            className: element.className || ''
        };
    }
    
    // Check if we should track this event
    function shouldTrackEvent() {
        return isInitialized && 
               sessionId && 
               eventCount < CONFIG.maxEventsPerSession &&
               CONFIG.apiEndpoint !== '{{API_ENDPOINT}}'; // Not replaced placeholder
    }
    
    // Send event data to server
    function sendEvent(eventData) {
        if (!shouldTrackEvent()) return;
        
        eventCount++;
        
        // Send data asynchronously
        try {
            fetch(CONFIG.apiEndpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(eventData),
                keepalive: true
            }).catch(error => {
                if (CONFIG.debug) {
                    console.error('Failed to send tracking event:', error);
                }
            });
        } catch (error) {
            if (CONFIG.debug) {
                console.error('Error sending tracking event:', error);
            }
        }
    }
    
    // Throttle function to limit event frequency
    function throttle(func, delay) {
        return function(...args) {
            if (throttleTimer) return;
            
            throttleTimer = setTimeout(() => {
                func.apply(this, args);
                throttleTimer = null;
            }, delay);
        };
    }
    
    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
    
    // Expose API for advanced usage
    window.UXAnalytics = {
        trackCustomEvent: function(eventType, data) {
            if (!shouldTrackEvent()) return;
            
            const eventData = {
                event_type: eventType,
                ...data,
                url: window.location.href,
                timestamp: new Date().toISOString(),
                session_id: sessionId
            };
            
            sendEvent(eventData);
        },
        getSessionId: function() {
            return sessionId;
        },
        isInitialized: function() {
            return isInitialized;
        }
    };
    
})();
