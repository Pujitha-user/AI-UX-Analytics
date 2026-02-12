#!/usr/bin/env python3
"""
Comprehensive test script for DataHarvesterPro Flask application
Tests landing page, authentication, dashboard, API endpoints, and tracking
"""

import requests
import json
import time
from datetime import datetime
from urllib.parse import urljoin

# Configuration
BASE_URL = "http://localhost:5000"
DEMO_KEYS = ["demo", "test", "admin"]

# Color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'

def print_test(name, passed, message=""):
    """Print test result"""
    status = f"{Colors.GREEN}PASS{Colors.RESET}" if passed else f"{Colors.RED}FAIL{Colors.RESET}"
    msg = f" - {message}" if message else ""
    print(f"[{status}] {name}{msg}")

def test_landing_page():
    """Test 1: Landing page loads correctly"""
    print(f"\n{Colors.BLUE}TEST 1: Landing Page{Colors.RESET}")
    print("-" * 60)
    
    try:
        response = requests.get(urljoin(BASE_URL, "/"))
        passed = response.status_code == 200 and "UX Analytics Pro" in response.text
        print_test("Landing page loads", passed, f"Status: {response.status_code}")
        
        # Check for key elements
        checks = [
            ("HTML structure", "<!DOCTYPE html>" in response.text),
            ("Page title", "<title>UX Analytics Pro" in response.text),
            ("Demo form", '<form method="POST" action="/authenticate"' in response.text),
            ("Features section", "Powerful Analytics Features" in response.text),
            ("CSS link", "style.css" in response.text)
        ]
        
        for check_name, result in checks:
            print_test(f"  - {check_name}", result)
        
        return passed
    except Exception as e:
        print_test("Landing page loads", False, str(e))
        return False

def test_authentication():
    """Test 2: Authentication flow"""
    print(f"\n{Colors.BLUE}TEST 2: Authentication Flow{Colors.RESET}")
    print("-" * 60)
    
    session = requests.Session()
    
    # Test invalid key
    try:
        response = session.post(
            urljoin(BASE_URL, "/authenticate"),
            data={"demo_key": "invalid_key"},
            allow_redirects=False
        )
        invalid_test = response.status_code in [302, 303] and "error=invalid_key" in response.headers.get("Location", "")
        print_test("Invalid key rejected", invalid_test, f"Status: {response.status_code}")
    except Exception as e:
        print_test("Invalid key rejected", False, str(e))
        invalid_test = False
    
    # Test valid keys
    auth_passed = False
    for key in DEMO_KEYS:
        try:
            response = session.post(
                urljoin(BASE_URL, "/authenticate"),
                data={"demo_key": key},
                allow_redirects=True
            )
            
            dashboard_loaded = response.status_code == 200 and "Analytics Dashboard" in response.text
            print_test(f"Valid key '{key}' accepted", dashboard_loaded, f"Status: {response.status_code}")
            
            if dashboard_loaded:
                auth_passed = True
                break
        except Exception as e:
            print_test(f"Valid key '{key}' accepted", False, str(e))
    
    return auth_passed

def test_dashboard():
    """Test 3: Dashboard page and elements"""
    print(f"\n{Colors.BLUE}TEST 3: Dashboard Page{Colors.RESET}")
    print("-" * 60)
    
    session = requests.Session()
    
    try:
        # Authenticate first
        session.post(
            urljoin(BASE_URL, "/authenticate"),
            data={"demo_key": "demo"}
        )
        
        # Load dashboard
        response = session.get(urljoin(BASE_URL, "/dashboard"))
        dashboard_loaded = response.status_code == 200 and "Analytics Dashboard" in response.text
        print_test("Dashboard loads", dashboard_loaded, f"Status: {response.status_code}")
        
        # Check for key dashboard elements
        checks = [
            ("Sidebar navigation", '<nav class="sidebar-nav">' in response.text),
            ("Overview section", 'id="overview-section"' in response.text),
            ("Heatmap section", 'id="heatmap-section"' in response.text),
            ("Scroll Analysis section", 'id="scroll-section"' in response.text),
            ("Suggestions section", 'id="suggestions-section"' in response.text),
            ("Export section", 'id="export-section"' in response.text),
            ("Refresh button", 'class="refresh-btn"' in response.text),
            ("Logout button", 'url_for.*logout' in response.text or '/logout' in response.text),
            ("Stats grid", 'class="stats-grid"' in response.text),
            ("Dashboard.js script", 'dashboard.js' in response.text)
        ]
        
        for check_name, result in checks:
            print_test(f"  - {check_name}", result)
        
        return dashboard_loaded and all(result for _, result in checks)
        
    except Exception as e:
        print_test("Dashboard loads", False, str(e))
        return False

