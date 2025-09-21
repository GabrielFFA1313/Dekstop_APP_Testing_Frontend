# MAIN.PY - Backend Main Application Logic with Enhanced Router Navigation Integration
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

# Import navigation router
from Paging.navigation_router import NavigationRouter


class MainApplication(QMainWindow):
    """Main application backend logic with enhanced router integration and permission management"""
    
    def __init__(self, user_role="admin"):
        super().__init__()
        self.user_role = user_role.lower()  # Ensure consistent case
        self.current_view = "calendar"  # Track current view
        self.current_date = QDate.currentDate()  # Track current date
        
        # Initialize event manager with correct JSON path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        mock_dir = os.path.join(os.path.dirname(current_dir), 'mock')
        json_file_path = os.path.join(mock_dir, 'demo_events.json')
        
        self.event_manager = EventManager(main_app=self, json_file_path=json_file_path)
        
        # Initialize navigation router FIRST with JSON state file in Paging directory
        paging_dir = os.path.join(os.path.dirname(current_dir), 'Paging')
        router_json_path = os.path.join(paging_dir, 'navigation_state.json')
        self.router = NavigationRouter(self, router_json_path)
        
        # Initialize view managers
        self.activities_manager = ActivitiesManager(self, self.event_manager)
        self.day_view_manager = DayViewManager(self, self.event_manager)
        self.add_event_manager = AddEventManager(self, self.event_manager)
        
        # Initialize controller
        self.calendar_controller = CalendarController(self)
        
        # Initialize UI references
        self.calendar_ui = None
        self.search_ui = None
        
        # Start with the route from JSON (or default based on user permissions)
        current_route = self.router.get_current_route()
        if current_route and self.router.is_view_allowed(current_route['view']):
            self.router.navigate_to(current_route['view'], current_route.get('params', {}))
        else:
            # Use default view for user role if current route is not allowed
            default_view = self.router.get_default_view_for_user()
            self.router.navigate_to(default_view, {})

    # PERMISSION CHECKING METHODS
    def check_permission_and_redirect(self, requested_view, fallback_view="calendar"):
        """Check if user has permission for requested view, redirect if not"""
        if not self.router.is_view_allowed(requested_view):
            QMessageBox.warning(
                self,
                "Access Denied",
                f"You do not have permission to access this feature.\n"
                f"User role: {self.user_role.title()}\n"
                f"Required permissions not available for this action."
            )
            self.router.to_calendar()  # Always redirect to calendar as safe fallback
            return False
        return True

    def can_modify_events(self):
        """Check if user can add/edit events"""
        permissions = self.router.get_user_permissions()
        return permissions['can_add_events'] or permissions['can_edit_events']

    def can_edit_activities(self):
        """Check if current user can edit/delete activities - Used by ActivitiesManager"""
        permissions = self.router.get_user_permissions()
        return permissions['can_edit_events'] and permissions['can_delete_events']

    def can_add_activities(self):
        """Check if current user can add new activities - Used by ActivitiesManager"""
        permissions = self.router.get_user_permissions()
        return permissions['can_add_events']

    # VIEW CREATION METHODS (Enhanced with router state integration)
    def create_calendar_view(self, params=None, saved_state=None):
        """Create calendar view UI components with router state integration"""
        try:
            # Store current geometry to preserve window size
            geometry = self.geometry() if hasattr(self, 'geometry') and self.geometry().isValid() else None
            
            # Clear any existing central widget
            self.setCentralWidget(None)
            
            # Force garbage collection
            import gc
            gc.collect()
            
            # Create and setup Calendar UI
            self.calendar_ui = CalendarUi()
            self.calendar_ui.setupUi(self, self.user_role)
            
            # Setup connections through controller
            self.calendar_controller.setup_calendar_connections()
            
            # Apply parameters from router
            if params:
                selected_date = params.get('selected_date')
                if selected_date and hasattr(self.calendar_ui, 'calendarWidget'):
                    self.calendar_ui.calendarWidget.setSelectedDate(selected_date)
                    self.current_date = selected_date
            
            # Restore saved state from router
            if saved_state:
                if saved_state.get('selected_date'):
                    if hasattr(self.calendar_ui, 'calendarWidget'):
                        self.calendar_ui.calendarWidget.setSelectedDate(saved_state['selected_date'])
                        self.current_date = saved_state['selected_date']
                
                if saved_state.get('filter_selection'):
                    if hasattr(self.calendar_ui, 'comboUpcomingFilter'):
                        index = self.calendar_ui.comboUpcomingFilter.findText(saved_state['filter_selection'])
                        if index >= 0:
                            self.calendar_ui.comboUpcomingFilter.setCurrentIndex(index)
            
            # Populate upcoming events after UI is ready
            QTimer.singleShot(100, self.populate_upcoming_events)
            
            # Restore geometry to preserve window size
            if geometry:
                self.setGeometry(geometry)
            
            self.current_view = "calendar"
            self.search_ui = None  # Clear search reference
            self.setWindowTitle(f"Campus Event Manager - Calendar ({self.user_role.title()})")
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self, "Error", f"Could not create calendar view: {str(e)}")

    def create_search_view(self, params=None, saved_state=None):
        """Create search view UI components with router state integration"""
        try:
            search_query = params.get('query', '') if params else ''
            
            # Store current geometry to preserve window size
            geometry = self.geometry() if hasattr(self, 'geometry') and self.geometry().isValid() else None
            
            # Clear any existing central widget
            self.setCentralWidget(None)
            
            # Force garbage collection
            import gc
            gc.collect()
            
            # Create and setup Search UI
            self.search_ui = SearchUi()
            self.search_ui.setupSearchUi(self, self.user_role)
            
            # Setup search connections through controller
            self.calendar_controller.setup_search_connections()
            
            # Populate upcoming events in search view
            self.populate_upcoming_events_search()
            
            # Apply saved state if available
            if saved_state:
                # Could restore search filters or previous search query here
                pass
            
            # Perform search if query provided
            if search_query:
                self.execute_search(search_query)
            
            # Restore geometry to preserve window size
            if geometry:
                self.setGeometry(geometry)
            
            self.current_view = "search"
            self.calendar_ui = None  # Clear calendar reference
            self.setWindowTitle(f"Campus Event Manager - Search Results ({self.user_role.title()})")
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self, "Error", f"Could not create search view: {str(e)}")

    def create_day_view(self, params=None, saved_state=None):
        """Create day view UI components with router state integration"""
        try:
            # Get date from params first, then saved_state, then current_date
            selected_date = None
            if params and params.get('date'):
                selected_date = params['date']
            elif saved_state and saved_state.get('current_date'):
                selected_date = saved_state['current_date']
            else:
                selected_date = self.current_date
            
            # Store current geometry to preserve window size
            geometry = self.geometry() if hasattr(self, 'geometry') and self.geometry().isValid() else None
            
            # Clear any existing central widget
            self.setCentralWidget(None)
            
            # Force garbage collection
            import gc
            gc.collect()
            
            # Setup day view UI
            self.day_view_manager.setup_day_view_ui(selected_date)
            
            # Update current date
            self.current_date = selected_date
            
            # Restore additional saved state if available
            if saved_state:
                self.day_view_manager.restore_day_view_state(saved_state)
            
            self.current_view = "day_view"
            self.calendar_ui = None  # Clear calendar reference
            self.setWindowTitle(f"Campus Event Manager - Day View ({self.user_role.title()})")
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self, "Error", f"Could not create day view: {str(e)}")

    def create_activities_view(self, params=None, saved_state=None):
        """Create activities view UI components with router state integration"""
        try:
            # Clear any existing central widget
            self.setCentralWidget(None)
            
            # Force garbage collection
            import gc
            gc.collect()
            
            # Setup activities UI
            self.activities_manager.setup_activities_ui()
            
            # Restore saved state if available
            if saved_state:
                self.activities_manager.restore_activities_state(saved_state)
            
            self.current_view = "activities"
            self.calendar_ui = None  # Clear calendar reference
            self.setWindowTitle(f"Campus Event Manager - Activities ({self.user_role.title()})")
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self, "Error", f"Could not create activities view: {str(e)}")

    def create_add_event_view(self, params=None, saved_state=None):
        """Create add event view UI components with permission checking"""
        try:
            # Check permissions before creating view
            if not self.check_permission_and_redirect("add_event"):
                return
            
            # Clear any existing central widget
            self.setCentralWidget(None)
            
            # Force garbage collection
            import gc
            gc.collect()
            
            # Setup add event UI
            self.add_event_manager.setup_add_event_ui()
            
            # Apply parameters (like pre-filled date)
            if params:
                if params.get('preset_date') and hasattr(self.add_event_manager, 'set_date'):
                    self.add_event_manager.set_date(params['preset_date'])
            
            # Restore saved state if available (but be cautious about form data)
            if saved_state:
                # Only restore non-sensitive UI state, not form data
                self.add_event_manager.restore_event_form_state(saved_state)
            
            self.current_view = "add_event"
            self.calendar_ui = None  # Clear calendar reference
            self.setWindowTitle(f"Campus Event Manager - Add Event ({self.user_role.title()})")
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self, "Error", f"Could not create add event view: {str(e)}")

    def create_edit_event_view(self, params=None, saved_state=None):
        """Create edit event view UI components with permission checking"""
        try:
            # Check permissions before creating view
            if not self.check_permission_and_redirect("edit_event"):
                return
            
            event_data = params.get('event_data') if params else None
            if not event_data:
                QMessageBox.warning(self, "Error", "No event data provided for editing.")
                self.router.to_calendar()
                return
            
            # Clear any existing central widget
            self.setCentralWidget(None)
            
            # Force garbage collection
            import gc
            gc.collect()
            
            # Setup edit event UI
            self.add_event_manager.setup_edit_event_ui(event_data)
            
            # Restore saved state if available (but prioritize event_data)
            if saved_state:
                self.add_event_manager.restore_event_form_state(saved_state)
            
            self.current_view = "edit_event"
            self.calendar_ui = None  # Clear calendar reference
            self.setWindowTitle(f"Campus Event Manager - Edit Event ({self.user_role.title()})")
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self, "Error", f"Could not create edit event view: {str(e)}")

    # ROUTER-INTEGRATED CONTROLLER INTERFACE METHODS
    def handle_calendar_date_clicked(self, clicked_date):
        """Handle calendar date click - use router for navigation"""
        self.current_date = clicked_date
        self.router.to_day_view(clicked_date)

    def handle_search_request(self, search_query):
        """Handle search request - use router for navigation"""
        self.router.to_search(search_query)

    def handle_view_change(self, view_type):
        """Handle view switching - use router for navigation"""
        if view_type == "Day" and self.current_view == "calendar":
            self.router.to_day_view(self.current_date)
        elif view_type == "Month" and self.current_view == "day_view":
            self.router.to_calendar()

    def handle_show_activities_view(self):
        """Handle showing activities view - use router"""
        self.router.to_activities()

    def handle_show_calendar_view(self):
        """Handle showing calendar view - use router"""
        self.router.to_calendar()

    def handle_add_event_request(self, preset_date=None):
        """Handle add event request with permission checking"""
        if preset_date:
            self.router.navigate_to('add_event', {'preset_date': preset_date})
        else:
            self.router.to_add_event()

    def handle_edit_event_request(self, event_data):
        """Handle edit event request with permission checking"""
        self.router.to_edit_event(event_data)

    def handle_navigation_back(self):
        """Handle back navigation using router"""
        success = self.router.go_back()
        if not success:
            # If no history, go to default view
            self.router.to_calendar()

    def handle_time_slot_click(self, hour):
        """Handle time slot click from day view - could open add event with preset time"""
        if self.can_add_activities():
            preset_date = self.current_date
            self.router.navigate_to('add_event', {
                'preset_date': preset_date,
                'preset_hour': hour
            })
        else:
            QMessageBox.information(
                self, 
                "Time Slot", 
                f"Selected {hour}:00 time slot on {self.current_date.toString('MMM dd, yyyy')}"
            )

    def handle_event_click(self, event_title, category, event_date=None):
        """Handle event click from various views - could show details or edit"""
        if event_date is None:
            event_date = self.current_date
            
        # Create event data for potential editing
        event_data = {
            'title': event_title,
            'category': category,
            'date': event_date
        }
        
        if self.can_edit_activities():
            # Show edit dialog
            reply = QMessageBox.question(
                self,
                "Event Action",
                f"What would you like to do with '{event_title}'?",
                QMessageBox.StandardButton.No,  # View Details (default)
                QMessageBox.StandardButton.Yes  # Edit Event
            )
            reply.button(QMessageBox.StandardButton.Yes).setText("Edit Event")
            reply.button(QMessageBox.StandardButton.No).setText("View Details")
            
            if reply == QMessageBox.StandardButton.Yes:
                self.handle_edit_event_request(event_data)
            else:
                self.show_event_details(event_data)
        else:
            self.show_event_details(event_data)

    def show_event_details(self, event_data):
        """Show event details in a message box"""
        details = f"Event: {event_data['title']}\n"
        details += f"Type: {event_data['category']}\n"
        details += f"Date: {event_data['date'].toString('MMM dd, yyyy')}"
        
        QMessageBox.information(self, "Event Details", details)

    # ROUTER STATE UPDATE METHODS
    def update_current_date(self, selected_date):
        """Update the current date and notify router if needed"""
        self.current_date = selected_date
        # Router will save this state automatically when navigating

    def handle_filter_upcoming_events(self, filter_text):
        """Handle filtering upcoming events with state management"""
        self.filter_upcoming_events(filter_text)
        # State will be saved by router when navigating away

    def handle_execute_search(self, search_query):
        """Handle search execution with state management"""
        self.execute_search(search_query)

    def handle_filter_upcoming_events_search(self, filter_text):
        """Handle filtering upcoming events in search view"""
        self.filter_upcoming_events_search(filter_text)

    # PERMISSION-AWARE LEGACY METHODS (Updated to use router with permission checks)
    def show_day_view(self):
        """Legacy method - use router instead"""
        self.router.to_day_view(self.current_date)

    def show_activities_view(self):
        """Legacy method - use router instead"""
        self.router.to_activities()

    def show_add_event_view(self):
        """Legacy method - use router with permission check"""
        self.router.to_add_event()

    def setup_calendar_view(self):
        """Legacy method - use router instead"""
        self.router.to_calendar()

    def setup_search_view(self, search_query=""):
        """Legacy method - use router instead"""
        self.router.to_search(search_query)

    # BUSINESS LOGIC METHODS (Unchanged but with better error handling)
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

    # SEARCH LOGIC METHODS (Unchanged)
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
            for event_tuple in events:
                title = event_tuple[0]  # Handle both old and new tuple formats
                category = event_tuple[1]
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

    # EVENT MANAGER INTERFACE METHODS (Updated with enhanced manager integration)
    def update_upcoming_events(self):
        """Update upcoming events - called by EventManager when events change"""
        if self.current_view == "calendar":
            self.populate_upcoming_events()
        elif self.current_view == "day_view":
            if hasattr(self.day_view_manager, 'refresh_day_view'):
                self.day_view_manager.refresh_day_view()
        elif self.current_view == "activities":
            if hasattr(self.activities_manager, 'refresh_activities'):
                self.activities_manager.refresh_activities()
        elif self.current_view == "search":  
            # Refresh upcoming events in search view
            self.populate_upcoming_events_search()
        elif self.current_view in ["add_event", "edit_event"]:
            if hasattr(self.add_event_manager, 'refresh_upcoming_events'):
                self.add_event_manager.refresh_upcoming_events()

    def refresh_events_display(self):
        """Refresh events display - called by EventManager and managers"""
        self.update_upcoming_events()

    def refresh_all_displays(self):
        """Comprehensive refresh of all displays - used by managers after CRUD operations"""
        try:
            # Refresh event manager first
            if hasattr(self.event_manager, 'refresh_events_display'):
                self.event_manager.refresh_events_display()
            
            # Refresh current view
            self.update_upcoming_events()
            
            # Refresh specific managers
            if hasattr(self.activities_manager, 'refresh_activities'):
                self.activities_manager.refresh_activities()
            
            if hasattr(self.day_view_manager, 'refresh_day_view'):
                self.day_view_manager.refresh_day_view()
            
            if hasattr(self.add_event_manager, 'populate_upcoming_events'):
                self.add_event_manager.populate_upcoming_events()
                
        except Exception as e:
            pass  # Error during comprehensive refresh

    def on_event_created(self, event_data):
        """Called when an event is successfully created - used by AddEventManager"""
        self.refresh_all_displays()
        
    def on_event_updated(self, event_data):
        """Called when an event is successfully updated - used by AddEventManager"""
        self.refresh_all_displays()
        
    def on_event_deleted(self, event_data):
        """Called when an event is successfully deleted - used by ActivitiesManager"""
        self.refresh_all_displays()

    # ROUTER UTILITY METHODS
    def get_current_permissions(self):
        """Get current user permissions from router"""
        return self.router.get_user_permissions()

    def cleanup_router_data(self):
        """Force cleanup of router data"""
        self.router.force_cleanup()

    # APPLICATION SHUTDOWN AND CLEANUP
    def closeEvent(self, event):
        """Handle application shutdown - ensure router state is saved"""
        try:
            # Save router state before closing
            self.router.save_navigation_state()
            
            # Cleanup any manager resources
            try:
                if hasattr(self.day_view_manager, 'cleanup'):
                    self.day_view_manager.cleanup()
                if hasattr(self.activities_manager, 'cleanup'):
                    self.activities_manager.cleanup()
                if hasattr(self.add_event_manager, 'cleanup'):
                    self.add_event_manager.cleanup()
            except Exception as cleanup_error:
                pass  # Error during manager cleanup
                
        except Exception as e:
            pass  # Error saving router state on shutdown
        
        # Call parent close event
        super().closeEvent(event)

    def get_category_color_hex(self, category):
        """Get hex color for event category - utility method for managers"""
        colors = {
            'Academic': '#4CAF50',      # Green
            'Organizational': '#2196F3', # Blue  
            'Deadline': '#FF9800',      # Orange
            'Holiday': '#F44336'        # Red
        }
        return colors.get(category, '#9E9E9E')  # Default gray

    def format_date_for_display(self, date):
        """Format date for consistent display across managers"""
        if isinstance(date, QDate):
            return date.toString("MMM dd, yyyy")
        return str(date)

    def format_time_for_display(self, time):
        """Format time for consistent display across managers"""
        if hasattr(time, 'toString'):
            return time.toString("h:mm AP")
        return str(time)


def main():
    """Main function to run the application with different user role options"""
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("Campus Event Manager")
    
    # User role options and their capabilities:
    # - "admin": Can add, edit, delete all events and access all views
    # - "organization" or "org": Can add events but not edit/delete existing ones
    # - "faculty": Can add events but not edit/delete existing ones  
    # - "student": Can only view events, cannot add/edit/delete
    
    # Change this to test different permission levels:
    user_role = "admin"  # Try: "admin", "organization", "faculty", "student"
    
    try:
        main_window = MainApplication(user_role=user_role)
        main_window.setWindowTitle(f"Campus Event Manager - {user_role.title()} Mode")
        main_window.show()
        
        sys.exit(app.exec())
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        
        # Show error dialog
        error_app = QApplication([]) if not QApplication.instance() else QApplication.instance()
        QMessageBox.critical(
            None,
            "Application Error",
            f"Failed to start Campus Event Manager:\n\n{str(e)}\n\nCheck console for detailed error information."
        )
        sys.exit(1)


if __name__ == "__main__":
    main()