# DAY_VIEW_CONTROLLER.PY - Controller for day view UI interactions
import sys
import os
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import QDate, Qt
from PyQt6 import QtWidgets, QtCore

# Add parent directory to path to access Backend
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)


class DayViewController:
    """Controller class to handle UI interactions and events for the day view"""
    
    def __init__(self, day_view_manager):
        self.day_view_manager = day_view_manager
        self.main_app = day_view_manager.main_app
        
    def setup_day_view_connections(self):
        """Setup day view specific UI connections"""
        try:
            if not self.day_view_manager.day_view_ui:
                return
                
            # Connect view dropdown to switch back to calendar
            if hasattr(self.day_view_manager.day_view_ui, 'comboView'):
                try:
                    self.day_view_manager.day_view_ui.comboView.currentTextChanged.disconnect()
                except:
                    pass
                self.day_view_manager.day_view_ui.comboView.currentTextChanged.connect(self.on_view_change)
                
            # Connect day view navigation buttons
            if hasattr(self.day_view_manager.day_view_ui, 'btnPrevDay'):
                try:
                    self.day_view_manager.day_view_ui.btnPrevDay.clicked.disconnect()
                except:
                    pass
                self.day_view_manager.day_view_ui.btnPrevDay.clicked.connect(self.on_previous_day)
            
            if hasattr(self.day_view_manager.day_view_ui, 'btnNextDay'):
                try:
                    self.day_view_manager.day_view_ui.btnNextDay.clicked.disconnect()
                except:
                    pass
                self.day_view_manager.day_view_ui.btnNextDay.clicked.connect(self.on_next_day)
            
            if hasattr(self.day_view_manager.day_view_ui, 'btnToday'):
                try:
                    self.day_view_manager.day_view_ui.btnToday.clicked.disconnect()
                except:
                    pass
                self.day_view_manager.day_view_ui.btnToday.clicked.connect(self.on_go_to_today)
            
            # Connect filter dropdown if it exists in day view
            if hasattr(self.day_view_manager.day_view_ui, 'comboUpcomingFilter'):
                try:
                    self.day_view_manager.day_view_ui.comboUpcomingFilter.currentTextChanged.disconnect()
                except:
                    pass
                self.day_view_manager.day_view_ui.comboUpcomingFilter.currentTextChanged.connect(self.on_filter_upcoming_events)
            
            # Connect search bars if they exist
            if hasattr(self.day_view_manager.day_view_ui, 'searchBarTop'):
                try:
                    self.day_view_manager.day_view_ui.searchBarTop.returnPressed.disconnect()
                except:
                    pass
                self.day_view_manager.day_view_ui.searchBarTop.returnPressed.connect(self.on_search_request)
            
            # Connect any add event button if it exists
            if hasattr(self.day_view_manager.day_view_ui, 'btnAddEvent'):
                try:
                    self.day_view_manager.day_view_ui.btnAddEvent.clicked.disconnect()
                except:
                    pass
                self.day_view_manager.day_view_ui.btnAddEvent.clicked.connect(self.on_add_event)
            
        except Exception as e:
            import traceback
            traceback.print_exc()

    # Navigation Event Handlers
    def on_previous_day(self):
        """Handle previous day navigation button click"""
        try:
            # Notify day view manager to handle the logic
            self.day_view_manager.handle_previous_day()
        except Exception as e:
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self.main_app, "Error", f"Could not navigate to previous day: {str(e)}")

    def on_next_day(self):
        """Handle next day navigation button click"""
        try:
            # Notify day view manager to handle the logic
            self.day_view_manager.handle_next_day()
        except Exception as e:
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self.main_app, "Error", f"Could not navigate to next day: {str(e)}")

    def on_go_to_today(self):
        """Handle go to today button click"""
        try:
            # Notify day view manager to handle the logic
            self.day_view_manager.handle_go_to_today()
        except Exception as e:
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self.main_app, "Error", f"Could not navigate to today: {str(e)}")

    # View Change Event Handlers
    def on_view_change(self, view_type):
        """Handle view switching between Day and Month views"""
        try:
            # Notify day view manager to handle the logic
            self.day_view_manager.handle_view_change(view_type)
        except Exception as e:
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self.main_app, "Error", f"Could not switch view: {str(e)}")

    # Filter Event Handlers
    def on_filter_upcoming_events(self, filter_text):
        """Handle filtering upcoming events dropdown change"""
        try:
            # Notify day view manager to handle the logic
            self.day_view_manager.handle_filter_upcoming_events(filter_text)
        except Exception as e:
            import traceback
            traceback.print_exc()

    # Search Event Handlers
    def on_search_request(self):
        """Handle search request from search bar"""
        try:
            search_query = ""
            if hasattr(self.day_view_manager.day_view_ui, 'searchBarTop'):
                search_query = self.day_view_manager.day_view_ui.searchBarTop.text().strip()
            
            if search_query:
                # Notify main app through day view manager to handle search
                self.day_view_manager.handle_search_request(search_query)
            else:
                QMessageBox.information(self.main_app, "Search", "Please enter a search term.")
                
        except Exception as e:
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self.main_app, "Error", f"Search failed: {str(e)}")

    # Event Management Event Handlers
    def on_add_event(self):
        """Handle add event button click"""
        try:
            # Notify day view manager to handle the logic
            self.day_view_manager.handle_add_event_request()
        except Exception as e:
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self.main_app, "Error", f"Could not open add event: {str(e)}")

    # Time Slot Event Handlers
    def on_time_slot_click(self, hour):
        """Handle time slot click for adding events"""
        try:
            # Notify day view manager to handle time slot interaction
            self.day_view_manager.handle_time_slot_click(hour)
        except Exception as e:
            import traceback
            traceback.print_exc()

    def on_event_click(self, event_title, category):
        """Handle clicking on an event in the day view"""
        try:
            # Notify day view manager to handle event interaction
            self.day_view_manager.handle_event_click(event_title, category)
        except Exception as e:
            import traceback
            traceback.print_exc()

    # Calendar Widget Event Handlers (if date picker exists)
    def on_date_picker_change(self, selected_date):
        """Handle date picker change if one exists in day view"""
        try:
            # Notify day view manager to handle date change
            self.day_view_manager.handle_date_picker_change(selected_date)
        except Exception as e:
            import traceback
            traceback.print_exc()

    # Utility Methods for UI State
    def get_current_filter_selection(self):
        """Get current filter selection from UI"""
        if hasattr(self.day_view_manager.day_view_ui, 'comboUpcomingFilter'):
            return self.day_view_manager.day_view_ui.comboUpcomingFilter.currentText()
        return "All Events"

    def get_current_search_query(self):
        """Get current search query from UI"""
        if hasattr(self.day_view_manager.day_view_ui, 'searchBarTop'):
            return self.day_view_manager.day_view_ui.searchBarTop.text().strip()
        return ""

    def clear_search_bar(self):
        """Clear the search bar"""
        if hasattr(self.day_view_manager.day_view_ui, 'searchBarTop'):
            self.day_view_manager.day_view_ui.searchBarTop.clear()

    def update_view_combo_selection(self, view_type):
        """Update view combo box selection programmatically"""
        try:
            if hasattr(self.day_view_manager.day_view_ui, 'comboView'):
                # Temporarily disconnect to avoid triggering events
                try:
                    self.day_view_manager.day_view_ui.comboView.currentTextChanged.disconnect()
                except:
                    pass
                
                # Update selection
                index = self.day_view_manager.day_view_ui.comboView.findText(view_type)
                if index != -1:
                    self.day_view_manager.day_view_ui.comboView.setCurrentIndex(index)
                
                # Reconnect
                self.day_view_manager.day_view_ui.comboView.currentTextChanged.connect(self.on_view_change)
                
        except Exception as e:
            import traceback
            traceback.print_exc()