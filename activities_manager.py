# ACTIVITIES_MANAGER.PY - Handles all activities view functionality (UPDATED)
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import QDate, QTimer, Qt
from PyQt6 import QtWidgets, QtGui, QtCore

from activities import Ui_MainWindow


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
            
            # Connect Add Event button - UPDATED TO USE SAME WINDOW
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
                    # Determine status based on date
                    current_date = QDate.currentDate()
                    if date < current_date:
                        status = "Completed"
                    elif date == current_date:
                        status = "Active"
                    else:
                        status = "Upcoming"
                    
                    # Create activity entry
                    activity = {
                        'date': date,
                        'title': title,
                        'category': category,
                        'location': self.get_default_location(category),
                        'status': status,
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
                
                # Status
                status_item = QtWidgets.QTableWidgetItem(activity['status'])
                status_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                status_item.setBackground(self.get_status_color(activity['status']))
                table.setItem(row, 4, status_item)
                
                # Action
                action_item = QtWidgets.QTableWidgetItem("📋 Details")
                action_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                action_item.setBackground(QtGui.QColor(240, 240, 240))
                action_item.setForeground(QtGui.QColor(8, 73, 36))
                table.setItem(row, 5, action_item)
            
            # Re-enable sorting
            table.setSortingEnabled(True)
            
            # Sort by date by default (column 0) - most recent first
            table.sortItems(0, Qt.SortOrder.DescendingOrder)
            
        except Exception as e:
            import traceback
            traceback.print_exc()

    def get_category_color(self, category):
        """Get background color for event category"""
        colors = {
            'Academic': QtGui.QColor(200, 255, 200, 150),
            'Organizational': QtGui.QColor(200, 200, 255, 150),
            'Deadline': QtGui.QColor(255, 220, 200, 150),
            'Holiday': QtGui.QColor(255, 200, 200, 150)
        }
        return colors.get(category, QtGui.QColor(240, 240, 240, 150))

    def get_status_color(self, status):
        """Get background color for event status"""
        colors = {
            'Upcoming': QtGui.QColor(200, 220, 255, 150),
            'Active': QtGui.QColor(255, 255, 200, 150),
            'Completed': QtGui.QColor(200, 255, 200, 150),
            'Cancelled': QtGui.QColor(255, 200, 200, 150)
        }
        return colors.get(status, QtGui.QColor(240, 240, 240, 150))

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
        """Show the add event interface in the same window - UPDATED METHOD"""
        try:
            # Use the main app's show_add_event_view method to navigate in same window
            if hasattr(self.main_app, 'show_add_event_view'):
                self.main_app.show_add_event_view()
            else:
                # Fallback message if the method doesn't exist
                QMessageBox.information(
                    self.main_app, 
                    "Add Event", 
                    "Add Event functionality requires the show_add_event_view method in the main application.\n\nPlease ensure the main application has been updated with the add event manager."
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