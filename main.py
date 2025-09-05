# MAIN.PY - Calendar focused main application
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt6.QtCore import QDate, QTimer, Qt
from PyQt6 import QtWidgets, QtGui, QtCore

# Import UI modules
from calendar_ui import CalendarUi
from event_manager import EventManager

# Import view managers
from activities_manager import ActivitiesManager
from day_view_manager import DayViewManager


class MainApplication(QMainWindow):
    """Main application focused on Calendar UI with view managers"""
    
    def __init__(self, user_role="admin"):
        super().__init__()
        self.user_role = user_role
        self.current_view = "calendar"  # Track current view
        self.current_date = QDate.currentDate()  # Track current date
        
        # Initialize event manager
        self.event_manager = EventManager(main_app=self)
        
        # Initialize view managers
        self.activities_manager = ActivitiesManager(self, self.event_manager)
        self.day_view_manager = DayViewManager(self, self.event_manager)
        
        # Initialize calendar UI
        self.calendar_ui = None
        
        # Setup Calendar UI (default view)
        self.setup_calendar_view()

    def setup_calendar_view(self):
        """Setup the calendar view as the main content"""
        try:
            # Store current geometry
            geometry = self.geometry() if hasattr(self, 'geometry') and self.geometry().isValid() else None
            
            # Clear any existing central widget
            self.setCentralWidget(None)
            
            # Create and setup Calendar UI
            self.calendar_ui = CalendarUi()
            self.calendar_ui.setupUi(self, self.user_role)
            
            # Setup connections
            self.setup_calendar_connections()
            
            # Restore geometry if we had one
            if geometry:
                self.setGeometry(geometry)
            
            # Populate upcoming events after UI is ready
            QTimer.singleShot(100, self.populate_upcoming_events)
            
            self.current_view = "calendar"
            self.setWindowTitle("Campus Event Manager - Calendar")
            
        except Exception as e:
            import traceback
            traceback.print_exc()

    def setup_calendar_connections(self):
        """Setup calendar-specific connections"""
        try:
            # Setup filter section
            if hasattr(self.calendar_ui, 'setup_filter_section'):
                self.calendar_ui.setup_filter_section()
            
            # Connect filter dropdown
            if hasattr(self.calendar_ui, 'comboUpcomingFilter'):
                try:
                    self.calendar_ui.comboUpcomingFilter.currentTextChanged.disconnect()
                except:
                    pass
                self.calendar_ui.comboUpcomingFilter.currentTextChanged.connect(self.filter_upcoming_events)
            
            # Connect view dropdown to switch between calendar and day view
            if hasattr(self.calendar_ui, 'comboView'):
                try:
                    self.calendar_ui.comboView.currentTextChanged.disconnect()
                except:
                    pass
                self.calendar_ui.comboView.currentTextChanged.connect(self.handle_view_change)
            
            # Connect view button to switch to activities
            if hasattr(self.calendar_ui, 'btnviewEvent'):
                try:
                    self.calendar_ui.btnviewEvent.clicked.disconnect()
                except:
                    pass
                self.calendar_ui.btnviewEvent.clicked.connect(self.show_activities_view)
            
            # Connect calendar date selection
            if hasattr(self.calendar_ui, 'calendarWidget'):
                try:
                    self.calendar_ui.calendarWidget.selectionChanged.disconnect()
                except:
                    pass
                self.calendar_ui.calendarWidget.selectionChanged.connect(self.on_calendar_date_changed)
            
        except Exception as e:
            import traceback
            traceback.print_exc()

    def handle_view_change(self, view_type):
        """Handle switching between Month and Day views"""
        try:
            if view_type == "Day" and self.current_view == "calendar":
                self.show_day_view()
            elif view_type == "Month" and self.current_view == "day":
                self.setup_calendar_view()
        except Exception as e:
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self, "Error", f"Could not switch view: {str(e)}")

    def on_calendar_date_changed(self):
        """Handle calendar date selection change"""
        try:
            if hasattr(self.calendar_ui, 'calendarWidget'):
                selected_date = self.calendar_ui.calendarWidget.selectedDate()
                self.current_date = selected_date
        except Exception as e:
            import traceback
            traceback.print_exc()

    def show_day_view(self):
        """Switch to day view using day view manager"""
        try:
            self.day_view_manager.setup_day_view(self.current_date)
            self.current_view = "day"
            self.calendar_ui = None  # Clear calendar reference
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not switch to day view: {str(e)}")

    def show_activities_view(self):
        """Switch to activities view using activities manager"""
        try:
            self.activities_manager.setup_activities_view()
            self.current_view = "activities"
            self.calendar_ui = None  # Clear calendar reference
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not switch to activities view: {str(e)}")

    def show_calendar_view(self):
        """Switch back to calendar view"""
        try:
            self.setup_calendar_view()
        except Exception as e:
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self, "Error", f"Could not switch to calendar view: {str(e)}")

    def filter_upcoming_events(self, filter_text):
        """Filter upcoming events based on selected category in calendar view"""
        try:
            if self.current_view != "calendar" or not self.calendar_ui:
                return
            
            if not hasattr(self.calendar_ui, 'listUpcoming'):
                return
                
            # Map filter text to categories used by EventManager
            filter_map = {
                "All Events": "All",
                "Academic Activities": "Academic",
                "Organizational Activities": "Organizational", 
                "Deadlines": "Deadline",
                "Holidays": "Holiday"
            }
            
            filter_category = filter_map.get(filter_text, "All")
            upcoming_events = self.event_manager.get_upcoming_events(filter_category, limit=None)
            
            # Clear the existing list
            self.calendar_ui.listUpcoming.clear()
            
            # Add filtered events to the list
            for date, title, category in upcoming_events:
                formatted_date = date.toString("MMM dd, yyyy")
                
                icon_map = {
                    "Academic": "🟢",
                    "Organizational": "🔵", 
                    "Deadline": "🟠",
                    "Holiday": "🔴"
                }
                icon = icon_map.get(category, "⚪")
                
                item_text = f"{icon} {title}\n     {formatted_date}"
                item = QtWidgets.QListWidgetItem(item_text)
                self.calendar_ui.listUpcoming.addItem(item)
            
        except Exception as e:
            import traceback
            traceback.print_exc()

    def populate_upcoming_events(self):
        """Populate upcoming events from Event Manager in calendar view"""
        try:
            if self.current_view != "calendar" or not self.calendar_ui:
                return
            
            if not hasattr(self.calendar_ui, 'listUpcoming'):
                return
            
            # Get upcoming events from event manager
            upcoming_events = self.event_manager.get_upcoming_events(limit=None)
            
            # Clear the existing list
            self.calendar_ui.listUpcoming.clear()
            
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
                self.calendar_ui.listUpcoming.addItem(item)
            
        except Exception as e:
            import traceback
            traceback.print_exc()

    def update_upcoming_events(self):
        """Update upcoming events - called by EventManager when events change"""
        if self.current_view == "calendar":
            self.populate_upcoming_events()
        elif self.current_view == "day":
            self.day_view_manager.refresh_day_view()
        elif self.current_view == "activities":
            self.activities_manager.refresh_activities()

    def refresh_events_display(self):
        """Refresh events display - called by EventManager"""
        self.update_upcoming_events()


def main():
    """Main function to run the application"""
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("Campus Event Manager")
    
    # Create and show main window with Calendar UI
    main_window = MainApplication(user_role="admin")
    main_window.setWindowTitle("Campus Event Manager")
    main_window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()