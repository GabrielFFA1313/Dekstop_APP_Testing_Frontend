# DAY_VIEW_MANAGER.PY - Backend logic for day view functionality
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import QDate, QTimer, Qt
from PyQt6 import QtWidgets, QtGui, QtCore
from datetime import datetime

from UI.day_view import DayViewUi
from Controller.day_view_controller import DayViewController


class DayViewManager:
    """Manager class for handling day view business logic and data operations"""
    
    def __init__(self, main_app, event_manager):
        self.main_app = main_app
        self.event_manager = event_manager
        self.day_view_ui = None
        # Initialize controller
        self.day_view_controller = DayViewController(self)

    # VIEW SETUP METHODS (Backend Logic)
    def setup_day_view(self, selected_date=None):
        """Setup the day view as the main content - Backend logic"""
        try:
            # Store current geometry
            geometry = self.main_app.geometry() if hasattr(self.main_app, 'geometry') and self.main_app.geometry().isValid() else None
            
            # Set current date
            if selected_date:
                self.main_app.current_date = selected_date
            else:
                self.main_app.current_date = QDate.currentDate()
            
            # Clear any existing central widget
            self.main_app.setCentralWidget(None)
            
            # Force garbage collection to avoid lag
            import gc
            gc.collect()
            
            # Create and setup Day View UI
            self.day_view_ui = DayViewUi()
            self.day_view_ui.setupDayViewUi(self.main_app, self.main_app.user_role)
            
            # Setup connections through controller
            self.day_view_controller.setup_day_view_connections()
            
            # Restore geometry if we had one
            if geometry:
                self.main_app.setGeometry(geometry)
            
            # Load day view data with delay to ensure UI is ready
            QTimer.singleShot(100, self.load_day_view_events)
            
            self.main_app.setWindowTitle("Campus Event Manager - Day View")
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self.main_app, "Error", f"Could not setup day view: {str(e)}")

    # CONTROLLER INTERFACE METHODS (Called by Controller)
    def handle_previous_day(self):
        """Handle previous day navigation logic"""
        self.main_app.current_date = self.main_app.current_date.addDays(-1)
        self.update_day_view_date()
        self.load_day_view_events()

    def handle_next_day(self):
        """Handle next day navigation logic"""
        self.main_app.current_date = self.main_app.current_date.addDays(1)
        self.update_day_view_date()
        self.load_day_view_events()

    def handle_go_to_today(self):
        """Handle go to today navigation logic"""
        self.main_app.current_date = QDate.currentDate()
        self.update_day_view_date()
        self.load_day_view_events()

    def handle_view_change(self, view_type):
        """Handle view switching logic"""
        if view_type == "Month":
            # Switch back to calendar view through main app
            if hasattr(self.main_app, 'handle_show_calendar_view'):
                self.main_app.handle_show_calendar_view()
            elif hasattr(self.main_app, 'setup_calendar_view'):
                self.main_app.setup_calendar_view()
            else:
                QMessageBox.information(self.main_app, "Navigation", "Returning to Calendar View")

    def handle_filter_upcoming_events(self, filter_text):
        """Handle filtering upcoming events logic"""
        self.filter_day_view_upcoming_events(filter_text)

    def handle_search_request(self, search_query):
        """Handle search request logic through main app"""
        if hasattr(self.main_app, 'handle_search_request'):
            self.main_app.handle_search_request(search_query)
        elif hasattr(self.main_app, 'setup_search_view'):
            self.main_app.setup_search_view(search_query)

    def handle_add_event_request(self):
        """Handle add event request logic"""
        if hasattr(self.main_app, 'show_add_event_view'):
            self.main_app.show_add_event_view()

    def handle_time_slot_click(self, hour):
        """Handle time slot click logic for adding events"""
        # Could open add event dialog with pre-filled time
        # For now, just show a message
        QMessageBox.information(self.main_app, "Time Slot", f"Clicked on {hour}:00 time slot")

    def handle_event_click(self, event_title, category):
        """Handle event click logic for viewing/editing events"""
        # Could open event details or edit dialog
        QMessageBox.information(self.main_app, "Event", f"Clicked on event: {event_title} ({category})")

    def handle_date_picker_change(self, selected_date):
        """Handle date picker change logic"""
        self.main_app.current_date = selected_date
        self.update_day_view_date()
        self.load_day_view_events()

    # BUSINESS LOGIC METHODS
    def load_day_view_events(self):
        """Load events for the current day from event manager"""
        try:
            if not self.day_view_ui or not hasattr(self.day_view_ui, 'dayCalendarLayout'):
                return
            
            # Clear existing events from time slots
            self.clear_day_view_events()
            
            # Get events for the current date
            events_dict = self.event_manager.get_events()
            current_date_events = events_dict.get(self.main_app.current_date, [])
            
            # Add events to appropriate time slots
            for title, category in current_date_events:
                # Assign default times based on category
                hour = self.get_default_hour_for_category(category)
                self.add_event_to_time_slot(hour, title, category)
            
            # Update the upcoming events list in day view
            self.populate_day_view_upcoming_events()
            
            # Update the date display
            self.update_day_view_date()
            
        except Exception as e:
            import traceback
            traceback.print_exc()

    def clear_day_view_events(self):
        """Clear all events from day view time slots"""
        try:
            if not hasattr(self.day_view_ui, 'dayCalendarWidget'):
                return
            
            # Find all time slot containers and clear their event areas
            for i in range(self.day_view_ui.dayCalendarLayout.count()):
                time_slot_container = self.day_view_ui.dayCalendarLayout.itemAt(i).widget()
                if time_slot_container and hasattr(time_slot_container, 'layout'):
                    layout = time_slot_container.layout()
                    if layout and layout.count() > 1:
                        # Get the event area widget (second widget in the layout)
                        event_area = layout.itemAt(1).widget()
                        if event_area and hasattr(event_area, 'layout'):
                            event_layout = event_area.layout()
                            # Clear all events from this time slot
                            while event_layout.count():
                                child = event_layout.takeAt(0)
                                if child.widget():
                                    child.widget().deleteLater()
                            
        except Exception as e:
            import traceback
            traceback.print_exc()

    def get_default_hour_for_category(self, category):
        """Get default hour for event category - Business logic"""
        hour_map = {
            "Academic": 9,      # 9 AM
            "Organizational": 14, # 2 PM
            "Deadline": 17,     # 5 PM
            "Holiday": 10       # 10 AM
        }
        return hour_map.get(category, 12)  # Default to 12 PM

    def add_event_to_time_slot(self, hour, title, category):
        """Add an event to a specific time slot - Data operation"""
        try:
            if not hasattr(self.day_view_ui, 'dayCalendarWidget'):
                return
            
            start_hour = 7  # Day view starts at 7 AM
            if hour < start_hour or hour > 19:  # Day view ends at 7 PM
                return
            
            slot_index = hour - start_hour
            
            # Get the time slot container
            if slot_index < self.day_view_ui.dayCalendarLayout.count():
                time_slot_container = self.day_view_ui.dayCalendarLayout.itemAt(slot_index).widget()
                if time_slot_container and hasattr(time_slot_container, 'layout'):
                    layout = time_slot_container.layout()
                    if layout and layout.count() > 1:
                        # Get the event area widget
                        event_area = layout.itemAt(1).widget()
                        if event_area and hasattr(event_area, 'layout'):
                            event_layout = event_area.layout()
                            
                            # Get category color
                            color = self.get_category_color_hex(category)
                            
                            # Add the event using the existing method
                            self.day_view_ui.add_compact_event(event_layout, title, color)
                            
        except Exception as e:
            import traceback
            traceback.print_exc()

    def get_category_color_hex(self, category):
        """Get hex color for event category - Business logic"""
        colors = {
            'Academic': '#4CAF50',      # Green
            'Organizational': '#2196F3', # Blue  
            'Deadline': '#FF9800',      # Orange
            'Holiday': '#F44336'        # Red
        }
        return colors.get(category, '#9E9E9E')  # Default gray

    def populate_day_view_upcoming_events(self):
        """Populate upcoming events list in day view - Data operation"""
        try:
            if not hasattr(self.day_view_ui, 'listUpcoming'):
                return
            
            # Get upcoming events from event manager
            upcoming_events = self.event_manager.get_upcoming_events("All", limit=10)
            
            # Clear the existing list
            self.day_view_ui.listUpcoming.clear()
            
            # Add events to the upcoming events list
            for date, title, category in upcoming_events:
                formatted_date = date.toString("MMM dd, yyyy")
                
                icon_map = {
                    "Academic": "🟢",
                    "Organizational": "🔵", 
                    "Deadline": "🟠",
                    "Holiday": "🔴"
                }
                icon = icon_map.get(category, "⚪")
                
                item_text = f"{icon} {title}\n    {formatted_date}"
                item = QtWidgets.QListWidgetItem(item_text)
                self.day_view_ui.listUpcoming.addItem(item)
                
        except Exception as e:
            import traceback
            traceback.print_exc()

    def filter_day_view_upcoming_events(self, filter_text):
        """Filter upcoming events in day view - Business logic"""
        try:
            if not hasattr(self.day_view_ui, 'listUpcoming'):
                return
            
            # Map filter text to categories
            filter_map = {
                "All Events": "All",
                "Academic Activities": "Academic",
                "Organizational Activities": "Organizational", 
                "Deadlines": "Deadline",
                "Holidays": "Holiday"
            }
            
            filter_category = filter_map.get(filter_text, "All")
            upcoming_events = self.event_manager.get_upcoming_events(filter_category, limit=10)
            
            # Clear and repopulate the list
            self.day_view_ui.listUpcoming.clear()
            
            for date, title, category in upcoming_events:
                formatted_date = date.toString("MMM dd, yyyy")
                
                icon_map = {
                    "Academic": "🟢",
                    "Organizational": "🔵", 
                    "Deadline": "🟠",
                    "Holiday": "🔴"
                }
                icon = icon_map.get(category, "⚪")
                
                item_text = f"{icon} {title}\n    {formatted_date}"
                item = QtWidgets.QListWidgetItem(item_text)
                self.day_view_ui.listUpcoming.addItem(item)
                
        except Exception as e:
            import traceback
            traceback.print_exc()

    def update_day_view_date(self):
        """Update the date label in day view - UI data update"""
        try:
            if hasattr(self.day_view_ui, 'labelCurrentDate'):
                # Convert QDate to string format directly
                formatted_date = self.main_app.current_date.toString("dddd\nMMMM d, yyyy")
                self.day_view_ui.labelCurrentDate.setText(formatted_date)
        except Exception as e:
            import traceback
            traceback.print_exc()

    # PUBLIC INTERFACE METHODS
    def refresh_day_view(self):
        """Refresh day view data and display - Public interface"""
        try:
            self.load_day_view_events()
        except Exception as e:
            import traceback
            traceback.print_exc()

    def get_current_date(self):
        """Get the current date being displayed"""
        return self.main_app.current_date

    def set_current_date(self, date):
        """Set the current date and refresh view"""
        self.main_app.current_date = date
        self.update_day_view_date()
        self.load_day_view_events()

    def get_events_for_current_date(self):
        """Get events for the currently displayed date"""
        events_dict = self.event_manager.get_events()
        return events_dict.get(self.main_app.current_date, [])

    def add_event_to_current_date(self, title, category, hour=None):
        """Add an event to the current date - Business logic"""
        try:
            # Use provided hour or default for category
            if hour is None:
                hour = self.get_default_hour_for_category(category)
            
            # Add event through event manager
            self.event_manager.add_event(self.main_app.current_date, title, category)
            
            # Refresh the display
            self.refresh_day_view()
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self.main_app, "Error", f"Could not add event: {str(e)}")

    def remove_event_from_current_date(self, title):
        """Remove an event from the current date - Business logic"""
        try:
            # Remove event through event manager
            if hasattr(self.event_manager, 'remove_event'):
                self.event_manager.remove_event(self.main_app.current_date, title)
                
                # Refresh the display
                self.refresh_day_view()
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self.main_app, "Error", f"Could not remove event: {str(e)}")

    def get_time_slot_events(self, hour):
        """Get events for a specific time slot"""
        current_events = self.get_events_for_current_date()
        slot_events = []
        
        for title, category in current_events:
            event_hour = self.get_default_hour_for_category(category)
            if event_hour == hour:
                slot_events.append((title, category))
                
        return slot_events

    def is_time_slot_available(self, hour):
        """Check if a time slot is available for new events"""
        slot_events = self.get_time_slot_events(hour)
        # Could implement logic for maximum events per slot
        return len(slot_events) < 3  # Example: max 3 events per time slot