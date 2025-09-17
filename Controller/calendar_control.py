# CALENDAR_CONTROL.PY - Controller for UI interactions
import sys
import os
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import QTimer, Qt
from PyQt6 import QtWidgets, QtCore

# Add parent directory to path to access Backend
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)


class CalendarController:
    """Controller class to handle UI interactions and events for the calendar application"""
    
    def __init__(self, main_app):
        self.main_app = main_app
        
    def setup_calendar_connections(self):
        """Setup calendar-specific UI connections"""
        try:
            # Setup filter section
            if hasattr(self.main_app.calendar_ui, 'setup_filter_section'):
                self.main_app.calendar_ui.setup_filter_section()
            
            # Connect filter dropdown
            if hasattr(self.main_app.calendar_ui, 'comboUpcomingFilter'):
                try:
                    self.main_app.calendar_ui.comboUpcomingFilter.currentTextChanged.disconnect()
                except:
                    pass
                self.main_app.calendar_ui.comboUpcomingFilter.currentTextChanged.connect(self.on_filter_upcoming_events)
            
            # Connect view dropdown to switch between calendar and day view
            if hasattr(self.main_app.calendar_ui, 'comboView'):
                try:
                    self.main_app.calendar_ui.comboView.currentTextChanged.disconnect()
                except:
                    pass
                self.main_app.calendar_ui.comboView.currentTextChanged.connect(self.on_view_change)
            
            # Connect view button to switch to activities
            if hasattr(self.main_app.calendar_ui, 'btnviewEvent'):
                try:
                    self.main_app.calendar_ui.btnviewEvent.clicked.disconnect()
                except:
                    pass
                self.main_app.calendar_ui.btnviewEvent.clicked.connect(self.on_show_activities_view)
            
            # Connect calendar search bar to search functionality
            if hasattr(self.main_app.calendar_ui, 'searchBarCalendar'):
                try:
                    self.main_app.calendar_ui.searchBarCalendar.returnPressed.disconnect()
                except:
                    pass
                self.main_app.calendar_ui.searchBarCalendar.returnPressed.connect(self.on_perform_search)
            
            # Connect top search bar to search functionality
            if hasattr(self.main_app.calendar_ui, 'searchBarTop'):
                try:
                    self.main_app.calendar_ui.searchBarTop.returnPressed.disconnect()
                except:
                    pass
                self.main_app.calendar_ui.searchBarTop.returnPressed.connect(self.on_perform_search)
            
            # Connect calendar date selection for tracking current date
            if hasattr(self.main_app.calendar_ui, 'calendarWidget'):
                try:
                    self.main_app.calendar_ui.calendarWidget.selectionChanged.disconnect()
                except:
                    pass
                self.main_app.calendar_ui.calendarWidget.selectionChanged.connect(self.on_calendar_date_changed)
                
                # Connect calendar click to go to day view on clicked date
                try:
                    self.main_app.calendar_ui.calendarWidget.clicked.disconnect()
                except:
                    pass
                self.main_app.calendar_ui.calendarWidget.clicked.connect(self.on_calendar_date_clicked)
            
        except Exception as e:
            import traceback
            traceback.print_exc()

    def setup_search_connections(self):
        """Setup search-specific UI connections"""
        try:
            if not self.main_app.search_ui:
                return
            
            # Connect back button to return to calendar
            if hasattr(self.main_app.search_ui, 'btnBack'):
                try:
                    self.main_app.search_ui.btnBack.clicked.disconnect()
                except:
                    pass
                self.main_app.search_ui.btnBack.clicked.connect(self.on_show_calendar_view)
            
            # Connect search button
            if hasattr(self.main_app.search_ui, 'btnSearch'):
                try:
                    self.main_app.search_ui.btnSearch.clicked.disconnect()
                except:
                    pass
                self.main_app.search_ui.btnSearch.clicked.connect(self.on_execute_search_from_ui)
            
            # Connect search bar in search results panel
            if hasattr(self.main_app.search_ui, 'searchBarResults'):
                try:
                    self.main_app.search_ui.searchBarResults.returnPressed.disconnect()
                except:
                    pass
                self.main_app.search_ui.searchBarResults.returnPressed.connect(self.on_execute_search_from_ui)
            
            # Connect top search bar
            if hasattr(self.main_app.search_ui, 'searchBarTop'):
                try:
                    self.main_app.search_ui.searchBarTop.returnPressed.disconnect()
                except:
                    pass
                self.main_app.search_ui.searchBarTop.returnPressed.connect(self.on_execute_search_from_top_bar)
            
            # Connect filter dropdown for search view
            if hasattr(self.main_app.search_ui, 'comboUpcomingFilter'):
                try:
                    self.main_app.search_ui.comboUpcomingFilter.currentTextChanged.disconnect()
                except:
                    pass
                self.main_app.search_ui.comboUpcomingFilter.currentTextChanged.connect(self.on_filter_upcoming_events_search)
            
        except Exception as e:
            import traceback
            traceback.print_exc()

    # Calendar UI Event Handlers
    def on_calendar_date_clicked(self, clicked_date):
        """Handle calendar date click - go to day view for that date"""
        try:
            # Notify backend to handle the logic
            self.main_app.handle_calendar_date_clicked(clicked_date)
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self.main_app, "Error", f"Could not navigate to day view: {str(e)}")

    def on_calendar_date_changed(self):
        """Handle calendar date selection change"""
        try:
            if hasattr(self.main_app.calendar_ui, 'calendarWidget'):
                selected_date = self.main_app.calendar_ui.calendarWidget.selectedDate()
                # Notify backend to update current date
                self.main_app.update_current_date(selected_date)
        except Exception as e:
            import traceback
            traceback.print_exc()

    def on_perform_search(self):
        """Handle search request from UI"""
        try:
            search_query = ""
            
            # Get search query from the appropriate search bar
            if self.main_app.current_view == "calendar" and self.main_app.calendar_ui:
                if hasattr(self.main_app.calendar_ui, 'searchBarCalendar') and self.main_app.calendar_ui.searchBarCalendar.text():
                    search_query = self.main_app.calendar_ui.searchBarCalendar.text().strip()
                elif hasattr(self.main_app.calendar_ui, 'searchBarTop') and self.main_app.calendar_ui.searchBarTop.text():
                    search_query = self.main_app.calendar_ui.searchBarTop.text().strip()
            
            if search_query:
                # Notify backend to handle search
                self.main_app.handle_search_request(search_query)
            else:
                QMessageBox.information(self.main_app, "Search", "Please enter a search term.")
                
        except Exception as e:
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self.main_app, "Error", f"Search failed: {str(e)}")

    def on_view_change(self, view_type):
        """Handle view switching between Month and Day views"""
        try:
            # Notify backend to handle view change
            self.main_app.handle_view_change(view_type)
        except Exception as e:
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self.main_app, "Error", f"Could not switch view: {str(e)}")

    def on_show_activities_view(self):
        """Handle switch to activities view"""
        try:
            # Notify backend to handle activities view
            self.main_app.handle_show_activities_view()
        except Exception as e:
            QMessageBox.critical(self.main_app, "Error", f"Could not switch to activities view: {str(e)}")

    def on_show_calendar_view(self):
        """Handle switch back to calendar view"""
        try:
            # Notify backend to handle calendar view
            self.main_app.handle_show_calendar_view()
        except Exception as e:
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self.main_app, "Error", f"Could not switch to calendar view: {str(e)}")

    def on_filter_upcoming_events(self, filter_text):
        """Handle filtering upcoming events in calendar view"""
        try:
            # Notify backend to handle filtering
            self.main_app.handle_filter_upcoming_events(filter_text)
        except Exception as e:
            import traceback
            traceback.print_exc()

    # Search UI Event Handlers
    def on_execute_search_from_ui(self):
        """Handle search execution from search UI elements"""
        try:
            if not self.main_app.search_ui:
                return
            
            search_query = ""
            if hasattr(self.main_app.search_ui, 'searchBarResults'):
                search_query = self.main_app.search_ui.searchBarResults.text().strip()
            
            if search_query:
                # Notify backend to execute search
                self.main_app.handle_execute_search(search_query)
            else:
                QMessageBox.information(self.main_app, "Search", "Please enter a search term.")
                
        except Exception as e:
            import traceback
            traceback.print_exc()

    def on_execute_search_from_top_bar(self):
        """Handle search execution from top search bar in search view"""
        try:
            if not self.main_app.search_ui:
                return
            
            search_query = ""
            if hasattr(self.main_app.search_ui, 'searchBarTop'):
                search_query = self.main_app.search_ui.searchBarTop.text().strip()
            
            if search_query:
                # Notify backend to execute search
                self.main_app.handle_execute_search(search_query)
            else:
                QMessageBox.information(self.main_app, "Search", "Please enter a search term.")
                
        except Exception as e:
            import traceback
            traceback.print_exc()

    def on_filter_upcoming_events_search(self, filter_text):
        """Handle filtering upcoming events in search view"""
        try:
            # Notify backend to handle search filtering
            self.main_app.handle_filter_upcoming_events_search(filter_text)
        except Exception as e:
            import traceback
            traceback.print_exc()