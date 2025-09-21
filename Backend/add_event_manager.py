# ADD_EVENT_MANAGER.PY - Backend logic for add/edit event functionality with CRUD operations - Router Compatible
from PyQt6.QtWidgets import QMessageBox, QDialog
from PyQt6.QtCore import QDate, QTime, Qt, QTimer
from PyQt6 import QtWidgets, QtGui, QtCore
from datetime import datetime, time

from UI.add_event import Ui_MainWindow as AddEventUi
from UI.edit_event import Ui_MainWindow as EditEventUi
from Controller.add_event_controller import AddEventController


class AddEventManager:
    """Manager class for handling both add and edit event business logic with CRUD operations - Router Compatible"""
    
    def __init__(self, main_app, event_manager):
        self.main_app = main_app
        self.event_manager = event_manager
        self.add_event_ui = None
        self.mode = "add"
        self.edit_event_data = None
        self.add_event_controller = None  # Initialize after UI is created

    # 12-HOUR TIME CONVERSION METHODS
    def format_time_to_12h(self, qtime):
        """Convert QTime to 12-hour format string"""
        hour = qtime.hour()
        minute = qtime.minute()
        
        if hour == 0:
            return f"12:{minute:02d} AM"
        elif hour < 12:
            return f"{hour}:{minute:02d} AM"
        elif hour == 12:
            return f"12:{minute:02d} PM"
        else:
            return f"{hour - 12}:{minute:02d} PM"

    def get_12h_time_from_form(self, time_edit, am_btn, pm_btn):
        """Get 24-hour QTime from 12-hour form inputs"""
        time_12h = time_edit.time()
        hour = time_12h.hour()
        minute = time_12h.minute()
        
        # Convert based on AM/PM selection
        if pm_btn.isChecked():
            if hour < 12:
                hour += 12
            elif hour == 12:
                hour = 12  # 12 PM stays 12
        else:  # AM is checked
            if hour == 12:
                hour = 0  # 12 AM becomes 0
        
        return QTime(hour, minute)

    def set_12h_time_in_form(self, qtime_24h, time_edit, am_btn, pm_btn):
        """Set 12-hour time in form from 24-hour QTime"""
        hour_24 = qtime_24h.hour()
        minute = qtime_24h.minute()
        
        if hour_24 == 0:
            # 12 AM
            display_hour = 12
            am_btn.setChecked(True)
            pm_btn.setChecked(False)
        elif hour_24 < 12:
            # 1-11 AM
            display_hour = hour_24
            am_btn.setChecked(True)
            pm_btn.setChecked(False)
        elif hour_24 == 12:
            # 12 PM
            display_hour = 12
            am_btn.setChecked(False)
            pm_btn.setChecked(True)
        else:
            # 1-11 PM
            display_hour = hour_24 - 12
            am_btn.setChecked(False)
            pm_btn.setChecked(True)
        
        display_time = QTime(display_hour, minute)
        time_edit.setTime(display_time)

    # UI SETUP METHODS (Called by main app's create methods)
    def setup_add_event_ui(self):
        """Setup the add event UI components - Called by main app"""
        self.mode = "add"
        self.edit_event_data = None
        self._setup_event_ui(AddEventUi)

    def setup_edit_event_ui(self, event_data=None):
        """Setup the edit event UI components - Called by main app"""
        self.mode = "edit"
        self.edit_event_data = event_data
        self._setup_event_ui(EditEventUi)
    
    def _setup_event_ui(self, ui_class):
        """Common setup for both add and edit event UIs"""
        try:
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
            
            # Load upcoming events data with delay to ensure UI is ready
            QTimer.singleShot(100, self.populate_upcoming_events)
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self.main_app, "Error", f"Could not setup {self.mode} event UI: {str(e)}")

    def restore_event_form_state(self, saved_state):
        """Restore event form state from router data"""
        try:
            if not saved_state or not self.add_event_ui:
                return
            
            # Restore mode if available
            if 'mode' in saved_state:
                self.mode = saved_state['mode']
            
            # Note: We typically don't restore form data for security/privacy reasons
            # But we could restore other UI state here if needed
                
        except Exception as e:
            import traceback
            traceback.print_exc()

    def populate_form_with_data(self, event_data):
        """Populate form fields with existing event data for editing - IMPROVED 12-HOUR HANDLING"""
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
                if isinstance(event_data['date'], QDate):
                    self.add_event_ui.dateStart.setDate(event_data['date'])
                    self.add_event_ui.dateEnd.setDate(event_data['date'])
            else:
                if 'start_date' in event_data and isinstance(event_data['start_date'], QDate):
                    self.add_event_ui.dateStart.setDate(event_data['start_date'])
                
                if 'end_date' in event_data and isinstance(event_data['end_date'], QDate):
                    self.add_event_ui.dateEnd.setDate(event_data['end_date'])
            
            # Times - IMPROVED 12-hour handling
            if 'start_time' in event_data:
                start_time = event_data['start_time']
                if isinstance(start_time, QTime):
                    self.set_12h_time_in_form(
                        start_time,
                        self.add_event_ui.timeStart,
                        self.add_event_ui.btnStartAM,
                        self.add_event_ui.btnStartPM
                    )
                elif isinstance(start_time, str):
                    # Parse time string if needed
                    try:
                        if 'AM' in start_time or 'PM' in start_time:
                            time_part = start_time.replace('AM', '').replace('PM', '').strip()
                            hour, minute = map(int, time_part.split(':'))
                            
                            if 'PM' in start_time and hour != 12:
                                hour += 12
                            elif 'AM' in start_time and hour == 12:
                                hour = 0
                            
                            q_time = QTime(hour, minute)
                            self.set_12h_time_in_form(
                                q_time,
                                self.add_event_ui.timeStart,
                                self.add_event_ui.btnStartAM,
                                self.add_event_ui.btnStartPM
                            )
                    except:
                        pass  # Use default time if parsing fails
            
            if 'end_time' in event_data:
                end_time = event_data['end_time']
                if isinstance(end_time, QTime):
                    self.set_12h_time_in_form(
                        end_time,
                        self.add_event_ui.timeEnd,
                        self.add_event_ui.btnEndAM,
                        self.add_event_ui.btnEndPM
                    )
            
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
            start_time = event_data.get('start_time')
            end_time = event_data.get('end_time')
            
            # Validate date
            if not isinstance(date, QDate):
                raise ValueError("Date must be a QDate object")
            
            # Add to event manager memory with time information
            self.event_manager.add_event_to_memory(date, title, category, start_time, end_time)
            
            # Save to JSON
            if self.event_manager.save_to_json():
                # Refresh display
                self.refresh_displays()
                
                time_str = self.format_time_to_12h(start_time) if start_time else "N/A"
                print(f"Event created: {title} on {self.event_manager.date_to_string(date)} at {time_str}")
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
            new_start_time = updated_data.get('start_time')
            new_end_time = updated_data.get('end_time')
            
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
                
                # Add updated event with time information
                self.event_manager.add_event_to_memory(new_date, new_title, new_category, new_start_time, new_end_time)
                
                # Save to JSON
                if self.event_manager.save_to_json():
                    # Refresh display
                    self.refresh_displays()
                    
                    time_str = self.format_time_to_12h(new_start_time) if new_start_time else "N/A"
                    print(f"Event updated: {original_title} -> {new_title} at {time_str}")
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
        """Extract data from the form - IMPROVED 12-HOUR CONVERSION"""
        try:
            # Get basic event data
            title = self.add_event_ui.inputEventTitle.text().strip()
            description = self.add_event_ui.inputDescription.toPlainText().strip()
            event_type = self.add_event_ui.comboEventType.currentText()
            location = self.add_event_ui.inputLocation.text().strip()
            
            # Get dates
            start_date = self.add_event_ui.dateStart.date()
            end_date = self.add_event_ui.dateEnd.date()
            
            # Get times using the new 12-hour conversion method
            start_time = self.get_12h_time_from_form(
                self.add_event_ui.timeStart,
                self.add_event_ui.btnStartAM,
                self.add_event_ui.btnStartPM
            )
            
            end_time = self.get_12h_time_from_form(
                self.add_event_ui.timeEnd,
                self.add_event_ui.btnEndAM,
                self.add_event_ui.btnEndPM
            )
            
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
        """Validate the form data - 12-HOUR FORMAT MESSAGES"""
        if not event_data:
            return {'valid': False, 'message': 'Could not read form data.'}
        
        # Check required fields
        if not event_data['title']:
            return {'valid': False, 'message': 'Please enter an event title.'}
        
        if event_data['type'] == "Select Event Type":
            return {'valid': False, 'message': 'Please select an event type.'}
        
         # Check if start_date is before today
        if event_data['start_date'] < QDate.currentDate():
            return {'valid': False, 'message': 'Start date cannot be before today.'}
        
        # Check date logic
        if event_data['end_date'] < event_data['start_date']:
            return {'valid': False, 'message': 'End date cannot be before start date.'}
        
        # Check target audience
        if not event_data['target_audience']:
            return {'valid': False, 'message': 'Please select at least one target audience.'}
        
        # Check time constraints
        start_time = event_data.get('start_time')
        end_time = event_data.get('end_time')
        
        if start_time and end_time:
            # Define allowed time range (7:00 AM to 9:00 PM)
            min_time = QTime(7, 0)   # 7:00 AM
            max_time = QTime(21, 0)  # 9:00 PM
            
            # Check if start time is within allowed range
            if start_time < min_time or start_time > max_time:
                return {'valid': False, 'message': 'Start time must be between 7:00 AM and 9:00 PM.'}
            
            # Check if end time is within allowed range
            if end_time < min_time or end_time > max_time:
                return {'valid': False, 'message': 'End time must be between 7:00 AM and 9:00 PM.'}
            
            # Check if end time is after start time (for same day events)
            if event_data['start_date'] == event_data['end_date']:
                if end_time <= start_time:
                    return {'valid': False, 'message': 'End time must be later than start time.'}
        
        return {'valid': True, 'message': 'Validation passed.'}

    def clear_form(self):
        """Clear all form fields - UPDATED 12-HOUR DEFAULTS"""
        try:
            if not self.add_event_ui:
                return
                
            self.add_event_ui.inputEventTitle.clear()
            self.add_event_ui.inputDescription.clear()
            self.add_event_ui.inputLocation.clear()
            self.add_event_ui.comboEventType.setCurrentIndex(0)
            self.add_event_ui.dateStart.setDate(QDate.currentDate())
            self.add_event_ui.dateEnd.setDate(QDate.currentDate())
            
            # Set default times in 12-hour format
            self.add_event_ui.timeStart.setTime(QTime(9, 0))  # 9:00 (will show as 9 AM)
            self.add_event_ui.timeEnd.setTime(QTime(5, 0))    # 5:00 (will show as 5 PM)
            
            # Set correct AM/PM buttons for defaults
            self.add_event_ui.btnStartAM.setChecked(True)   # 9 AM
            self.add_event_ui.btnStartPM.setChecked(False)
            self.add_event_ui.btnEndAM.setChecked(False)    # 5 PM
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
            # Navigate to activities using router
            if hasattr(self.main_app, 'router'):
                self.main_app.router.to_activities()
            else:
                # Fallback to legacy methods
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
            # Navigate to calendar using router
            self.go_back_to_calendar()
            
        except Exception as e:
            import traceback
            traceback.print_exc()

    def go_back_to_previous_view(self):
        """Navigate back to the previous view (could be calendar or activities)"""
        try:
            # Check if we came from activities (edit mode typically comes from activities)
            if self.mode == "edit":
                if hasattr(self.main_app, 'router'):
                    self.main_app.router.to_activities()
                else:
                    # Fallback to legacy methods
                    if hasattr(self.main_app, 'handle_show_activities_view'):
                        self.main_app.handle_show_activities_view()
                    elif hasattr(self.main_app, 'show_activities_view'):
                        self.main_app.show_activities_view()
            else:
                # Default to calendar view
                self.go_back_to_calendar()
        except Exception as e:
            import traceback
            traceback.print_exc()

    def go_back_to_calendar(self):
        """Navigate back to calendar view using router"""
        try:
            if hasattr(self.main_app, 'router'):
                self.main_app.router.to_calendar()
            else:
                # Fallback to legacy methods
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