def test_api_endpoints():
    """Test 4: API endpoints"""
    print(f"\n{Colors.BLUE}TEST 4: API Endpoints{Colors.RESET}")
    print("-" * 60)
    
    session = requests.Session()
    
    try:
        # Authenticate first
        session.post(
            urljoin(BASE_URL, "/authenticate"),
            data={"demo_key": "demo"}
        )
        
        # Test API endpoints
        endpoints = [
            ("/api/heatmap-data", "Heatmap"),
            ("/api/scroll-data", "Scroll Data"),
            ("/api/suggestions", "UX Suggestions"),
            ("/api/export-data", "Export Data")
        ]
        
        all_passed = True
        for endpoint, name in endpoints:
            try:
                response = session.get(urljoin(BASE_URL, endpoint))
                passed = response.status_code == 200
                
                # Try to parse JSON
                try:
                    data = response.json()
                    is_json = True
                    json_status = "Valid JSON"
                except:
                    is_json = False
                    json_status = "Invalid/No JSON"
                
                print_test(f"{name} endpoint", passed and is_json, f"Status: {response.status_code} - {json_status}")
                all_passed = all_passed and passed and is_json
                
            except Exception as e:
                print_test(f"{name} endpoint", False, str(e))
                all_passed = False
        
        return all_passed
        
    except Exception as e:
        print_test("API endpoints", False, str(e))
        return False

def test_tracking_endpoint():
    """Test 5: Tracking endpoint"""
    print(f"\n{Colors.BLUE}TEST 5: Tracking Endpoint{Colors.RESET}")
    print("-" * 60)
    
    try:
        # Create test tracking data
        test_events = [
            {
                "event_type": "click",
                "x": 100,
                "y": 200,
                "element_type": "button",
                "element_text": "Test Button",
                "url": "http://test.example.com",
                "timestamp": datetime.utcnow().isoformat(),
                "session_id": "test_session_123"
            },
            {
                "event_type": "scroll",
                "scroll_depth": 50,
                "url": "http://test.example.com",
                "timestamp": datetime.utcnow().isoformat(),
                "session_id": "test_session_123"
            },
            {
                "event_type": "pageview",
                "url": "http://test.example.com",
                "title": "Test Page",
                "timestamp": datetime.utcnow().isoformat(),
                "session_id": "test_session_123"
            }
        ]
        
        all_passed = True
        for event in test_events:
            try:
                response = requests.post(
                    urljoin(BASE_URL, "/api/track"),
                    json=event,
                    headers={"Content-Type": "application/json"}
                )
                
                passed = response.status_code == 200
                event_type = event.get("event_type", "unknown")
                print_test(f"Track {event_type} event", passed, f"Status: {response.status_code}")
                all_passed = all_passed and passed
                
            except Exception as e:
                print_test(f"Track event", False, str(e))
                all_passed = False
        
        return all_passed
        
    except Exception as e:
        print_test("Tracking endpoint", False, str(e))
        return False

def test_tracking_script():
    """Test 6: Tracking script endpoint"""
    print(f"\n{Colors.BLUE}TEST 6: Tracking Script{Colors.RESET}")
    print("-" * 60)
    
    try:
        response = requests.get(urljoin(BASE_URL, "/tracking-script"))
        script_loaded = response.status_code == 200 and "UX Analytics" in response.text
        print_test("Tracking script loads", script_loaded, f"Status: {response.status_code}")
        
        checks = [
            ("Script is JavaScript", "function" in response.text or "const" in response.text),
            ("Session ID generation", "generateSessionId" in response.text),
            ("Click tracking", "handleClick" in response.text),
            ("Scroll tracking", "handleScroll" in response.text),
            ("Event sending", "sendEvent" in response.text),
            ("API endpoint placeholder", "apiEndpoint" in response.text),
        ]
        
        for check_name, result in checks:
            print_test(f"  - {check_name}", result)
        
        return script_loaded and all(result for _, result in checks)
        
    except Exception as e:
        print_test("Tracking script", False, str(e))
        return False

