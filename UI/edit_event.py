# EDIT_EVENT.py - Edit Event UI
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
        """Setup the edit event form section - RESPONSIVE FOR ALL SCREEN SIZES"""
        # Create a scroll area for better handling of different screen sizes
        self.scrollArea = QtWidgets.QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        # Create scroll widget
        self.scrollWidget = QtWidgets.QWidget()
        self.scrollLayout = QtWidgets.QVBoxLayout(self.scrollWidget)
        self.scrollLayout.setContentsMargins(20, 20, 20, 20)
        self.scrollLayout.setSpacing(15)
        
        # Edit Event Form Container - RESPONSIVE SIZING
        self.editEventContainer = QtWidgets.QFrame()
        self.editEventContainer.setMinimumWidth(500)
        self.editEventContainer.setMaximumWidth(1200)  # Allow it to grow larger
        self.editEventContainer.setObjectName("editEventContainer")
        self.editEventContainer.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Preferred)
        self.editEventContainer.setStyleSheet("""
            QFrame#editEventContainer {
                background-color: white;
                border: 2px solid #084924;
                border-radius: 12px;
                margin: 20px;
            }
        """)
        
        self.editEventLayout = QtWidgets.QVBoxLayout(self.editEventContainer)
        self.editEventLayout.setContentsMargins(20, 20, 20, 20)
        self.editEventLayout.setSpacing(15)
        
        # Header with back arrow and title
        self.setup_header()
        
        # Event form fields
        self.setup_event_form()
        
        # User Type Selection
        self.setup_user_selection()
        
        # Action buttons
        self.setup_action_buttons()
        
        # Add the form to the scroll layout
        self.scrollLayout.addWidget(self.editEventContainer, 0, Qt.AlignmentFlag.AlignCenter)
        self.scrollLayout.addStretch()
        
        # Set the scroll widget
        self.scrollArea.setWidget(self.scrollWidget)
        
        # Add the scroll area to the content layout
        self.contentLayout.addWidget(self.scrollArea)

    def setup_header(self):
        """Setup the header with back button and title"""
        # Create bordered header container
        self.headerContainer = QtWidgets.QFrame()
        self.headerContainer.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border: 1px solid #e9ecef;
                border-radius: 6px;
                padding: 10px;
                margin-bottom: 15px;
            }
        """)
        
        self.headerLayout = QtWidgets.QHBoxLayout(self.headerContainer)
        
        # Back button
        self.btnBack = QtWidgets.QPushButton("← Edit Event")
        self.btnBack.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #084924;
                border: none;
                font-size: 18px;
                font-weight: bold;
                text-align: left;
                padding: 5px;
            }
            QPushButton:hover {
                color: #FDC601;
            }
        """)
        self.btnBack.clicked.connect(self.go_back_to_calendar)
        self.headerLayout.addWidget(self.btnBack)
        
        # Stretch to push buttons to the right
        self.headerLayout.addStretch()
        
        # Action buttons in header
        self.btnManageEvents = QtWidgets.QPushButton("Manage Events")
        self.btnManageEvents.setStyleSheet("""
            QPushButton {
                background-color: #084924;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-size: 12px;
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
                border-radius: 4px;
                padding: 8px 16px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #e6b400;
            }
        """)
        self.headerLayout.addWidget(self.btnViewAll)
        
        # # Search field
        # self.searchField = QtWidgets.QLineEdit()
        # self.searchField.setPlaceholderText("Search")
        # self.searchField.setFixedWidth(150)
        # self.searchField.setStyleSheet("""
        #     QLineEdit {
        #         border: 1px solid #ccc;
        #         border-radius: 4px;
        #         padding: 6px;
        #         background-color: white;
        #     }
        #     QLineEdit:focus {
        #         border-color: #FDC601;
        #     }
        # """)
        # self.headerLayout.addWidget(self.searchField)
        
        # # Search button
        # self.btnSearch = QtWidgets.QPushButton("🔍")
        # self.btnSearch.setFixedSize(30, 30)
        # self.btnSearch.setStyleSheet("""
        #     QPushButton {
        #         background-color: #f0f0f0;
        #         border: 1px solid #ccc;
        #         border-radius: 4px;
        #         font-size: 14px;
        #     }
        #     QPushButton:hover {
        #         background-color: #FDC601;
        #     }
        # """)
        # self.headerLayout.addWidget(self.btnSearch)
        
        # Add the header container to the main layout
        self.editEventLayout.addWidget(self.headerContainer)

    def setup_event_form(self):
        """Setup the event form fields - RESPONSIVE GRID LAYOUT"""
        # Create a bordered container for the form
        self.formContainer = QtWidgets.QFrame()
        self.formContainer.setStyleSheet("""
            QFrame {
                border: 2px solid #ddd;
                border-radius: 8px;
                background-color: #f9f9f9;
                padding: 15px;
                margin: 10px 0px;
            }
        """)
        
        # Form layout - MODIFIED FOR RESPONSIVENESS
        self.formLayout = QtWidgets.QGridLayout(self.formContainer)
        self.formLayout.setSpacing(15)
        self.formLayout.setContentsMargins(20, 20, 20, 20)
        
        # Set column stretch factors to make them responsive
        self.formLayout.setColumnStretch(0, 0)  # Label column - fixed width
        self.formLayout.setColumnStretch(1, 1)  # Input column - expandable
        self.formLayout.setColumnStretch(2, 0)  # Label column - fixed width  
        self.formLayout.setColumnStretch(3, 1)  # Input column - expandable
        
        # Set minimum column widths
        self.formLayout.setColumnMinimumWidth(1, 200)
        self.formLayout.setColumnMinimumWidth(3, 200)
        
        # Input field styling - RESPONSIVE SIZING
        input_style = """
            QLineEdit, QComboBox, QDateEdit, QTimeEdit, QTextEdit {
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 8px;
                background-color: white;
                font-size: 12px;
                min-height: 20px;
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
        """
        
        # Label styling
        label_style = "font-weight: bold; color: #084924; font-size: 12px;"
        
        # Event Title
        row = 0
        self.labelEventTitle = QtWidgets.QLabel("Event Title")
        self.labelEventTitle.setStyleSheet(label_style)
        self.formLayout.addWidget(self.labelEventTitle, row, 0, Qt.AlignmentFlag.AlignTop)
        
        self.inputEventTitle = QtWidgets.QLineEdit()
        self.inputEventTitle.setPlaceholderText("Input Event Title Here")
        self.inputEventTitle.setStyleSheet(input_style)
        self.inputEventTitle.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        self.formLayout.addWidget(self.inputEventTitle, row, 1)
        
        # Description
        self.labelDescription = QtWidgets.QLabel("Description")
        self.labelDescription.setStyleSheet(label_style)
        self.formLayout.addWidget(self.labelDescription, row, 2, Qt.AlignmentFlag.AlignTop)
        
        self.inputDescription = QTextEdit()
        self.inputDescription.setPlaceholderText("(Optional)")
        self.inputDescription.setMaximumHeight(80)
        self.inputDescription.setMinimumHeight(80)
        self.inputDescription.setStyleSheet(input_style)
        self.inputDescription.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        self.formLayout.addWidget(self.inputDescription, row, 3)
        
        # Event Type
        row = 1
        self.labelEventType = QtWidgets.QLabel("Event Type")
        self.labelEventType.setStyleSheet(label_style)
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
        self.formLayout.addWidget(self.labelStartTime, row, 2, Qt.AlignmentFlag.AlignTop)
        
        # Start Time Layout with AM/PM buttons - RESPONSIVE
        self.startTimeWidget = QtWidgets.QWidget()
        self.startTimeLayout = QtWidgets.QHBoxLayout(self.startTimeWidget)
        self.startTimeLayout.setContentsMargins(0, 0, 0, 0)
        self.startTimeLayout.setSpacing(5)
        
        self.timeStart = QTimeEdit()
        self.timeStart.setTime(QTime(9, 0))
        self.timeStart.setDisplayFormat("hh:mm")
        self.timeStart.setStyleSheet(input_style)
        self.timeStart.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        self.startTimeLayout.addWidget(self.timeStart, 1)
        
        self.btnStartAM = QtWidgets.QPushButton("AM")
        self.btnStartAM.setCheckable(True)
        self.btnStartAM.setChecked(True)
        self.btnStartAM.setFixedSize(40, 30)
        self.btnStartAM.clicked.connect(lambda: self.set_am_pm(self.btnStartAM, self.btnStartPM))
        
        self.btnStartPM = QtWidgets.QPushButton("PM")
        self.btnStartPM.setCheckable(True)
        self.btnStartPM.setFixedSize(40, 30)
        self.btnStartPM.clicked.connect(lambda: self.set_am_pm(self.btnStartPM, self.btnStartAM))
        
        # AM/PM button styling
        ampm_style = """
            QPushButton {
                border: 1px solid #ccc;
                border-radius: 4px;
                background-color: white;
                font-size: 10px;
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
        self.formLayout.addWidget(self.labelEndTime, row, 2, Qt.AlignmentFlag.AlignTop)
        
        # End Time Layout with AM/PM buttons - RESPONSIVE
        self.endTimeWidget = QtWidgets.QWidget()
        self.endTimeLayout = QtWidgets.QHBoxLayout(self.endTimeWidget)
        self.endTimeLayout.setContentsMargins(0, 0, 0, 0)
        self.endTimeLayout.setSpacing(5)
        
        self.timeEnd = QTimeEdit()
        self.timeEnd.setTime(QTime(17, 0))
        self.timeEnd.setDisplayFormat("hh:mm")
        self.timeEnd.setStyleSheet(input_style)
        self.timeEnd.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        self.endTimeLayout.addWidget(self.timeEnd, 1)
        
        self.btnEndAM = QtWidgets.QPushButton("AM")
        self.btnEndAM.setCheckable(True)
        self.btnEndAM.setFixedSize(40, 30)
        self.btnEndAM.clicked.connect(lambda: self.set_am_pm(self.btnEndAM, self.btnEndPM))
        
        self.btnEndPM = QtWidgets.QPushButton("PM")
        self.btnEndPM.setCheckable(True)
        self.btnEndPM.setChecked(True)
        self.btnEndPM.setFixedSize(40, 30)
        self.btnEndPM.clicked.connect(lambda: self.set_am_pm(self.btnEndPM, self.btnEndAM))
        
        self.btnEndAM.setStyleSheet(ampm_style)
        self.btnEndPM.setStyleSheet(ampm_style)
        
        self.endTimeLayout.addWidget(self.btnEndAM)
        self.endTimeLayout.addWidget(self.btnEndPM)
        self.formLayout.addWidget(self.endTimeWidget, row, 3)
        
        # Add the form container to the main layout
        self.editEventLayout.addWidget(self.formContainer)

    def setup_user_selection(self):
        """Setup user type selection checkboxes"""
        # Create a bordered container for user selection
        self.userSelectionContainer = QtWidgets.QFrame()
        self.userSelectionContainer.setStyleSheet("""
            QFrame {
                border: 2px solid #ddd;
                border-radius: 8px;
                background-color: #f9f9f9;
                padding: 15px;
                margin: 10px 0px;
            }
        """)
        
        self.userContainerLayout = QtWidgets.QVBoxLayout(self.userSelectionContainer)
        self.userContainerLayout.setContentsMargins(15, 15, 15, 15)
        
        # Add a title for this section
        self.userSelectionTitle = QtWidgets.QLabel("Target Audience")
        self.userSelectionTitle.setStyleSheet("font-weight: bold; color: #084924; font-size: 14px; margin-bottom: 10px;")
        self.userContainerLayout.addWidget(self.userSelectionTitle)
        
        self.userSelectionLayout = QtWidgets.QHBoxLayout()
        self.userSelectionLayout.setSpacing(20)
        
        # Checkbox styling
        checkbox_style = """
            QCheckBox {
                font-size: 12px;
                color: #084924;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
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
        """Setup the update and cancel buttons"""
        self.actionButtonsLayout = QtWidgets.QHBoxLayout()
        self.actionButtonsLayout.addStretch()
        
        # Cancel button
        self.btnCancel = QtWidgets.QPushButton("Cancel")
        self.btnCancel.setFixedSize(100, 35)
        self.btnCancel.setStyleSheet("""
            QPushButton {
                background-color: #f0f0f0;
                color: #666;
                border: 1px solid #ccc;
                border-radius: 4px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """)
        self.btnCancel.clicked.connect(self.cancel_event)
        self.actionButtonsLayout.addWidget(self.btnCancel)
        
        # Update button (changed from Save)
        self.btnUpdate = QtWidgets.QPushButton("Update")
        self.btnUpdate.setFixedSize(100, 35)
        self.btnUpdate.setStyleSheet("""
            QPushButton {
                background-color: #084924;
                color: white;
                border: none;
                border-radius: 4px;
                font-size: 12px;
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
        
        # Set window properties
        self.setMinimumSize(1000, 700)
        self.resize(1200, 800)
        
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