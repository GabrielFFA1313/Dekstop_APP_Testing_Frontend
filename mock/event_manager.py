# EVENT MANAGER - Enhanced to store time information
from PyQt6.QtCore import QDate, QTime
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
    
    def time_to_string(self, qtime):
        """Convert QTime to string format for JSON"""
        return qtime.toString("hh:mm")
    
    def string_to_time(self, time_string):
        """Convert string to QTime object"""
        return QTime.fromString(time_string, "hh:mm")
    
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
                        
                        # Handle time data (backward compatibility)
                        if 'start_time' in event:
                            start_time = self.string_to_time(event['start_time'])
                        else:
                            # Use default time for backward compatibility
                            start_time = self.get_default_time_for_category(category)
                        
                        if 'end_time' in event:
                            end_time = self.string_to_time(event['end_time'])
                        else:
                            # Use default end time
                            end_time = start_time.addSecs(3600)  # Add 1 hour
                        
                        # Store as tuple: (title, category, start_time, end_time)
                        self._event_map[qdate].append((title, category, start_time, end_time))
                
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
                
                for event_tuple in events_list:
                    if len(event_tuple) == 4:  # New format with times
                        title, category, start_time, end_time = event_tuple
                        events_data[date_string].append({
                            'title': title,
                            'category': category,
                            'start_time': self.time_to_string(start_time),
                            'end_time': self.time_to_string(end_time)
                        })
                    else:  # Old format (backward compatibility)
                        title, category = event_tuple
                        default_time = self.get_default_time_for_category(category)
                        events_data[date_string].append({
                            'title': title,
                            'category': category,
                            'start_time': self.time_to_string(default_time),
                            'end_time': self.time_to_string(default_time.addSecs(3600))
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
    
    def get_default_time_for_category(self, category):
        """Get default QTime for event category"""
        time_map = {
            "Academic": QTime(9, 0),      # 9:00 AM
            "Organizational": QTime(14, 0), # 2:00 PM
            "Deadline": QTime(17, 0),     # 5:00 PM
            "Holiday": QTime(10, 0)       # 10:00 AM
        }
        return time_map.get(category, QTime(12, 0))  # Default to 12:00 PM
    
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
    
    def add_event_to_memory(self, date, title, category, start_time=None, end_time=None):
        """Add event to memory only (no save) with time support"""
        self._event_map.setdefault(date, [])
        
        # Use provided times or defaults
        if start_time is None:
            start_time = self.get_default_time_for_category(category)
        if end_time is None:
            end_time = start_time.addSecs(3600)  # Default 1 hour duration
        
        # Store as tuple: (title, category, start_time, end_time)
        self._event_map[date].append((title, category, start_time, end_time))
    
    def remove_event_from_memory(self, date, title):
        """Remove event from memory only (no save)"""
        if date in self._event_map:
            # Handle both old and new tuple formats
            new_events = []
            for event_tuple in self._event_map[date]:
                event_title = event_tuple[0]  # Title is always first
                if event_title != title:
                    new_events.append(event_tuple)
            
            self._event_map[date] = new_events
            if not self._event_map[date]:
                del self._event_map[date]
    
    def get_upcoming_events(self, filter_category="All", limit=None):
        """Get upcoming events with optional filtering and limit"""
        upcoming = []
        current_date = QDate.currentDate()
        
        for date, events in sorted(self._event_map.items()):
            if date >= current_date:
                for event_tuple in events:
                    title = event_tuple[0]
                    category = event_tuple[1]
                    
                    if filter_category == "All" or category == filter_category:
                        upcoming.append((date, title, category))
                        if limit and len(upcoming) >= limit:
                            return upcoming
        return upcoming
    
    def get_events_by_category(self, category):
        """Get all events of a specific category"""
        categorized_events = []
        for date, events in self._event_map.items():
            for event_tuple in events:
                title = event_tuple[0]
                event_category = event_tuple[1]
                
                if event_category == category:
                    categorized_events.append((date, title, event_category))
        
        return sorted(categorized_events, key=lambda x: x[0])
    
    def get_events_in_date_range(self, start_date, end_date):
        """Get events within a specific date range"""
        range_events = []
        for date, events in self._event_map.items():
            if start_date <= date <= end_date:
                for event_tuple in events:
                    title = event_tuple[0]
                    category = event_tuple[1]
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
            for event_tuple in events:
                category = event_tuple[1]
                counts[category] = counts.get(category, 0) + 1
        return counts
    
    def search_events(self, search_term, search_in_title=True, search_in_category=False):
        """Search for events by title or category"""
        results = []
        search_term = search_term.lower()
        
        for date, events in self._event_map.items():
            for event_tuple in events:
                title = event_tuple[0]
                category = event_tuple[1]
                match = False
                
                if search_in_title and search_term in title.lower():
                    match = True
                
                if search_in_category and search_term in category.lower():
                    match = True
                
                if match:
                    results.append((date, title, category))
        
        return sorted(results, key=lambda x: x[0])
    
    # NEW TIME-RELATED METHODS
    def get_event_time(self, date, title):
        """Get the time for a specific event"""
        events = self.get_events_for_date(date)
        for event_tuple in events:
            if event_tuple[0] == title:
                if len(event_tuple) >= 3:
                    return event_tuple[2]  # start_time
                else:
                    # Fallback to default time
                    return self.get_default_time_for_category(event_tuple[1])
        return QTime(12, 0)  # Default fallback
    
    def get_events_for_date_with_times(self, date):
        """Get events for a date with full time information"""
        events = self.get_events_for_date(date)
        result = []
        
        for event_tuple in events:
            if len(event_tuple) >= 4:
                title, category, start_time, end_time = event_tuple
                result.append({
                    'title': title,
                    'category': category,
                    'start_time': start_time,
                    'end_time': end_time
                })
            elif len(event_tuple) >= 2:
                title, category = event_tuple[:2]
                start_time = self.get_default_time_for_category(category)
                end_time = start_time.addSecs(3600)
                result.append({
                    'title': title,
                    'category': category,
                    'start_time': start_time,
                    'end_time': end_time
                })
        
        return result
    
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