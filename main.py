# MAIN APPLICATION - Simple connection between Calendar UI and Event Manager
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import QDate
from PyQt6 import QtWidgets

# Import your existing modules
from calendar_ui import CalendarUi
from event_manager import EventManager


class MainApplication(QMainWindow):
    """Simple main application that connects Calendar UI with Event Manager"""
    
    def __init__(self, user_role="admin"):
        super().__init__()
        self.user_role = user_role
        
        # Initialize event manager
        self.event_manager = EventManager(main_app=self)
        
        # Setup Calendar UI
        self.ui = CalendarUi()
        self.ui.setupUi(self, user_role)
        
        # Connect the upcoming events
        self.populate_upcoming_events()
        
        # Setup filter connection
        self.setup_filter_connection()

    def setup_filter_connection(self):
        """Setup connection for the filter dropdown"""
        # Make sure the filter section is setup
        self.ui.setup_filter_section()
        
        # Connect the filter change signal to our filter function
        self.ui.comboUpcomingFilter.currentTextChanged.connect(self.filter_upcoming_events)

    def filter_upcoming_events(self, filter_text):
        """Filter upcoming events based on selected category"""
        try:
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
            
            # # Limit to 10 events
            # filtered_events = filtered_events[:20]
            
            # Clear the existing list
            self.ui.listUpcoming.clear()
            
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
                self.ui.listUpcoming.addItem(item)
            
        except Exception as e:
            print(f"Error filtering upcoming events: {e}")
            # Print more debug info
            import traceback
            traceback.print_exc()

    def populate_upcoming_events(self):
        """Populate upcoming events from Event Manager"""
        try:
            # Get upcoming events from event manager
            upcoming_events = self.event_manager.get_upcoming_events(limit=None)
            
            # Clear the existing list
            self.ui.listUpcoming.clear()
            
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
                self.ui.listUpcoming.addItem(item)
        
            
        except Exception as e:
            print(f"Error populating upcoming events: {e}")

    def update_upcoming_events(self):
        """Update upcoming events - called by EventManager when events change"""
        self.populate_upcoming_events()

    def refresh_events_display(self):
        """Refresh events display - called by EventManager"""
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