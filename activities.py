# ACTIVITIES.py - UI Only Version
import sys
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QHeaderView, QTableWidget, QTableWidgetItem, QApplication, QMainWindow
from PyQt6.QtCore import Qt, QDate
from base_ui import BaseUi

class Ui_MainWindow(BaseUi):

    def setupUi(self, MainWindow, user_role="student"):
        # Call the base UI setup first
        self.setupBaseUi(MainWindow, user_role)
        
        # Store reference to MainWindow for navigation
        self.main_window = MainWindow
        
        # Now add the specific content for this page - the Activities Table
        self.setup_activities_section()
        
        # Load mock data for demonstration
        # self.load_mock_activities_data()
        
        # Connect UI elements and set translations
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def setup_activities_section(self):
        """Setup the right sidebar with Activities Table"""
        # Right Sidebar - Activities Table
        self.rightSidebar = QtWidgets.QFrame()
        self.rightSidebar.setMinimumWidth(600)  
        self.rightSidebar.setObjectName("rightSidebar")
        self.rightSidebar.setStyleSheet("background-color: #084924; color: white;")
        self.rightLayout = QtWidgets.QVBoxLayout(self.rightSidebar)
        self.rightLayout.setContentsMargins(10, 10, 10, 10)
        
        # Activities Table Label
        self.labelActivities = QtWidgets.QLabel("Daily Activities")
        self.labelActivities.setStyleSheet("font-size: 18px; font-weight: bold; color: white; margin-bottom: 15px; text-align: center;")
        self.labelActivities.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.rightLayout.addWidget(self.labelActivities)

        # Top controls section
        self.setup_top_controls()
        
        # Activities Table Widget
        self.setup_activities_table()
        
        # Add the activities section to the content layout
        self.contentLayout.addWidget(self.rightSidebar)

    def setup_top_controls(self):
        """Setup the top control section with filters and back button"""
        # Create horizontal layout for top controls
        self.topControlsWidget = QtWidgets.QWidget()
        self.topControlsLayout = QtWidgets.QHBoxLayout(self.topControlsWidget)
        self.topControlsLayout.setContentsMargins(0, 0, 0, 10)
        
        # Filters section
        self.filtersWidget = QtWidgets.QWidget()
        self.filtersLayout = QtWidgets.QHBoxLayout(self.filtersWidget)
        self.filtersLayout.setContentsMargins(0, 0, 0, 0)
        
        # Filter label
        self.filterLabel = QtWidgets.QLabel("Filter by:")
        self.filterLabel.setStyleSheet("color: white; font-weight: bold; font-size: 12px;")
        self.filtersLayout.addWidget(self.filterLabel)
        
        combo_style = """
            QComboBox {
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 6px 12px;
                background-color: white;
                min-width: 140px;
                color: #084924;
                font-size: 12px;
                font-weight: bold;
            }
            QComboBox:focus {
                border-color: #FDC601;
                border-width: 2px;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                width: 12px;
                height: 12px;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                border: 1px solid #ccc;
                selection-background-color: #FDC601;
                selection-color: #084924;
                color: #084924;
            }
        """
        
        self.comboActivityType = QtWidgets.QComboBox()
        self.comboActivityType.setStyleSheet(combo_style)
        # Add filter options
        self.comboActivityType.addItems([
            "All Events",
            "Academic", 
            "Organizational",
            "Deadline",
            "Holiday"
        ])
        # self.comboActivityType.currentTextChanged.connect(self.filter_activities)
        self.filtersLayout.addWidget(self.comboActivityType)
        
        # Add stretch to push back button to the right
        self.filtersLayout.addStretch()
        
        # Add filters to top controls
        self.topControlsLayout.addWidget(self.filtersWidget)
        self.topControlsLayout.addStretch()
        
        # Back button - positioned on the right
        self.btnback = QtWidgets.QPushButton("← Back to Calendar")
        self.btnback.setStyleSheet("""
            QPushButton {
                background-color: #FDC601;
                color: #084924;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 12px;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #e6b400;
                border: 2px solid #084924;
            }
            QPushButton:pressed {
                background-color: #cc9f00;
                border: 2px solid #084924;
            }
        """)
        # self.btnback.clicked.connect(self.go_back_to_calendar)
        self.topControlsLayout.addWidget(self.btnback)
        
        # Add top controls to main layout
        self.rightLayout.addWidget(self.topControlsWidget)

    def setup_activities_table(self):
        """Setup the activities table widget"""
        # Activities Table Widget
        self.activitiesTable = QTableWidget(0, 6)  # Start with 0 rows, will be populated
        self.activitiesTable.setMinimumSize(400, 300)
        self.activitiesTable.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Expanding
        )
        
        # Set column headers
        headers = ["Date & Time", "Event", "Type", "Location", "Status", "Action"]
        self.activitiesTable.setHorizontalHeaderLabels(headers)
        
        # Style the table
        self.activitiesTable.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 2px solid #FDC601;
                border-radius: 8px;
                gridline-color: #e0e0e0;
                font-size: 11px;
                alternate-background-color: #f8f9fa;
            }
            
            QTableWidget::item {
                padding: 10px;
                border-bottom: 1px solid #f0f0f0;
                color: #333;
            }
            
            QTableWidget::item:selected {
                background-color: #FDC601;
                color: #084924;
                font-weight: bold;
            }
            
            QTableWidget::item:hover {
                background-color: #f8f9fa;
            }
            
            QHeaderView::section {
                background-color: #084924;
                color: white;
                border: 1px solid #FDC601;
                padding: 12px;
                font-weight: bold;
                font-size: 11px;
                text-align: center;
            }
            
            QHeaderView::section:hover {
                background-color: #0a5228;
            }
            
            QScrollBar:vertical {
                background-color: #f0f0f0;
                width: 12px;
                border-radius: 6px;
                margin: 0px;
            }
            
            QScrollBar::handle:vertical {
                background-color: #084924;
                border-radius: 6px;
                min-height: 20px;
            }
            
            QScrollBar::handle:vertical:hover {
                background-color: #FDC601;
            }
            
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
        
        # Set column widths
        self.activitiesTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)  # Date & Time
        self.activitiesTable.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)  # Event
        self.activitiesTable.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)  # Type
        self.activitiesTable.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)  # Location
        self.activitiesTable.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)  # Status
        self.activitiesTable.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)  # Action
        
        # Set row height
        self.activitiesTable.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.activitiesTable.setAlternatingRowColors(True)
        
        # Hide row numbers
        self.activitiesTable.verticalHeader().setVisible(False)
        
        # Enable sorting
        self.activitiesTable.setSortingEnabled(True)
        
        self.rightLayout.addWidget(self.activitiesTable)
