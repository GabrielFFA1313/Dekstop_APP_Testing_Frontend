# ACTIVITIES.py - UI Only Version
import sys
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QHeaderView, QTableWidget, QTableWidgetItem, QApplication, QMainWindow, QWidget, QHBoxLayout, QPushButton
from PyQt6.QtCore import Qt, QDate
# Error handling to be able to run it both in layout file itself and in main
try:
    from .base_ui import BaseUi 
except ImportError:
    from base_ui import BaseUi


class Ui_MainWindow(BaseUi):

    def setupUi(self, MainWindow, user_role="student"):
        # Call the base UI setup first
        self.setupBaseUi(MainWindow, user_role)
        
        # Store reference to MainWindow for navigation
        self.main_window = MainWindow
        
        # Initialize event manager reference
        self.event_manager = None
        
        # Now add the specific content for this page - the Activities Table
        self.setup_activities_section()

        self.apply_role_based_visibility()
        
        # Setup filter section AFTER BaseUi is complete
        self.setup_filter_section()
        
        # Connect UI elements and set translations
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def set_event_manager(self, event_manager):
        """Set the event manager reference"""
        self.event_manager = event_manager
        print("Event manager set in activities UI")

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

    def setup_filter_section(self):
        """Setup filter section for activity types - using existing BaseUi upcoming events"""
        # Update the existing comboUpcomingFilter from base UI (same as calendar)
        if hasattr(self, 'comboUpcomingFilter'):
            self.comboUpcomingFilter.clear()
            self.comboUpcomingFilter.addItems([
                "All Events",
                "Academic Activities", 
                "Organizational Activities",
                "Deadlines",
                "Holidays"
            ])
            self.comboUpcomingFilter.setCurrentText("All Events")

    def populate_upcoming_events(self, events_data=None):
        """Populate the upcoming events list using existing BaseUi component"""
        if not hasattr(self, 'listUpcoming'):
            return
            
        if events_data is None and hasattr(self, 'event_manager') and self.event_manager:
            # Get upcoming events from event manager
            upcoming_events = self.event_manager.get_upcoming_events(limit=20)
            events_data = []
            
            for date, title, category in upcoming_events:
                # Choose icon based on category
                icon_map = {
                    "Academic": "🟢",
                    "Organizational": "🔵", 
                    "Deadline": "🟠",
                    "Holiday": "🔴"
                }
                icon = icon_map.get(category, "⚪")
                
                # Format date
                formatted_date = date.toString("MMM dd, yyyy")
                
                events_data.append({
                    "type": category, 
                    "title": title, 
                    "date": formatted_date, 
                    "icon": icon
                })
        
        # Fallback to sample data if no event manager
        if events_data is None:
            events_data = [
                {"type": "Academic", "title": "Midterm Exams", "date": "Sept 15-20, 2025", "icon": "🟢"},
                {"type": "Organizational", "title": "Student Council Meeting", "date": "Sept 10, 2025", "icon": "🔵"},
                {"type": "Deadline", "title": "Project Submission", "date": "Sept 12, 2025", "icon": "🟠"},
                {"type": "Holiday", "title": "Independence Day", "date": "Sept 21, 2025", "icon": "🔴"},
            ]
        
        self.listUpcoming.clear()
        for event in events_data:
            item_text = f"{event['icon']} {event['title']}\n    {event['date']}"
            item = QtWidgets.QListWidgetItem(item_text)
            self.listUpcoming.addItem(item)

    def setup_top_controls(self):
        """Setup the top control section with filters and buttons"""
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
        self.filtersLayout.addWidget(self.comboActivityType)
        
        # Add stretch to push buttons to the right
        self.filtersLayout.addStretch()
        
        # Add filters to top controls
        self.topControlsLayout.addWidget(self.filtersWidget)
        self.topControlsLayout.addStretch()
        
        # Add Event button - positioned before back button
        self.btnAddEvent = QtWidgets.QPushButton("+ Add Event")
        self.btnAddEvent.setStyleSheet("""
            QPushButton {
                background-color: #084924;
                color: white;
                border: 1px solid #FDC601 ;
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 12px;
                min-width: 120px;
                margin-right: 10px;
            }
            QPushButton:hover {
                background-color: #0a5228;
                border: 2px solid #FDC601;
            }
            QPushButton:pressed {
                background-color: #063018;
                border: 2px solid #FDC601;
            }
        """)
        self.topControlsLayout.addWidget(self.btnAddEvent)
        self.btnAddEvent.setVisible(True)
        
        
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

    def create_action_buttons(self, row, edit_callback=None, delete_callback=None):
        """Create Edit/Delete action buttons for a table row (UI creation only)"""
        # Check user role to determine if buttons should be created
        if self.user_role.lower() not in ['admin', 'administrator', 'super_admin']:
            return None
        
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
        
        # Connect to callback if provided
        if edit_callback:
            edit_btn.clicked.connect(lambda: edit_callback(row))
        
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
        
        # Connect to callback if provided
        if delete_callback:
            delete_btn.clicked.connect(lambda: delete_callback(row))
        
        # Add buttons to layout
        button_layout.addWidget(edit_btn)
        button_layout.addWidget(delete_btn)
        button_layout.addStretch()
        
        return button_widget

    def can_show_action_buttons(self):
        """Check if action buttons should be shown based on user role"""
        return self.user_role.lower() in ['admin', 'administrator', 'super_admin']

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

    def apply_role_based_visibility(self):
        if self.user_role == "student":
            self.btnAddEvent.setVisible(False)
        else:
            self.btnAddEvent.setVisible(True)



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
    ui.setupUi(MainWindow, user_role="admin")  # change role here if needed

    MainWindow.show()
    sys.exit(app.exec())