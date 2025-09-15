# EVENT MANAGER - Simplified for data storage and basic operations only
from PyQt6.QtCore import QDate
import json
import os
from datetime import datetime


class EventManager:
    def __init__(self, main_app=None, json_file_path="demo_events.json"):
        self.main_app = main_app  # Reference to the main application
        self.json_file_path = json_file_path
        self._event_map = {}
        self.load_from_json()
    
    def date_to_string(self, qdate):
        """Convert QDate to string format for JSON"""
        return qdate.toString("yyyy-MM-dd")
    
    def string_to_date(self, date_string):
        """Convert string to QDate object"""
        return QDate.fromString(date_string, "yyyy-MM-dd")
    
    def load_from_json(self):
        """Load events from JSON file"""
        try:
            if os.path.exists(self.json_file_path):
                with open(self.json_file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    
                # Clear existing events
                self._event_map = {}
                
                # Load events from JSON
                events_data = data.get('events', {})
                for date_string, events_list in events_data.items():
                    qdate = self.string_to_date(date_string)
                    self._event_map[qdate] = []
                    
                    for event in events_list:
                        title = event.get('title', '')
                        category = event.get('category', 'Academic')
                        self._event_map[qdate].append((title, category))
                
            else:
                print(f"JSON file {self.json_file_path} not found. Starting with empty events.")
                self._event_map = {}
                
        except Exception as e:
            print(f"Error loading events from JSON: {e}")
            self._event_map = {}
    
    def save_to_json(self):
        """Save events to JSON file"""
        try:
            # Convert event map to JSON-serializable format
            events_data = {}
            for qdate, events_list in self._event_map.items():
                date_string = self.date_to_string(qdate)
                events_data[date_string] = []
                
                for title, category in events_list:
                    events_data[date_string].append({
                        'title': title,
                        'category': category
                    })
            
            # Prepare final JSON structure
            json_data = {
                'events': events_data,
                'metadata': {
                    'last_updated': datetime.now().isoformat(),
                    'total_events': self.get_event_count()
                }
            }
            
            # Save to file
            with open(self.json_file_path, 'w', encoding='utf-8') as file:
                json.dump(json_data, file, indent=2, ensure_ascii=False)
            
            print(f"Successfully saved {self.get_event_count()} events to {self.json_file_path}")
            return True
            
        except Exception as e:
            print(f"Error saving events to JSON: {e}")
            return False
    
    # Basic data operations (getters/setters)
    def get_events(self):
        """Get all events"""
        return self._event_map
    
    def get_events_for_date(self, date):
        """Get events for a specific date"""
        return self._event_map.get(date, [])
    
    def set_events_for_date(self, date, events_list):
        """Set events for a specific date"""
        self._event_map[date] = events_list
        if not events_list:  # Remove date if no events
            self._event_map.pop(date, None)
    
    def add_event_to_memory(self, date, title, category):
        """Add event to memory only (no save)"""
        self._event_map.setdefault(date, [])
        self._event_map[date].append((title, category))
    
    def remove_event_from_memory(self, date, title):
        """Remove event from memory only (no save)"""
        if date in self._event_map:
            self._event_map[date] = [
                (t, c) for t, c in self._event_map[date] if t != title
            ]
            if not self._event_map[date]:
                del self._event_map[date]
    
    def get_upcoming_events(self, filter_category="All", limit=None):
        """Get upcoming events with optional filtering and limit"""
        upcoming = []
        current_date = QDate.currentDate()
        
        for date, events in sorted(self._event_map.items()):
            if date >= current_date:
                for title, category in events:
                    if filter_category == "All" or category == filter_category:
                        upcoming.append((date, title, category))
                        if limit and len(upcoming) >= limit:
                            return upcoming
        return upcoming
    
    def get_events_by_category(self, category):
        """Get all events of a specific category"""
        categorized_events = []
        for date, events in self._event_map.items():
            for title, event_category in events:
                if event_category == category:
                    categorized_events.append((date, title, event_category))
        
        return sorted(categorized_events, key=lambda x: x[0])
    
    def get_events_in_date_range(self, start_date, end_date):
        """Get events within a specific date range"""
        range_events = []
        for date, events in self._event_map.items():
            if start_date <= date <= end_date:
                for title, category in events:
                    range_events.append((date, title, category))
        
        return sorted(range_events, key=lambda x: x[0])
    
    def get_event_count(self):
        """Get total number of events"""
        total = 0
        for events in self._event_map.values():
            total += len(events)
        return total
    
    def get_category_counts(self):
        """Get count of events by category"""
        counts = {}
        for events in self._event_map.values():
            for title, category in events:
                counts[category] = counts.get(category, 0) + 1
        return counts
    
    def search_events(self, search_term, search_in_title=True, search_in_category=False):
        """Search for events by title or category"""
        results = []
        search_term = search_term.lower()
        
        for date, events in self._event_map.items():
            for title, category in events:
                match = False
                
                if search_in_title and search_term in title.lower():
                    match = True
                
                if search_in_category and search_term in category.lower():
                    match = True
                
                if match:
                    results.append((date, title, category))
        
        return sorted(results, key=lambda x: x[0])
    
    def refresh_events_display(self):
        """Refresh the events display after adding/removing events"""
        try:
            if not self.main_app:
                print("No main app reference available for refresh")
                return
                
            # Refresh the activities table
            if hasattr(self.main_app, 'load_activities_data'):
                self.main_app.load_activities_data()
            
            # Refresh the upcoming events list
            if hasattr(self.main_app, 'update_upcoming_events'):
                self.main_app.update_upcoming_events()
            
            # Refresh calendar highlighting
            if hasattr(self.main_app, 'highlight_calendar_events'):
                self.main_app.highlight_calendar_events()
                
            print("Events display refreshed successfully")
            
        except Exception as e:
            print(f"Error refreshing events display: {e}")

    # Legacy methods for backward compatibility
    def add_event(self, date, title, category="Academic"):
        """Legacy method - adds to memory and saves"""
        self.add_event_to_memory(date, title, category)
        return self.save_to_json()
    
    def remove_event(self, date, title):
        """Legacy method - removes from memory and saves"""
        self.remove_event_from_memory(date, title)
        return self.save_to_json()
    
    def handle_new_event(self, event_data):
        """Legacy method for handling new events from forms"""
        try:
            title = event_data['title']
            start_date_str = event_data['start_date']
            
            # Parse the date string (assuming MM/dd/yyyy format)
            if start_date_str:
                date_parts = start_date_str.split('/')
                if len(date_parts) == 3:
                    month, day, year = map(int, date_parts)
                    event_date = QDate(year, month, day)
                    
                    # Determine category based on target audience
                    target_students = event_data.get('target_students', False)
                    target_faculty = event_data.get('target_faculty', False)
                    target_org_officers = event_data.get('target_org_officers', False)
                    target_all = event_data.get('target_all', False)
                    
                    if target_all or (target_students and target_faculty and target_org_officers):
                        category = "Academic"
                    elif target_students:
                        category = "Academic"
                    elif target_faculty:
                        category = "Academic"
                    elif target_org_officers:
                        category = "Organizational"
                    else:
                        category = "Academic"  # Default
                    
                    # Add event and save
                    if self.add_event(event_date, title, category):
                        self.refresh_events_display()
                        return True
                        
        except Exception as e:
            print(f"Error handling new event: {e}")
            return False