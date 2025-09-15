# BASE_UI
from PyQt6 import QtCore, QtGui, QtWidgets

class BaseUi(object):
    """Base UI class containing common elements (sidebar, top bar, etc.)"""
    
    def setupBaseUi(self, MainWindow, user_role="student"):
        """Setup the common UI elements"""
        self.user_role = user_role.lower()
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        # Main Horizontal Layout
        self.mainLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(0)

        # Setup left sidebar
        self.setup_left_sidebar()
        
        # Setup top title bar and content area structure
        self.setup_content_area()
        
        # Add layouts to main layout
        leftWidget = QtWidgets.QWidget()
        leftWidget.setLayout(self.leftContainer)
        self.mainLayout.addWidget(leftWidget)
        
        rightWidget = QtWidgets.QWidget()
        rightWidget.setLayout(self.rightContainer)
        self.mainLayout.addWidget(rightWidget)

        # Handle both QMainWindow and QWidget
        if isinstance(MainWindow, QtWidgets.QMainWindow):
            MainWindow.setCentralWidget(self.centralwidget)
        elif isinstance(MainWindow, QtWidgets.QWidget):
            layout = QtWidgets.QVBoxLayout(MainWindow)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.addWidget(self.centralwidget)

    def setup_left_sidebar(self):
        """Setup the left sidebar with Virtual Hub and navigation"""
        self.leftContainer = QtWidgets.QVBoxLayout()
        self.leftContainer.setContentsMargins(0, 0, 0, 0)
        self.leftContainer.setSpacing(0)

        # Virtual Hub Box at the top
        self.topVirtualHubBox = QtWidgets.QFrame()
        self.topVirtualHubBox.setMinimumWidth(200)
        self.topVirtualHubBox.setFixedHeight(40)
        self.topVirtualHubBox.setStyleSheet("background-color: #FDC601;")
        self.topVirtualHubLayout = QtWidgets.QHBoxLayout(self.topVirtualHubBox)
        self.topVirtualHubLayout.setContentsMargins(10, 5, 10, 5)
        self.labelTopVirtualHub = QtWidgets.QLabel("Virtual Hub")
        self.labelTopVirtualHub.setStyleSheet("font-weight: bold; font-size: 16px; color: white;")
        self.topVirtualHubLayout.addWidget(self.labelTopVirtualHub)
        self.leftContainer.addWidget(self.topVirtualHubBox)

        # Main sidebar
        self.sidebar = QtWidgets.QFrame()
        self.sidebar.setMinimumWidth(200)
        self.sidebar.setObjectName("sidebar")
        self.sidebar.setStyleSheet("background-color: #084924; color: white;")
        self.sidebarLayout = QtWidgets.QVBoxLayout(self.sidebar)

        # Create sidebar buttons
        self.create_sidebar_buttons()
        
        self.leftContainer.addWidget(self.sidebar)

    def create_sidebar_buttons(self):
        """Create all sidebar navigation buttons"""
        # Button styling
        button_style = """
            QPushButton {
                background-color: transparent;
                color: white;
                border: none;
                padding: 10px;
                text-align: left;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #FDC601;
            }
            QPushButton:pressed {
                background-color: rgba(255, 255, 255, 0.2);
            }
        """

        sub_button_style = """
            QPushButton {
                background-color: transparent;
                color: white;
                border: none;
                padding: 5px 5px 5px 30px;
                text-align: left;
                font-size: 12px;
                margin-left: 10px;
            }
            QPushButton:hover {
                background-color: #FDC601;
                color: white;
            }
            QPushButton:pressed {
                background-color: rgba(255, 255, 255, 0.25);
            }
        """

        # Dashboard
        self.btnDashboard = QtWidgets.QPushButton("Dashboard")
        self.btnDashboard.setStyleSheet(button_style)
        self.sidebarLayout.addWidget(self.btnDashboard)
        
        # Academics section
        self.btnAcademics = QtWidgets.QPushButton("Academics")
        self.btnAcademics.setStyleSheet(button_style)
        self.sidebarLayout.addWidget(self.btnAcademics)
        
        self.btnclasses = QtWidgets.QPushButton("Classes")
        self.btnclasses.setStyleSheet(sub_button_style)
        self.sidebarLayout.addWidget(self.btnclasses)

        self.btnschedule = QtWidgets.QPushButton("Schedule")
        self.btnschedule.setStyleSheet(sub_button_style)
        self.sidebarLayout.addWidget(self.btnschedule)

        self.btnsprogress = QtWidgets.QPushButton("Progress")
        self.btnsprogress.setStyleSheet(sub_button_style)
        self.sidebarLayout.addWidget(self.btnsprogress)

        self.btnsappointments = QtWidgets.QPushButton("Appointment")
        self.btnsappointments.setStyleSheet(sub_button_style)
        self.sidebarLayout.addWidget(self.btnsappointments)

        # Organization section
        self.btnorganization = QtWidgets.QPushButton("Organization")
        self.btnorganization.setStyleSheet(button_style)
        self.sidebarLayout.addWidget(self.btnorganization)

        self.btnsbrowser = QtWidgets.QPushButton("Browser")
        self.btnsbrowser.setStyleSheet(sub_button_style)
        self.sidebarLayout.addWidget(self.btnsbrowser)

        self.btnsmembership = QtWidgets.QPushButton("Membership")
        self.btnsmembership.setStyleSheet(sub_button_style)
        self.sidebarLayout.addWidget(self.btnsmembership)

        self.btnsevents = QtWidgets.QPushButton("Events")
        self.btnsevents.setStyleSheet(sub_button_style)
        self.sidebarLayout.addWidget(self.btnsevents)
        
        # Campus section
        self.btnCampus = QtWidgets.QPushButton("Campus")
        self.btnCampus.setStyleSheet(button_style)
        self.sidebarLayout.addWidget(self.btnCampus)

        self.btnscalendar = QtWidgets.QPushButton("Calendar")
        self.btnscalendar.setStyleSheet(sub_button_style)
        self.sidebarLayout.addWidget(self.btnscalendar)

        self.btnsannouncement = QtWidgets.QPushButton("Announcement")
        self.btnsannouncement.setStyleSheet(sub_button_style)
        self.sidebarLayout.addWidget(self.btnsannouncement)

        self.btnshouse = QtWidgets.QPushButton("House")
        self.btnshouse.setStyleSheet(sub_button_style)
        self.sidebarLayout.addWidget(self.btnshouse)

        self.btnsshowcase = QtWidgets.QPushButton("Showcase")
        self.btnsshowcase.setStyleSheet(sub_button_style)
        self.sidebarLayout.addWidget(self.btnsshowcase)
        
        # Tools section
        self.btnTools = QtWidgets.QPushButton("Tools")
        self.btnTools.setStyleSheet(button_style)
        self.sidebarLayout.addWidget(self.btnTools)

        self.btnsdocument = QtWidgets.QPushButton("Documents")
        self.btnsdocument.setStyleSheet(sub_button_style)
        self.sidebarLayout.addWidget(self.btnsdocument)

        self.btnsmessage = QtWidgets.QPushButton("Message")
        self.btnsmessage.setStyleSheet(sub_button_style)
        self.sidebarLayout.addWidget(self.btnsmessage)

        self.btnsstudent = QtWidgets.QPushButton("Student Service")
        self.btnsstudent.setStyleSheet(sub_button_style)
        self.sidebarLayout.addWidget(self.btnsstudent)

        # Spacer to push everything up
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum,
                                          QtWidgets.QSizePolicy.Policy.Expanding)
        self.sidebarLayout.addItem(spacerItem)

    def setup_content_area(self):
        """Setup the right content area structure (without specific content)"""
        self.rightContainer = QtWidgets.QVBoxLayout()
        self.rightContainer.setContentsMargins(0, 0, 0, 0)
        self.rightContainer.setSpacing(0)

        # Top Title Bar
        self.topTitleBar = QtWidgets.QWidget()
        self.topTitleBar.setFixedHeight(40)
        self.topTitleBar.setStyleSheet("background-color: #f0f0f0; border-bottom: 1px solid #ccc;")
        self.topLayout = QtWidgets.QHBoxLayout(self.topTitleBar)
        self.topLayout.setContentsMargins(10, 5, 10, 5)

        # Title label
        self.labelTitleBar = QtWidgets.QLabel("CISC Virtual Hub System")
        self.labelTitleBar.setStyleSheet("font-weight: bold; font-size: 18px; color: black;")
        self.topLayout.addWidget(self.labelTitleBar)

        # Stretch to push search bar to the right
        self.topLayout.addStretch()

        # # Search bar
        # self.searchBarTop = QtWidgets.QLineEdit()
        # self.searchBarTop.setFixedWidth(200)
        # self.searchBarTop.setPlaceholderText("Search Here")
        # self.searchBarTop.setStyleSheet("""
        #     QLineEdit {
        #         border: 1px solid #ccc;
        #         border-radius: 4px;
        #         padding: 4px;
        #         background-color: white;
        #     }
        #     QLineEdit:focus {
        #         border-color: #FDC601;
        #     }
        # """)
        # self.topLayout.addWidget(self.searchBarTop)

        self.rightContainer.addWidget(self.topTitleBar)

        # Content Layout (this will be populated by specific UI classes)
        self.contentLayout = QtWidgets.QHBoxLayout()
        self.contentLayout.setContentsMargins(0, 0, 0, 0)
        self.contentLayout.setSpacing(0)

        # Setup central upcoming events section
        self.setup_upcoming_events_section()
        
        # Add content layout to right container
        contentWidget = QtWidgets.QWidget()
        contentWidget.setLayout(self.contentLayout)
        self.rightContainer.addWidget(contentWidget)

    def setup_upcoming_events_section(self):
        """Setup the central upcoming events section with legends"""
        # Central Content for Upcoming Events
        self.centralContent = QtWidgets.QWidget()
        self.centralContent.setStyleSheet("background-color: white;")
        self.centralContent.setMinimumWidth(150)
        self.centralContent.setMaximumWidth(500)
        self.centralContentLayout = QtWidgets.QVBoxLayout(self.centralContent)
        self.contentLayout.setSpacing(0)
        self.contentLayout.setContentsMargins(0, 0, 0, 0)

        # Top Bar with title and search
        self.topBar = QtWidgets.QHBoxLayout()
        self.labelTitle = QtWidgets.QLabel()
        self.labelTitle.setStyleSheet("font-size: 16px; font-weight: bold; color: #084924;")
        self.topBar.addWidget(self.labelTitle)
        self.topBar.addStretch()
        
        self.searchEvent = QtWidgets.QLineEdit()
        self.searchEvent.setPlaceholderText("Search Event...")
        self.searchEvent.setStyleSheet("""
            QLineEdit {
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 6px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #FDC601;
            }
        """)
        self.topBar.addWidget(self.searchEvent)
        self.centralContentLayout.addLayout(self.topBar)

        # UPCOMING EVENTS FRAME
        self.upcomingEventsFrame = QtWidgets.QFrame()
        self.upcomingEventsFrame.setStyleSheet("""
            QFrame {
                border: 1px solid #ddd;
                border-radius: 8px;
                background-color: #FFFFFF;
                padding: 10px;
            }
        """)
        self.upcomingLayout = QtWidgets.QVBoxLayout(self.upcomingEventsFrame)
        
        # Upcoming Events Label
        self.labelUpcoming = QtWidgets.QLabel("Upcoming Events")
        self.labelUpcoming.setStyleSheet("font-size: 18px; font-weight: bold; color: #084924; text-align: center; padding: 10px;")
        self.labelUpcoming.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.upcomingLayout.addWidget(self.labelUpcoming)

        # Legend 
        self.legendLayout = QtWidgets.QHBoxLayout()
        self.legendLayout.setSpacing(8)  # Reduced from 20 to 8
        
        legend_style = """
            QLabel {
                padding: 3px 6px;
                border-radius: 3px;
                background-color: #f8f9fa;
                border: 1px solid #e9ecef;
                font-size: 11px;
                font-weight: 500;
            }
        """
        
        self.labelAcademic = QtWidgets.QLabel("🟢 Academic Activities")
        self.labelAcademic.setStyleSheet(legend_style)
        self.labelOrg = QtWidgets.QLabel("🔵 Organizational Activities")
        self.labelOrg.setStyleSheet(legend_style)
        self.labelDeadline = QtWidgets.QLabel("🟠 Deadlines")
        self.labelDeadline.setStyleSheet(legend_style)
        self.labelHoliday = QtWidgets.QLabel("🔴 Holidays")
        self.labelHoliday.setStyleSheet(legend_style)
        
        self.legendLayout.addWidget(self.labelAcademic)
        self.legendLayout.addWidget(self.labelOrg)
        self.legendLayout.addWidget(self.labelDeadline)
        self.legendLayout.addWidget(self.labelHoliday)
        self.legendLayout.addStretch()
        
        self.centralContentLayout.addLayout(self.legendLayout)

        # Activity Type Filter
        self.comboUpcomingFilter = QtWidgets.QComboBox()
        self.comboUpcomingFilter.setStyleSheet("""
            QComboBox {
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 6px 12px;
                background-color: white;
                min-width: 150px;
                color: #666;
                font-size: 12px;
                margin: 5px 0px 10px 0px;
            }
            QComboBox:focus {
                border-color: #FDC601;
            }
            QComboBox::drop-down {
                border: 0px;
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
                selection-color: white;
                color: #084924;
            }
        """)
        
        # Add items to the upcoming events dropdown
        self.comboUpcomingFilter.addItems([
            "All Events",
            "Academic Activities", 
            "Organizational Activities",
            "Deadlines",
            "Holidays"
        ])
        self.comboUpcomingFilter.setCurrentText("All Events")
        self.upcomingLayout.addWidget(self.comboUpcomingFilter)
        
        # Upcoming Events List
        self.listUpcoming = QtWidgets.QListWidget()
        self.listUpcoming.setMinimumHeight(300)
        self.listUpcoming.setStyleSheet("""
            QListWidget {
                background-color: white; 
                color: black; 
                border-radius: 8px; 
                padding: 8px;
                border: 1px solid #ddd;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #eee;
                margin: 2px;
            }
            QListWidget::item:hover {
                background-color: #f0f0f0;
                border-radius: 4px;
            }
            QListWidget::item:selected {
                background-color: #FDC601;
                color: white;
                border-radius: 4px;
            }
        """)
        self.upcomingLayout.addWidget(self.listUpcoming)
        
        self.centralContentLayout.addWidget(self.upcomingEventsFrame)
        self.contentLayout.addWidget(self.centralContent)

    def get_title_for_role(self, page_name=""):
        """Generate title based on user role and page"""
        role_titles = {
            "admin": f"CISC {page_name} - Admin Panel - Academic Year 2025 - 2026",
            "student": f"CISC {page_name} - Student Panel - Academic Year 2025 - 2026",
            "faculty": f"CISC {page_name} - Faculty Panel - Academic Year 2025 - 2026",
            "organization": f"CISC {page_name} - Organization Panel - Academic Year 2025 - 2026",

        }
        return role_titles.get(self.user_role, role_titles["admin"])
    
if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication, QMainWindow

    app = QApplication(sys.argv)

    # Create the main window
    MainWindow = QMainWindow()

    # Create instance of CalendarUi
    ui = BaseUi()
    ui.setupBaseUi(MainWindow, user_role="Admin")  # change role here if needed

    MainWindow.show()
    sys.exit(app.exec())