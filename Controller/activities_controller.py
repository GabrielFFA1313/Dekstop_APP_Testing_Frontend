# ACTIVITIES_CONTROLLER.PY - Controller for activities UI interactions
import sys
import os
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import QDate, Qt
from PyQt6 import QtWidgets, QtCore

# Add parent directory to path to access Backend
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)


class ActivitiesController:
    """Controller class to handle UI interactions and events for activities functionality"""
    
    def __init__(self, activities_manager):
        self.activities_manager = activities_manager
        self.main_app = activities_manager.main_app
        
    def setup_activities_connections(self):
        """Setup activities-specific connections"""
        try:
            # Connect back button
            if hasattr(self.activities_manager.activities_ui, 'btnback'):
                try:
                    self.activities_manager.activities_ui.btnback.clicked.disconnect()
                except:
                    pass
                self.activities_manager.activities_ui.btnback.clicked.connect(self.on_go_back_to_calendar)
            
            # Connect Add Event button - Navigate to AddEventManager
            if hasattr(self.activities_manager.activities_ui, 'btnAddEvent'):
                if self.activities_manager.can_add_activities():
                    try:
                        self.activities_manager.activities_ui.btnAddEvent.clicked.disconnect()
                    except:
                        pass
                    self.activities_manager.activities_ui.btnAddEvent.clicked.connect(self.on_show_add_event)
                else:
                    # Hide Add Event button for students only
                    self.activities_manager.activities_ui.btnAddEvent.setVisible(False)
            
            # Connect activities table filter
            if hasattr(self.activities_manager.activities_ui, 'comboActivityType'):
                try:
                    self.activities_manager.activities_ui.comboActivityType.currentTextChanged.disconnect()
                except:
                    pass
                self.activities_manager.activities_ui.comboActivityType.currentTextChanged.connect(self.on_filter_activities_table)
            
            # Connect upcoming events filter in activities view
            if hasattr(self.activities_manager.activities_ui, 'comboUpcomingFilter'):
                try:
                    self.activities_manager.activities_ui.comboUpcomingFilter.currentTextChanged.disconnect()
                except:
                    pass
                self.activities_manager.activities_ui.comboUpcomingFilter.currentTextChanged.connect(self.on_filter_activities_upcoming_events)
            
        except Exception as e:
            import traceback
            traceback.print_exc()

    # Navigation Event Handlers
    def on_go_back_to_calendar(self):
        """Handle back to calendar button click"""
        try:
            self.activities_manager.go_back_to_calendar()
        except Exception as e:
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self.main_app, "Error", f"Could not return to calendar: {str(e)}")

    def on_show_add_event(self):
        """Handle show add event button click"""
        try:
            self.activities_manager.show_add_event()
        except Exception as e:
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self.main_app, "Error", f"Could not show add event interface: {str(e)}")

    # Activity Management Event Handlers
    def on_edit_activity(self, row):
        """Handle edit activity button click"""
        try:
            self.activities_manager.edit_activity(row)
        except Exception as e:
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self.main_app, "Error", f"Could not open edit view: {str(e)}")

    def on_delete_activity(self, row):
        """Handle delete activity button click"""
        try:
            self.activities_manager.delete_activity(row)
        except Exception as e:
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self.main_app, "Delete Activity Failed", f"Failed to delete activity: {str(e)}")

    # Filter Event Handlers
    def on_filter_activities_table(self, filter_type):
        """Handle activities table filter change"""
        try:
            self.activities_manager.filter_activities_table(filter_type)
        except Exception as e:
            import traceback
            traceback.print_exc()

    def on_filter_activities_upcoming_events(self, filter_text):
        """Handle upcoming events filter change"""
        try:
            self.activities_manager.filter_activities_upcoming_events(filter_text)
        except Exception as e:
            import traceback
            traceback.print_exc()

    # Utility methods for creating action button callbacks
    def create_edit_callback(self, row):
        """Create edit callback for specific row"""
        return lambda: self.on_edit_activity(row)

    def create_delete_callback(self, row):
        """Create delete callback for specific row"""
        return lambda: self.on_delete_activity(row)