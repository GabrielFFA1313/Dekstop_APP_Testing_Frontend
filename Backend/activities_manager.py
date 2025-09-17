# ACTIVITIES_MANAGER.PY - Backend logic for activities view functionality (listing and deleting) - Router Compatible
from PyQt6.QtWidgets import QMessageBox, QWidget, QHBoxLayout, QPushButton
from PyQt6.QtCore import QDate, QTimer, Qt
from PyQt6 import QtWidgets, QtGui, QtCore

from UI.activities import Ui_MainWindow
from Controller.activities_controller import ActivitiesController


class ActivitiesManager:
    """Manager class for handling activities view business logic (listing and deleting) - Router Compatible"""
    
    def __init__(self, main_app, event_manager):
        self.main_app = main_app
        self.event_manager = event_manager
        self.activities_ui = None
        self.all_activities = []
        self.activities_controller = None  # Will be initialized when UI is created

    # UI SETUP METHOD (Called by main app's create_activities_view)
    def setup_activities_ui(self):
        """Setup the activities UI components - Called by main app"""
        try:
            # Create activities UI and setup
            self.activities_ui = Ui_MainWindow()
            self.activities_ui.setupUi(self.main_app, user_role=self.main_app.user_role)
            
            # Initialize controller after UI is created
            self.activities_controller = ActivitiesController(self)
            
            # Update table headers after UI setup
            self.update_table_headers()
            
            # Set event manager reference
            if hasattr(self.activities_ui, 'set_event_manager'):
                self.activities_ui.set_event_manager(self.event_manager)
            else:
                self.activities_ui.event_manager = self.event_manager
            
            # Setup connections through controller
            self.activities_controller.setup_activities_connections()
            
            # Load data with delay to ensure UI is ready
            QTimer.singleShot(100, self.load_activities_data_delayed)
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self.main_app, "Error", f"Could not setup activities UI: {str(e)}")

    def restore_activities_state(self, saved_state):
        """Restore activities view state from router data"""
        try:
            if not saved_state or not self.activities_ui:
                return
            
            # Restore activity filter
            if 'activity_filter' in saved_state and hasattr(self.activities_ui, 'comboActivityType'):
                filter_text = saved_state['activity_filter']
                index = self.activities_ui.comboActivityType.findText(filter_text)
                if index >= 0:
                    self.activities_ui.comboActivityType.setCurrentIndex(index)
            
            # Restore upcoming filter
            if 'upcoming_filter' in saved_state and hasattr(self.activities_ui, 'comboUpcomingFilter'):
                filter_text = saved_state['upcoming_filter']
                index = self.activities_ui.comboUpcomingFilter.findText(filter_text)
                if index >= 0:
                    self.activities_ui.comboUpcomingFilter.setCurrentIndex(index)
                    
        except Exception as e:
            import traceback
            traceback.print_exc()

    def update_table_headers(self):
        """Update table headers based on user role"""
        if hasattr(self.activities_ui, 'activitiesTable'):
            # Check if action buttons should be shown (using UI method)
            if hasattr(self.activities_ui, 'can_show_action_buttons') and self.activities_ui.can_show_action_buttons():
                # Show Actions column for admin users
                self.activities_ui.activitiesTable.setColumnCount(5)
                headers = ["Date & Time", "Event", "Type", "Location", "Actions"]
                self.activities_ui.activitiesTable.setHorizontalHeaderLabels(headers)
                
                # Set column widths
                header = self.activities_ui.activitiesTable.horizontalHeader()
                header.setSectionResizeMode(0, header.ResizeMode.Fixed)             # Date & Time - Fixed
                header.setSectionResizeMode(1, header.ResizeMode.Fixed)             # Event - Fixed
                header.setSectionResizeMode(2, header.ResizeMode.Fixed)             # Type - Fixed
                header.setSectionResizeMode(3, header.ResizeMode.Fixed)             # Location - Fixed
                header.setSectionResizeMode(4, header.ResizeMode.Fixed)             # Actions - Fixed
                
                # Set specific widths for all columns
                self.activities_ui.activitiesTable.setColumnWidth(0, 120)  # Date & Time
                self.activities_ui.activitiesTable.setColumnWidth(1, 210)  # Event column 
                self.activities_ui.activitiesTable.setColumnWidth(2, 130)  # Type
                self.activities_ui.activitiesTable.setColumnWidth(3, 140)  # Location
                self.activities_ui.activitiesTable.setColumnWidth(4, 150)  # Actions
            else:
                # Hide Actions column for student, org, faculty users
                self.activities_ui.activitiesTable.setColumnCount(4)
                headers = ["Date & Time", "Event", "Type", "Location"]
                self.activities_ui.activitiesTable.setHorizontalHeaderLabels(headers)
                
                # Set column widths for 4-column layout
                header = self.activities_ui.activitiesTable.horizontalHeader()
                header.setSectionResizeMode(0, header.ResizeMode.Fixed)             # Date & Time - Fixed
                header.setSectionResizeMode(1, header.ResizeMode.Stretch)           # Event - Stretch to fill
                header.setSectionResizeMode(2, header.ResizeMode.Fixed)             # Type - Fixed
                header.setSectionResizeMode(3, header.ResizeMode.Fixed)             # Location - Fixed
                
                # Set specific widths
                self.activities_ui.activitiesTable.setColumnWidth(0, 120)  # Date & Time
                self.activities_ui.activitiesTable.setColumnWidth(2, 120)  # Type
                self.activities_ui.activitiesTable.setColumnWidth(3, 160)  # Location

    def load_activities_data_delayed(self):
        """Load activities data with a small delay to ensure UI is ready"""
        self.load_activities_data()
        self.populate_activities_upcoming_events()

    def load_activities_data(self):
        """Load activities data from event manager into the table"""
        try:
            if not hasattr(self.activities_ui, 'activitiesTable'):
                return
            
            if not self.event_manager:
                return
            
            # Get all events from event manager
            all_events_dict = self.event_manager.get_events()
            
            all_activities = []
            
            # Convert events to activities format
            for date, events in all_events_dict.items():
                # Get events with time information for this date
                events_with_times = self.event_manager.get_events_for_date_with_times(date)
                
                for event_data in events_with_times:
                    title = event_data['title']
                    category = event_data['category']
                    start_time = event_data['start_time']
                    
                    # Format time as string
                    time_str = start_time.toString("h:mm AP")  # e.g., "2:30 PM"
                    
                    # Create activity entry
                    activity = {
                        'date': date,
                        'title': title,
                        'category': category,
                        'location': self.get_default_location(category),
                        'time': time_str
                    }
                    all_activities.append(activity)
            
            # Sort activities to show upcoming events first in proper chronological order
            current_date = QDate.currentDate()
            
            # Separate upcoming and past events
            upcoming_activities = [activity for activity in all_activities if activity['date'] >= current_date]
            past_activities = [activity for activity in all_activities if activity['date'] < current_date]
            
            # Sort upcoming events chronologically (EARLIEST first: Sept 16, then Sept 18, then Sept 22, then Sept 30)
            upcoming_activities.sort(key=lambda x: x['date'])
            
            # Sort past events reverse chronologically (most recent past first)  
            past_activities.sort(key=lambda x: x['date'], reverse=True)
            
            # Combine: upcoming first, then past
            all_activities = upcoming_activities + past_activities
            
            # Store all activities for filtering
            self.all_activities = all_activities
            
            # Populate the table with all activities
            self.populate_activities_table(all_activities)
            
        except Exception as e:
            import traceback
            traceback.print_exc()

    def get_default_location(self, category):
        """Get default location based on event category"""
        location_map = {
            "Academic": "Main Building",
            "Organizational": "Conference Room",
            "Deadline": "Online/Various",
            "Holiday": "Campus-wide"
        }
        return location_map.get(category, "TBA")

    def get_default_time(self, category):
        """Get default time based on event category"""
        time_map = {
            "Academic": "9:00 AM",
            "Organizational": "2:00 PM", 
            "Deadline": "11:59 PM",
            "Holiday": "All Day"
        }
        return time_map.get(category, "TBA")

    def can_edit_activities(self):
        """Check if current user can edit/delete activities"""
        user_role = getattr(self.main_app, 'user_role', '').lower()
        return user_role in ['admin', 'administrator', 'super_admin']
    
    def can_add_activities(self):
        """Check if current user can add new activities"""
        user_role = getattr(self.main_app, 'user_role', '').lower()
        return user_role in ['admin', 'administrator', 'super_admin', 'org','organization', 'faculty']

    def populate_activities_table(self, activities_list):
        """Populate the activities table with event data"""
        try:
            if not hasattr(self.activities_ui, 'activitiesTable'):
                return
            
            table = self.activities_ui.activitiesTable
            
            # Disable sorting temporarily to avoid issues during population
            try:
                table.setSortingEnabled(False)
            except RuntimeError:
                print("Table widget has been deleted, skipping population")
                return
            
            # Set the number of rows
            table.setRowCount(len(activities_list))
            
            # Check if user can edit activities (using UI method)
            show_actions = (hasattr(self.activities_ui, 'can_show_action_buttons') and 
                          self.activities_ui.can_show_action_buttons())
            
            for row, activity in enumerate(activities_list):
                # Date & Time
                date_time = f"{activity['date'].toString('MMM dd, yyyy')}\n{activity['time']}"
                date_item = QtWidgets.QTableWidgetItem(date_time)
                date_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                table.setItem(row, 0, date_item)
                
                # Event
                event_item = QtWidgets.QTableWidgetItem(activity['title'])
                event_item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
                table.setItem(row, 1, event_item)
                
                # Type
                type_item = QtWidgets.QTableWidgetItem(activity['category'])
                type_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                type_item.setBackground(self.get_category_color(activity['category']))
                table.setItem(row, 2, type_item)
                
                # Location
                location_item = QtWidgets.QTableWidgetItem(activity['location'])
                location_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                table.setItem(row, 3, location_item)
                
                # Actions - Create Edit/Delete buttons only for authorized users
                if show_actions and hasattr(self.activities_ui, 'create_action_buttons'):
                    # Create direct callbacks to avoid controller dependency issues
                    edit_callback = lambda r=row: self.edit_activity(r)
                    delete_callback = lambda r=row: self.delete_activity(r)
                    
                    action_buttons = self.activities_ui.create_action_buttons(
                        row, 
                        edit_callback=edit_callback, 
                        delete_callback=delete_callback
                    )
                    if action_buttons:  # Only set if buttons were created
                        table.setCellWidget(row, 4, action_buttons)
            
            # Re-enable sorting but keep our custom order
            table.setSortingEnabled(False)  # Disable to preserve our custom sorting order
            
        except Exception as e:
            import traceback
            traceback.print_exc()

    # =========================
    # DELETE OPERATION (Business Logic)
    # =========================
    
    def delete_activity(self, row):
        """DELETE - Delete an activity (Business logic)"""
        try:
            # Check permission first
            if not self.can_edit_activities():
                QMessageBox.warning(
                    self.main_app,
                    "Access Denied",
                    "You do not have permission to delete activities."
                )
                return False
                
            if not hasattr(self.activities_ui, 'activitiesTable'):
                return False
                
            if row >= len(self.all_activities):
                raise ValueError("Invalid activity row")
                
            # Get activity data
            activity_data = self.all_activities[row]
            title = activity_data['title']
            date = activity_data['date']
            category = activity_data['category']
            
            # Confirm deletion
            reply = QMessageBox.question(
                self.main_app,
                "Delete Activity",
                f"Are you sure you want to delete this activity?\n\n"
                f"Event: {title}\n"
                f"Type: {category}\n"
                f"Date: {date.toString('MMM dd, yyyy')}\n\n"
                f"This action cannot be undone.",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                # Store backup for rollback
                backup_events = self.event_manager.get_events_for_date(date)[:]
                
                try:
                    # Remove from event manager memory
                    self.event_manager.remove_event_from_memory(date, title)
                    
                    # Save to JSON
                    if self.event_manager.save_to_json():
                        # Refresh display
                        self.refresh_activities()
                        self.event_manager.refresh_events_display()
                        
                        QMessageBox.information(
                            self.main_app,
                            "Activity Deleted",
                            f"Activity '{title}' has been deleted successfully."
                        )
                        
                        print(f"Activity deleted: {title} on {self.event_manager.date_to_string(date)}")
                        return True
                    else:
                        raise Exception("Failed to save changes to JSON file")
                        
                except Exception as save_error:
                    # Rollback - restore the original events for that date
                    self.event_manager.set_events_for_date(date, backup_events)
                    raise save_error
            
            return False
                
        except Exception as e:
            print(f"Error deleting activity: {e}")
            QMessageBox.critical(
                self.main_app,
                "Delete Activity Failed",
                f"Failed to delete activity: {str(e)}"
            )
            return False
    
    # =========================
    # BUSINESS LOGIC METHODS
    # =========================
    
    def edit_activity(self, row):
        """Handle edit activity action - Business logic"""
        try:
            # Check permission first
            if not self.can_edit_activities():
                QMessageBox.warning(
                    self.main_app,
                    "Access Denied",
                    "You do not have permission to edit activities."
                )
                return
                
            if row >= len(self.all_activities):
                return
                
            # Get the activity data
            activity_data = self.all_activities[row]
            
            # Prepare minimal edit data - AddEventManager will handle the rest
            edit_data = {
                'title': activity_data['title'],
                'category': activity_data['category'],
                'date': activity_data['date'],
                'location': activity_data['location'],
                'time': activity_data['time']
            }
            
            # Route to edit event view using router
            if hasattr(self.main_app, 'router'):
                self.main_app.router.to_edit_event(edit_data)
            else:
                QMessageBox.warning(
                    self.main_app,
                    "Error",
                    "Navigation router not available. Please check main app setup."
                )
                
        except Exception as e:
            print(f"Error routing to edit: {e}")
            QMessageBox.critical(self.main_app, "Error", f"Could not open edit view: {str(e)}")

    def show_add_event(self):
        """Show the add event interface - Business logic"""
        try:
            # Check permission first
            if not self.can_add_activities():
                QMessageBox.warning(
                    self.main_app,
                    "Access Denied",
                    "You do not have permission to add new activities."
                )
                return
                
            # Use router to navigate to add event view
            if hasattr(self.main_app, 'router'):
                self.main_app.router.to_add_event()
            else:
                # Fallback message if router doesn't exist
                QMessageBox.information(
                    self.main_app, 
                    "Add Event", 
                    "Add Event functionality requires the router to be connected to the main application.\n\nPlease ensure the main application has been updated with the router."
                )
                
        except Exception as e:
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self.main_app, "Error", f"Could not show add event interface: {str(e)}")

    def get_category_color(self, category):
        """Get background color for event category"""
        colors = {
            'Academic': QtGui.QColor(200, 255, 200, 150),
            'Organizational': QtGui.QColor(200, 200, 255, 150),
            'Deadline': QtGui.QColor(255, 220, 200, 150),
            'Holiday': QtGui.QColor(255, 200, 200, 150)
        }
        return colors.get(category, QtGui.QColor(240, 240, 240, 150))

    def filter_activities_table(self, filter_type):
        """Filter activities table based on selected type - Business logic"""
        try:
            if not hasattr(self, 'all_activities'):
                return
                
            if filter_type == "All Events":
                filtered_activities = self.all_activities
            else:
                filtered_activities = [
                    activity for activity in self.all_activities 
                    if activity['category'] == filter_type
                ]
            
            self.populate_activities_table(filtered_activities)
            
        except Exception as e:
            import traceback
            traceback.print_exc()

    def populate_activities_upcoming_events(self):
        """Populate upcoming events list in activities view - Data operation"""
        try:
            if not hasattr(self.activities_ui, 'listUpcoming'):
                return
            
            if not self.event_manager:
                return
            
            # Get upcoming events from event manager
            upcoming_events = self.event_manager.get_upcoming_events("All", limit=10)
            
            # Clear the existing list with error handling
            try:
                self.activities_ui.listUpcoming.clear()
            except RuntimeError:
                print("ListUpcoming widget has been deleted, skipping population")
                return
            
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
                self.activities_ui.listUpcoming.addItem(item)
                
        except Exception as e:
            import traceback
            traceback.print_exc()

    def filter_activities_upcoming_events(self, filter_text):
        """Filter upcoming events in activities view - Business logic"""
        try:
            if not hasattr(self.activities_ui, 'listUpcoming'):
                return
            
            if not self.event_manager:
                return
            
            # Map filter text to categories
            filter_map = {
                "All Events": "All",
                "Academic Activities": "Academic",
                "Organizational Activities": "Organizational", 
                "Deadlines": "Deadline",
                "Holidays": "Holiday"
            }
            
            filter_category = filter_map.get(filter_text, "All")
            upcoming_events = self.event_manager.get_upcoming_events(filter_category, limit=10)
            
            # Clear and repopulate the list with error handling
            try:
                self.activities_ui.listUpcoming.clear()
            except RuntimeError:
                print("ListUpcoming widget has been deleted, skipping filter")
                return
            
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
                self.activities_ui.listUpcoming.addItem(item)
                
        except Exception as e:
            import traceback
            traceback.print_exc()

    def go_back_to_calendar(self):
        """Return to calendar from activities - Business logic using router"""
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
            QMessageBox.critical(self.main_app, "Error", f"Could not return to calendar: {str(e)}")

    def refresh_activities(self):
        """Refresh activities data and display - Public interface"""
        try:
            self.load_activities_data()
            self.populate_activities_upcoming_events()
        except RuntimeError as e:
            print(f"Runtime error during activities refresh (widget deleted): {e}")
        except Exception as e:
            import traceback
            traceback.print_exc()