def test_static_files():
    """Test 7: Static files (CSS, JS)"""
    print(f"\n{Colors.BLUE}TEST 7: Static Files{Colors.RESET}")
    print("-" * 60)
    
    files = [
        ("/static/css/style.css", "CSS"),
        ("/static/js/dashboard.js", "Dashboard JS"),
        ("/static/js/tracking.js", "Tracking JS")
    ]
    
    all_passed = True
    for path, name in files:
        try:
            response = requests.get(urljoin(BASE_URL, path))
            passed = response.status_code == 200 and len(response.text) > 0
            print_test(f"{name} loads", passed, f"Status: {response.status_code}, Size: {len(response.text)} bytes")
            all_passed = all_passed and passed
        except Exception as e:
            print_test(f"{name} loads", False, str(e))
            all_passed = False
    
    return all_passed

def test_logout():
    """Test 8: Logout functionality"""
    print(f"\n{Colors.BLUE}TEST 8: Logout{Colors.RESET}")
    print("-" * 60)
    
    session = requests.Session()
    
    try:
        # Authenticate
        session.post(
            urljoin(BASE_URL, "/authenticate"),
            data={"demo_key": "demo"}
        )
        
        # Verify authenticated - can access dashboard
        response = session.get(urljoin(BASE_URL, "/dashboard"))
        authenticated = response.status_code == 200
        print_test("Can access dashboard when authenticated", authenticated)
        
        # Logout
        response = session.get(urljoin(BASE_URL, "/logout"), allow_redirects=False)
        logout_works = response.status_code in [301, 302, 303]
        print_test("Logout redirects", logout_works, f"Status: {response.status_code}")
        
        # Verify logged out - cannot access dashboard
        response = session.get(urljoin(BASE_URL, "/dashboard"), allow_redirects=False)
        logged_out = response.status_code in [301, 302, 303]
        print_test("Cannot access dashboard when logged out", logged_out, f"Status: {response.status_code}")
        
        return authenticated and logout_works and logged_out
        
    except Exception as e:
        print_test("Logout flow", False, str(e))
        return False

def run_all_tests():
    """Run all tests"""
    print(f"\n{Colors.BLUE}{'='*60}")
    print(f"DataHarvesterPro - Comprehensive Application Tests")
    print(f"{'='*60}{Colors.RESET}")
    print(f"Testing: {BASE_URL}")
    print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    results = {
        "Landing Page": test_landing_page(),
        "Authentication": test_authentication(),
        "Dashboard": test_dashboard(),
        "API Endpoints": test_api_endpoints(),
        "Tracking Endpoint": test_tracking_endpoint(),
        "Tracking Script": test_tracking_script(),
        "Static Files": test_static_files(),
        "Logout": test_logout()
    }
    
    # Print summary
    print(f"\n{Colors.BLUE}{'='*60}")
    print(f"Test Summary")
    print(f"{'='*60}{Colors.RESET}")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = f"{Colors.GREEN}PASS{Colors.RESET}" if result else f"{Colors.RED}FAIL{Colors.RESET}"
        print(f"[{status}] {test_name}")
    
    percentage = (passed / total) * 100 if total > 0 else 0
    print(f"\n{Colors.YELLOW}Total: {passed}/{total} tests passed ({percentage:.1f}%){Colors.RESET}")
    
    if passed == total:
        print(f"{Colors.GREEN}All tests passed! Application is working correctly.{Colors.RESET}")
    else:
        print(f"{Colors.RED}Some tests failed. Please review the output above.{Colors.RESET}")
    
    print(f"\nEnd time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    return passed == total

if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
