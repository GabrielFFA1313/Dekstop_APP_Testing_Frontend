# DAY_VIEW_MANAGER.PY - Handles all day view functionality
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import QDate, QTimer, Qt
from PyQt6 import QtWidgets, QtGui, QtCore
from datetime import datetime

from day_view import DayViewUi


class DayViewManager:
    """Manager class for handling day view functionality"""
    
    def __init__(self, main_app, event_manager):
        self.main_app = main_app
        self.event_manager = event_manager
        self.day_view_ui = None

    def setup_day_view(self, selected_date=None):
        """Setup the day view as the main content"""
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
            
            # Force garbage collection
            import gc
            gc.collect()
            
            # Create and setup Day View UI
            self.day_view_ui = DayViewUi()
            self.day_view_ui.setupDayViewUi(self.main_app, self.main_app.user_role)
            
            # Setup connections
            self.setup_day_view_connections()
            
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

    def setup_day_view_connections(self):
        """Setup day view specific connections"""
        try:
            # Connect day view navigation buttons
            if hasattr(self.day_view_ui, 'btnPrevDay'):
                try:
                    self.day_view_ui.btnPrevDay.clicked.disconnect()
                except:
                    pass
                self.day_view_ui.btnPrevDay.clicked.connect(self.previous_day)
            
            if hasattr(self.day_view_ui, 'btnNextDay'):
                try:
                    self.day_view_ui.btnNextDay.clicked.disconnect()
                except:
                    pass
                self.day_view_ui.btnNextDay.clicked.connect(self.next_day)
            
            if hasattr(self.day_view_ui, 'btnToday'):
                try:
                    self.day_view_ui.btnToday.clicked.disconnect()
                except:
                    pass
                self.day_view_ui.btnToday.clicked.connect(self.go_to_today)
            
            # Connect filter dropdown if it exists in day view
            if hasattr(self.day_view_ui, 'comboUpcomingFilter'):
                try:
                    self.day_view_ui.comboUpcomingFilter.currentTextChanged.disconnect()
                except:
                    pass
                self.day_view_ui.comboUpcomingFilter.currentTextChanged.connect(self.filter_day_view_upcoming_events)
            
        except Exception as e:
            import traceback
            traceback.print_exc()

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
        """Get default hour for event category"""
        hour_map = {
            "Academic": 9,      # 9 AM
            "Organizational": 14, # 2 PM
            "Deadline": 17,     # 5 PM
            "Holiday": 10       # 10 AM
        }
        return hour_map.get(category, 12)  # Default to 12 PM

    def add_event_to_time_slot(self, hour, title, category):
        """Add an event to a specific time slot"""
        try:
            if not hasattr(self.day_view_ui, 'dayCalendarWidget'):
                return
            
            # Calculate which time slot index this hour corresponds to
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
        """Get hex color for event category"""
        colors = {
            'Academic': '#4CAF50',      # Green
            'Organizational': '#2196F3', # Blue  
            'Deadline': '#FF9800',      # Orange
            'Holiday': '#F44336'        # Red
        }
        return colors.get(category, '#9E9E9E')  # Default gray

    def populate_day_view_upcoming_events(self):
        """Populate upcoming events list in day view"""
        try:
            if not hasattr(self.day_view_ui, 'listUpcoming'):
                return
            
            # Get upcoming events from event manager
            upcoming_events = self.event_manager.get_upcoming_events("All", limit=20)
            
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
        """Filter upcoming events in day view"""
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
            upcoming_events = self.event_manager.get_upcoming_events(filter_category, limit=20)
            
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

    def previous_day(self):
        """Navigate to previous day"""
        try:
            self.main_app.current_date = self.main_app.current_date.addDays(-1)
            self.update_day_view_date()
            self.load_day_view_events()
        except Exception as e:
            import traceback
            traceback.print_exc()

    def next_day(self):
        """Navigate to next day"""
        try:
            self.main_app.current_date = self.main_app.current_date.addDays(1)
            self.update_day_view_date()
            self.load_day_view_events()
        except Exception as e:
            import traceback
            traceback.print_exc()

    def go_to_today(self):
        """Navigate to today"""
        try:
            self.main_app.current_date = QDate.currentDate()
            self.update_day_view_date()
            self.load_day_view_events()
        except Exception as e:
            import traceback
            traceback.print_exc()

    def handle_view_change(self, view_type):
        """Handle switching between Day and Month views"""
        try:
            print(f"Day View: handle_view_change called with view_type: {view_type}")  # Debug line
            if view_type == "Month":
                print("Day View: Switching to calendar view...")  # Debug line
                # Switch back to calendar view
                if hasattr(self.main_app, 'show_calendar_view'):
                    self.main_app.show_calendar_view()
                    print("Day View: Successfully called show_calendar_view()")  # Debug line
                elif hasattr(self.main_app, 'setup_calendar_view'):
                    self.main_app.setup_calendar_view()
                    print("Day View: Successfully called setup_calendar_view()")  # Debug line
                else:
                    print("Day View: No calendar view method found!")  # Debug line
                    QMessageBox.information(self.main_app, "Navigation", "Returning to Calendar View")
        except Exception as e:
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self.main_app, "Error", f"Could not switch to calendar view: {str(e)}")

    def update_day_view_date(self):
        """Update the date label in day view"""
        try:
            if hasattr(self.day_view_ui, 'labelCurrentDate'):
                # Convert QDate to string format directly
                formatted_date = self.main_app.current_date.toString("dddd\nMMMM d, yyyy")
                self.day_view_ui.labelCurrentDate.setText(formatted_date)
        except Exception as e:
            import traceback
            traceback.print_exc()

    def refresh_day_view(self):
        """Refresh day view data and display"""
        try:
            self.load_day_view_events()
        except Exception as e:
            import traceback
            traceback.print_exc()