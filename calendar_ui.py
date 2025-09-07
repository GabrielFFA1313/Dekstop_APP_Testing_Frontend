# CALENDAR UI FILE
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt
from base_ui import BaseUi

class CalendarUi(BaseUi):
    """Calendar UI that inherits from BaseUi for consistent layout"""
    
    def setupUi(self, MainWindow, user_role="student"):
        """Setup the calendar UI with base layout"""
        # Setup base UI (sidebar, top bar, etc.)
        self.setupBaseUi(MainWindow, user_role)
        
        # Update title for calendar page
        self.labelTitleBar.setText(self.get_title_for_role("Calendar"))
        
        # Update the central content title
        self.labelTitle.setText("Campus Calendar")
        
        # Setup calendar-specific content in the right content area
        self.setup_calendar_content()
        
        # Highlight the Calendar button in sidebar since we're on calendar page
        self.highlight_current_page()

    def setup_calendar_content(self):
        """Setup the calendar content in the right side content area"""
        # Create a new widget to hold the calendar
        self.calendarWidget_main = QtWidgets.QWidget()
        self.calendarLayout = QtWidgets.QVBoxLayout(self.calendarWidget_main)
        self.calendarLayout.setContentsMargins(20, 20, 20, 20)
        self.calendarLayout.setSpacing(15)

        # Calendar controls
        self.setup_calendar_controls()
        
        # Action buttons (moved here - between controls and calendar)
        self.setup_action_buttons()
        
        # Main calendar widget
        self.setup_main_calendar()

        # Add the calendar widget to the existing content layout
        # This adds it to the right side of the base UI layout
        self.contentLayout.addWidget(self.calendarWidget_main)

    def setup_calendar_controls(self):
        """Setup calendar view and month controls"""
        self.calendarControlsLayout = QtWidgets.QHBoxLayout()
        self.calendarControlsLayout.setSpacing(15)
        
        # View selector (moved to left side)
        self.labelView = QtWidgets.QLabel("View:")
        self.labelView.setStyleSheet("font-weight: bold; color: #084924; font-size: 14px;")
        
        self.comboView = QtWidgets.QComboBox()
        self.comboView.setMinimumWidth(100)
        self.comboView.addItems(["Month", "Day"])
        self.comboView.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                background-color: white;
                font-size: 12px;
            }
            QComboBox:hover {
                border-color: #FDC601;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #666;
            }
        """)
        
        self.calendarControlsLayout.addWidget(self.labelView)
        self.calendarControlsLayout.addWidget(self.comboView)
        
        # Add stretch to push buttons to the right
        self.calendarControlsLayout.addStretch()
        
        self.calendarLayout.addLayout(self.calendarControlsLayout)

    def setup_main_calendar(self):
        """Setup the main calendar widget"""
        self.calendarWidget = QtWidgets.QCalendarWidget()
        self.calendarWidget.setMinimumSize(500, 400)
        self.calendarWidget.setStyleSheet("""
            QCalendarWidget {
                background-color: white;
                border: 2px solid #084924;
                border-radius: 10px;
                font-family: Arial, sans-serif;
            }
            QCalendarWidget QToolButton {
                height: 35px;
                width: 70px;
                color: #084924;
                font-size: 14px;
                font-weight: bold;
                background-color: transparent;
                border: none;
                margin: 3px;
            }
            QCalendarWidget QToolButton:hover {
                background-color: #FDC601;
                border-radius: 5px;
                color: white;
            }
            QCalendarWidget QToolButton:pressed {
                background-color: #d4a000;
            }
            QCalendarWidget QWidget#qt_calendar_navigationbar {
                background-color: #f8f9fa;
                border-bottom: 2px solid #084924;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
            }
            QCalendarWidget QAbstractItemView:enabled {
                font-size: 13px;
                selection-background-color: #FDC601;
                selection-color: white;
                alternate-background-color: #f0f0f0;
                background-color: white;
            }
            QCalendarWidget QAbstractItemView:disabled {
                color: #bbb;
            }
            QCalendarWidget QHeaderView::section {
                background-color: #084924;
                color: #084924;
                font-weight: bold;
                font-size: 12px;
                border: none;
                padding: 5px;
            }
                                          
        """)
        self.calendarLayout.addWidget(self.calendarWidget)

    def setup_action_buttons(self):
        """Setup action buttons for calendar operations"""
        
        button_style = """
            QPushButton {
                background-color: #084924;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 12px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #FDC601;
                color: #084924;
            }
            QPushButton:pressed {
                background-color: #d4a000;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
        """
        
        # View Event button (available to all roles)
        self.btnviewEvent = QtWidgets.QPushButton("View Event")
        self.btnviewEvent.setStyleSheet(button_style)
        self.calendarControlsLayout.addWidget(self.btnviewEvent)
        
        # Search Bar beside View Event button
        self.searchBarCalendar = QtWidgets.QLineEdit()
        self.searchBarCalendar.setFixedWidth(200)
        self.searchBarCalendar.setPlaceholderText("Search events...")
        self.searchBarCalendar.setStyleSheet("""
            QLineEdit {
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 8px 12px;
                background-color: white;
                font-size: 12px;
            }
            QLineEdit:focus {
                border-color: #FDC601;
                outline: none;
            }
            QLineEdit::placeholder {
                color: #999;
            }
        """)
        self.calendarControlsLayout.addWidget(self.searchBarCalendar)


        # Apply role-based button visibility
        self.apply_role_based_visibility()

    def setup_filter_section(self):
        """Setup filter section for activity types"""
        # Update the existing comboUpcomingFilter from base UI
        self.comboUpcomingFilter.clear()
        self.comboUpcomingFilter.addItems([
            "All Events",
            "Academic Activities", 
            "Organizational Activities",
            "Deadlines",
            "Holidays"
        ])
        self.comboUpcomingFilter.setCurrentText("All Events")
    def apply_role_based_visibility(self):
        if self.user_role == "admin":
            # Admin can see all buttons
            self.btnviewEvent.setVisible(True)
    
    def highlight_current_page(self):
        """Highlight the Calendar button in sidebar to show current page"""
        self.btnscalendar.setStyleSheet("""
            QPushButton {
                background-color: #FDC601;
                color: #084924;
                border: none;
                padding: 5px 5px 5px 30px;
                text-align: left;
                font-size: 12px;
                margin-left: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #FDC601;
                color: #084924;
            }
        """)

    def populate_upcoming_events(self, events_data=None):
        """Populate the upcoming events list with sample or real data"""
        if events_data is None:
            # Sample events for demonstration
            events_data = [
                {"type": "Academic", "title": "Midterm Exams", "date": "Sept 15-20, 2025", "icon": "🟢"},
                {"type": "Organizational", "title": "Student Council Meeting", "date": "Sept 10, 2025", "icon": "🔵"},
                {"type": "Deadline", "title": "Project Submission", "date": "Sept 12, 2025", "icon": "🟠"},
                {"type": "Holiday", "title": "Independence Day", "date": "Sept 21, 2025", "icon": "🔴"},
                {"type": "Academic", "title": "Faculty Development", "date": "Sept 25, 2025", "icon": "🟢"},
            ]
        
        self.listUpcoming.clear()
        for event in events_data:
            item_text = f"{event['icon']} {event['title']}\n    {event['date']}"
            item = QtWidgets.QListWidgetItem(item_text)
            self.listUpcoming.addItem(item)


if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication, QMainWindow

    app = QApplication(sys.argv)

    # Create the main window
    MainWindow = QMainWindow()
    

    # Create instance of CalendarUi
    ui = CalendarUi()
    ui.setupUi(MainWindow, user_role="Admin")  # change role here if needed

    MainWindow.show()
    sys.exit(app.exec())