# FIX this might have to be deleted 
    # def load_mock_activities_data(self):
    #     """Load mock activities data for demonstration"""
    #     # Mock data for demonstration
    #     mock_activities = [
    #         {
    #             'date': QDate.currentDate().addDays(1),
    #             'title': 'Programming Fundamentals Quiz',
    #             'category': 'Academic',
    #             'location': 'Room 101',
    #             'status': 'Confirmed',
    #             'time': '09:00 AM'
    #         },
    #         {
    #             'date': QDate.currentDate().addDays(3),
    #             'title': 'CISC Organization Meeting',
    #             'category': 'Organizational',
    #             'location': 'Conference Room A',
    #             'status': 'Pending',
    #             'time': '02:00 PM'
    #         },
    #         {
    #             'date': QDate.currentDate().addDays(5),
    #             'title': 'Final Project Submission',
    #             'category': 'Deadline',
    #             'location': 'Online Portal',
    #             'status': 'Active',
    #             'time': '11:59 PM'
    #         },
    #         {
    #             'date': QDate.currentDate().addDays(7),
    #             'title': 'Database Systems Exam',
    #             'category': 'Academic',
    #             'location': 'Auditorium',
    #             'status': 'Confirmed',
    #             'time': '10:00 AM'
    #         },
    #         {
    #             'date': QDate.currentDate().addDays(10),
    #             'title': 'New Year Holiday',
    #             'category': 'Holiday',
    #             'location': 'Campus-wide',
    #             'status': 'Confirmed',
    #             'time': 'All Day'
    #         },
    #         {
    #             'date': QDate.currentDate().addDays(15),
    #             'title': 'Research Paper Review',
    #             'category': 'Deadline',
    #             'location': 'Online Submission',
    #             'status': 'Active',
    #             'time': '05:00 PM'
    #         }
    #     ]
        
    #     # Store mock data
    #     self.all_activities = mock_activities
        
    #     # Populate the table
    #     self.populate_table(mock_activities)
