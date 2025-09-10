# day_view.py
from PyQt6 import QtCore, QtGui, QtWidgets
from .base_ui import BaseUi
from datetime import datetime, timedelta

class DayViewUi(BaseUi):
    """Day View UI class that extends BaseUi"""
    
    def setupDayViewUi(self, MainWindow, user_role="student"):
        """Setup the day view UI"""
        # First setup the base UI
        super().setupBaseUi(MainWindow, user_role)
        
        # Update the title
        self.labelTitleBar.setText("Calendar - Day View")
        self.labelTitle.setText("Upcoming Events")
        
        # Adjust the upcoming events section width to match calendar UI
        self.adjust_upcoming_events_width()
        
        # Add day view to the existing content layout
        self.setup_day_view_content()

    def adjust_upcoming_events_width(self):
        """Adjust the upcoming events section width to match calendar UI"""
        # Set the same width constraints as in calendar_ui.py
        self.centralContent.setMinimumWidth(150)
        self.centralContent.setMaximumWidth(500)
        
        # Ensure the central content maintains its size
        self.centralContent.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Fixed,
            QtWidgets.QSizePolicy.Policy.Expanding
        )

    def setup_day_view_content(self):
        """Setup the day view content area to fill remaining space like calendar UI"""
        
        # Create day view container that expands like calendar UI does
        self.dayViewContainer = QtWidgets.QWidget()
        self.dayViewContainer.setStyleSheet("background-color: white; border-left: 1px solid #ddd;")
        # Remove the fixed width completely to match calendar UI behavior
        # Don't set any width constraints - let it expand naturally
        
        self.dayViewLayout = QtWidgets.QVBoxLayout(self.dayViewContainer)
        self.dayViewLayout.setContentsMargins(20, 20, 20, 20)
        self.dayViewLayout.setSpacing(15)
        
        # Setup day view header and calendar
        self.setup_day_view_header()
        self.setup_day_view_calendar()
        
        # Add to the existing contentLayout from base UI exactly like calendar UI does
        self.contentLayout.addWidget(self.dayViewContainer)
        
        # Don't set any stretch factors or spacers - let it behave like calendar UI
        # The calendar UI doesn't set stretch factors, so neither should we

    def setup_day_view_header(self):
        """Setup the header with date navigation and view controls"""
        # View selector at the top
        self.viewControlLayout = QtWidgets.QHBoxLayout()
        self.viewControlLayout.setSpacing(10)
        
        # View dropdown label and combo
        self.labelView = QtWidgets.QLabel("View:")
        self.labelView.setStyleSheet("font-weight: bold; color: #084924; font-size: 14px;")
        
        self.comboView = QtWidgets.QComboBox()
        self.comboView.setMinimumWidth(100)
        self.comboView.addItems(["Day", "Month"])  # Day is selected by default
        self.comboView.setCurrentText("Day")
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
        
        self.viewControlLayout.addWidget(self.labelView)
        self.viewControlLayout.addWidget(self.comboView)
        self.viewControlLayout.addStretch()  # Push to left side
        
        self.dayViewLayout.addLayout(self.viewControlLayout)
        
        # Day View Title
        self.dayViewTitle = QtWidgets.QLabel("Daily Schedule")
        self.dayViewTitle.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #084924;
            margin-bottom: 10px;
        """)
        self.dayViewLayout.addWidget(self.dayViewTitle)
        
        # Current date label
        current_date = datetime.now()
        self.labelCurrentDate = QtWidgets.QLabel(current_date.strftime("%A\n%B %d, %Y"))
        self.labelCurrentDate.setStyleSheet("""
            font-size: 14px;
            font-weight: bold;
            color: #084924;
            text-align: center;
            margin: 5px 0px;
            padding: 8px;
            border: 2px solid #FDC601;
            border-radius: 6px;
            background-color: #fffef7;
        """)
        self.labelCurrentDate.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.dayViewLayout.addWidget(self.labelCurrentDate)
        
        # Navigation buttons layout (horizontal)
        self.navButtonsLayout = QtWidgets.QHBoxLayout()
        self.navButtonsLayout.setSpacing(10)
        
        # Previous day button
        self.btnPrevDay = QtWidgets.QPushButton("◀ Previous")
        self.btnPrevDay.setStyleSheet("""
            QPushButton {
                background-color: #084924;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 6px 12px;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #FDC601;
            }
        """)
        
        # Next day button
        self.btnNextDay = QtWidgets.QPushButton("Next ▶")
        self.btnNextDay.setStyleSheet("""
            QPushButton {
                background-color: #084924;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 6px 12px;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #FDC601;
            }
        """)
        
        self.navButtonsLayout.addWidget(self.btnPrevDay)
        self.navButtonsLayout.addWidget(self.btnNextDay)
        
        self.dayViewLayout.addLayout(self.navButtonsLayout)
        
        # Today button (separate row)
        self.btnToday = QtWidgets.QPushButton("Today")
        self.btnToday.setStyleSheet("""
            QPushButton {
                background-color: #FDC601;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 6px 12px;
                font-weight: bold;
                font-size: 11px;
                margin-top: 5px;
            }
            QPushButton:hover {
                background-color: #084924;
            }
        """)
        
        self.dayViewLayout.addWidget(self.btnToday)

    def setup_day_view_calendar(self):
        """Setup the day view calendar with time slots"""
        # Create scroll area for the day view
        self.dayScrollArea = QtWidgets.QScrollArea()
        self.dayScrollArea.setWidgetResizable(True)
        self.dayScrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.dayScrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        # Create the calendar widget
        self.dayCalendarWidget = QtWidgets.QWidget()
        self.dayCalendarLayout = QtWidgets.QVBoxLayout(self.dayCalendarWidget)
        self.dayCalendarLayout.setContentsMargins(0, 0, 0, 0)
        self.dayCalendarLayout.setSpacing(0)
        
        # Create time slots (8 AM to 6 PM)
        self.create_time_slots()
        
        # Set the widget for scroll area
        self.dayScrollArea.setWidget(self.dayCalendarWidget)
        self.dayViewLayout.addWidget(self.dayScrollArea)

    def create_time_slots(self):
        """Create time slots that expand to fill available width"""
        start_hour = 7  # 7 AM
        end_hour = 19   # 7 PM 
        
        for hour in range(start_hour, end_hour + 1):
            # Create time slot container that fills available width
            timeSlotContainer = QtWidgets.QWidget()
            timeSlotContainer.setFixedHeight(60)  # Fixed height but expandable width
            timeSlotContainer.setSizePolicy(
                QtWidgets.QSizePolicy.Policy.Expanding,  # Expand horizontally
                QtWidgets.QSizePolicy.Policy.Fixed       # Fixed height
            )
            timeSlotContainer.setStyleSheet("""
                QWidget {
                    border-bottom: 1px solid #e0e0e0;
                    background-color: white;
                }
                QWidget:hover {
                    background-color: #f9f9f9;
                }
            """)
            
            timeSlotLayout = QtWidgets.QHBoxLayout(timeSlotContainer)
            timeSlotLayout.setContentsMargins(0, 0, 0, 0)
            timeSlotLayout.setSpacing(0)
            
            # Time label with fixed width
            if hour == 0:
                display_time = "12:00 AM"
            elif hour < 12:
                display_time = f"{hour}:00 AM"
            elif hour == 12:
                display_time = "12:00 PM"
            else:
                display_time = f"{hour-12}:00 PM"
            
            timeLabel = QtWidgets.QLabel(display_time)
            timeLabel.setFixedWidth(100)  # Fixed width for time column
            timeLabel.setStyleSheet("""
                QLabel {
                    color: #666;
                    font-size: 12px;
                    font-weight: bold;
                    padding: 8px;
                    border-right: 2px solid #e0e0e0;
                    background-color: #f8f9fa;
                }
            """)
            timeLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignCenter)
            
            # Event area that expands to fill ALL available space
            eventArea = QtWidgets.QWidget()
            eventArea.setSizePolicy(
                QtWidgets.QSizePolicy.Policy.Expanding,  # Fill all remaining width
                QtWidgets.QSizePolicy.Policy.Expanding   # Fill available height
            )
            eventArea.setStyleSheet("""
                QWidget {
                    background-color: #fafafa;
                    border: none;
                }
                QWidget:hover {
                    background-color: #f0f0f0;
                }
            """)
            eventLayout = QtWidgets.QVBoxLayout(eventArea)
            eventLayout.setContentsMargins(15, 8, 15, 8)  # More generous margins
            
            # Add a placeholder label for events
            placeholderLabel = QtWidgets.QLabel("No events scheduled")
            placeholderLabel.setStyleSheet("""
                QLabel {
                    color: #999;
                    font-style: italic;
                    font-size: 12px;
                    padding: 5px;
                }
            """)
            eventLayout.addWidget(placeholderLabel)
            
            timeSlotLayout.addWidget(timeLabel)
            timeSlotLayout.addWidget(eventArea, 1)  # Stretch factor 1 to fill remaining space
            
            self.dayCalendarLayout.addWidget(timeSlotContainer)

    def add_compact_event(self, layout, title, color):
        """Add a compact event for the right sidebar"""
        eventWidget = QtWidgets.QFrame()
        eventWidget.setStyleSheet(f"""
            QFrame {{
                background-color: {color};
                border-radius: 3px;
                margin: 1px;
                padding: 2px;
            }}
        """)
        
        eventLayout = QtWidgets.QVBoxLayout(eventWidget)
        eventLayout.setContentsMargins(4, 2, 4, 2)
        eventLayout.setSpacing(0)
        
        # Event title (compact)
        titleLabel = QtWidgets.QLabel(title)
        titleLabel.setStyleSheet("""
            QLabel {
                color: white;
                font-weight: bold;
                font-size: 9px;
            }
        """)
        
        eventLayout.addWidget(titleLabel)
        layout.addWidget(eventWidget)

    def connect_day_view_signals(self):
        """Connect day view specific signals"""
        # Connect navigation buttons
        self.btnPrevDay.clicked.connect(self.previous_day)
        self.btnNextDay.clicked.connect(self.next_day)
        self.btnToday.clicked.connect(self.go_to_today)

    def previous_day(self):
        """Navigate to previous day"""
        # This would update the date and refresh the view
        print("Previous day clicked")

    def next_day(self):
        """Navigate to next day"""
        # This would update the date and refresh the view
        print("Next day clicked")

    def go_to_today(self):
        """Navigate to today"""
        current_date = datetime.now()
        self.labelCurrentDate.setText(current_date.strftime("%A\n%B %d, %Y"))
        print("Today clicked")

if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication, QMainWindow

    app = QApplication(sys.argv)

    # Create the main window
    MainWindow = QMainWindow()
    MainWindow.setWindowTitle("CISC Virtual Hub - Day View")
    MainWindow.setGeometry(100, 100, 1200, 800)

    # Create instance of DayViewUi
    ui = DayViewUi()
    ui.setupDayViewUi(MainWindow, user_role="Admin")
    
    # Connect signals
    ui.connect_day_view_signals()

    MainWindow.show()
    sys.exit(app.exec())