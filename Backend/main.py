# MAIN.PY - Backend Main Application Logic
import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt6.QtCore import QDate, QTimer, Qt
from PyQt6 import QtWidgets, QtGui, QtCore

# Add parent directory to path for imports
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

# Import UI modules
from UI.calendar_ui import CalendarUi
from UI.search import SearchUi 
from mock.event_manager import EventManager

# Import view managers 
from Backend.activities_manager import ActivitiesManager
from Backend.day_view_manager import DayViewManager
from Backend.add_event_manager import AddEventManager

# Import controller
from Controller.calendar_control import CalendarController


class MainApplication(QMainWindow):
    """Main application backend logic focused on data management and business logic"""
    
    def __init__(self, user_role="admin"):
        super().__init__()
        self.user_role = user_role
        self.current_view = "calendar"  # Track current view
        self.current_date = QDate.currentDate()  # Track current date
        
        # Initialize event manager with correct JSON path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        mock_dir = os.path.join(os.path.dirname(current_dir), 'mock')
        json_file_path = os.path.join(mock_dir, 'demo_events.json')
        
        self.event_manager = EventManager(main_app=self, json_file_path=json_file_path)
        
        # Initialize view managers
        self.activities_manager = ActivitiesManager(self, self.event_manager)
        self.day_view_manager = DayViewManager(self, self.event_manager)
        self.add_event_manager = AddEventManager(self, self.event_manager)
        
        # Initialize controller
        self.calendar_controller = CalendarController(self)
        
        # Initialize UI references
        self.calendar_ui = None
        self.search_ui = None
        
        # Setup Calendar UI (default view)
        self.setup_calendar_view()

    # VIEW SETUP METHODS (Backend Logic)
    def setup_calendar_view(self):
        """Setup the calendar view as the main content - Backend logic"""
        try:
            # Store current geometry
            geometry = self.geometry() if hasattr(self, 'geometry') and self.geometry().isValid() else None
            
            # Clear any existing central widget
            self.setCentralWidget(None)
            
            # Create and setup Calendar UI
            self.calendar_ui = CalendarUi()
            self.calendar_ui.setupUi(self, self.user_role)
            
            # Setup connections through controller
            self.calendar_controller.setup_calendar_connections()
            
            # Restore geometry if we had one
            if geometry:
                self.setGeometry(geometry)
            
            # Populate upcoming events after UI is ready
            QTimer.singleShot(100, self.populate_upcoming_events)
            
            self.current_view = "calendar"
            self.search_ui = None  # Clear search reference
            self.setWindowTitle("Campus Event Manager - Calendar")
            
        except Exception as e:
            import traceback
            traceback.print_exc()

    def setup_search_view(self, search_query=""):
        """Setup search view - Backend logic"""
        try:
            # Store current geometry
            geometry = self.geometry()
            
            # Clear any existing central widget
            self.setCentralWidget(None)
            
            # Create and setup Search UI
            self.search_ui = SearchUi()
            self.search_ui.setupSearchUi(self, self.user_role)
            
            # Setup search connections through controller
            self.calendar_controller.setup_search_connections()
            
            # Populate upcoming events in search view
            self.populate_upcoming_events_search()
            
            # Perform search if query provided
            if search_query:
                self.execute_search(search_query)
            
            # Restore geometry
            if geometry:
                self.setGeometry(geometry)
            
            self.current_view = "search"
            self.calendar_ui = None  # Clear calendar reference
            self.setWindowTitle("Campus Event Manager - Search Results")
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self, "Error", f"Could not switch to search view: {str(e)}")

    # CONTROLLER INTERFACE METHODS (Called by Controller)
    def handle_calendar_date_clicked(self, clicked_date):
        """Handle calendar date click logic"""
        # Update current date to the clicked date
        self.current_date = clicked_date
        # Switch to day view with the clicked date
        self.show_day_view()

    def update_current_date(self, selected_date):
        """Update the current date"""
        self.current_date = selected_date

    def handle_search_request(self, search_query):
        """Handle search request logic"""
        self.setup_search_view(search_query)

    def handle_view_change(self, view_type):
        """Handle view switching logic"""
        if view_type == "Day" and self.current_view == "calendar":
            self.show_day_view()
        elif view_type == "Month" and self.current_view == "day":
            self.setup_calendar_view()

    def handle_show_activities_view(self):
        """Handle showing activities view logic"""
        self.show_activities_view()

    def handle_show_calendar_view(self):
        """Handle showing calendar view logic"""
        self.setup_calendar_view()

    def handle_filter_upcoming_events(self, filter_text):
        """Handle filtering upcoming events logic"""
        self.filter_upcoming_events(filter_text)

    def handle_execute_search(self, search_query):
        """Handle search execution logic"""
        self.execute_search(search_query)

    def handle_filter_upcoming_events_search(self, filter_text):
        """Handle filtering upcoming events in search view logic"""
        self.filter_upcoming_events_search(filter_text)

    # BUSINESS LOGIC METHODS
    def show_day_view(self):
        """Switch to day view using day view manager"""
        try:
            self.day_view_manager.setup_day_view(self.current_date)
            self.current_view = "day"
            self.calendar_ui = None  # Clearing calendar reference
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not switch to day view: {str(e)}")

    def show_activities_view(self):
        """Switch to activities view using activities manager"""
        try:
            self.activities_manager.setup_activities_view()
            self.current_view = "activities"
            self.calendar_ui = None  # Clearing calendar reference
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not switch to activities view: {str(e)}")

    def show_add_event_view(self):
        """Switch to add event view using add event manager"""
        try:
            self.add_event_manager.setup_add_event_view()
            self.current_view = "add_event"
            self.calendar_ui = None  # Clearing calendar reference
            self.setWindowTitle("Campus Event Manager - Add Event")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not switch to add event view: {str(e)}")

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

    def filter_upcoming_events_search(self, filter_text):
        """Filter upcoming events in search view"""
        try:
            if self.current_view != "search" or not self.search_ui:
                return
            
            if not hasattr(self.search_ui, 'listUpcoming'):
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
            upcoming_events = self.event_manager.get_upcoming_events(filter_category, limit=10)
            
            # Clear the existing list
            self.search_ui.listUpcoming.clear()
            
            if upcoming_events:
                # Manually limit to 10 events as a safety measure
                limited_events = upcoming_events[:10]
                
                # Add filtered events to the list
                for date, title, category in limited_events:
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
                    self.search_ui.listUpcoming.addItem(item)
            
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
            
            # Get upcoming events from event manager (limited to 10 events for better performance)
            upcoming_events = self.event_manager.get_upcoming_events(limit=10)
            
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

    def populate_upcoming_events_search(self):
        """Populate upcoming events in search view using the proper listUpcoming widget"""
        try:
            if not self.search_ui:
                return
            
            # Use the inherited listUpcoming widget from BaseUi
            if not hasattr(self.search_ui, 'listUpcoming'):
                return
            
            # Clear the existing upcoming events list
            self.search_ui.listUpcoming.clear()
            
            # Get upcoming events from event manager (limited to 10 events)
            upcoming_events = self.event_manager.get_upcoming_events(limit=10)
            
            if upcoming_events:
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
                    
                    item_text = f"{icon} {title}\n     {formatted_date}"
                    item = QtWidgets.QListWidgetItem(item_text)
                    self.search_ui.listUpcoming.addItem(item)
            
        except Exception as e:
            import traceback
            traceback.print_exc()

    # SEARCH LOGIC METHODS
    def execute_search(self, search_query):
        """Execute search through event manager and display results"""
        try:
            if not search_query or not self.search_ui:
                return
            
            # Search through all events in event manager
            search_results = self.search_events(search_query.lower())
            
            # Clear only the search results area (not upcoming events)
            self.clear_search_results_only()
            
            # Display search results in the search results area
            if search_results:
                for date, title, category in search_results:
                    self.add_search_result_to_ui(date, title, category)
                
                # Update search results title
                if hasattr(self.search_ui, 'labelSearchResults'):
                    self.search_ui.labelSearchResults.setText(f"Search Results ({len(search_results)} found)")
            else:
                # No results found
                if hasattr(self.search_ui, 'labelSearchResults'):
                    self.search_ui.labelSearchResults.setText("Search Results (0 found)")
                
                # Add "no results" message to search results area
                no_results_widget = QtWidgets.QLabel("No events found matching your search.")
                no_results_widget.setStyleSheet("""
                    QLabel {
                        color: #666;
                        font-style: italic;
                        padding: 20px;
                        text-align: center;
                    }
                """)
                no_results_widget.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.search_ui.searchResultsContentLayout.addWidget(no_results_widget)
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self, "Error", f"Search execution failed: {str(e)}")

    def search_events(self, search_query):
        """Search through events in event manager"""
        results = []
        all_events = self.event_manager.get_events()
        
        for date, events in all_events.items():
            for title, category in events:
                # Search in title (case-insensitive)
                if search_query in title.lower():
                    results.append((date, title, category))
        
        # Sort results by date
        results.sort(key=lambda x: x[0])
        return results

    def add_search_result_to_ui(self, date, title, category):
        """Add a search result to the search UI"""
        try:
            if not self.search_ui:
                return
            
            # Format date
            formatted_date = date.toString("MMM dd\nyyyy")
            
            # Get color based on category
            color_map = {
                "Academic": "#28a745",
                "Organizational": "#007bff",
                "Deadline": "#fd7e14", 
                "Holiday": "#dc3545"
            }
            color = color_map.get(category, "#6c757d")
            
            # Create the search result item using the search UI's method
            if hasattr(self.search_ui, 'create_search_result_item'):
                self.search_ui.create_search_result_item(formatted_date, title, color, category)
            
        except Exception as e:
            import traceback
            traceback.print_exc()

    def clear_search_results_only(self):
        """Method to clear only the search results area, not upcoming events"""
        try:
            if not self.search_ui:
                return
            
            # Clear only the search results area
            if hasattr(self.search_ui, 'searchResultsContentLayout'):
                # Clear all existing result widgets
                for i in reversed(range(self.search_ui.searchResultsContentLayout.count())):
                    child = self.search_ui.searchResultsContentLayout.itemAt(i).widget()
                    if child:
                        child.setParent(None)
        except Exception as e:
            import traceback
            traceback.print_exc()

    # EVENT MANAGER INTERFACE METHODS
    def update_upcoming_events(self):
        """Update upcoming events - called by EventManager when events change"""
        if self.current_view == "calendar":
            self.populate_upcoming_events()
        elif self.current_view == "day":
            self.day_view_manager.refresh_day_view()
        elif self.current_view == "activities":
            self.activities_manager.refresh_activities()
        elif self.current_view == "search":  
            # Refresh upcoming events in search view
            self.populate_upcoming_events_search()

    def refresh_events_display(self):
        """Refresh events display - called by EventManager"""
        self.update_upcoming_events()


def main():
    """Main function to run the application"""
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("Campus Event Manager")
    
    # Create and show main window with Calendar UI
    # NOTE roles (Admin)(Organization)(Faculty)(Student)
    main_window = MainApplication(user_role="Admin")
    main_window.setWindowTitle("Campus Event Manager")
    main_window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()