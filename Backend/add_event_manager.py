# ADD_EVENT_MANAGER.PY - Backend logic for add/edit event functionality with CRUD operations
from PyQt6.QtWidgets import QMessageBox, QDialog
from PyQt6.QtCore import QDate, QTime, Qt, QTimer
from PyQt6 import QtWidgets, QtGui, QtCore
from datetime import datetime, time

from UI.add_event import Ui_MainWindow as AddEventUi
from UI.edit_event import Ui_MainWindow as EditEventUi
from Controller.add_event_controller import AddEventController


class AddEventManager:
    """Manager class for handling both add and edit event business logic with CRUD operations"""
    
    def __init__(self, main_app, event_manager):
        self.main_app = main_app
        self.event_manager = event_manager
        self.add_event_ui = None
        self.mode = "add"
        self.edit_event_data = None
        self.add_event_controller = None  # Initialize after UI is created

    def setup_add_event_view(self):
        """Setup the add event view in the main window"""
        self.mode = "add"
        self.edit_event_data = None
        self._setup_event_view(AddEventUi)

    def setup_edit_event_view(self, event_data=None):
        """Setup the edit event view in the main window"""
        self.mode = "edit"
        self.edit_event_data = event_data
        self._setup_event_view(EditEventUi)
    
    # NOTE the geometry helps with the window size
    def _setup_event_view(self, ui_class):
        """Common setup for both add and edit event views"""
        try:
            # Store current geometry
            geometry = self.main_app.geometry() if hasattr(self.main_app, 'geometry') and self.main_app.geometry().isValid() else None
            
            # Clear any existing central widget
            self.main_app.setCentralWidget(None)
            
            # NOTE collection of garbage so that the changing of ui avoids lagging the application 
            # Force garbage collection
            import gc
            gc.collect()
            
            # Create and setup Event UI
            self.add_event_ui = ui_class()
            self.add_event_ui.setupUi(self.main_app, user_role=self.main_app.user_role)
            
            # Initialize controller after UI is created
            from Controller.add_event_controller import AddEventController
            self.add_event_controller = AddEventController(self)
            
            # Set event manager reference in the UI
            if hasattr(self.add_event_ui, 'set_event_manager'):
                self.add_event_ui.set_event_manager(self.event_manager)
            else:
                self.add_event_ui.event_manager = self.event_manager
            
            # Setup connections through controller
            self.add_event_controller.setup_add_event_connections()
            
            # Populate form with existing data if in edit mode
            if self.mode == "edit" and self.edit_event_data:
                self.populate_form_with_data(self.edit_event_data)
            
            # Restore geometry if we had one
            if geometry:
                self.main_app.setGeometry(geometry)
            
            # Load upcoming events data with delay to ensure UI is ready
            QTimer.singleShot(100, self.populate_upcoming_events)
            
            self.main_app.current_view = f"{self.mode}_event"
            title = "Campus Event Manager - Add Event" if self.mode == "add" else "Campus Event Manager - Edit Event"
            self.main_app.setWindowTitle(title)
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self.main_app, "Error", f"Could not setup {self.mode} event view: {str(e)}")

    def populate_form_with_data(self, event_data):
        """Populate form fields with existing event data for editing"""
        try:
            if not event_data or not self.add_event_ui:
                return
            
            # Basic fields
            if 'title' in event_data:
                self.add_event_ui.inputEventTitle.setText(event_data['title'])
            
            if 'description' in event_data:
                self.add_event_ui.inputDescription.setPlainText(event_data['description'])
            
            if 'location' in event_data:
                self.add_event_ui.inputLocation.setText(event_data['location'])
            
            # Event type
            if 'type' in event_data or 'category' in event_data:
                event_type = event_data.get('type', event_data.get('category', ''))
                index = self.add_event_ui.comboEventType.findText(event_type)
                if index >= 0:
                    self.add_event_ui.comboEventType.setCurrentIndex(index)
            
            # Dates
            if 'date' in event_data:
                # If single date field
                if isinstance(event_data['date'], QDate):
                    self.add_event_ui.dateStart.setDate(event_data['date'])
                    self.add_event_ui.dateEnd.setDate(event_data['date'])
            else:
                # Separate start/end dates
                if 'start_date' in event_data and isinstance(event_data['start_date'], QDate):
                    self.add_event_ui.dateStart.setDate(event_data['start_date'])
                
                if 'end_date' in event_data and isinstance(event_data['end_date'], QDate):
                    self.add_event_ui.dateEnd.setDate(event_data['end_date'])
            
            # Times
            if 'time' in event_data:
                # Parse time string if needed
                time_str = event_data['time']
                if isinstance(time_str, str):
                    try:
                        # Handle formats like "9:00 AM", "2:00 PM"
                        if 'AM' in time_str or 'PM' in time_str:
                            time_part = time_str.replace('AM', '').replace('PM', '').strip()
                            hour, minute = map(int, time_part.split(':'))
                            
                            if 'PM' in time_str and hour != 12:
                                hour += 12
                            elif 'AM' in time_str and hour == 12:
                                hour = 0
                            
                            q_time = QTime(hour, minute)
                            self.add_event_ui.timeStart.setTime(q_time)
                            
                            # Set AM/PM buttons
                            if 'AM' in time_str:
                                self.add_event_ui.btnStartAM.setChecked(True)
                                self.add_event_ui.btnStartPM.setChecked(False)
                            else:
                                self.add_event_ui.btnStartAM.setChecked(False)
                                self.add_event_ui.btnStartPM.setChecked(True)
                    except:
                        pass  # Use default time if parsing fails
            
            # Target audience (if available)
            if 'target_audience' in event_data:
                audience = event_data['target_audience']
                if isinstance(audience, list):
                    self.add_event_ui.checkStudents.setChecked('Students' in audience)
                    self.add_event_ui.checkFaculty.setChecked('Faculty' in audience)
                    self.add_event_ui.checkOrgOfficer.setChecked('Organization Officer' in audience)
                    self.add_event_ui.checkAll.setChecked('All' in audience)
            
        except Exception as e:
            import traceback
            traceback.print_exc()

    def populate_upcoming_events(self):
        """Populate upcoming events from Event Manager in add event view"""
        try:
            if not hasattr(self.add_event_ui, 'listUpcoming'):
                return
            
            if not self.event_manager:
                return
            
            # Get upcoming events from event manager
            upcoming_events = self.event_manager.get_upcoming_events("All", limit=10)
            
            # Clear the existing list
            self.add_event_ui.listUpcoming.clear()
            
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
                self.add_event_ui.listUpcoming.addItem(item)
                
        except Exception as e:
            import traceback
            traceback.print_exc()

    def filter_upcoming_events(self, filter_text):
        """Filter upcoming events based on selected category in add event view"""
        try:
            if not hasattr(self.add_event_ui, 'listUpcoming'):
                return
            
            if not self.event_manager:
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
            self.add_event_ui.listUpcoming.clear()
            
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
                self.add_event_ui.listUpcoming.addItem(item)
            
        except Exception as e:
            import traceback
            traceback.print_exc()

    # =========================
    # CRUD CREATE/UPDATE OPERATIONS
    # =========================
    
    def save_event(self):
        """Handle save or update event action based on current mode"""
        try:
            # Get form data
            event_data = self.get_form_data()
            
            # Validate form data
            validation_result = self.validate_form_data(event_data)
            if not validation_result['valid']:
                QMessageBox.warning(
                    self.main_app, 
                    "Validation Error", 
                    validation_result['message']
                )
                return
            
            # Save or update based on mode
            if self.mode == "add":
                success = self.create_event(event_data)
                action = "created"
            else:  # edit mode
                success = self.update_event(event_data)
                action = "updated"
            
            if success:
                QMessageBox.information(
                    self.main_app,
                    "Success",
                    f"Event '{event_data['title']}' has been {action} successfully!"
                )
                # Clear form only if adding and navigate back
                if self.mode == "add":
                    self.clear_form()
                self.go_back_to_previous_view()
            else:
                QMessageBox.critical(
                    self.main_app,
                    "Error",
                    f"Failed to {action[:-1]} event. Please try again."
                )
                    
        except Exception as e:
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self.main_app, "Error", f"Could not {self.mode} event: {str(e)}")

    def create_event(self, event_data):
        """CREATE - Add a new event"""
        try:
            # Validate required fields
            if not event_data.get('title', '').strip():
                raise ValueError("Event title is required")
            
            if not event_data.get('start_date'):
                raise ValueError("Event date is required")
            
            # Extract data
            title = event_data['title'].strip()
            date = event_data['start_date']
            category = self.determine_category_from_event_type(event_data.get('type', 'Academic'))
            
            # Validate date
            if not isinstance(date, QDate):
                raise ValueError("Date must be a QDate object")
            
            # Add to event manager memory
            self.event_manager.add_event_to_memory(date, title, category)
            
            # Save to JSON
            if self.event_manager.save_to_json():
                # Refresh display
                self.refresh_displays()
                
                print(f"Event created: {title} on {self.event_manager.date_to_string(date)}")
                return True
            else:
                # Rollback on save failure
                self.event_manager.remove_event_from_memory(date, title)
                raise Exception("Failed to save event to JSON file")
                
        except Exception as e:
            print(f"Error creating event: {e}")
            return False
    
    def update_event(self, updated_data):
        """UPDATE - Update an existing event"""
        try:
            if not self.edit_event_data:
                raise ValueError("No original event data for update")
            
            # Get original data
            original_title = self.edit_event_data.get('title', '').strip()
            original_date = self.edit_event_data.get('date')
            
            if not original_title or not original_date:
                raise ValueError("Original event data is incomplete")
            
            # Get updated values
            new_title = updated_data.get('title', original_title).strip()
            new_category = self.determine_category_from_event_type(updated_data.get('type', 'Academic'))
            new_date = updated_data.get('start_date', original_date)
            
            if not new_title:
                raise ValueError("Updated title cannot be empty")
            
            # Store backup for rollback
            backup_events = {}
            if original_date in self.event_manager._event_map:
                backup_events[original_date] = self.event_manager._event_map[original_date][:]
            if new_date != original_date and new_date in self.event_manager._event_map:
                backup_events[new_date] = self.event_manager._event_map[new_date][:]
            
            try:
                # Remove original event
                self.event_manager.remove_event_from_memory(original_date, original_title)
                
                # Add updated event
                self.event_manager.add_event_to_memory(new_date, new_title, new_category)
                
                # Save to JSON
                if self.event_manager.save_to_json():
                    # Refresh display
                    self.refresh_displays()
                    
                    print(f"Event updated: {original_title} -> {new_title}")
                    return True
                else:
                    raise Exception("Failed to save changes to JSON file")
                    
            except Exception as save_error:
                # Rollback changes
                for date, events in backup_events.items():
                    self.event_manager._event_map[date] = events
                raise save_error
                
        except Exception as e:
            print(f"Error updating event: {e}")
            return False

    def determine_category_from_event_type(self, event_type):
        """Convert UI event type to EventManager category"""
        category_map = {
            "Academic": "Academic",
            "Organizational": "Organizational",
            "Deadline": "Deadline", 
            "Holiday": "Holiday"
        }
        return category_map.get(event_type, "Academic")

    def refresh_displays(self):
        """Refresh all displays after event changes"""
        try:
            # Refresh event manager displays
            self.event_manager.refresh_events_display()
            
            # Refresh upcoming events in current view
            self.populate_upcoming_events()
            
            # Refresh activities manager if available
            if hasattr(self.main_app, 'activities_manager'):
                self.main_app.activities_manager.refresh_activities()
                
        except Exception as e:
            print(f"Error refreshing displays: {e}")

    def get_form_data(self):
        """Extract data from the form"""
        try:
            # Get basic event data
            title = self.add_event_ui.inputEventTitle.text().strip()
            description = self.add_event_ui.inputDescription.toPlainText().strip()
            event_type = self.add_event_ui.comboEventType.currentText()
            location = self.add_event_ui.inputLocation.text().strip()
            
            # Get dates
            start_date = self.add_event_ui.dateStart.date()
            end_date = self.add_event_ui.dateEnd.date()
            
            # Get times and convert based on AM/PM
            start_time = self.add_event_ui.timeStart.time()
            end_time = self.add_event_ui.timeEnd.time()
            
            # Adjust for AM/PM
            if self.add_event_ui.btnStartPM.isChecked() and start_time.hour() < 12:
                start_time = start_time.addSecs(12 * 3600)  # Add 12 hours for PM
            elif self.add_event_ui.btnStartAM.isChecked() and start_time.hour() == 12:
                start_time = start_time.addSecs(-12 * 3600)  # Subtract 12 hours for 12 AM
            
            if self.add_event_ui.btnEndPM.isChecked() and end_time.hour() < 12:
                end_time = end_time.addSecs(12 * 3600)  # Add 12 hours for PM
            elif self.add_event_ui.btnEndAM.isChecked() and end_time.hour() == 12:
                end_time = end_time.addSecs(-12 * 3600)  # Subtract 12 hours for 12 AM
            
            # Get target audience
            target_audience = []
            if self.add_event_ui.checkStudents.isChecked():
                target_audience.append("Students")
            if self.add_event_ui.checkFaculty.isChecked():
                target_audience.append("Faculty")
            if self.add_event_ui.checkOrgOfficer.isChecked():
                target_audience.append("Organization Officer")
            if self.add_event_ui.checkAll.isChecked():
                target_audience = ["All"]
            
            return {
                'title': title,
                'description': description,
                'type': event_type,
                'location': location,
                'start_date': start_date,
                'end_date': end_date,
                'start_time': start_time,
                'end_time': end_time,
                'target_audience': target_audience
            }
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            return None

    def validate_form_data(self, event_data):
        """Validate the form data"""
        if not event_data:
            return {'valid': False, 'message': 'Could not read form data.'}
        
        # Check required fields
        if not event_data['title']:
            return {'valid': False, 'message': 'Please enter an event title.'}
        
        if event_data['type'] == "Select Event Type":
            return {'valid': False, 'message': 'Please select an event type.'}
        
        # Check date logic
        if event_data['end_date'] < event_data['start_date']:
            return {'valid': False, 'message': 'End date cannot be before start date.'}
        
        # Check target audience
        if not event_data['target_audience']:
            return {'valid': False, 'message': 'Please select at least one target audience.'}
        
        return {'valid': True, 'message': 'Validation passed.'}

    def clear_form(self):
        """Clear all form fields"""
        try:
            if not self.add_event_ui:
                return
                
            self.add_event_ui.inputEventTitle.clear()
            self.add_event_ui.inputDescription.clear()
            self.add_event_ui.inputLocation.clear()
            self.add_event_ui.comboEventType.setCurrentIndex(0)
            self.add_event_ui.dateStart.setDate(QDate.currentDate())
            self.add_event_ui.dateEnd.setDate(QDate.currentDate())
            self.add_event_ui.timeStart.setTime(QTime(9, 0))
            self.add_event_ui.timeEnd.setTime(QTime(17, 0))
            
            # Reset AM/PM buttons
            self.add_event_ui.btnStartAM.setChecked(True)
            self.add_event_ui.btnStartPM.setChecked(False)
            self.add_event_ui.btnEndAM.setChecked(False)
            self.add_event_ui.btnEndPM.setChecked(True)
            
            # Reset checkboxes
            self.add_event_ui.checkStudents.setChecked(False)
            self.add_event_ui.checkFaculty.setChecked(False)
            self.add_event_ui.checkOrgOfficer.setChecked(False)
            self.add_event_ui.checkAll.setChecked(False)
            
        except Exception as e:
            import traceback
            traceback.print_exc()

    def cancel_event(self):
        """Handle cancel action"""
        try:
            # Ask for confirmation if form has data
            if self.form_has_data():
                action = "adding" if self.mode == "add" else "editing"
                reply = QMessageBox.question(
                    self.main_app,
                    "Confirm Cancel",
                    f"You have unsaved changes. Are you sure you want to cancel {action} this event?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                    QMessageBox.StandardButton.No
                )
                
                if reply == QMessageBox.StandardButton.No:
                    return
            
            # Clear form only if in add mode and navigate back
            if self.mode == "add":
                self.clear_form()
            self.go_back_to_previous_view()
                
        except Exception as e:
            import traceback
            traceback.print_exc()

    def form_has_data(self):
        """Check if form has any data entered"""
        try:
            if not self.add_event_ui:
                return False
                
            return (
                bool(self.add_event_ui.inputEventTitle.text().strip()) or
                bool(self.add_event_ui.inputDescription.toPlainText().strip()) or
                bool(self.add_event_ui.inputLocation.text().strip()) or
                self.add_event_ui.comboEventType.currentIndex() != 0 or
                self.add_event_ui.checkStudents.isChecked() or
                self.add_event_ui.checkFaculty.isChecked() or
                self.add_event_ui.checkOrgOfficer.isChecked() or
                self.add_event_ui.checkAll.isChecked()
            )
        except Exception as e:
            return False

    def toggle_all_users(self):
        """Handle the 'All' checkbox to toggle all user types"""
        try:
            if hasattr(self.add_event_ui, 'checkAll'):
                is_checked = self.add_event_ui.checkAll.isChecked()
                if hasattr(self.add_event_ui, 'checkStudents'):
                    self.add_event_ui.checkStudents.setChecked(is_checked)
                if hasattr(self.add_event_ui, 'checkFaculty'):
                    self.add_event_ui.checkFaculty.setChecked(is_checked)
                if hasattr(self.add_event_ui, 'checkOrgOfficer'):
                    self.add_event_ui.checkOrgOfficer.setChecked(is_checked)
        except Exception as e:
            import traceback
            traceback.print_exc()

    def manage_events(self):
        """Handle manage events button - navigate to activities view"""
        try:
            # Navigate to activities using main app method (try new MVC method first)
            if hasattr(self.main_app, 'handle_show_activities_view'):
                self.main_app.handle_show_activities_view()
            elif hasattr(self.main_app, 'show_activities_view'):
                self.main_app.show_activities_view()
            
        except Exception as e:
            import traceback
            traceback.print_exc()

    def view_all_events(self):
        """Handle view all events button - navigate to calendar"""
        try:
            # Navigate to calendar using main app method
            self.go_back_to_calendar()
            
        except Exception as e:
            import traceback
            traceback.print_exc()

    def go_back_to_previous_view(self):
        """Navigate back to the previous view (could be calendar or activities)"""
        try:
            # Check if we came from activities (edit mode typically comes from activities)
            if self.mode == "edit" and hasattr(self.main_app, 'handle_show_activities_view'):
                self.main_app.handle_show_activities_view()
            elif self.mode == "edit" and hasattr(self.main_app, 'show_activities_view'):
                self.main_app.show_activities_view()
            else:
                # Default to calendar view
                self.go_back_to_calendar()
        except Exception as e:
            import traceback
            traceback.print_exc()

    def go_back_to_calendar(self):
        """Navigate back to calendar view"""
        try:
            # Use main app method to show calendar (try new MVC method first)
            if hasattr(self.main_app, 'handle_show_calendar_view'):
                self.main_app.handle_show_calendar_view()
            elif hasattr(self.main_app, 'show_calendar_view'):
                self.main_app.show_calendar_view()
            elif hasattr(self.main_app, 'setup_calendar_view'):
                self.main_app.setup_calendar_view()
        except Exception as e:
            import traceback
            traceback.print_exc()

    def refresh_upcoming_events(self):
        """Refresh upcoming events display - called when events are updated"""
        try:
            self.populate_upcoming_events()
        except Exception as e:
            import traceback
            traceback.print_exc()