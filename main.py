# MAIN APPLICATION - Simple connection between Calendar UI and Event Manager
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt6.QtCore import QDate
from PyQt6 import QtWidgets

# Import your existing modules
from calendar_ui import CalendarUi
from event_manager import EventManager
from activities import Ui_MainWindow 


class MainApplication(QMainWindow):
    """Simple main application that connects Calendar UI with Event Manager"""
    
    def __init__(self, user_role="admin"):
        super().__init__()
        self.user_role = user_role
        self.current_view = "calendar"  # Track current view
        
        # Initialize event manager
        self.event_manager = EventManager(main_app=self)
        
        # Setup Calendar UI (default view)
        self.setup_calendar_view()
        
        # Initialize activities UI but don't show it yet
        self.activities_ui = None

    def setup_calendar_view(self):
        """Setup the calendar view as the main content"""
        # Setup Calendar UI
        self.calendar_ui = CalendarUi()
        self.calendar_ui.setupUi(self, self.user_role)
        
        # Connect the upcoming events
        self.populate_upcoming_events()
        
        # Setup filter connection
        self.setup_filter_connection()
        
        # Setup view button connection
        self.setup_view_button()
        
        self.current_view = "calendar"

    def setup_activities_view(self):
        """Setup the activities view as the main content"""
        # Clear the current central widget content
        self.clear_content_area()
        
        # Create activities UI and setup
        self.activities_ui = Ui_MainWindow()
        self.activities_ui.setupUi(self, user_role=self.user_role)
        
        # Connect the back button to return to calendar
        if hasattr(self.activities_ui, 'btnback'):
            self.activities_ui.btnback.clicked.connect(self.show_calendar_view)
        
        # Update window title to reflect activities view
        self.setWindowTitle("Campus Event Manager - Activities")
        
        self.current_view = "activities"

    def clear_content_area(self):
        """Clear the main content area to prepare for new view"""
        # Get the central widget
        central_widget = self.centralWidget()
        if central_widget:
            # Clear the content layout but keep the base structure
            if hasattr(self.calendar_ui, 'contentLayout'):
                # Remove all widgets from content layout
                while self.calendar_ui.contentLayout.count():
                    child = self.calendar_ui.contentLayout.takeAt(0)
                    if child.widget():
                        child.widget().deleteLater()

    def setup_view_button(self):
        """Setup the view button to switch to activities view"""
        try:
            # Connect the btnviewEvent button from calendar_ui.py to show activities
            if hasattr(self.calendar_ui, 'btnviewEvent'):
                self.calendar_ui.btnviewEvent.clicked.connect(self.show_activities_view)
            else:
                print("Warning: btnviewEvent not found in CalendarUi")
        except Exception as e:
            print(f"Error setting up view button: {e}")

    def show_activities_view(self):
        """Switch to activities view in the same window"""
        try:
            self.setup_activities_view()
            
        except Exception as e:
            print(f"Error switching to activities view: {e}")
            QMessageBox.critical(self, "Error", f"Could not switch to activities view: {str(e)}")

    def show_calendar_view(self):
        """Switch back to calendar view in the same window"""
        try:
            print("Switching back to calendar view...")
            
            # Clear current content
            self.clear_content_area()
            
            # Recreate calendar view
            self.setup_calendar_view()
            
            # Update window title back to calendar
            self.setWindowTitle("Campus Event Manager")
            
            print("Calendar view loaded successfully")
            
        except Exception as e:
            print(f"Error switching to calendar view: {e}")
            QMessageBox.critical(self, "Error", f"Could not switch to calendar view: {str(e)}")

    def setup_filter_connection(self):
        """Setup connection for the filter dropdown"""
        # Make sure the filter section is setup
        self.calendar_ui.setup_filter_section()
        
        # Connect the filter change signal to our filter function
        self.calendar_ui.comboUpcomingFilter.currentTextChanged.connect(self.filter_upcoming_events)

    def filter_upcoming_events(self, filter_text):
        """Filter upcoming events based on selected category"""
        try:
            # Only filter if we're in calendar view
            if self.current_view != "calendar":
                return
                
            # Map filter text to categories used by EventManager
            filter_map = {
                "All Events": "All",
                "Academic Activities": "Academic",
                "Organizational Activities": "Organizational", 
                "Deadlines": "Deadline",
                "Holidays": "Holiday"
            }
            
            # Get the category to filter by
            filter_category = filter_map.get(filter_text, "All")
            
            # Get ALL upcoming events first, then filter manually
            all_upcoming_events = self.event_manager.get_upcoming_events("All", limit=None)
            
            # Filter events based on category
            if filter_category == "All":
                filtered_events = all_upcoming_events
            else:
                filtered_events = []
                for date, title, category in all_upcoming_events:
                    if category == filter_category:
                        filtered_events.append((date, title, category))
            
            # Clear the existing list
            self.calendar_ui.listUpcoming.clear()
            
            # Add filtered events to the list
            for date, title, category in filtered_events:
                # Format the date
                formatted_date = date.toString("MMM dd, yyyy")
                
                # Choose icon based on category
                icon_map = {
                    "Academic": "🟢",
                    "Organizational": "🔵", 
                    "Deadline": "🟠",
                    "Holiday": "🔴"
                }
                icon = icon_map.get(category)
                
                # Create the display text
                item_text = f"{icon} {title}\n     {formatted_date}"
                
                # Add to the list widget
                item = QtWidgets.QListWidgetItem(item_text)
                self.calendar_ui.listUpcoming.addItem(item)
            
        except Exception as e:
            print(f"Error filtering upcoming events: {e}")
            # Print more debug info
            import traceback
            traceback.print_exc()

    def populate_upcoming_events(self):
        """Populate upcoming events from Event Manager"""
        try:
            # Only populate if we're in calendar view
            if self.current_view != "calendar":
                return
                
            # Get upcoming events from event manager
            upcoming_events = self.event_manager.get_upcoming_events(limit=None)
            
            # Clear the existing list
            self.calendar_ui.listUpcoming.clear()
            
            # Add events to the upcoming events list
            for date, title, category in upcoming_events:
                # Format the date
                formatted_date = date.toString("MMM dd, yyyy")
                
                # Choose icon based on category
                icon_map = {
                    "Academic": "🟢",
                    "Organizational": "🔵", 
                    "Deadline": "🟠",
                    "Holiday": "🔴"
                }
                icon = icon_map.get(category)
                
                # Create the display text
                item_text = f"{icon} {title}\n    {formatted_date}"
                
                # Add to the list widget
                item = QtWidgets.QListWidgetItem(item_text)
                self.calendar_ui.listUpcoming.addItem(item)
        
            
        except Exception as e:
            print(f"Error populating upcoming events: {e}")

    def update_upcoming_events(self):
        """Update upcoming events - called by EventManager when events change"""
        if self.current_view == "calendar":
            self.populate_upcoming_events()

    def refresh_events_display(self):
        """Refresh events display - called by EventManager"""
        if self.current_view == "calendar":
            self.populate_upcoming_events()


def main():
    """Main function to run the application"""
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("Campus Event Manager")
    
    # Create and show main window with Calendar UI
    # Change user_role here if needed: "admin", "faculty", or "student"
    main_window = MainApplication(user_role="admin")
    main_window.setWindowTitle("Campus Event Manager")
    main_window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()