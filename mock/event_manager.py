# EVENT MANAGER - Enhanced with more comprehensive demo data
from PyQt6.QtCore import QDate


class EventManager:
    def __init__(self, main_app=None):
        self.main_app = main_app  # Reference to the main application
        self._event_map = {}
        self.setup_demo_events()
    
    def setup_demo_events(self):
        """Setup comprehensive demo events for testing"""
        events = {
            # August 2025 events
            QDate(2025, 8, 4): [("Start of Classes", "Academic")],
            QDate(2025, 8, 12): [("Organization Expo", "Organizational")],
            QDate(2025, 8, 15): [("Assignment #1 Due", "Deadline")],
            QDate(2025, 8, 19): [("Project Milestone 1", "Deadline")],
            QDate(2025, 8, 21): [("Ninoy Aquino Day", "Holiday")],
            QDate(2025, 8, 25): [("Programming Assignment Due", "Deadline")],
            QDate(2025, 8, 30): [("National Heroes Day", "Holiday")],
            
            # September 2025 events
            QDate(2025, 9, 1): [("New Semester Orientation", "Academic")],
            QDate(2025, 9, 3): [("Faculty Meeting", "Academic")],
            QDate(2025, 9, 5): [("Math Exam", "Academic")],
            QDate(2025, 9, 8): [("Student Council Elections", "Organizational")],
            QDate(2025, 9, 10): [("Computer Science Club Meeting", "Organizational")],
            QDate(2025, 9, 12): [("Research Paper Draft Due", "Deadline")],
            QDate(2025, 9, 15): [("Midterm Exam Period Starts", "Academic")],
            QDate(2025, 9, 18): [("Database Systems Quiz", "Academic")],
            QDate(2025, 9, 20): [("IT Symposium", "Academic")],
            QDate(2025, 9, 22): [("Programming Contest", "Organizational")],
            QDate(2025, 9, 25): [("Project Presentation", "Academic")],
            QDate(2025, 9, 27): [("Career Fair", "Organizational")],
            QDate(2025, 9, 30): [("End of Quarter Assessment", "Academic")],
            
            # October 2025 events
            QDate(2025, 10, 2): [("Software Engineering Workshop", "Academic")],
            QDate(2025, 10, 5): [("Hackathon 2025", "Organizational")],
            QDate(2025, 10, 8): [("Web Development Seminar", "Academic")],
            QDate(2025, 10, 10): [("Thesis Defense - Group A", "Academic")],
            QDate(2025, 10, 12): [("AI/ML Workshop", "Academic")],
            QDate(2025, 10, 15): [("Student Council Meeting", "Organizational")],
            QDate(2025, 10, 17): [("Final Project Proposal Due", "Deadline")],
            QDate(2025, 10, 18): [("Cybersecurity Awareness Day", "Academic")],
            QDate(2025, 10, 20): [("Tech Talk: Industry Trends", "Academic")],
            QDate(2025, 10, 22): [("Alumni Homecoming", "Organizational")],
            QDate(2025, 10, 25): [("Code Review Session", "Academic")],
            QDate(2025, 10, 28): [("Halloween Costume Contest", "Organizational")],
            QDate(2025, 10, 30): [("All Saints' Day Break", "Holiday")],
            
            # November 2025 events
            QDate(2025, 11, 1): [("All Saints' Day", "Holiday")],
            QDate(2025, 11, 3): [("System Analysis Final Project Due", "Deadline")],
            QDate(2025, 11, 5): [("Mobile App Development Contest", "Organizational")],
            QDate(2025, 11, 8): [("Computer Graphics Exhibition", "Academic")],
            QDate(2025, 11, 10): [("Network Security Assessment", "Academic")],
            QDate(2025, 11, 12): [("IT Research Conference", "Academic")],
            QDate(2025, 11, 15): [("Pre-Finals Review Session", "Academic")],
            QDate(2025, 11, 18): [("Capstone Project Showcase", "Academic")],
            QDate(2025, 11, 20): [("Industry Partnership Forum", "Organizational")],
            QDate(2025, 11, 22): [("Thanksgiving Break Starts", "Holiday")],
            QDate(2025, 11, 25): [("Final Exam Schedule Release", "Academic")],
            QDate(2025, 11, 28): [("Study Week Begins", "Academic")],
            QDate(2025, 11, 30): [("Bonifacio Day", "Holiday")],
            
            # December 2025 events
            QDate(2025, 12, 2): [("Finals Week - Day 1", "Academic")],
            QDate(2025, 12, 5): [("Database Systems Final Exam", "Academic")],
            QDate(2025, 12, 8): [("Software Engineering Final Project", "Academic")],
            QDate(2025, 12, 10): [("Web Development Portfolio Due", "Deadline")],
            QDate(2025, 12, 12): [("Last Day of Classes", "Academic")],
            QDate(2025, 12, 15): [("Grade Submission Deadline", "Deadline")],
            QDate(2025, 12, 18): [("Christmas Party", "Organizational")],
            QDate(2025, 12, 20): [("Winter Break Starts", "Holiday")],
            QDate(2025, 12, 25): [("Christmas Day", "Holiday")],
            QDate(2025, 12, 30): [("Rizal Day", "Holiday")],
        }

        # Build event map
        for date, items in events.items():
            self._event_map.setdefault(date, [])
            for title, category in items:
                self._event_map[date].append((title, category))
    
    def get_events(self):
        """Get all events"""
        return self._event_map
    
    def get_events_for_date(self, date):
        """Get events for a specific date"""
        return self._event_map.get(date, [])
    
    def add_event(self, date, title, category):
        """Add a new event"""
        self._event_map.setdefault(date, [])
        self._event_map[date].append((title, category))
        
        # Notify main app if available
        if self.main_app:
            self.refresh_events_display()
    
    def remove_event(self, date, title):
        """Remove an event"""
        if date in self._event_map:
            self._event_map[date] = [
                (t, c) for t, c in self._event_map[date] if t != title
            ]
            if not self._event_map[date]:
                del self._event_map[date]
            
            # Notify main app if available
            if self.main_app:
                self.refresh_events_display()
    
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
        
        # Sort by date
        return sorted(categorized_events, key=lambda x: x[0])
    
    def get_events_in_date_range(self, start_date, end_date):
        """Get events within a specific date range"""
        range_events = []
        for date, events in self._event_map.items():
            if start_date <= date <= end_date:
                for title, category in events:
                    range_events.append((date, title, category))
        
        # Sort by date
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
    
    # Adding of Events
    def handle_new_event(self, event_data):
        """Handle creation of new events"""
        try:
            print(f"New event created: {event_data['title']}")
            
            # Process the event data
            title = event_data['title']
            start_date_str = event_data['start_date']
            end_date_str = event_data['end_date']
            start_time_am = event_data['start_time_am']
            start_time_pm = event_data['start_time_pm']
            end_time_am = event_data['end_time_am']
            end_time_pm = event_data['end_time_pm']
            description = event_data['description']
            location = event_data['location']
            attachment = event_data['attachment']
            
            # Target audience flags
            target_students = event_data['target_students']
            target_faculty = event_data['target_faculty']
            target_org_officers = event_data['target_org_officers']
            target_all = event_data['target_all']
            
            # Parse the date string (assuming MM/dd/yyyy format)
            try:
                if start_date_str:
                    date_parts = start_date_str.split('/')
                    if len(date_parts) == 3:
                        month, day, year = map(int, date_parts)
                        event_date = QDate(year, month, day)
                        
                        # Determine category based on target audience or content
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
                        
                        # Add the event to the event map
                        self.add_event(event_date, title, category)
                        
            except ValueError as date_error:
                print(f"Error parsing date: {date_error}")
            
            # Update the UI with the new event (if main_app reference exists)
            if self.main_app:
                self.refresh_events_display()
                
                # Show success message
                from PyQt6.QtWidgets import QMessageBox
                QMessageBox.information(
                    self.main_app,
                    "Success",
                    f"Event '{title}' has been created successfully!"
                )
            
            # Log the event creation
            print(f"Event Details:")
            print(f"  Title: {title}")
            print(f"  Date: {start_date_str} to {end_date_str}")
            print(f"  Location: {location}")
            print(f"  Description: {description}")
            print(f"  Targets: Students={target_students}, Faculty={target_faculty}, Org Officers={target_org_officers}, All={target_all}")
            
        except Exception as e:
            print(f"Error handling new event: {e}")
            if self.main_app:
                from PyQt6.QtWidgets import QMessageBox
                QMessageBox.critical(
                    self.main_app,
                    "Error",
                    f"Failed to create event: {str(e)}"
                )

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