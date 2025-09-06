# SEARCH
from PyQt6 import QtCore, QtGui, QtWidgets
from base_ui import BaseUi

class SearchUi(BaseUi):
    """Search UI class that extends BaseUi with search results functionality"""
    
    def setupSearchUi(self, MainWindow, user_role="student"):
        """Setup the search UI with base elements and search results panel"""
        # Setup base UI first
        self.setupBaseUi(MainWindow, user_role)
        
        # Update title for search page
        self.labelTitleBar.setText("CISC Virtual Hub System - Search")
        self.labelTitle.setText("Search Events")
        
        # Add search results panel to the right
        self.setup_search_results_panel()
        
    def setup_search_results_panel(self):
        """Setup the search results panel on the right side"""
        # Search Results Container - MADE MUCH BIGGER
        self.searchResultsContainer = QtWidgets.QWidget()
        self.searchResultsContainer.setStyleSheet("background-color: white;")
        self.searchResultsContainer.setMinimumWidth(600)  # INCREASED from 300
        self.searchResultsContainer.setMaximumWidth(900)  # INCREASED from 400
        
        self.searchResultsLayout = QtWidgets.QVBoxLayout(self.searchResultsContainer)
        self.searchResultsLayout.setContentsMargins(20, 20, 20, 20)  # INCREASED padding
        self.searchResultsLayout.setSpacing(15)  # INCREASED spacing
        
        # Search Results Header
        self.searchResultsHeader = QtWidgets.QHBoxLayout()
        
        # ADDED: Back Button
        self.btnBack = QtWidgets.QPushButton("← Back")
        self.btnBack.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 15px;
                font-size: 13px;
                font-weight: bold;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
            QPushButton:pressed {
                background-color: #545b62;
            }
        """)
        self.searchResultsHeader.addWidget(self.btnBack)
        
        # Search Results Title
        self.labelSearchResults = QtWidgets.QLabel("Upcoming Events")
        self.labelSearchResults.setStyleSheet("font-size: 18px; font-weight: bold; color: #084924; margin-left: 15px;")  # INCREASED font size
        self.searchResultsHeader.addWidget(self.labelSearchResults)
        
        self.searchResultsHeader.addStretch()
        
        # View Events Dropdown - IMPROVED STYLING
        self.comboViewEvents = QtWidgets.QComboBox()
        self.comboViewEvents.setStyleSheet("""
            QComboBox {
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 6px 12px;
                background-color: #084924;
                color: white;
                min-width: 100px;
                font-size: 13px;
                font-weight: bold;
            }
            QComboBox:focus {
                border-color: #FDC601;
            }
            QComboBox::drop-down {
                border: 0px;
                width: 25px;
            }
            QComboBox::down-arrow {
                image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIiIGhlaWdodD0iOCIgdmlld0JveD0iMCAwIDEyIDgiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxwYXRoIGQ9Ik0xIDFMNiA2TDExIDEiIHN0cm9rZT0id2hpdGUiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIi8+Cjwvc3ZnPgo=);
                width: 12px;
                height: 8px;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                border: 1px solid #ccc;
                selection-background-color: #FDC601;
                selection-color: white;
                color: #084924;
            }
        """)
        self.comboViewEvents.addItems(["View Events"])
        self.comboViewEvents.setCurrentText("View Events")
        self.searchResultsHeader.addWidget(self.comboViewEvents)
        
        # Search Bar beside View Events button - MADE BIGGER
        self.searchBarResults = QtWidgets.QLineEdit()
        self.searchBarResults.setFixedWidth(200)  # INCREASED from 150
        self.searchBarResults.setPlaceholderText("Search events...")
        self.searchBarResults.setStyleSheet("""
            QLineEdit {
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 6px 12px;
                background-color: white;
                font-size: 13px;
            }
            QLineEdit:focus {
                border-color: #FDC601;
                outline: none;
            }
            QLineEdit::placeholder {
                color: #999;
            }
        """)
        self.searchResultsHeader.addWidget(self.searchBarResults)
        
        # View Dropdown - IMPROVED STYLING
        self.comboView = QtWidgets.QComboBox()
        self.comboView.setStyleSheet("""
            QComboBox {
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 6px 12px;
                background-color: #FDC601;
                color: white;
                min-width: 80px;
                font-size: 13px;
                font-weight: bold;
            }
            QComboBox:focus {
                border-color: #084924;
            }
            QComboBox::drop-down {
                border: 0px;
                width: 25px;
            }
            QComboBox::down-arrow {
                image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIiIGhlaWdodD0iOCIgdmlld0JveD0iMCAwIDEyIDgiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxwYXRoIGQ9Ik0xIDFMNiA2TDExIDEiIHN0cm9rZT0id2hpdGUiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIi8+Cjwvc3ZnPgo=);
                width: 12px;
                height: 8px;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                border: 1px solid #ccc;
                selection-background-color: #FDC601;
                selection-color: white;
                color: #084924;
            }
        """)
        self.comboView.addItems(["View"])
        self.comboView.setCurrentText("View")
        self.searchResultsHeader.addWidget(self.comboView)
        
        # Search Button - IMPROVED STYLING
        self.btnSearch = QtWidgets.QPushButton("🔍 Search")
        self.btnSearch.setStyleSheet("""
            QPushButton {
                background-color: #f8f9fa;
                border: 1px solid #ccc;
                border-radius: 4px;
                padding: 6px 12px;
                color: #666;
                font-size: 13px;
                min-width: 80px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #e9ecef;
                border-color: #adb5bd;
            }
            QPushButton:pressed {
                background-color: #dee2e6;
            }
        """)
        self.searchResultsHeader.addWidget(self.btnSearch)
        
        self.searchResultsLayout.addLayout(self.searchResultsHeader)
        
        # Search Results Table Header - MADE BIGGER
        self.tableHeader = QtWidgets.QWidget()
        self.tableHeader.setFixedHeight(50)  # INCREASED from 40
        self.tableHeader.setStyleSheet("background-color: #084924; border-radius: 6px;")
        
        self.tableHeaderLayout = QtWidgets.QHBoxLayout(self.tableHeader)
        self.tableHeaderLayout.setContentsMargins(15, 0, 15, 0)  # INCREASED margins
        
        self.labelDate = QtWidgets.QLabel("Date")
        self.labelDate.setStyleSheet("color: white; font-weight: bold; font-size: 14px;")  # INCREASED font
        self.tableHeaderLayout.addWidget(self.labelDate)
        
        self.tableHeaderLayout.addStretch()
        
        self.labelEvent = QtWidgets.QLabel("Event")
        self.labelEvent.setStyleSheet("color: white; font-weight: bold; font-size: 14px;")  # INCREASED font
        self.tableHeaderLayout.addWidget(self.labelEvent)
        
        self.searchResultsLayout.addWidget(self.tableHeader)
        
        # Search Results List - IMPROVED STYLING
        self.searchResultsList = QtWidgets.QScrollArea()
        self.searchResultsList.setWidgetResizable(True)
        self.searchResultsList.setStyleSheet("""
            QScrollArea {
                border: 1px solid #ddd;
                border-radius: 6px;
                background-color: white;
            }
            QScrollBar:vertical {
                background-color: #f1f1f1;
                width: 14px;
                border-radius: 7px;
            }
            QScrollBar::handle:vertical {
                background-color: #c1c1c1;
                border-radius: 7px;
                min-height: 25px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #a8a8a8;
            }
        """)
        
        # Content widget for scroll area
        self.searchResultsContent = QtWidgets.QWidget()
        self.searchResultsContentLayout = QtWidgets.QVBoxLayout(self.searchResultsContent)
        self.searchResultsContentLayout.setContentsMargins(8, 8, 8, 8)  # INCREASED margins
        self.searchResultsContentLayout.setSpacing(5)  # INCREASED spacing
        
        # REMOVED: No longer adding sample search results here
        # The main application will populate this with real data
        
        # DEBUG: Add a test label to verify layout is working
        test_label = QtWidgets.QLabel("Loading events...")
        test_label.setStyleSheet("color: #999; padding: 20px; text-align: center;")
        test_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.searchResultsContentLayout.addWidget(test_label)
        
        self.searchResultsList.setWidget(self.searchResultsContent)
        self.searchResultsLayout.addWidget(self.searchResultsList)
        
        # Add search results container to content layout
        self.contentLayout.addWidget(self.searchResultsContainer)
        
        print(f"Search results panel setup completed. Layout object: {self.searchResultsContentLayout}")
        print(f"Content widget set in scroll area: {self.searchResultsContent}")

    def clear_search_results(self):
        """Clear all search results from the display"""
        try:
            if hasattr(self, 'searchResultsContentLayout'):
                # Clear all existing result widgets
                for i in reversed(range(self.searchResultsContentLayout.count())):
                    child = self.searchResultsContentLayout.itemAt(i).widget()
                    if child:
                        child.setParent(None)
        except Exception as e:
            print(f"Error clearing search results: {e}")
    
    def create_search_result_item(self, date, event, color, description):
        """Create a single search result item - MADE BIGGER"""
        item_widget = QtWidgets.QWidget()
        item_widget.setFixedHeight(90)  # INCREASED from 80
        item_widget.setStyleSheet(f"""
            QWidget {{
                background-color: {color};
                border-radius: 8px;
                margin: 4px;
            }}
            QWidget:hover {{
                background-color: {self.adjust_color_brightness(color, -20)};
            }}
        """)
        
        item_layout = QtWidgets.QHBoxLayout(item_widget)
        item_layout.setContentsMargins(20, 10, 20, 10)  # INCREASED margins
        
        # Date column - MADE BIGGER
        date_label = QtWidgets.QLabel(date)
        date_label.setStyleSheet("color: white; font-weight: bold; font-size: 13px;")  # INCREASED font
        date_label.setFixedWidth(120)  # INCREASED from 100
        date_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        item_layout.addWidget(date_label)
        
        # Event details column
        event_layout = QtWidgets.QVBoxLayout()
        event_layout.setSpacing(6)  # INCREASED spacing
        
        event_title = QtWidgets.QLabel(event)
        event_title.setStyleSheet("color: white; font-weight: bold; font-size: 15px;")  # INCREASED font
        event_layout.addWidget(event_title)
        
        event_desc = QtWidgets.QLabel(description)
        event_desc.setStyleSheet("color: white; font-size: 13px;")  # INCREASED font
        event_desc.setWordWrap(True)
        event_layout.addWidget(event_desc)
        
        item_layout.addLayout(event_layout)
        
        self.searchResultsContentLayout.addWidget(item_widget)
    
    def adjust_color_brightness(self, hex_color, percent):
        """Adjust the brightness of a hex color"""
        # Remove '#' if present
        hex_color = hex_color.lstrip('#')
        
        # Convert hex to RGB
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        
        # Adjust brightness
        rgb = tuple(max(0, min(255, int(c + (255 - c) * percent / 100))) for c in rgb)
        
        # Convert back to hex
        return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"

if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication, QMainWindow

    app = QApplication(sys.argv)

    # Create the main window
    MainWindow = QMainWindow()
    MainWindow.setWindowTitle("CISC Virtual Hub - Search")
    MainWindow.resize(1400, 800)  # INCREASED window size

    # Create instance of SearchUi
    ui = SearchUi()
    ui.setupSearchUi(MainWindow, user_role="admin")  # change role here if needed

    MainWindow.show()
    sys.exit(app.exec())