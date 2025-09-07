# MAIN.PY - Calendar focused main application (UPDATED with Search Integration)
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt6.QtCore import QDate, QTimer, Qt
from PyQt6 import QtWidgets, QtGui, QtCore

# Import UI modules
from calendar_ui import CalendarUi
from search import SearchUi  # ADDED: Import search UI
from event_manager import EventManager

# Import view managers
from activities_manager import ActivitiesManager
from day_view_manager import DayViewManager
from add_event_manager import AddEventManager


class MainApplication(QMainWindow):
    """Main application focused on Calendar UI with view managers and search functionality"""
    
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
        self.add_event_manager = AddEventManager(self, self.event_manager)
        
        # Initialize UI references
        self.calendar_ui = None
        self.search_ui = None  # ADDED: Search UI reference
        
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
            self.search_ui = None  # Clear search reference
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
            
            # ADDED: Connect calendar search bar to search functionality
            if hasattr(self.calendar_ui, 'searchBarCalendar'):
                try:
                    self.calendar_ui.searchBarCalendar.returnPressed.disconnect()
                except:
                    pass
                self.calendar_ui.searchBarCalendar.returnPressed.connect(self.perform_search)
            
            # ADDED: Connect top search bar to search functionality
            if hasattr(self.calendar_ui, 'searchBarTop'):
                try:
                    self.calendar_ui.searchBarTop.returnPressed.disconnect()
                except:
                    pass
                self.calendar_ui.searchBarTop.returnPressed.connect(self.perform_search)
            
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

    def perform_search(self):
        """ADDED: Perform search based on search bar input"""
        try:
            search_query = ""
            
            # Get search query from the appropriate search bar
            if self.current_view == "calendar" and self.calendar_ui:
                if hasattr(self.calendar_ui, 'searchBarCalendar') and self.calendar_ui.searchBarCalendar.text():
                    search_query = self.calendar_ui.searchBarCalendar.text().strip()
                elif hasattr(self.calendar_ui, 'searchBarTop') and self.calendar_ui.searchBarTop.text():
                    search_query = self.calendar_ui.searchBarTop.text().strip()
            
            if search_query:
                self.show_search_view(search_query)
            else:
                QMessageBox.information(self, "Search", "Please enter a search term.")
                
        except Exception as e:
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self, "Error", f"Search failed: {str(e)}")

    def show_search_view(self, search_query=""):
        """ADDED: Switch to search view and perform search"""
        try:
            # Store current geometry
            geometry = self.geometry()
            
            # Clear any existing central widget
            self.setCentralWidget(None)
            
            # Create and setup Search UI
            self.search_ui = SearchUi()
            self.search_ui.setupSearchUi(self, self.user_role)
            
            # Setup search connections
            self.setup_search_connections()
            
            # FIXED: Populate upcoming events in search view
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

    def setup_search_connections(self):
        """ADDED: Setup search-specific connections"""
        try:
            if not self.search_ui:
                return
            
            # FIXED: Connect back button to return to calendar
            if hasattr(self.search_ui, 'btnBack'):
                try:
                    self.search_ui.btnBack.clicked.disconnect()
                except:
                    pass
                self.search_ui.btnBack.clicked.connect(self.show_calendar_view)
            
            # Connect search button
            if hasattr(self.search_ui, 'btnSearch'):
                try:
                    self.search_ui.btnSearch.clicked.disconnect()
                except:
                    pass
                self.search_ui.btnSearch.clicked.connect(self.execute_search_from_ui)
            
            # Connect search bar in search results panel
            if hasattr(self.search_ui, 'searchBarResults'):
                try:
                    self.search_ui.searchBarResults.returnPressed.disconnect()
                except:
                    pass
                self.search_ui.searchBarResults.returnPressed.connect(self.execute_search_from_ui)
            
            # Connect top search bar
            if hasattr(self.search_ui, 'searchBarTop'):
                try:
                    self.search_ui.searchBarTop.returnPressed.disconnect()
                except:
                    pass
                self.search_ui.searchBarTop.returnPressed.connect(self.execute_search_from_top_bar)
            
            # ADDED: Connect filter dropdown for search view
            if hasattr(self.search_ui, 'comboUpcomingFilter'):
                try:
                    self.search_ui.comboUpcomingFilter.currentTextChanged.disconnect()
                except:
                    pass
                self.search_ui.comboUpcomingFilter.currentTextChanged.connect(self.filter_upcoming_events_search)
            
        except Exception as e:
            import traceback
            traceback.print_exc()

    def filter_upcoming_events_search(self, filter_text):
        """ADDED: Filter upcoming events in search view"""
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
            upcoming_events = self.event_manager.get_upcoming_events(filter_category, limit=None)
            
            # Clear the existing list
            self.search_ui.listUpcoming.clear()
            
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
                self.search_ui.listUpcoming.addItem(item)
            
            print(f"Filtered upcoming events in search view: {filter_category} ({len(upcoming_events)} events)")
            
        except Exception as e:
            import traceback
            traceback.print_exc()

    def populate_upcoming_events_search(self):
        """FIXED: Populate upcoming events in search view using the proper listUpcoming widget"""
        try:
            if not self.search_ui:
                return
            
            # Use the inherited listUpcoming widget from BaseUi, not the search results area
            if not hasattr(self.search_ui, 'listUpcoming'):
                print("Warning: listUpcoming widget not found in search UI")
                return
            
            # Clear the existing upcoming events list
            self.search_ui.listUpcoming.clear()
            
            # Get upcoming events from event manager
            upcoming_events = self.event_manager.get_upcoming_events(limit=None)  # Get all upcoming events
            
            if upcoming_events:
                # Add events to the upcoming events list (same format as calendar view)
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
            
            print(f"Populated {len(upcoming_events) if upcoming_events else 0} events in search view upcoming list")
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f"Error populating upcoming events in search view: {e}")

    def clear_search_results_only(self):
        """ADDED: Method to clear only the search results area, not upcoming events"""
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

    def execute_search(self, search_query):
        """UPDATED: Execute search through event manager and display results"""
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

    def execute_search_from_ui(self):
        """ADDED: Execute search from search UI elements"""
        try:
            if not self.search_ui:
                return
            
            search_query = ""
            if hasattr(self.search_ui, 'searchBarResults'):
                search_query = self.search_ui.searchBarResults.text().strip()
            
            if search_query:
                self.execute_search(search_query)
            else:
                QMessageBox.information(self, "Search", "Please enter a search term.")
                
        except Exception as e:
            import traceback
            traceback.print_exc()

    def execute_search_from_top_bar(self):
        """ADDED: Execute search from top search bar in search view"""
        try:
            if not self.search_ui:
                return
            
            search_query = ""
            if hasattr(self.search_ui, 'searchBarTop'):
                search_query = self.search_ui.searchBarTop.text().strip()
            
            if search_query:
                self.execute_search(search_query)
            else:
                QMessageBox.information(self, "Search", "Please enter a search term.")
                
        except Exception as e:
            import traceback
            traceback.print_exc()

    def execute_search(self, search_query):
        """ADDED: Execute search through event manager and display results"""
        try:
            if not search_query or not self.search_ui:
                return
            
            # Search through all events in event manager
            search_results = self.search_events(search_query.lower())
            
            # Clear existing search results
            if hasattr(self.search_ui, 'searchResultsContentLayout'):
                # Clear all existing result widgets
                for i in reversed(range(self.search_ui.searchResultsContentLayout.count())):
                    child = self.search_ui.searchResultsContentLayout.itemAt(i).widget()
                    if child:
                        child.setParent(None)
            
            # Display search results
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
                
                # Add "no results" message
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
        """ADDED: Search through events in event manager"""
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
        """ADDED: Add a search result to the search UI"""
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

    def show_add_event_view(self):
        """Switch to add event view using add event manager"""
        try:
            self.add_event_manager.setup_add_event_view()
            self.current_view = "add_event"
            self.calendar_ui = None  # Clear calendar reference
            self.setWindowTitle("Campus Event Manager - Add Event")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not switch to add event view: {str(e)}")

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
        elif self.current_view == "add_event":
            # No refresh needed for add event view
            pass
        elif self.current_view == "search":  # FIXED: Handle search view properly
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
    main_window = MainApplication(user_role="admin")
    main_window.setWindowTitle("Campus Event Manager")
    main_window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()