# FIX this might have to be deleted 
    # def populate_table(self, activities_list):
    #     """Populate the activities table with event data"""
    #     # Disable sorting temporarily to avoid issues during population
    #     self.activitiesTable.setSortingEnabled(False)
        
    #     # Set the number of rows
    #     self.activitiesTable.setRowCount(len(activities_list))
        
    #     for row, activity in enumerate(activities_list):
    #         # Date & Time
    #         date_time = f"{activity['date'].toString('MMM dd, yyyy')}\n{activity['time']}"
    #         date_item = QTableWidgetItem(date_time)
    #         date_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
    #         self.activitiesTable.setItem(row, 0, date_item)
            
    #         # Event
    #         event_item = QTableWidgetItem(activity['title'])
    #         event_item.setTextAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
    #         self.activitiesTable.setItem(row, 1, event_item)
            
    #         # Type
    #         type_item = QTableWidgetItem(activity['category'])
    #         type_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
    #         # Color code the type based on category
    #         type_item.setBackground(self.get_category_color(activity['category']))
    #         self.activitiesTable.setItem(row, 2, type_item)
            
    #         # Location
    #         location_item = QTableWidgetItem(activity['location'])
    #         location_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
    #         self.activitiesTable.setItem(row, 3, location_item)
            
    #         # Status
    #         status_item = QTableWidgetItem(activity['status'])
    #         status_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
    #         status_item.setBackground(self.get_status_color(activity['status']))
    #         self.activitiesTable.setItem(row, 4, status_item)
            
    #         # Action - Add a simple button or text
    #         action_item = QTableWidgetItem("📋 Details")
    #         action_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
    #         action_item.setBackground(QtGui.QColor(240, 240, 240))
    #         action_item.setForeground(QtGui.QColor(8, 73, 36))
    #         self.activitiesTable.setItem(row, 5, action_item)
        
        # Re-enable sorting
        self.activitiesTable.setSortingEnabled(True)
        
        # Sort by date by default (column 0)
        self.activitiesTable.sortItems(0, Qt.SortOrder.AscendingOrder)

    # def get_category_color(self, category):
    #     """Get background color for event category"""
    #     colors = {
    #         'Academic': QtGui.QColor(200, 255, 200, 150),      # Light green
    #         'Organizational': QtGui.QColor(200, 200, 255, 150), # Light blue
    #         'Deadline': QtGui.QColor(255, 220, 200, 150),      # Light orange
    #         'Holiday': QtGui.QColor(255, 200, 200, 150)        # Light red
    #     }
    #     return colors.get(category, QtGui.QColor(240, 240, 240, 150))

    # def get_status_color(self, status):
    #     """Get background color for event status"""
    #     colors = {
    #         'Confirmed': QtGui.QColor(200, 255, 200, 150),     # Light green
    #         'Pending': QtGui.QColor(255, 255, 200, 150),       # Light yellow
    #         'Active': QtGui.QColor(200, 220, 255, 150),        # Light blue
    #         'Cancelled': QtGui.QColor(255, 200, 200, 150)      # Light red
    #     }
    #     return colors.get(status, QtGui.QColor(240, 240, 240, 150))

    # def filter_activities(self, filter_type):
    #     """Filter activities based on selected type"""
    #     if not hasattr(self, 'all_activities'):
    #         return
            
    #     if filter_type == "All Events":
    #         filtered_activities = self.all_activities
    #     else:
    #         filtered_activities = [
    #             activity for activity in self.all_activities 
    #             if activity['category'] == filter_type
    #         ]
        
    #     # Repopulate table with filtered data
    #     self.populate_table(filtered_activities)

    # def go_back_to_calendar(self):
    #     """Navigate back to calendar view"""
    #     # This will be connected to the main application's navigation method
    #     # The connection is made in the main application
    #     pass

    def retranslateUi(self, MainWindow):
        """Set text for UI elements"""
        _translate = QtCore.QCoreApplication.translate
        
        # Set title based on role using the base class method
        title = self.get_title_for_role("Activities")
        if hasattr(self, 'labelTitle'):
            self.labelTitle.setText(_translate("MainWindow", title))
        
        # Set combo box first item text
        if hasattr(self, 'comboActivityType'):
            self.comboActivityType.setItemText(0, _translate("MainWindow", "All Events"))


class ActivitiesApp(QMainWindow):
    """Standalone application class for activities window (for testing)"""
    
    def __init__(self, user_role="student"):
        super().__init__()
        self.user_role = user_role.lower()
        
        # Initialize the UI
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self, user_role=self.user_role)
        
        # Connect back button for standalone mode
        self.ui.btnback.clicked.connect(self.close)
        
        # Set window properties
        self.setMinimumSize(900, 700)
        self.resize(1200, 800)
        
        # Set window title based on role
        self.set_window_title()
        
    def set_window_title(self):
        """Set window title based on user role"""
        role_titles = {
            "admin": "CISC Calendar - Activities (Admin)",
            "student": "CISC Calendar - Activities (Student)",
            "faculty": "CISC Calendar - Activities (Faculty)",
            "organization": "CISC Calendar - Activities (Organization)"
        }
        title = role_titles.get(self.user_role, "CISC Calendar - Activities")
        self.setWindowTitle(title)


if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication, QMainWindow

    app = QApplication(sys.argv)

    # Create the main window
    MainWindow = QMainWindow()

    # Create instance of Ui_MainWindow
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow, user_role="student")  # change role here if needed

    MainWindow.show()
    sys.exit(app.exec())