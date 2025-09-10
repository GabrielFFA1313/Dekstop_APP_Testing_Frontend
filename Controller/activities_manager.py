# ACTIVITIES_MANAGER.PY - Handles all activities view functionality (UPDATED with Event Form Manager)
from PyQt6.QtWidgets import QMessageBox, QWidget, QHBoxLayout, QPushButton
from PyQt6.QtCore import QDate, QTimer, Qt
from PyQt6 import QtWidgets, QtGui, QtCore

from UI.activities import Ui_MainWindow


class ActivitiesManager:
    """Manager class for handling activities view functionality"""
    
    def __init__(self, main_app, event_manager):
        self.main_app = main_app
        self.event_manager = event_manager
        self.activities_ui = None
        self.all_activities = []

    def setup_activities_view(self):
        """Setup the activities view as the main content"""
        try:
            # Store current window properties
            geometry = self.main_app.geometry()
            
            # Clear the current central widget
            self.main_app.setCentralWidget(None)
            
            # Force garbage collection
            import gc
            gc.collect()
            
            # Create activities UI and setup
            self.activities_ui = Ui_MainWindow()
            self.activities_ui.setupUi(self.main_app, user_role=self.main_app.user_role)
            
            # Update table headers after UI setup
            self.update_table_headers()
            
            # Set event manager reference
            if hasattr(self.activities_ui, 'set_event_manager'):
                self.activities_ui.set_event_manager(self.event_manager)
            else:
                self.activities_ui.event_manager = self.event_manager
            
            # Setup connections
            self.setup_activities_connections()
            
            # Restore window properties
            self.main_app.setGeometry(geometry)
            
            # Load data with delay to ensure UI is ready
            QTimer.singleShot(100, self.load_activities_data_delayed)
            
            # Update window title
            self.main_app.setWindowTitle("Campus Event Manager - Activities")
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self.main_app, "Error", f"Could not setup activities view: {str(e)}")

    def update_table_headers(self):
        """Update table headers to remove Status column"""
        if hasattr(self.activities_ui, 'activitiesTable'):
            # Update to 5 columns: Date & Time, Event, Type, Location, Actions
            self.activities_ui.activitiesTable.setColumnCount(5)
            headers = ["Date & Time", "Event", "Type", "Location", "Actions"]
            self.activities_ui.activitiesTable.setHorizontalHeaderLabels(headers)
            
            # Set column widths to prevent Event column from being too wide
            header = self.activities_ui.activitiesTable.horizontalHeader()
            header.setSectionResizeMode(0, header.ResizeMode.Fixed)             # Date & Time - Fixed
            header.setSectionResizeMode(1, header.ResizeMode.Fixed)             # Event - Fixed
            header.setSectionResizeMode(2, header.ResizeMode.Fixed)             # Type - Fixed
            header.setSectionResizeMode(3, header.ResizeMode.Fixed)             # Location - Fixed
            header.setSectionResizeMode(4, header.ResizeMode.Fixed)             # Actions - Fixed
            
            # Set specific widths for all columns to fill the space properly
            self.activities_ui.activitiesTable.setColumnWidth(0, 120)  # Date & Time
            self.activities_ui.activitiesTable.setColumnWidth(1, 280)  # Event column 
            self.activities_ui.activitiesTable.setColumnWidth(2, 120)  # Type
            self.activities_ui.activitiesTable.setColumnWidth(3, 140)  # Location
            self.activities_ui.activitiesTable.setColumnWidth(4, 160)  # Actions - wider to prevent cutoff

    def setup_activities_connections(self):
        """Setup activities-specific connections"""
        try:
            # Connect back button
            if hasattr(self.activities_ui, 'btnback'):
                try:
                    self.activities_ui.btnback.clicked.disconnect()
                except:
                    pass
                self.activities_ui.btnback.clicked.connect(self.go_back_to_calendar)
            
            # Connect Add Event button - UPDATED TO USE EVENT FORM MANAGER
            if hasattr(self.activities_ui, 'btnAddEvent'):
                try:
                    self.activities_ui.btnAddEvent.clicked.disconnect()
                except:
                    pass
                self.activities_ui.btnAddEvent.clicked.connect(self.show_add_event)
            
            # Connect activities table filter
            if hasattr(self.activities_ui, 'comboActivityType'):
                try:
                    self.activities_ui.comboActivityType.currentTextChanged.disconnect()
                except:
                    pass
                self.activities_ui.comboActivityType.currentTextChanged.connect(self.filter_activities_table)
            
            # Connect upcoming events filter in activities view
            if hasattr(self.activities_ui, 'comboUpcomingFilter'):
                try:
                    self.activities_ui.comboUpcomingFilter.currentTextChanged.disconnect()
                except:
                    pass
                self.activities_ui.comboUpcomingFilter.currentTextChanged.connect(self.filter_activities_upcoming_events)
            
        except Exception as e:
            import traceback
            traceback.print_exc()

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
                for title, category in events:
                    # Create activity entry (removed status field)
                    activity = {
                        'date': date,
                        'title': title,
                        'category': category,
                        'location': self.get_default_location(category),
                        'time': self.get_default_time(category)
                    }
                    all_activities.append(activity)
            
            # Sort activities by date (most recent first)
            all_activities.sort(key=lambda x: x['date'], reverse=True)
            
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

    def create_action_buttons(self, row):
        """Create Edit/Delete action buttons for a table row"""
        # Create widget to hold buttons
        button_widget = QWidget()
        button_widget.setStyleSheet("background-color: white;")  # Ensure widget background is white
        button_layout = QHBoxLayout(button_widget)
        button_layout.setContentsMargins(5, 2, 5, 2)
        button_layout.setSpacing(5)
        
        # Edit button
        edit_btn = QPushButton("Edit")
        edit_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #084924;
                border: 1px solid #084924;
                border-radius: 4px;
                padding: 4px 8px;
                font-weight: bold;
                font-size: 10px;
                min-width: 40px;
            }
            QPushButton:hover {
                background-color: #f8f9fa;
                border: 2px solid #084924;
                color: #063018;
            }
            QPushButton:pressed {
                background-color: #e9ecef;
                color: #063018;
            }
        """)
        edit_btn.clicked.connect(lambda: self.edit_activity(row))
        
        # Delete button
        delete_btn = QPushButton("Delete")
        delete_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #dc3545;
                border: 1px solid #dc3545;
                border-radius: 4px;
                padding: 4px 8px;
                font-weight: bold;
                font-size: 10px;
                min-width: 40px;
            }
            QPushButton:hover {
                background-color: #f8f9fa;
                border: 2px solid #dc3545;
                color: #c82333;
            }
            QPushButton:pressed {
                background-color: #e9ecef;
                color: #a71e2a;
            }
        """)
        delete_btn.clicked.connect(lambda: self.delete_activity(row))
        
        # Add buttons to layout
        button_layout.addWidget(edit_btn)
        button_layout.addWidget(delete_btn)
        button_layout.addStretch()
        
        return button_widget

    def populate_activities_table(self, activities_list):
        """Populate the activities table with event data"""
        try:
            if not hasattr(self.activities_ui, 'activitiesTable'):
                return
            
            table = self.activities_ui.activitiesTable
            
            # Disable sorting temporarily to avoid issues during population
            table.setSortingEnabled(False)
            
            # Set the number of rows
            table.setRowCount(len(activities_list))
            
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
                
                # Actions - Create Edit/Delete buttons
                action_buttons = self.create_action_buttons(row)
                table.setCellWidget(row, 4, action_buttons)
            
            # Re-enable sorting
            table.setSortingEnabled(True)
            
            # Sort by date by default (column 0) - most recent first
            table.sortItems(0, Qt.SortOrder.DescendingOrder)
            
        except Exception as e:
            import traceback
            traceback.print_exc()

    def edit_activity(self, row):
        """Handle edit activity action - UPDATED TO USE ADD EVENT MANAGER"""
        try:
            if not hasattr(self.activities_ui, 'activitiesTable'):
                return
                
            table = self.activities_ui.activitiesTable
            
            # Get activity details from the row
            date_time_item = table.item(row, 0)
            event_item = table.item(row, 1)
            type_item = table.item(row, 2)
            location_item = table.item(row, 3)
            
            if event_item and row < len(self.all_activities):
                # Get the activity data from our stored list
                activity_data = self.all_activities[row]
                
                # Prepare event data for editing
                edit_data = {
                    'title': activity_data['title'],
                    'category': activity_data['category'],
                    'type': activity_data['category'],  # Same as category
                    'location': activity_data['location'],
                    'date': activity_data['date'],
                    'time': activity_data['time'],
                    'description': '',  # Default empty description
                    'target_audience': ['All']  # Default target audience
                }
                
                # Use the main app's add event manager to show edit view
                if hasattr(self.main_app, 'add_event_manager'):
                    self.main_app.add_event_manager.setup_edit_event_view(edit_data)
                elif hasattr(self.main_app, 'show_edit_event_view'):
                    self.main_app.show_edit_event_view(edit_data)
                else:
                    # Fallback: Show a message with the activity details
                    QMessageBox.information(
                        self.main_app,
                        "Edit Activity",
                        f"Edit functionality for:\n\n"
                        f"Event: {activity_data['title']}\n"
                        f"Type: {activity_data['category']}\n"
                        f"Location: {activity_data['location']}\n"
                        f"Date: {activity_data['date'].toString('MMM dd, yyyy')}\n\n"
                        f"Add Event Manager needs to be connected to main app."
                    )
                
        except Exception as e:
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self.main_app, "Error", f"Could not edit activity: {str(e)}")

    def delete_activity(self, row):
        """Handle delete activity action"""
        try:
            if not hasattr(self.activities_ui, 'activitiesTable'):
                return
                
            table = self.activities_ui.activitiesTable
            
            # Get activity details from the row
            event_item = table.item(row, 1)
            type_item = table.item(row, 2)
            
            if event_item and row < len(self.all_activities):
                activity_data = self.all_activities[row]
                activity_name = activity_data['title']
                activity_type = activity_data['category']
                
                # Confirm deletion
                reply = QMessageBox.question(
                    self.main_app,
                    "Delete Activity",
                    f"Are you sure you want to delete this activity?\n\n"
                    f"Event: {activity_name}\n"
                    f"Type: {activity_type}\n\n"
                    f"This action cannot be undone.",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                    QMessageBox.StandardButton.No
                )
                
                if reply == QMessageBox.StandardButton.Yes:
                    # TODO: Implement actual delete functionality with event manager
                    if self.event_manager and hasattr(self.event_manager, 'delete_event'):
                        # If event manager has delete method
                        success = self.event_manager.delete_event(activity_data)
                        if success:
                            QMessageBox.information(
                                self.main_app,
                                "Activity Deleted",
                                f"Activity '{activity_name}' has been deleted successfully."
                            )
                        else:
                            QMessageBox.warning(
                                self.main_app,
                                "Delete Failed",
                                f"Failed to delete activity '{activity_name}'. Please try again."
                            )
                    else:
                        # Fallback: just remove from table and show info
                        table.removeRow(row)
                        
                        QMessageBox.information(
                            self.main_app,
                            "Activity Deleted",
                            f"Activity '{activity_name}' has been removed from the list.\n\n"
                            f"Note: Actual database deletion functionality needs to be implemented."
                        )
                    
                    # Refresh the activities list
                    self.refresh_activities()
                
        except Exception as e:
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self.main_app, "Error", f"Could not delete activity: {str(e)}")

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
        """Filter activities table based on selected type"""
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
        """Populate upcoming events list in activities view"""
        try:
            if not hasattr(self.activities_ui, 'listUpcoming'):
                return
            
            if not self.event_manager:
                return
            
            # Get upcoming events from event manager
            upcoming_events = self.event_manager.get_upcoming_events("All", limit=20)
            
            # Clear the existing list
            self.activities_ui.listUpcoming.clear()
            
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
        """Filter upcoming events in activities view"""
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
            upcoming_events = self.event_manager.get_upcoming_events(filter_category, limit=20)
            
            # Clear and repopulate the list
            self.activities_ui.listUpcoming.clear()
            
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

    def show_add_event(self):
        """Show the add event interface - UPDATED TO USE ADD EVENT MANAGER"""
        try:
            # Use the main app's add event manager to show add event view
            if hasattr(self.main_app, 'add_event_manager'):
                self.main_app.add_event_manager.setup_add_event_view()
            elif hasattr(self.main_app, 'show_add_event_view'):
                self.main_app.show_add_event_view()
            else:
                # Fallback message if the method doesn't exist
                QMessageBox.information(
                    self.main_app, 
                    "Add Event", 
                    "Add Event functionality requires the Add Event Manager to be connected to the main application.\n\nPlease ensure the main application has been updated with the Add Event Manager."
                )
                
        except Exception as e:
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self.main_app, "Error", f"Could not show add event interface: {str(e)}")

    def go_back_to_calendar(self):
        """Return to calendar from activities"""
        try:
            self.main_app.show_calendar_view()
        except Exception as e:
            import traceback
            traceback.print_exc()
            QMessageBox.critical(self.main_app, "Error", f"Could not return to calendar: {str(e)}")

    def refresh_activities(self):
        """Refresh activities data and display"""
        try:
            self.load_activities_data()
            self.populate_activities_upcoming_events()
        except Exception as e:
            import traceback
            traceback.print_exc()