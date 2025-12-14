import sys
import json
import datetime
import math
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QHBoxLayout, QVBoxLayout, QWidget, QScrollArea, QLabel, QLineEdit, QComboBox, QPushButton
from PyQt5.QtGui import QFont
from functools import partial


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        #Setting window properties
        self.setWindowTitle("Munchy")
        self.setMinimumSize(1400, 1100)
        self.setMaximumSize(1400, 1100)
        self.setStyleSheet("background-color: #24201f")
        self.setWindowFlags(Qt.FramelessWindowHint)

        #Mouse pos
        self.oldPos = self.pos()

        #Initiation methods
        self.read_data_file()
        self.initUI()

            #----- Mouse controls -----#

        #Check the mouse pos when user clicks and determine if area is titlebar
        def mousePressEvent(self, event):
            
            x = event.pos().x()
            y = event.pos().y()

            width = self.width()

            if (0 < x < width - 96 and 0 < y < 44):
                self.dragging = True
                self.oldPos = event.globalPos()
            else:
                self.dragging = False

        #If mouse clicked on titlebar then window is able to be moved with mouse
        def mouseMoveEvent(self, event):

            if self.dragging:
                delta = QPoint(event.globalPos() - self.oldPos)
                self.move(self.x() + delta.x(), self.y() + delta.y())
                self.oldPos = event.globalPos()
        
        #resets dragging bool to false to prevent moving window from other areas
        def mouseReleaseEvent(self, event):
            self.dragging = False

    #Reading the data.json file on load
    def read_data_file(self):
        with open('./src/data.json', 'r') as json_file:
            self.data = json.load(json_file)
            self.local_profiles = self.data['profiles']
            self.local_consumables = self.data['consumables']

        #Creating a local Profiles instance with a .profile for all stored profiles

           

    def initUI(self):

        #Central application widget - This is the widget that covers the full application
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        #Central application layout
        self.central_layout = QVBoxLayout()
        self.central_layout.setContentsMargins(0, 0, 0, 0)
        self.central_layout.setSpacing(0)

        # ----------------------- Start with new profile page or profile page -----------------------------

        self.titlebar()
        self.tabs()
        
        self.central_widget.setLayout(self.central_layout)

        if not self.local_profiles:
            self.tabs_widget.hide()
            self.new_profile()

        else:
            self.profiles()



    def titlebar(self):

        #title bar elements
        title_label = QLabel("", self)
        title_label.setFixedWidth(280)
        title_label.setFixedHeight(44)
        title_label.setStyleSheet("image: url(./assets/titlebar/title.png)")

        min_button = QPushButton("", self)
        min_button.setFixedWidth(48)
        min_button.setFixedHeight(44)
        min_button.setFocusPolicy(Qt.NoFocus)
        min_button.clicked.connect(self.showMinimized)
        min_button.setStyleSheet("""
                                        QPushButton {
                                            image: url(assets/titlebar/min.png);
                                            background-color: transparent;
                                            outline: none;
                                            padding: 0px;
                                            margin: 0px;
                                            border: none;
                                        }
                                        QPushButton:hover {                                                        
                                            image: url(assets/titlebar/min_highlight.png);
                                        }
                                        QPushButton:focus {
                                            image: url(assets/titlebar/min.png);
                                            border: none;
                                        }""")

        exit_button = QPushButton("", self)
        exit_button.setFixedWidth(48)
        exit_button.setFixedHeight(44)
        exit_button.setFocusPolicy(Qt.NoFocus)
        exit_button.clicked.connect(QApplication.instance().quit)
        exit_button.setStyleSheet("""
                                        QPushButton {
                                            image: url(./assets/titlebar/exit.png);
                                            background-color: transparent;
                                            outline: none;
                                            padding: 0px;
                                            margin: 0px;
                                            border: none;
                                        }
                                        QPushButton:hover {                                                      
                                            image: url(./assets/titlebar/exit_highlight.png);
                                        }
                                        QPushButton:focus {
                                            image: url(./assets/titlebar/exit_highlight.png);
                                        }""")

        #Titlebar Widget - Also setting the layout of the titlebar elements within the widget
        titlebar_widget = QWidget()
        titlebar_widget.setFixedHeight(44)
        titlebar_widget.setStyleSheet("background-color: #171514")

        titlebar_layout = QHBoxLayout()
        titlebar_layout.setContentsMargins(0, 0, 0, 0)
        titlebar_layout.setSpacing(0)

        #Sorting titlebar elements(sub-widgets of the titlebar widget)
        titlebar_layout.addStretch()
        titlebar_layout.addWidget(title_label)
        titlebar_layout.addSpacing(48)
        titlebar_layout.addStretch()
        titlebar_layout.addWidget(min_button)
        titlebar_layout.addWidget(exit_button)

        #Applying the titlebar layout to the titlebar widget
        titlebar_widget.setLayout(titlebar_layout)

        #Adding the titlebar as a widget of the central widget layout
        self.central_layout.addWidget(titlebar_widget)




    def tabs(self):

        #Tab elements
        self.profiles_tab = QPushButton("Profiles", self)
        self.profiles_tab.setFixedHeight(106)
        self.profiles_tab.setFixedWidth(230)
        self.profiles_tab.setFont(QFont("Times New Roman", 20))
        self.profiles_tab.setStyleSheet("""
                                QPushButton {
                                    color: #645e59; background-color: #24201f; border: 0px; text-align: center;
                                }

                                QPushButton:Hover {
                                    background-color: #171514;
                                }
                            """)
        self.profiles_tab.clicked.connect(lambda: self.tab_switcher("Profiles"))

        self.consumables_tab = QPushButton("Consumables", self)
        self.consumables_tab.setFixedHeight(106)
        self.consumables_tab.setFixedWidth(230)
        self.consumables_tab.setFont(QFont("Times New Roman", 20))
        self.consumables_tab.setStyleSheet("""
                                QPushButton {
                                    color: #645e59; background-color: #24201f; border: 0px; text-align: center;
                                }

                                QPushButton:Hover {
                                    background-color: #171514;
                                }
                            """)
        self.consumables_tab.clicked.connect(lambda: self.tab_switcher("Consumables"))

        self.recipes_tab = QPushButton("Recipes", self)
        self.recipes_tab.setFixedHeight(106)
        self.recipes_tab.setFixedWidth(230)
        self.recipes_tab.setFont(QFont("Times New Roman", 20))
        self.recipes_tab.setStyleSheet("""
                                QPushButton {
                                    color: #645e59; background-color: #24201f; border: 0px; text-align: center;
                                }

                                QPushButton:Hover {
                                    background-color: #171514;
                                }
                            """)

        self.pantry_tab = QPushButton("Pantry", self)
        self.pantry_tab.setFixedHeight(106)
        self.pantry_tab.setFixedWidth(230)
        self.pantry_tab.setFont(QFont("Times New Roman", 20))
        self.pantry_tab.setStyleSheet("""
                                QPushButton {
                                    color: #645e59; background-color: #24201f; border: 0px; text-align: center;
                                }

                                QPushButton:Hover {
                                    background-color: #171514;
                                }
                            """)

        self.planner_tab = QPushButton("Planner", self)
        self.planner_tab.setFixedHeight(106)
        self.planner_tab.setFixedWidth(230)
        self.planner_tab.setFont(QFont("Times New Roman", 20))
        self.planner_tab.setStyleSheet("""
                                QPushButton {
                                    color: #645e59; background-color: #24201f; border: 0px; text-align: center;
                                }

                                QPushButton:Hover {
                                    background-color: #171514;
                                }
                            """)

        self.shopping_tab = QPushButton("Shopping", self)
        self.shopping_tab.setFixedHeight(106)
        self.shopping_tab.setFixedWidth(230)
        self.shopping_tab.setFont(QFont("Times New Roman", 20))
        self.shopping_tab.setStyleSheet("""
                                QPushButton {
                                    color: #645e59; background-color: #24201f; border: 0px; text-align: center;
                                }

                                QPushButton:Hover {
                                    background-color: #171514;
                                }
                            """)

        #Tabs Widget - Also setting the layout of the tab elements within the widget
        self.tabs_widget = QWidget()
        self.tabs_widget.setFixedHeight(112)
        self.tabs_widget.setStyleSheet("background-color: #161515")

        self.tabs_layout = QHBoxLayout()
        self.tabs_layout.setContentsMargins(0, 0, 0, 0)
        self.tabs_layout.setSpacing(3)

        #Sorting tab elements(sub-widgets of the tabs widget)
        self.tabs_layout.addStretch()
        self.tabs_layout.addWidget(self.profiles_tab, alignment=Qt.AlignVCenter)
        self.tabs_layout.addWidget(self.consumables_tab, alignment=Qt.AlignVCenter)
        self.tabs_layout.addWidget(self.recipes_tab, alignment=Qt.AlignVCenter)
        self.tabs_layout.addWidget(self.pantry_tab, alignment=Qt.AlignVCenter)
        self.tabs_layout.addWidget(self.planner_tab, alignment=Qt.AlignVCenter)
        self.tabs_layout.addWidget(self.shopping_tab, alignment=Qt.AlignVCenter)
        self.tabs_layout.addStretch()

        self.tabs_widget.setLayout(self.tabs_layout)
        
        self.central_layout.addWidget(self.tabs_widget)




    def new_profile(self):

        self.can_save_profile = False

        #Center column - Row 1 - Profile picture
        self.new_profile_picture = QLabel(self)
        self.new_profile_picture.setFixedHeight(260)
        self.new_profile_picture.setFixedWidth(260)
        self.new_profile_picture.setFocusPolicy(Qt.StrongFocus)
        self.new_profile_picture.setStyleSheet("background-color: #171514; border: 2px solid black; border-radius: 20px")

        #Center column - Row 2 - Name
        self.new_name_text = QLineEdit(self)
        self.new_name_text.setPlaceholderText("Name")
        self.new_name_text.setFixedHeight(60)
        self.new_name_text.setAlignment(Qt.AlignCenter)
        self.new_name_text.setFont(QFont("Times New Roman", 20))
        self.new_name_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid black; border-radius: 14px")
        self.new_name_text.textEdited.connect(lambda: self.is_empty(self.new_name_text))

        #Center column - Row 3 - D.O.B
            
            #elements left to right
            
        # -- element 1 --
        self.new_day_text = QLineEdit(self)
        self.new_day_text.setPlaceholderText("DD")
        self.new_day_text.setFixedHeight(60)
        self.new_day_text.setFixedWidth(146)
        self.new_day_text.setAlignment(Qt.AlignCenter)
        self.new_day_text.setFont(QFont("Times New Roman", 20))
        self.new_day_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid black; border-radius: 14px")
        self.new_day_text.textEdited.connect(lambda: self.is_empty(self.new_day_text))

        # -- element 2 --
        self.new_month_text = QLineEdit(self)
        self.new_month_text.setPlaceholderText("MM")
        self.new_month_text.setFixedHeight(60)
        self.new_month_text.setFixedWidth(146)
        self.new_month_text.setAlignment(Qt.AlignCenter)
        self.new_month_text.setFont(QFont("Times New Roman", 20))
        self.new_month_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid black; border-radius: 14px")
        self.new_month_text.textEdited.connect(lambda: self.is_empty(self.new_month_text))

        # -- element 3 --
        self.new_year_text = QLineEdit(self)
        self.new_year_text.setPlaceholderText("YYYY")
        self.new_year_text.setFixedHeight(60)
        self.new_year_text.setFixedWidth(296)
        self.new_year_text.setAlignment(Qt.AlignCenter)
        self.new_year_text.setFont(QFont("Times New Roman", 20))
        self.new_year_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid black; border-radius: 14px")
        self.new_year_text.textEdited.connect(lambda: self.is_empty(self.new_year_text))

        #Center column - Row 4 - Height
            
            #elements left to right

        # -- element 1 --
        self.new_foot_height_text = QLineEdit(self)
        self.new_foot_height_text.setPlaceholderText("Height (Feet)")
        self.new_foot_height_text.setFixedHeight(60)
        self.new_foot_height_text.setFixedWidth(297)
        self.new_foot_height_text.setAlignment(Qt.AlignCenter)
        self.new_foot_height_text.setFont(QFont("Times New Roman", 20))
        self.new_foot_height_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid black; border-radius: 14px")
        self.new_foot_height_text.textEdited.connect(lambda: self.is_empty(self.new_foot_height_text))

        # -- element 2 --
        self.new_inch_height_text = QLineEdit(self)
        self.new_inch_height_text.setPlaceholderText("Height (Inches)")
        self.new_inch_height_text.setFixedHeight(60)
        self.new_inch_height_text.setFixedWidth(297)
        self.new_inch_height_text.setAlignment(Qt.AlignCenter)
        self.new_inch_height_text.setFont(QFont("Times New Roman", 20))
        self.new_inch_height_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid black; border-radius: 14px")
        self.new_inch_height_text.textEdited.connect(lambda: self.is_empty(self.new_inch_height_text))

        #Center column - Row 5
            
            #elements left to right

        # -- element 1 --
        self.new_weight_text = QLineEdit(self)
        self.new_weight_text.setPlaceholderText("Weight")
        self.new_weight_text.setFixedHeight(60)
        self.new_weight_text.setFixedWidth(297)
        self.new_weight_text.setAlignment(Qt.AlignCenter)
        self.new_weight_text.setFont(QFont("Times New Roman", 20))
        self.new_weight_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid black; border-radius: 14px")
        self.new_weight_text.textEdited.connect(lambda: self.is_empty(self.new_weight_text))

        # -- element 2 --
        self.new_weight_combo = QComboBox(self)
        self.new_weight_combo.setFixedHeight(60)
        self.new_weight_combo.setFixedWidth(297)
        self.new_weight_combo.setFont(QFont("Times New Roman", 20))
        self.new_weight_combo.setStyleSheet("""
                                QComboBox {
                                    color: #645e59; background-color: #171514; border: 2px solid black; 
                                    border-radius: 14px; padding-left: 64px;
                                }
                                
                                QComboBox::drop-down {
                                    border-top-right-radius: 4px; border-top-right-radius: 4px;
                                }""")

        self.new_weight_combo.addItems([
                                "▼    KG's    ▼", 
                                "▼    LB's    ▼"
                                ])
        self.new_weight_combo.setCurrentIndex(0)

        #Center column - Row 6
        self.new_activity_combo = QComboBox(self)
        self.new_activity_combo.setFixedHeight(60)
        self.new_activity_combo.setFixedWidth(600)
        self.new_activity_combo.setFont(QFont("Times New Roman", 20))
        self.new_activity_combo.setStyleSheet("""
                                QComboBox {
                                    color: #645e59; background-color: #171514; border: 2px solid black; 
                                    border-radius: 14px; padding-left: 10 px;
                                }
                                
                                QComboBox::drop-down {
                                    border-top-right-radius: 4px; border-top-right-radius: 4px;
                                }
                            """)

        self.new_activity_combo.addItems([
                                "▼    Sedentary: little or no exercise", 
                                "▼    Light: exercise 1-3 times/week", 
                                "▼    Moderate: exercise 4-5 times/week", 
                                "▼    Active: intense exercise 3-4 times/week",
                                "▼    Very Active: intense exercise 6-7 times/week",
                                "▼    Extra Active: very intense daily exercise"
                                ])
        self.new_activity_combo.setCurrentIndex(2)

        #Right column
        new_save_button = QPushButton("Save", self)
        new_save_button.setFixedHeight(60)
        new_save_button.setFixedWidth(280)
        new_save_button.setFont(QFont("Times New Roman", 20))
        new_save_button.setStyleSheet("""
                                QPushButton {
                                    color: #645e59; background-color: #171514; border: 2px solid black; 
                                    border-radius: 14px; margin-left: 130px; text-align: center;
                                }

                                QPushButton:Hover {
                                    background-color: #1d1a19;
                                }
                                QPushButton:pressed {
                                    background-color: #1d1a19;
                                        }
                                QPushButton:focus {
                                    border: 2px solid black; outline: none; 
                                }
                            """)
        
        new_save_button.clicked.connect(self.save_profile)

        #Create profile widget containing form for first profile
        self.new_profile_widget = QWidget()

        new_profile_col1_widget = QWidget()
        new_profile_col1_widget.setStyleSheet("background-color: #24201f")

        new_profile_col2_widget = QWidget()
        new_profile_col2_widget.setFixedWidth(600)
        new_profile_col2_widget.setStyleSheet("background-color: #24201f")

        new_profile_col2_layout = QVBoxLayout()
        new_profile_col2_layout.setContentsMargins(0, 0, 0, 0)
        new_profile_col2_layout.setSpacing(20)

        new_profile_col2_row3_widget = QWidget()
        new_profile_col2_row3_widget.setFixedHeight(60)

        new_profile_col2_row3_layout = QHBoxLayout()
        new_profile_col2_row3_layout.setContentsMargins(0, 0, 0, 0)
        new_profile_col2_row3_layout.setSpacing(6)

        new_profile_col2_row3_layout.addWidget(self.new_day_text)
        new_profile_col2_row3_layout.addWidget(self.new_month_text)
        new_profile_col2_row3_layout.addWidget(self.new_year_text)

        new_profile_col2_row3_widget.setLayout(new_profile_col2_row3_layout)

        new_profile_col2_row4_widget = QWidget()
        new_profile_col2_row4_widget.setFixedHeight(60)

        new_profile_col2_row4_layout = QHBoxLayout()
        new_profile_col2_row4_layout.setContentsMargins(0, 0, 0, 0)
        new_profile_col2_row4_layout.setSpacing(6)

        new_profile_col2_row4_layout.addWidget(self.new_foot_height_text)
        new_profile_col2_row4_layout.addWidget(self.new_inch_height_text)

        new_profile_col2_row4_widget.setLayout(new_profile_col2_row4_layout)

        new_profile_col2_row5_widget = QWidget()
        new_profile_col2_row5_widget.setFixedHeight(60)

        new_profile_col2_row5_layout = QHBoxLayout()
        new_profile_col2_row5_layout.setContentsMargins(0, 0, 0, 0)
        new_profile_col2_row5_layout.setSpacing(6)

        new_profile_col2_row5_layout.addWidget(self.new_weight_text)
        new_profile_col2_row5_layout.addWidget(self.new_weight_combo)

        new_profile_col2_row5_widget.setLayout(new_profile_col2_row5_layout)


        new_profile_col2_layout.addStretch()
        new_profile_col2_layout.addSpacing(120)
        new_profile_col2_layout.addWidget(self.new_profile_picture, alignment=Qt.AlignHCenter)
        new_profile_col2_layout.addSpacing(140)
        new_profile_col2_layout.addWidget(self.new_name_text)
        new_profile_col2_layout.addWidget(new_profile_col2_row3_widget)
        new_profile_col2_layout.addWidget(new_profile_col2_row4_widget)
        new_profile_col2_layout.addWidget(new_profile_col2_row5_widget)
        new_profile_col2_layout.addWidget(self.new_activity_combo)
        new_profile_col2_layout.addSpacing(140)
        

        new_profile_col2_widget.setLayout(new_profile_col2_layout)

        new_profile_col3_widget = QWidget()
        new_profile_col3_widget.setStyleSheet("background-color: #24201f")

        new_profile_col3_layout = QVBoxLayout()
        new_profile_col3_layout.setContentsMargins(0, 0, 0, 0)
        new_profile_col3_layout.setSpacing(20)

        new_profile_col3_layout.addStretch()
        new_profile_col3_layout.addSpacing(20)
        new_profile_col3_layout.addWidget(new_save_button)
        new_profile_col3_layout.addSpacing(140)

        new_profile_col3_widget.setLayout(new_profile_col3_layout)

        new_profile_layout = QHBoxLayout()
        new_profile_layout.setContentsMargins(0, 0, 0, 0)
        new_profile_layout.setSpacing(0)

        new_profile_layout.addWidget(new_profile_col1_widget)
        new_profile_layout.addWidget(new_profile_col2_widget)
        new_profile_layout.addWidget(new_profile_col3_widget)

        self.new_profile_widget.setLayout(new_profile_layout)

        self.central_layout.insertWidget(1, self.new_profile_widget)

        self.current_widget = "New Profile"




    def save_profile(self):

        #Check to see if the profile name exists
        name = self.new_name_text.text()
        for profiles in self.local_profiles:
            for value in profiles.values():
                if value == self.new_name_text.text():
                    self.can_save_profile = False
                    self.new_name_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid #c32157; border-radius: 14px")
                    self.new_name_text.setText("")
                    self.new_name_text.setPlaceholderText("Name already taken")
                
        #Confirm that the day/month/year is valid
        try:
            day = int(self.new_day_text.text())

            if day < 1 or day > 31:
                self.can_save_profile = False
                self.new_day_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid #c32157; border-radius: 14px")
                self.new_day_text.setText("")
                self.new_day_text.setPlaceholderText("(1-31)")

        except ValueError:
            self.can_save_profile = False
            self.new_day_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid #c32157; border-radius: 14px")
            self.new_day_text.setText("")
            self.new_day_text.setPlaceholderText("(1-31)")

        try:
            month = int(self.new_month_text.text())

            if month < 1 or month > 12:
                self.can_save_profile = False
                self.new_month_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid #c32157; border-radius: 14px")
                self.new_month_text.setText("")
                self.new_month_text.setPlaceholderText("(1-12)")

        except ValueError:
            self.can_save_profile = False
            self.new_month_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid #c32157; border-radius: 14px")
            self.new_month_text.setText("")
            self.new_month_text.setPlaceholderText("(1-12)")

        try:
            year = int(self.new_year_text.text())

            if year < 1900 or year > 2025:
                self.can_save_profile = False
                self.new_year_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid #c32157; border-radius: 14px")
                self.new_year_text.setText("")
                self.new_year_text.setPlaceholderText("(1900-2025)")

        except ValueError:
            self.can_save_profile = False
            self.new_year_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid #c32157; border-radius: 14px")
            self.new_year_text.setText("")
            self.new_year_text.setPlaceholderText("(1900-2025)")


        #Confirm that the height Ft/In is valid
        try:
            ft = int(self.new_foot_height_text.text())

            if ft < 0 or ft > 9:
                self.can_save_profile = False
                self.new_foot_height_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid #c32157; border-radius: 14px")
                self.new_foot_height_text.setText("")
                self.new_foot_height_text.setPlaceholderText("(0-9)")

        except ValueError:
            self.can_save_profile = False
            self.new_foot_height_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid #c32157; border-radius: 14px")
            self.new_foot_height_text.setText("")
            self.new_foot_height_text.setPlaceholderText("(0-9)")

        try:
            inch = int(self.new_inch_height_text.text())

            if inch < 0 or inch > 11:
                self.can_save_profile = False
                self.new_inch_height_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid #c32157; border-radius: 14px")
                self.new_inch_height_text.setText("")
                self.new_inch_height_text.setPlaceholderText("(0-11)")

        except ValueError:
            self.can_save_profile = False
            self.new_inch_height_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid #c32157; border-radius: 14px")
            self.new_inch_height_text.setText("")
            self.new_inch_height_text.setPlaceholderText("(0-11)")

        #Confirm that the height weight is valid
        try:
            weight_number = float(self.new_weight_text.text())

            if weight_number < 1 or weight_number > 2000:
                self.can_save_profile = False
                self.new_weight_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid #c32157; border-radius: 14px")
                self.new_weight_text.setText("")
                self.new_weight_text.setPlaceholderText("(1-2000)")

            weight_number = float(f"{weight_number:.1f}")

        except ValueError:
            self.can_save_profile = False
            self.new_weight_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid #c32157; border-radius: 14px")
            self.new_weight_text.setText("")
            self.new_weight_text.setPlaceholderText("(1-2000)")

        measurement = self.new_weight_combo.currentIndex()

        #Activity - does not require validation checking
        activity = self.new_activity_combo.currentIndex()

        if self.can_save_profile == True:

            profile_update = {
                "name": name,
                "dob": {
                    "day": day,
                    "month": month,
                    "year": year
                }, 
                "height": {
                    "ft": ft,
                    "inch": inch
                }, 
                "weight": {
                    "unit": weight_number,
                    "kg/lb": measurement
                }, 
                "activity": activity
            }

            self.local_profiles.append(profile_update)

            with open('./src/data.json', 'w') as f:
                json.dump(self.data, f, indent=4)

            self.tabs_widget.show()

            self.tab_switcher("Profiles")




    def profiles(self):

        #Profiles - elements
        self.profile_picture = QLabel("munchy", self)
        self.profile_picture.setFixedHeight(412)
        self.profile_picture.setFixedWidth(412)
        self.profile_picture.setAlignment(Qt.AlignCenter)
        self.profile_picture.setFont(QFont("Times New Roman", 20))
        self.profile_picture.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid black; border-radius: 14px")

        self.next_profile_button = QPushButton("→", self)
        self.next_profile_button.setFixedHeight(88)
        self.next_profile_button.setFixedWidth(190)
        self.next_profile_button.setFont(QFont("Times New Roman", 60))
        self.next_profile_button.setStyleSheet("""
                                QPushButton {
                                    color: #645e59; background-color: #171514; border: 2px solid black; 
                                    border-radius: 14px; padding-bottom: 22px; text-align: center;
                                }

                                QPushButton:Hover {
                                    background-color: #1d1a19;
                                }
                                QPushButton:pressed {
                                    background-color: #1d1a19;
                                        }
                                QPushButton:focus {
                                    border: 2px solid black; outline: none; 
                                }
                            """)

        self.add_profile_button = QPushButton("+ Profile", self)
        self.add_profile_button.setFixedHeight(88)
        self.add_profile_button.setFixedWidth(190)
        self.add_profile_button.setFont(QFont("Times New Roman", 20))
        self.add_profile_button.setStyleSheet("""
                                QPushButton {
                                    color: #645e59; background-color: #171514; border: 2px solid black; 
                                    border-radius: 14px; text-align: center;
                                }

                                QPushButton:Hover {
                                    background-color: #1d1a19;
                                }
                                QPushButton:pressed {
                                    background-color: #1d1a19;
                                        }
                                QPushButton:focus {
                                    border: 2px solid black; outline: none; 
                                }
                            """)
        self.add_profile_button.clicked.connect(lambda: self.tab_switcher("New Profile"))
        
        name = f"Name:    {self.local_profiles[0]['name']}"
        self.name_label = QLabel(name, self)
        self.name_label.setFixedHeight(88)
        self.name_label.setFixedWidth(856)
        self.name_label.setAlignment(Qt.AlignCenter)
        self.name_label.setFont(QFont("Times New Roman", 20))
        self.name_label.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid black; border-radius: 14px")

        age = f"Date of Birth:    {self.local_profiles[0]['dob']['day']} - {self.local_profiles[0]['dob']['month']} - {self.local_profiles[0]['dob']['year']}"
        self.age_label = QLabel(age, self)
        self.age_label.setFixedHeight(88)
        self.age_label.setFixedWidth(856)
        self.age_label.setAlignment(Qt.AlignCenter)
        self.age_label.setFont(QFont("Times New Roman", 20))
        self.age_label.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid black; border-radius: 14px")

        height = f'Height:    {self.local_profiles[0]['height']['ft']} ft {self.local_profiles[0]['height']['inch']} "'
        self.height_label = QLabel(height, self)
        self.height_label.setFixedHeight(88)
        self.height_label.setFixedWidth(856)
        self.height_label.setAlignment(Qt.AlignCenter)
        self.height_label.setFont(QFont("Times New Roman", 20))
        self.height_label.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid black; border-radius: 14px")

        weight = ""
        match self.local_profiles[0]['weight']['kg/lb']:
            case 0:
                weight = f"Weight:    {self.local_profiles[0]['weight']['unit']} kg's"
            case 1:
                weight = f"Weight:    {self.local_profiles[0]['weight']['unit']} lb's"
        
        self.weight_label = QLabel(weight, self)
        self.weight_label.setFixedHeight(88)
        self.weight_label.setFixedWidth(856)
        self.weight_label.setAlignment(Qt.AlignCenter)
        self.weight_label.setFont(QFont("Times New Roman", 20))
        self.weight_label.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid black; border-radius: 14px")

        activity = ""
        match self.local_profiles[0]['activity']:
            case 0:
                activity = "Activity:    Sedentary - little or no exercise"
            case 1:
                activity = "Activity:    Light - exercise 1-3 times/week"
            case 2:
                activity = "Activity:    Moderate - exercise 4-5 times/week"
            case 3:
                activity = "Activity:    Active - intense exercise 3-4 times/week"
            case 4:
                activity = "Activity:    Very Active - intense exercise 6-7 times/week"
            case 5:
                activity = "Activity:    Extra Active - very intense daily exercise"

        self.activity_label = QLabel(activity, self)
        self.activity_label.setFixedHeight(88)
        self.activity_label.setFixedWidth(856)
        self.activity_label.setAlignment(Qt.AlignCenter)
        self.activity_label.setFont(QFont("Times New Roman", 20))
        self.activity_label.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid black; border-radius: 14px")

        #Men: (10 x weight in kg) + (6.25 x height in cm) - (5 x age in years) + 5
        #Women: (10 x weight in kg) + (6.25 x height in cm) - (5 x age in years) - 161 

        #kg's = lb's / 2.205

        # ((feet * 6) + inches) * 2.54 = cm's

        self.gain_label = QLabel("munchy", self)
        self.gain_label.setFixedHeight(90)
        self.gain_label.setFixedWidth(645)
        self.gain_label.setAlignment(Qt.AlignCenter)
        self.gain_label.setFont(QFont("Times New Roman", 20))
        self.gain_label.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid black; border-radius: 14px")

        self.maintain_label = QLabel("munchy", self)
        self.maintain_label.setFixedHeight(90)
        self.maintain_label.setFixedWidth(645)
        self.maintain_label.setAlignment(Qt.AlignCenter)
        self.maintain_label.setFont(QFont("Times New Roman", 20))
        self.maintain_label.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid black; border-radius: 14px")
        
        self.loss_label = QLabel("munchy", self)
        self.loss_label.setFixedHeight(90)
        self.loss_label.setFixedWidth(645)
        self.loss_label.setAlignment(Qt.AlignCenter)
        self.loss_label.setFont(QFont("Times New Roman", 20))
        self.loss_label.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid black; border-radius: 14px")
        
        self.extreme_loss_label = QLabel("munchy", self)
        self.extreme_loss_label.setFixedHeight(90)
        self.extreme_loss_label.setFixedWidth(645)
        self.extreme_loss_label.setAlignment(Qt.AlignCenter)
        self.extreme_loss_label.setFont(QFont("Times New Roman", 20))
        self.extreme_loss_label.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid black; border-radius: 14px")

        #Main widget of the profiles tab page
        self.profiles_widget = QWidget()

        #Main layout split into two row sections
        profiles_layout = QVBoxLayout()
        profiles_layout.setContentsMargins(0, 0, 0, 0)
        profiles_layout.setSpacing(0)

        profiles_row1_widget = QWidget()

        profiles_row1_layout = QHBoxLayout()
        profiles_row1_layout.setContentsMargins(0, 0, 0, 0)
        profiles_row1_layout.setSpacing(40)

        profiles_row1_col1_widget = QWidget()

        profiles_row1_col1_layout = QVBoxLayout()
        profiles_row1_col1_layout.setContentsMargins(0, 0, 0, 0)
        profiles_row1_col1_layout.setSpacing(40)

        profiles_row1_col1_layout.addWidget(self.profile_picture)

        profiles_row1_col1_buttons_widget = QWidget()

        profiles_row1_col1_buttons_layout = QHBoxLayout()
        profiles_row1_col1_buttons_layout.setContentsMargins(0, 0, 0, 0)
        profiles_row1_col1_buttons_layout.setSpacing(0)

        profiles_row1_col1_buttons_layout.addWidget(self.next_profile_button)
        profiles_row1_col1_buttons_layout.addStretch()
        profiles_row1_col1_buttons_layout.addWidget(self.add_profile_button)

        profiles_row1_col1_buttons_widget.setLayout(profiles_row1_col1_buttons_layout)

        profiles_row1_col1_layout.addWidget(profiles_row1_col1_buttons_widget) 

        profiles_row1_col1_widget.setLayout(profiles_row1_col1_layout)

        profiles_row1_col2_widget = QWidget(self)

        profiles_row1_col2_layout = QVBoxLayout()
        profiles_row1_col2_layout.setContentsMargins(0, 0, 0, 0)
        profiles_row1_col2_layout.setSpacing(25)

        profiles_row1_col2_layout.addWidget(self.name_label)
        profiles_row1_col2_layout.addWidget(self.age_label)
        profiles_row1_col2_layout.addWidget(self.height_label)
        profiles_row1_col2_layout.addWidget(self.weight_label)
        profiles_row1_col2_layout.addWidget(self.activity_label)

        profiles_row1_col2_widget.setLayout(profiles_row1_col2_layout)

        profiles_row1_layout.addStretch()
        profiles_row1_layout.addWidget(profiles_row1_col1_widget)
        profiles_row1_layout.addWidget(profiles_row1_col2_widget)
        profiles_row1_layout.addStretch()

        profiles_row1_widget.setLayout(profiles_row1_layout)

        profiles_row2_widget = QWidget()
        
        profiles_row2_layout = QHBoxLayout()
        profiles_row2_layout.setContentsMargins(0, 0, 0, 0)
        profiles_row2_layout.setSpacing(20)

        profiles_row2_col1_widget = QWidget()

        profiles_row2_col1_layout = QVBoxLayout()
        profiles_row2_col1_layout.setContentsMargins(0, 0, 0, 0)
        profiles_row2_col1_layout.setSpacing(20)

        profiles_row2_col1_layout.addStretch()
        profiles_row2_col1_layout.addWidget(self.maintain_label)
        profiles_row2_col1_layout.addWidget(self.gain_label)
        profiles_row2_col1_layout.addStretch()

        profiles_row2_col1_widget.setLayout(profiles_row2_col1_layout)

        profiles_row2_col2_widget = QWidget()

        profiles_row2_col2_layout = QVBoxLayout()
        profiles_row2_col2_layout.setContentsMargins(0, 0, 0, 0)
        profiles_row2_col2_layout.setSpacing(20)

        profiles_row2_col2_layout.addStretch()
        profiles_row2_col2_layout.addWidget(self.loss_label)
        profiles_row2_col2_layout.addWidget(self.extreme_loss_label)
        profiles_row2_col2_layout.addStretch()

        profiles_row2_col2_widget.setLayout(profiles_row2_col2_layout)

        profiles_row2_layout.addStretch()
        profiles_row2_layout.addWidget(profiles_row2_col1_widget)
        profiles_row2_layout.addWidget(profiles_row2_col2_widget)
        profiles_row2_layout.addStretch()

        profiles_row2_widget.setLayout(profiles_row2_layout)

        profiles_layout.addStretch()
        profiles_layout.addWidget(profiles_row1_widget)
        profiles_layout.addSpacing(60)
        profiles_layout.addWidget(profiles_row2_widget)
        profiles_layout.addStretch()

        self.profiles_widget.setLayout(profiles_layout)

        self.central_layout.insertWidget(1, self.profiles_widget)

        self.current_widget = "Profiles"




    def consumables(self):

        self.new_consumable_text = QLineEdit(self)
        self.new_consumable_text.setPlaceholderText("Consumable")
        self.new_consumable_text.setFixedHeight(60)
        self.new_consumable_text.setFixedWidth(400)
        self.new_consumable_text.setAlignment(Qt.AlignCenter)
        self.new_consumable_text.setFont(QFont("Times New Roman", 20))
        self.new_consumable_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid black; border-radius: 14px")

        add_consumable_button = QPushButton("Add", self)
        add_consumable_button.setFixedHeight(60)
        add_consumable_button.setFixedWidth(160)
        add_consumable_button.setFont(QFont("Times New Roman", 20))
        add_consumable_button.setStyleSheet("""
                                QPushButton {
                                    color: #645e59; background-color: #171514; border: 2px solid black; 
                                    border-radius: 14px; text-align: center;
                                }

                                QPushButton:Hover {
                                    background-color: #1d1a19;
                                }
                                QPushButton:pressed {
                                    background-color: #1d1a19;
                                        }
                                QPushButton:focus {
                                    border: 2px solid black; outline: none; 
                                }
                            """)

        add_consumable_button.clicked.connect(lambda: self.add_consumable(self.new_consumable_text.text()))
        
        consumables_scroll = QScrollArea()
        consumables_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        consumables_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        self.consumables_widget = QWidget()
        self.consumables_widget.setFixedHeight(944)
        self.consumables_widget.setFixedWidth(1400)

        consumables_layout = QVBoxLayout()
        consumables_layout.setContentsMargins(0, 0, 0, 0)
        consumables_layout.setSpacing(0)

        consumables_row1_widget = QWidget()
        consumables_row1_widget.setFixedHeight(60)

        consumables_row1_layout = QHBoxLayout()
        consumables_row1_layout.setContentsMargins(0, 0, 0, 0)
        consumables_row1_layout.setSpacing(40)

        consumables_row1_layout.addStretch()
        consumables_row1_layout.addWidget(self.new_consumable_text)
        consumables_row1_layout.addWidget(add_consumable_button)
        consumables_row1_layout.addStretch()

        consumables_row1_widget.setLayout(consumables_row1_layout)

        row1_row2_spacer = QWidget()
        row1_row2_spacer.setStyleSheet("background-color: #171514")
        row1_row2_spacer.setFixedHeight(2)
        

        consumables_row2_widget = QWidget()

        consumables_row2_layout = QGridLayout()
        consumables_row2_layout.setContentsMargins(60, 20, 60, 20)
        consumables_row2_layout.setSpacing(40)
        
        

        x = 0
        y = 0

        for key in self.local_consumables.keys():

            button = key
            button = QPushButton(key, self)
            button.setFixedHeight(80)
            button.setFixedWidth(400)
            button.setFont(QFont("Times New Roman", 20))
            button.setStyleSheet("""
                                QPushButton {
                                    color: #645e59; background-color: #171514; border: 2px solid black; 
                                    border-radius: 14px; text-align: center;
                                }

                                QPushButton:Hover {
                                    background-color: #1d1a19;
                                }
                                QPushButton:pressed {
                                    background-color: #1d1a19;
                                        }
                                QPushButton:focus {
                                    border: 2px solid black; outline: none; 
                                }
                            """)           

            button.clicked.connect(partial(self.consumable_variants, key)) 

            consumables_row2_layout.addWidget(button, x, y)

            if y < 2:
                y += 1
            
            else:
                y = 0
                x += 1

        consumables_row2_widget.setLayout(consumables_row2_layout)

        consumables_scroll.setWidget(consumables_row2_widget)

        consumables_layout.addSpacing(40)
        consumables_layout.addWidget(consumables_row1_widget)
        consumables_layout.addSpacing(40)
        consumables_layout.addWidget(row1_row2_spacer)
        consumables_layout.addWidget(consumables_scroll)

        self.consumables_widget.setLayout(consumables_layout)

        self.central_layout.insertWidget(1, self.consumables_widget)

        self.current_widget = "Consumables"




    def add_consumable(self, name):

        if not name:
            self.new_consumable_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid #c32157; border-radius: 14px")
            self.new_consumable_text.setText("")
            self.new_consumable_text.setPlaceholderText("No consumable detected")
            return

        if name in self.local_consumables:
            self.new_consumable_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid #c32157; border-radius: 14px")
            self.new_consumable_text.setText("")
            self.new_consumable_text.setPlaceholderText("Consumable already added")
            return

        self.local_consumables[name] = {}

        with open('./src/data.json', 'w') as f:
                json.dump(self.data, f, indent=4)

        self.tab_switcher("Consumables")




    def consumable_variants(self, consumable):
        
        #Row 1 - element 1
        self.consumable_button = QPushButton(consumable , self)
        self.consumable_button.setFixedHeight(60)
        self.consumable_button.setFixedWidth(400)
        self.consumable_button.setFont(QFont("Times New Roman", 20)) 
        self.consumable_button.setStyleSheet("""
                                QPushButton {
                                    color: #645e59; background-color: #171514; border: 2px solid black; 
                                    border-radius: 14px; text-align: center;
                                }

                                QPushButton:Hover {
                                    background-color: #1d1a19;
                                }
                                QPushButton:pressed {
                                    background-color: #1d1a19;
                                        }
                                QPushButton:focus {
                                    border: 2px solid black; outline: none; 
                                }
                            """)

        #Row 1 - element 2
        self.consumable_edit_button = QPushButton("Edit" , self)
        self.consumable_edit_button.setFixedHeight(60)
        self.consumable_edit_button.setFixedWidth(160)
        self.consumable_edit_button.setFont(QFont("Times New Roman", 20)) 
        self.consumable_edit_button.setStyleSheet("""
                                QPushButton {
                                    color: #645e59; background-color: #171514; border: 2px solid black; 
                                    border-radius: 14px; text-align: center;
                                }

                                QPushButton:Hover {
                                    background-color: #1d1a19;
                                }
                                QPushButton:pressed {
                                    background-color: #1d1a19;
                                        }
                                QPushButton:focus {
                                    border: 2px solid black; outline: none; 
                                }
                            """)
        self.consumable_edit_button.clicked.connect(self.consumable_edit)    

        #Row 1 - element 1 - edit mode
        self.delete_consumable_button = QPushButton("Delete" , self)
        self.delete_consumable_button.setFixedHeight(60)
        self.delete_consumable_button.setFixedWidth(160)
        self.delete_consumable_button.setFont(QFont("Times New Roman", 20)) 
        self.delete_consumable_button.setStyleSheet("""
                                QPushButton {
                                    color: #645e59; background-color: #171514; border: 2px solid black; 
                                    border-radius: 14px; text-align: center;
                                }

                                QPushButton:Hover {
                                    background-color: #1d1a19;
                                }
                                QPushButton:pressed {
                                    background-color: #1d1a19;
                                        }
                                QPushButton:focus {
                                    border: 2px solid black; outline: none; 
                                }
                            """)
        self.delete_consumable_button.hide()

        #Row 1 - element 2 - edit mode
        self.consumable_text = QLineEdit(consumable, self)
        self.consumable_text.setFixedHeight(60)
        self.consumable_text.setFixedWidth(400)
        self.consumable_text.setAlignment(Qt.AlignCenter)
        self.consumable_text.setFont(QFont("Times New Roman", 20))
        self.consumable_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid black; border-radius: 14px")
        self.consumable_text.hide()

        #Row 1 - element 3 - edit mode
        self.cancel_consumable_edit_button = QPushButton("Cancel" , self)
        self.cancel_consumable_edit_button.setFixedHeight(60)
        self.cancel_consumable_edit_button.setFixedWidth(160)
        self.cancel_consumable_edit_button.setFont(QFont("Times New Roman", 20)) 
        self.cancel_consumable_edit_button.setStyleSheet("""
                                QPushButton {
                                    color: #645e59; background-color: #171514; border: 2px solid black; 
                                    border-radius: 14px; text-align: center;
                                }

                                QPushButton:Hover {
                                    background-color: #1d1a19;
                                }
                                QPushButton:pressed {
                                    background-color: #1d1a19;
                                        }
                                QPushButton:focus {
                                    border: 2px solid black; outline: none; 
                                }
                            """)
        self.cancel_consumable_edit_button.clicked.connect(self.cancel_consumable_edit)                    
        self.cancel_consumable_edit_button.hide()

        #Row 1 - element 4 - edit mode
        self.save_consumable_button = QPushButton("Save" , self)
        self.save_consumable_button.setFixedHeight(60)
        self.save_consumable_button.setFixedWidth(160)
        self.save_consumable_button.setFont(QFont("Times New Roman", 20)) 
        self.save_consumable_button.setStyleSheet("""
                                QPushButton {
                                    color: #645e59; background-color: #171514; border: 2px solid black; 
                                    border-radius: 14px; text-align: center;
                                }

                                QPushButton:Hover {
                                    background-color: #1d1a19;
                                }
                                QPushButton:pressed {
                                    background-color: #1d1a19;
                                        }
                                QPushButton:focus {
                                    border: 2px solid black; outline: none; 
                                }
                            """)

        self.save_consumable_button.clicked.connect(lambda: self.save_consumable_edit(consumable, self.consumable_text.text()))   
        self.save_consumable_button.hide()

        #Row 3 - element 1
        brand_text = QLineEdit(self)
        brand_text.setFixedHeight(60)
        brand_text.setFixedWidth(400)
        brand_text.setPlaceholderText("Brand e.g. (Coke)")
        brand_text.setAlignment(Qt.AlignCenter)
        brand_text.setFont(QFont("Times New Roman", 20))
        brand_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid black; border-radius: 14px")

        #Row 3 - element 2
        protein_text = QLineEdit(self)
        protein_text.setFixedHeight(60)
        protein_text.setFixedWidth(280)
        protein_text.setPlaceholderText("Protein")
        protein_text.setAlignment(Qt.AlignCenter)
        protein_text.setFont(QFont("Times New Roman", 20))
        protein_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid black; border-radius: 14px")

        #Row 3 - element 3
        carbs_text = QLineEdit(self)
        carbs_text.setFixedHeight(60)
        carbs_text.setFixedWidth(280)
        carbs_text.setPlaceholderText("Carbs")
        carbs_text.setAlignment(Qt.AlignCenter)
        carbs_text.setFont(QFont("Times New Roman", 20))
        carbs_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid black; border-radius: 14px")

        #Row 3 - element 4
        fat_text = QLineEdit(self)
        fat_text.setFixedHeight(60)
        fat_text.setFixedWidth(280)
        fat_text.setPlaceholderText("Fat")
        fat_text.setAlignment(Qt.AlignCenter)
        fat_text.setFont(QFont("Times New Roman", 20))
        fat_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid black; border-radius: 14px")

        #Row 4 - element 1
        variant_text = QLineEdit(self)
        variant_text.setFixedHeight(60)
        variant_text.setFixedWidth(400)
        variant_text.setPlaceholderText("Variant e.g. (Vanilla)")
        variant_text.setAlignment(Qt.AlignCenter)
        variant_text.setFont(QFont("Times New Roman", 20))
        variant_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid black; border-radius: 14px")

        #Row 4 - element 2
        servings_text = QLineEdit(self)
        servings_text.setFixedHeight(60)
        servings_text.setFixedWidth(280)
        servings_text.setPlaceholderText("Servings e.g. (12) for eggs")
        servings_text.setAlignment(Qt.AlignCenter)
        servings_text.setFont(QFont("Times New Roman", 20))
        servings_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid black; border-radius: 14px")

        #Row 4 - element 3
        price_text = QLineEdit(self)
        price_text.setFixedHeight(60)
        price_text.setFixedWidth(280)
        price_text.setPlaceholderText("Price e.g. (2.99)")
        price_text.setAlignment(Qt.AlignCenter)
        price_text.setFont(QFont("Times New Roman", 20))
        price_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid black; border-radius: 14px")

        #Row 4 - element 4
        save_variant_button = QPushButton("Save" , self)
        save_variant_button.setFixedHeight(60)
        save_variant_button.setFixedWidth(160)
        save_variant_button.setFont(QFont("Times New Roman", 20)) 
        save_variant_button.setStyleSheet("""
                                QPushButton {
                                    color: #645e59; background-color: #171514; border: 2px solid black; 
                                    border-radius: 14px; text-align: center;
                                }

                                QPushButton:Hover {
                                    background-color: #1d1a19;
                                }
                                QPushButton:pressed {
                                    background-color: #1d1a19;
                                        }
                                QPushButton:focus {
                                    border: 2px solid black; outline: none; 
                                }
                            """)        

        variants_scroll = QScrollArea()
        variants_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        variants_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        self.variants_widget = QWidget()
        self.variants_widget.setFixedHeight(944)
        self.variants_widget.setFixedWidth(1400)

        variants_layout = QVBoxLayout()
        variants_layout.setContentsMargins(0, 0, 0, 0)
        variants_layout.setSpacing(0)

        #Row 1 widget/layout
        variants_row1_widget = QWidget()
        variants_row1_widget.setFixedHeight(100)

        variants_row1_layout = QHBoxLayout()
        variants_row1_layout.setContentsMargins(0, 0, 0, 0)
        variants_row1_layout.setSpacing(40)
        
        variants_row1_layout.addStretch()
        variants_row1_layout.addWidget(self.consumable_button)
        variants_row1_layout.addWidget(self.consumable_edit_button)
        variants_row1_layout.addWidget(self.delete_consumable_button)
        variants_row1_layout.addWidget(self.consumable_text)
        variants_row1_layout.addWidget(self.cancel_consumable_edit_button)
        variants_row1_layout.addWidget(self.save_consumable_button)
        variants_row1_layout.addStretch()

        variants_row1_widget.setLayout(variants_row1_layout)

        spacer = QWidget()
        spacer.setStyleSheet("background-color: #171514")
        spacer.setFixedHeight(2)

        spacer2 = QWidget()
        spacer2.setStyleSheet("background-color: #171514")
        spacer2.setFixedHeight(2)

        variants_row2_widget = QWidget()

        variants_row2_layout = QGridLayout()
        variants_row2_layout.setContentsMargins(60, 20, 60, 20)
        variants_row2_layout.setSpacing(40)

        x = 0
        y = 0

        for variant in self.local_consumables[consumable]:

            button = variant

            button = QPushButton(variant, self)
            button.setFixedHeight(80)
            button.setFixedWidth(400)
            button.setFont(QFont("Times New Roman", 20))
            button.setStyleSheet("""
                                QPushButton {
                                    color: #645e59; background-color: #171514; border: 2px solid black; 
                                    border-radius: 14px; text-align: center;
                                }

                                QPushButton:Hover {
                                    background-color: #1d1a19;
                                }
                                QPushButton:pressed {
                                    background-color: #1d1a19;
                                        }
                                QPushButton:focus {
                                    border: 2px solid black; outline: none; 
                                }
                            """)            

            variants_row2_layout.addWidget(button, x, y)

            if y < 2:
                y += 1
            
            else:
                y = 0
                x += 1

        variants_row2_widget.setLayout(variants_row2_layout)

        variants_scroll.setWidget(variants_row2_widget)

        #Row 3 widget/layout
        variants_row3_widget = QWidget()
        variants_row3_widget.setFixedHeight(100)

        variants_row3_layout = QHBoxLayout()
        variants_row3_layout.setContentsMargins(0, 0, 0, 0)
        variants_row3_layout.setSpacing(40)

        variants_row3_layout.addSpacing(20)
        variants_row3_layout.addWidget(brand_text)
        variants_row3_layout.addWidget(protein_text)
        variants_row3_layout.addWidget(carbs_text)
        variants_row3_layout.addWidget(fat_text)
        variants_row3_layout.addSpacing(20)

        variants_row3_widget.setLayout(variants_row3_layout)


        #Row 4 widget/layout
        variants_row4_widget = QWidget()
        variants_row4_widget.setFixedHeight(100)

        variants_row4_layout = QHBoxLayout()
        variants_row4_layout.setContentsMargins(0, 0, 0, 0)
        variants_row4_layout.setSpacing(40)

        variants_row4_layout.addSpacing(20)
        variants_row4_layout.addWidget(variant_text)
        variants_row4_layout.addWidget(servings_text)
        variants_row4_layout.addWidget(price_text)
        variants_row4_layout.addSpacing(60)
        variants_row4_layout.addWidget(save_variant_button)
        variants_row4_layout.addSpacing(60)
        variants_row4_layout.addSpacing(20)

        variants_row4_widget.setLayout(variants_row4_layout)

        #Set variants layout
        variants_layout.addWidget(variants_row1_widget)
        variants_layout.addWidget(spacer)
        variants_layout.addWidget(variants_scroll)
        variants_layout.addWidget(spacer2)
        variants_layout.addWidget(variants_row3_widget)
        variants_layout.addWidget(variants_row4_widget)

        self.variants_widget.setLayout(variants_layout)

        self.central_layout.insertWidget(1, self.variants_widget)

        self.current_widget = "Variants"
        



    def consumable_edit(self):
        self.consumable_button.hide()
        self.consumable_edit_button.hide()
        self.delete_consumable_button.show()
        self.consumable_text.show()
        self.cancel_consumable_edit_button.show()
        self.save_consumable_button.show()

    def cancel_consumable_edit(self):
        self.consumable_button.show()
        self.consumable_edit_button.show()
        self.delete_consumable_button.hide()
        self.consumable_text.hide()
        self.cancel_consumable_edit_button.hide()
        self.save_consumable_button.hide()

    def save_consumable_edit(self, current, new):
        if new:
            self.local_consumables[new] = self.local_consumables.pop(current)

            with open('./src/data.json', 'w') as f:
                json.dump(self.data, f, indent=4)

            self.consumable_button.setText(new)

            self.cancel_consumable_edit()

    def recipes(self):
        pass




    def pantry(self):
        pass




    def planner(self):
        pass




    def shopping(self):
        pass




    def delete_profile(self, name):
        #TODO - Logic for deleting a profile
        if not self.local_profiles['name'].default:
            #Delete if not the default profile
            pass
        else:
            if self.local_profiles['name'].additional:
                #Choose a new default profile
                pass
            else:
                #Delete profile
                pass





    def tab_switcher(self, new_widget):

        match self.current_widget:
            case "New Profile":
                self.central_layout.removeWidget(self.new_profile_widget)
                self.new_profile_widget.setParent(None)
                self.new_profile_widget.deleteLater()
            case "Profiles":
                self.central_layout.removeWidget(self.profiles_widget)
                self.profiles_widget.setParent(None)
                self.profiles_widget.deleteLater()
            case "Consumables":
                self.central_layout.removeWidget(self.consumables_widget)
                self.consumables_widget.setParent(None)
                self.consumables_widget.deleteLater()
            case "Variants":
                self.central_layout.removeWidget(self.variants_widget)
                self.variants_widget.setParent(None)
                self.variants_widget.deleteLater()

        match new_widget:
            case "New Profile":
                self.new_profile()
            case "Profiles":
                self.profiles()
            case "Consumables":
                self.consumables()
            case "Variants":
                self.consumable_variants()

        
    
    def create_consumable(self):
        #TODO - Reset grid to show only new consumable
        #Allow user to type in a name for the new consumable and confirm
        createProduct() # pass in consumable
        pass

    def delete_consumable(self):
        #TODO - delete the consumable container
        pass

    def add_product(self, consumable):
        #TODO - Show the consumable (parent of this product)
        #Allow user to create a product with required details
            #Brand/Variant
            #Quantity
            #Carbs
            #Protein
            #Fat
            #Average cost
        pass

    def remove_product(self):
        #TODO - Delete product from consumable (parent of this product)
        pass

    def create_recipe(self, ingredient):
        #TODO - Creates a Recipe container
        add_ingredient() # pass in ingredient
        pass

    def delete_recipe(self):
        #TODO - Deletes the selected Recipe container
        pass

    def add_ingredient(self):
        #TODO - Add a product from the stored consumables to recipe
        #Choose quantity of that product
        pass

    def remove_ingredient(self):
        #TODO - Remove product from recipe
        pass

    def select_calendar_day(self):
        #TODO - handle logic for clicking into and out of day on calender
        pass

    def item_min_increase(self):
        #TODO - Increase the storage amount of a consumable by it's minimum logical quantity amount
        pass

    def item_max_increase(self):
        #TODO - Increase the storage amount of a consumable by it's whole quantity amount
        pass

    def item_min_decrease(self):
        #TODO - Decrease the storage amount of a consumable by it's minimum logical quantity amount
        pass

    def item_max_decrease(self):
        #TODO - Decrease the storage amount of a consumable by it's whole quantity amount
        pass


    def generate_shopping_list(self):
        #TODO - Read a form filled in by user on click, then generate the shopping list
        pass

    #Check if the current text field is empty and show error color on border - only after typing and removing input
    def is_empty(self, text):
        if not text.text():
            self.can_save_profile = False
            text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid #c32157; border-radius: 14px")
        else:
            self.can_save_profile = True
            text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid #000000; border-radius: 14px")

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()