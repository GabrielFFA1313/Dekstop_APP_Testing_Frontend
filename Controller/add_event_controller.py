# ADD_EVENT_CONTROLLER.PY - Controller for add/edit event UI interactions
import sys
import os
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import QDate, QTime, Qt
from PyQt6 import QtWidgets, QtCore

# Add parent directory to path to access Backend
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)


class AddEventController:
    """Controller class to handle UI interactions and events for add/edit event functionality"""
    
    def __init__(self, add_event_manager):
        self.add_event_manager = add_event_manager
        self.main_app = add_event_manager.main_app
        
    def setup_add_event_connections(self):
        """Setup add event specific connections"""
        try:
            # Connect save/update button (check for both save and update buttons)
            save_btn = getattr(self.add_event_manager.add_event_ui, 'btnSave', None) or getattr(self.add_event_manager.add_event_ui, 'btnUpdate', None)
            if save_btn:
                try:
                    save_btn.clicked.disconnect()
                except:
                    pass
                save_btn.clicked.connect(self.on_save_event)
            
            # Connect cancel button
            if hasattr(self.add_event_manager.add_event_ui, 'btnCancel'):
                try:
                    self.add_event_manager.add_event_ui.btnCancel.clicked.disconnect()
                except:
                    pass
                self.add_event_manager.add_event_ui.btnCancel.clicked.connect(self.on_cancel_event)
            
            # Connect back button - modified to navigate back to previous view
            if hasattr(self.add_event_manager.add_event_ui, 'btnBack'):
                try:
                    self.add_event_manager.add_event_ui.btnBack.clicked.disconnect()
                except:
                    pass
                self.add_event_manager.add_event_ui.btnBack.clicked.connect(self.on_go_back_to_previous_view)
            
            # Connect manage events button
            if hasattr(self.add_event_manager.add_event_ui, 'btnManageEvents'):
                try:
                    self.add_event_manager.add_event_ui.btnManageEvents.clicked.disconnect()
                except:
                    pass
                self.add_event_manager.add_event_ui.btnManageEvents.clicked.connect(self.on_manage_events)
            
            # Connect view all button
            if hasattr(self.add_event_manager.add_event_ui, 'btnViewAll'):
                try:
                    self.add_event_manager.add_event_ui.btnViewAll.clicked.disconnect()
                except:
                    pass
                self.add_event_manager.add_event_ui.btnViewAll.clicked.connect(self.on_view_all_events)
            
            # Connect checkboxes for target audience
            if hasattr(self.add_event_manager.add_event_ui, 'checkAll'):
                try:
                    self.add_event_manager.add_event_ui.checkAll.stateChanged.disconnect()
                except:
                    pass
                self.add_event_manager.add_event_ui.checkAll.stateChanged.connect(self.on_toggle_all_users)
            
            # Connect upcoming events filter (if it exists from BaseUi)
            if hasattr(self.add_event_manager.add_event_ui, 'comboUpcomingFilter'):
                try:
                    self.add_event_manager.add_event_ui.comboUpcomingFilter.currentTextChanged.disconnect()
                except:
                    pass
                self.add_event_manager.add_event_ui.comboUpcomingFilter.currentTextChanged.connect(self.on_filter_upcoming_events)
            
        except Exception as e:
            import traceback
            traceback.print_exc()

    # Event Handlers - just route to manager
    def on_save_event(self):
        """Handle save/update event button click"""
        self.add_event_manager.save_event()

    def on_cancel_event(self):
        """Handle cancel button click"""
        self.add_event_manager.cancel_event()

    def on_go_back_to_previous_view(self):
        """Handle back button click"""
        self.add_event_manager.go_back_to_previous_view()

    def on_manage_events(self):
        """Handle manage events button click"""
        self.add_event_manager.manage_events()

    def on_view_all_events(self):
        """Handle view all events button click"""
        self.add_event_manager.view_all_events()

    def on_toggle_all_users(self):
        """Handle 'All' checkbox toggle"""
        self.add_event_manager.toggle_all_users()

    def on_filter_upcoming_events(self, filter_text):
        """Handle upcoming events filter change"""
        self.add_event_manager.filter_upcoming_events(filter_text)