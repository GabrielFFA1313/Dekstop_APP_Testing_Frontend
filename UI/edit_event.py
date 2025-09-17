# EDIT_EVENT.py - Edit Event UI with Compact Layout
import sys
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QApplication, QMainWindow, QDateEdit, QTimeEdit, QTextEdit
from PyQt6.QtCore import Qt, QDate, QTime
# Error handling to be able to run it both in layout file itself and in main
try:
    from .base_ui import BaseUi 
except ImportError:
    from base_ui import BaseUi


class Ui_MainWindow(BaseUi):

    def setupUi(self, MainWindow, user_role="admin"):
        # Call the base UI setup first
        self.setupBaseUi(MainWindow, user_role)
        
        # Store reference to MainWindow for navigation
        self.main_window = MainWindow
        
        # Now add the specific content for this page - the Edit Event Form
        self.setup_edit_event_section()
        
        # Connect UI elements and set translations
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def setup_edit_event_section(self):
        """Setup the edit event form section - COMPACT VERSION"""
        # Create a scroll area for better handling of different screen sizes
        self.scrollArea = QtWidgets.QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        # Create scroll widget
        self.scrollWidget = QtWidgets.QWidget()
        self.scrollLayout = QtWidgets.QVBoxLayout(self.scrollWidget)
        self.scrollLayout.setContentsMargins(10, 10, 10, 10)  # Smaller margins for more space
        self.scrollLayout.setSpacing(10)  # Reduced spacing
        
        # Edit Event Form Container - BIGGER SIZING, CENTERED WITH INCREASED HEIGHT
        self.editEventContainer = QtWidgets.QFrame()
        self.editEventContainer.setMinimumWidth(600)  # Bigger minimum
        self.editEventContainer.setMaximumWidth(950)  # Bigger maximum
        self.editEventContainer.setMinimumHeight(700)  # Set minimum height
        self.editEventContainer.setObjectName("editEventContainer")
        self.editEventContainer.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        self.editEventContainer.setStyleSheet("""
            QFrame#editEventContainer {
                background-color: white;
                border: 2px solid #084924;
                border-radius: 8px;
                margin: 10px;
            }
        """)
        
        self.editEventLayout = QtWidgets.QVBoxLayout(self.editEventContainer)
        self.editEventLayout.setContentsMargins(25, 15, 25, 25)  # Bigger margins for larger container
        self.editEventLayout.setSpacing(12)  # More spacing for bigger container
        
        # Header with back arrow and title
        self.setup_header()
        
        # Event form fields
        self.setup_event_form()
        
        # User Type Selection
        self.setup_user_selection()
        
        # Action buttons
        self.setup_action_buttons()
        
        # Add stretch at top to center the container vertically
        self.scrollLayout.addStretch()
        
        # Add the form to the scroll layout
        self.scrollLayout.addWidget(self.editEventContainer, 0, Qt.AlignmentFlag.AlignCenter)
        self.scrollLayout.addStretch()
        
        # Set the scroll widget
        self.scrollArea.setWidget(self.scrollWidget)
        
        # Add the scroll area to the content layout
        self.contentLayout.addWidget(self.scrollArea)

    def setup_header(self):
        """Setup the header with back button and title - COMPACT VERSION"""
        # Create bordered header container
        self.headerContainer = QtWidgets.QFrame()
        self.headerContainer.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border: 1px solid #e9ecef;
                border-radius: 4px;
                padding: 6px;
                margin-bottom: 8px;
            }
        """)
        
        self.headerLayout = QtWidgets.QHBoxLayout(self.headerContainer)
        self.headerLayout.setSpacing(8)  # Smaller spacing
        
        # Back button - SMALLER
        self.btnBack = QtWidgets.QPushButton("← Edit Event")
        self.btnBack.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #084924;
                border: none;
                font-size: 20px;
                font-weight: bold;
                text-align: left;
                padding: 4px;
                min-height: 28px;
            }
            QPushButton:hover {
                color: #FDC601;
            }
        """)
        self.btnBack.clicked.connect(self.go_back_to_calendar)
        self.headerLayout.addWidget(self.btnBack)
        
        # Stretch to push buttons to the right
        self.headerLayout.addStretch()
        
        # Action buttons in header - SMALLER
        self.btnManageEvents = QtWidgets.QPushButton("Manage Events")
        self.btnManageEvents.setStyleSheet("""
            QPushButton {
                background-color: #084924;
                color: white;
                border: none;
                border-radius: 3px;
                padding: 6px 12px;
                font-size: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0a5228;
            }
        """)
        self.headerLayout.addWidget(self.btnManageEvents)
        
        self.btnViewAll = QtWidgets.QPushButton("View All")
        self.btnViewAll.setStyleSheet("""
            QPushButton {
                background-color: #FDC601;
                color: #084924;
                border: none;
                border-radius: 3px;
                padding: 6px 12px;
                font-size: 11px;
                font-weight: bold;
                min-height: 28px;
            }
            QPushButton:hover {
                background-color: #e6b400;
            }
        """)
        self.headerLayout.addWidget(self.btnViewAll)
        
        # Add the header container to the main layout
        self.editEventLayout.addWidget(self.headerContainer)

    def setup_event_form(self):
        """Setup the event form fields - LARGER FONTS AND HEIGHTS"""
        # Create a bordered container for the form
        self.formContainer = QtWidgets.QFrame()
        self.formContainer.setStyleSheet("""
            QFrame {
                border: 2px solid #ddd;
                border-radius: 6px;
                background-color: #f9f9f9;
                padding: 10px;
                margin: 5px 0px;
            }
        """)
        
        # Form layout - OPTIMIZED FOR LABEL VISIBILITY
        self.formLayout = QtWidgets.QGridLayout(self.formContainer)
        self.formLayout.setSpacing(12)  # Balanced spacing
        self.formLayout.setContentsMargins(12, 12, 12, 12)  # Balanced margins
        
        # Set column stretch factors and minimum widths for better label visibility
        self.formLayout.setColumnStretch(0, 0)  # Label column - fixed width
        self.formLayout.setColumnStretch(1, 1)  # Input column - expandable
        self.formLayout.setColumnStretch(2, 0)  # Label column - fixed width  
        self.formLayout.setColumnStretch(3, 1)  # Input column - expandable
        
        # Set minimum column widths - more space for labels
        self.formLayout.setColumnMinimumWidth(0, 120)  # Label column width
        self.formLayout.setColumnMinimumWidth(1, 150)  # Input column width
        self.formLayout.setColumnMinimumWidth(2, 120)  # Label column width
        self.formLayout.setColumnMinimumWidth(3, 150)  # Input column width
        
        # Input field styling - LARGER FONTS AND HEIGHTS
        input_style = """
            QLineEdit, QComboBox, QDateEdit, QTimeEdit, QTextEdit {
                border: 1px solid #ccc;
                border-radius: 6px;
                padding: 10px;
                background-color: white;
                font-size: 14px;
                min-height: 35px;
            }
            QLineEdit:focus, QComboBox:focus, QDateEdit:focus, QTimeEdit:focus, QTextEdit:focus {
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
            
            /* KEEP LARGE CALENDAR POPUP STYLING AS REQUESTED */
            QCalendarWidget {
                min-width: 450px;
                min-height: 400px;
                max-width: 500px;
                max-height: 450px;
                font-size: 14px;
                background-color: white;
                border: 2px solid #084924;
                border-radius: 8px;
            }
            QCalendarWidget QWidget#qt_calendar_navigationbar {
                background-color: #084924;
                min-height: 45px;
                max-height: 45px;
            }
            QCalendarWidget QToolButton {
                color: white;
                background-color: #084924;
                border: none;
                font-size: 16px;
                font-weight: bold;
                min-width: 35px;
                min-height: 35px;
            }
            QCalendarWidget QToolButton:hover {
                background-color: #FDC601;
                color: #084924;
                border-radius: 4px;
            }
            QCalendarWidget QMenu {
                background-color: white;
                border: 1px solid #084924;
                font-size: 14px;
            }
            QCalendarWidget QSpinBox {
                background-color: white;
                color: #084924;
                font-size: 16px;
                font-weight: bold;
                min-width: 80px;
                min-height: 35px;
                border: 1px solid #ccc;
            }
            QCalendarWidget QAbstractItemView {
                font-size: 16px;
                selection-background-color: #FDC601;
                selection-color: #084924;
                font-weight: bold;
            }
            QCalendarWidget QAbstractItemView:enabled {
                color: #084924;
                background-color: white;
            }
            QCalendarWidget QHeaderView::section {
                background-color: #f8f9fa;
                color: #084924;
                font-weight: bold;
                font-size: 14px;
                border: 1px solid #e9ecef;
                min-height: 40px;
                padding: 8px;
            }
            QCalendarWidget QTableView {
                gridline-color: #e9ecef;
                alternate-background-color: #f8f9fa;
                font-size: 16px;
            }
            QCalendarWidget QTableView::item {
                padding: 8px;
                min-height: 25px;
                min-width: 25px;
            }
            QCalendarWidget QTableView::item:hover {
                background-color: #e3f2fd;
            }
            QCalendarWidget QTableView::item:selected {
                background-color: #FDC601;
                color: #084924;
                font-weight: bold;
            }
        """
        
        # Label styling - LARGER
        label_style = "font-weight: bold; color: #084924; font-size: 14px; margin-bottom: 5px;"
        
       # Event Title
        row = 0
        self.labelEventTitle = QtWidgets.QLabel("Event Title")
        self.labelEventTitle.setStyleSheet(label_style)
        self.labelEventTitle.setWordWrap(True)  # Allow text wrapping
        self.formLayout.addWidget(self.labelEventTitle, row, 0, Qt.AlignmentFlag.AlignTop)
        
        self.inputEventTitle = QtWidgets.QLineEdit()
        self.inputEventTitle.setPlaceholderText("Input Event Title Here")
        self.inputEventTitle.setStyleSheet(input_style)
        self.inputEventTitle.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        self.formLayout.addWidget(self.inputEventTitle, row, 1)
        
        # Description
        self.labelDescription = QtWidgets.QLabel("Description")
        self.labelDescription.setStyleSheet(label_style)
        self.labelDescription.setWordWrap(True)  # Allow text wrapping
        self.formLayout.addWidget(self.labelDescription, row, 2, Qt.AlignmentFlag.AlignTop)
        
        self.inputDescription = QTextEdit()
        self.inputDescription.setPlaceholderText("(Optional)")
        self.inputDescription.setMaximumHeight(80)  # Taller
        self.inputDescription.setMinimumHeight(80)  # Taller
        self.inputDescription.setStyleSheet(input_style)
        self.inputDescription.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        self.formLayout.addWidget(self.inputDescription, row, 3)
        
        # Event Type
        row = 1
        self.labelEventType = QtWidgets.QLabel("Event Type")
        self.labelEventType.setStyleSheet(label_style)
        self.labelEventType.setWordWrap(True)  # Allow text wrapping
        self.formLayout.addWidget(self.labelEventType, row, 0, Qt.AlignmentFlag.AlignTop)
        
        self.comboEventType = QtWidgets.QComboBox()
        self.comboEventType.addItems([
            "Select Event Type",
            "Academic",
            "Organizational", 
            "Deadline",
            "Holiday"
        ])
        self.comboEventType.setStyleSheet(input_style)
        self.comboEventType.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        self.formLayout.addWidget(self.comboEventType, row, 1)
        
        # Location/Venue
        self.labelLocation = QtWidgets.QLabel("Location/Venue")
        self.labelLocation.setStyleSheet(label_style)
        self.labelLocation.setWordWrap(True)  # Allow text wrapping
        self.formLayout.addWidget(self.labelLocation, row, 2, Qt.AlignmentFlag.AlignTop)
        
        self.inputLocation = QtWidgets.QLineEdit()
        self.inputLocation.setPlaceholderText("(Optional)")
        self.inputLocation.setStyleSheet(input_style)
        self.inputLocation.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        self.formLayout.addWidget(self.inputLocation, row, 3)
        
         # Start Date
        row = 2
        self.labelStartDate = QtWidgets.QLabel("Start Date")
        self.labelStartDate.setStyleSheet(label_style)
        self.labelStartDate.setWordWrap(True)  # Allow text wrapping
        self.formLayout.addWidget(self.labelStartDate, row, 0, Qt.AlignmentFlag.AlignTop)
        
        self.dateStart = QDateEdit()
        self.dateStart.setDate(QDate.currentDate())
        self.dateStart.setCalendarPopup(True)
        self.dateStart.setDisplayFormat("MM/dd/yyyy")
        self.dateStart.setStyleSheet(input_style)
        self.dateStart.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        self.formLayout.addWidget(self.dateStart, row, 1)
        
       # Start Time
        self.labelStartTime = QtWidgets.QLabel("Start Time")
        self.labelStartTime.setStyleSheet(label_style)
        self.labelStartTime.setWordWrap(True)  # Allow text wrapping
        self.formLayout.addWidget(self.labelStartTime, row, 2, Qt.AlignmentFlag.AlignTop)

    # Start Time Layout with AM/PM buttons - LARGER
        self.startTimeWidget = QtWidgets.QWidget()
        self.startTimeLayout = QtWidgets.QHBoxLayout(self.startTimeWidget)
        self.startTimeLayout.setContentsMargins(0, 0, 0, 0)
        self.startTimeLayout.setSpacing(5)  # Larger spacing
        
        self.timeStart = QTimeEdit()
        self.timeStart.setTime(QTime(9, 0))
        self.timeStart.setDisplayFormat("hh:mm")
        self.timeStart.setStyleSheet(input_style)
        self.timeStart.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        self.startTimeLayout.addWidget(self.timeStart, 1)
        
        self.btnStartAM = QtWidgets.QPushButton("AM")
        self.btnStartAM.setCheckable(True)
        self.btnStartAM.setChecked(True)
        self.btnStartAM.setFixedSize(40, 35)  # Larger buttons
        self.btnStartAM.clicked.connect(lambda: self.set_am_pm(self.btnStartAM, self.btnStartPM))
        
        self.btnStartPM = QtWidgets.QPushButton("PM")
        self.btnStartPM.setCheckable(True)
        self.btnStartPM.setFixedSize(40, 35)  # Larger buttons
        self.btnStartPM.clicked.connect(lambda: self.set_am_pm(self.btnStartPM, self.btnStartAM))
        
       # AM/PM button styling - LARGER
        ampm_style = """
            QPushButton {
                border: 1px solid #ccc;
                border-radius: 4px;
                background-color: white;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:checked {
                background-color: #FDC601;
                color: #084924;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
            }
        """
        self.btnStartAM.setStyleSheet(ampm_style)
        self.btnStartPM.setStyleSheet(ampm_style)
        
        self.startTimeLayout.addWidget(self.btnStartAM)
        self.startTimeLayout.addWidget(self.btnStartPM)
        self.formLayout.addWidget(self.startTimeWidget, row, 3)
        
       # End Date
        row = 3
        self.labelEndDate = QtWidgets.QLabel("End Date")
        self.labelEndDate.setStyleSheet(label_style)
        self.labelEndDate.setWordWrap(True)  # Allow text wrapping
        self.formLayout.addWidget(self.labelEndDate, row, 0, Qt.AlignmentFlag.AlignTop)
        
        
        self.dateEnd = QDateEdit()
        self.dateEnd.setDate(QDate.currentDate())
        self.dateEnd.setCalendarPopup(True)
        self.dateEnd.setDisplayFormat("MM/dd/yyyy")
        self.dateEnd.setStyleSheet(input_style)
        self.dateEnd.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        self.formLayout.addWidget(self.dateEnd, row, 1)
        
       # End Time
        self.labelEndTime = QtWidgets.QLabel("End Time")
        self.labelEndTime.setStyleSheet(label_style)
        self.labelEndTime.setWordWrap(True)  # Allow text wrapping
        self.formLayout.addWidget(self.labelEndTime, row, 2, Qt.AlignmentFlag.AlignTop)
        
        # End Time Layout with AM/PM buttons - LARGER
        self.endTimeWidget = QtWidgets.QWidget()
        self.endTimeLayout = QtWidgets.QHBoxLayout(self.endTimeWidget)
        self.endTimeLayout.setContentsMargins(0, 0, 0, 0)
        self.endTimeLayout.setSpacing(5)  # Larger spacing
        
        
        self.timeEnd = QTimeEdit()
        self.timeEnd.setTime(QTime(17, 0))
        self.timeEnd.setDisplayFormat("hh:mm")
        self.timeEnd.setStyleSheet(input_style)
        self.timeEnd.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        self.endTimeLayout.addWidget(self.timeEnd, 1)
        
        self.btnEndAM = QtWidgets.QPushButton("AM")
        self.btnEndAM.setCheckable(True)
        self.btnEndAM.setFixedSize(40, 35)  # Larger buttons
        self.btnEndAM.clicked.connect(lambda: self.set_am_pm(self.btnEndAM, self.btnEndPM))
        
        self.btnEndPM = QtWidgets.QPushButton("PM")
        self.btnEndPM.setCheckable(True)
        self.btnEndPM.setChecked(True)
        self.btnEndPM.setFixedSize(40, 35)  # Larger buttons
        self.btnEndPM.clicked.connect(lambda: self.set_am_pm(self.btnEndPM, self.btnEndAM))
        
        self.btnEndAM.setStyleSheet(ampm_style)
        self.btnEndPM.setStyleSheet(ampm_style)
        
        self.endTimeLayout.addWidget(self.btnEndAM)
        self.endTimeLayout.addWidget(self.btnEndPM)
        self.formLayout.addWidget(self.endTimeWidget, row, 3)
        
        # Add the form container to the main layout
        self.editEventLayout.addWidget(self.formContainer)

    def setup_user_selection(self):
        """Setup user type selection checkboxes - LARGER FONTS"""
        # Create a bordered container for user selection
        self.userSelectionContainer = QtWidgets.QFrame()
        self.userSelectionContainer.setStyleSheet("""
            QFrame {
                border: 2px solid #ddd;
                border-radius: 6px;
                background-color: #f9f9f9;
                padding: 10px;
                margin: 5px 0px;
            }
        """)
        
        self.userContainerLayout = QtWidgets.QVBoxLayout(self.userSelectionContainer)
        self.userContainerLayout.setContentsMargins(12, 8, 12, 8)  # Smaller margins
        
               # Add a title for this section
        self.userSelectionTitle = QtWidgets.QLabel("Target Audience")
        self.userSelectionTitle.setStyleSheet("font-weight: bold; color: #084924; font-size: 14px; margin-bottom: 6px;")
        self.userContainerLayout.addWidget(self.userSelectionTitle)
        
        self.userSelectionLayout = QtWidgets.QHBoxLayout()
        self.userSelectionLayout.setSpacing(15)  # Smaller spacing
        
         # Checkbox styling - LARGER
        checkbox_style = """
            QCheckBox {
                font-size: 14px;
                color: #084924;
                spacing: 10px;
                padding: 5px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
            }
            QCheckBox::indicator:unchecked {
                border: 2px solid #ccc;
                border-radius: 3px;
                background-color: white;
            }
            QCheckBox::indicator:checked {
                border: 2px solid #084924;
                border-radius: 3px;
                background-color: #FDC601;
            }
        """
        
        self.checkStudents = QtWidgets.QCheckBox("Students")
        self.checkStudents.setStyleSheet(checkbox_style)
        self.userSelectionLayout.addWidget(self.checkStudents)
        
        self.checkFaculty = QtWidgets.QCheckBox("Faculty")
        self.checkFaculty.setStyleSheet(checkbox_style)
        self.userSelectionLayout.addWidget(self.checkFaculty)
        
        self.checkOrgOfficer = QtWidgets.QCheckBox("Organization Officer")
        self.checkOrgOfficer.setStyleSheet(checkbox_style)
        self.userSelectionLayout.addWidget(self.checkOrgOfficer)
        
        self.checkAll = QtWidgets.QCheckBox("All")
        self.checkAll.setStyleSheet(checkbox_style)
        self.checkAll.stateChanged.connect(self.toggle_all_users)
        self.userSelectionLayout.addWidget(self.checkAll)
        
        self.userSelectionLayout.addStretch()
        
        # Add the checkbox layout to the container
        self.userContainerLayout.addLayout(self.userSelectionLayout)
        
        # Add the user selection container to main layout
        self.editEventLayout.addWidget(self.userSelectionContainer)

    def setup_action_buttons(self):
        """Setup the save and cancel buttons - LARGER"""
        self.actionButtonsLayout = QtWidgets.QHBoxLayout()
        self.actionButtonsLayout.addStretch()
        
        # Cancel button - LARGER
        self.btnCancel = QtWidgets.QPushButton("Cancel")
        self.btnCancel.setFixedSize(100, 45)  # Larger size
        self.btnCancel.setStyleSheet("""
           QPushButton {
                background-color: #f0f0f0;
                color: #666;
                border: 1px solid #ccc;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """)
        self.btnCancel.clicked.connect(self.cancel_event)
        self.actionButtonsLayout.addWidget(self.btnCancel)
        
        # Update button - SMALLER (changed from Save)
        self.btnUpdate = QtWidgets.QPushButton("Update")
        self.btnUpdate.setFixedSize(100, 45)  # Smaller size
        self.btnUpdate.setStyleSheet("""
             QPushButton {
                background-color: #084924;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0a5228;
            }
        """)
        self.btnUpdate.clicked.connect(self.update_event)
        self.actionButtonsLayout.addWidget(self.btnUpdate)
        
        self.editEventLayout.addLayout(self.actionButtonsLayout)

    def set_am_pm(self, selected_btn, other_btn):
        """Handle AM/PM button selection"""
        selected_btn.setChecked(True)
        other_btn.setChecked(False)

    def toggle_all_users(self):
        """Handle the 'All' checkbox to toggle all user types"""
        is_checked = self.checkAll.isChecked()
        self.checkStudents.setChecked(is_checked)
        self.checkFaculty.setChecked(is_checked)
        self.checkOrgOfficer.setChecked(is_checked)

    def update_event(self):
        """Handle update event action"""
        # Get form data
        event_title = self.inputEventTitle.text()
        event_type = self.comboEventType.currentText()
        
        if not event_title.strip():
            QtWidgets.QMessageBox.warning(
                self.main_window, 
                "Warning", 
                "Please enter an event title."
            )
            return
            
        if event_type == "Select Event Type":
            QtWidgets.QMessageBox.warning(
                self.main_window, 
                "Warning", 
                "Please select an event type."
            )
            return
        
        # Here you would update the event data
        # For now, just show a success message
        QtWidgets.QMessageBox.information(
            self.main_window,
            "Success",
            f"Event '{event_title}' has been updated successfully!"
        )

    def cancel_event(self):
        """Handle cancel action"""
        # Could go back to previous view or clear form
        pass

    def populate_event_data(self, event_data):
        """Populate form fields with existing event data"""
        if event_data:
            self.inputEventTitle.setText(event_data.get('title', ''))
            self.inputDescription.setPlainText(event_data.get('description', ''))
            self.inputLocation.setText(event_data.get('location', ''))
            
            # Set event type
            event_type = event_data.get('type', '')
            index = self.comboEventType.findText(event_type)
            if index >= 0:
                self.comboEventType.setCurrentIndex(index)

    def go_back_to_calendar(self):
        """Navigate back to calendar view"""
        # This will be connected to the main application's navigation method
        pass

    def retranslateUi(self, MainWindow):
        """Set text for UI elements"""
        _translate = QtCore.QCoreApplication.translate
        
        # Set title based on role using the base class method
        title = self.get_title_for_role("Edit Event")
        if hasattr(self, 'labelTitle'):
            self.labelTitle.setText(_translate("MainWindow", title))


class EditEventApp(QMainWindow):
    """Standalone application class for edit event window (for testing)"""
    
    def __init__(self, user_role="admin"):
        super().__init__()
        self.user_role = user_role.lower()
        
        # Initialize the UI
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self, user_role=self.user_role)
        
        # Connect back button for standalone mode
        self.ui.btnBack.clicked.connect(self.close)
        
         # Set window properties - LARGER for taller content
        self.setMinimumSize(900, 800)  # Larger minimum window size for taller content
        self.resize(1000, 900)  # Larger default size
        
        # Set window title
        self.setWindowTitle(f"CISC Calendar - Edit Event ({self.user_role.title()})")


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