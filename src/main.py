import sys
import json
import datetime
import math
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QHBoxLayout, QVBoxLayout, QWidget, QScrollArea, QLabel, QLineEdit, QComboBox, QPushButton, QFileDialog
from PyQt5.QtGui import QFont, QPixmap
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
                                QPushButton:pressed {
                                    background-color: #171514;
                                        }
                                QPushButton:focus {
                                    border: 0px; outline: none; 
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

        self.tabs_widget.hide()

        #Center column - Row 1 - Profile picture
        self.new_profile_picture = QLabel(self)
        self.picture_URL = "./assets/profile picture/Profile.png"
        pixmap = QPixmap(self.picture_URL)
        self.new_profile_picture.setPixmap(pixmap)
        self.new_profile_picture.setScaledContents(True)
        self.new_profile_picture.setFixedHeight(260)
        self.new_profile_picture.setFixedWidth(260)
        self.new_profile_picture.setAlignment(Qt.AlignCenter)
        self.new_profile_picture.setFocusPolicy(Qt.StrongFocus)
        self.new_profile_picture.setStyleSheet("background-color: #171514; border: 2px solid black")

        add_new_picture_button = QPushButton("Upload", self)
        add_new_picture_button.setFixedHeight(60)
        add_new_picture_button.setFixedWidth(140)
        add_new_picture_button.setFont(QFont("Times New Roman", 20))
        add_new_picture_button.setStyleSheet("""
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
        
        add_new_picture_button.clicked.connect(lambda: self.update_profile_picture("New Profile"))

        #Center column - Row 2 - Name
        self.new_name_text = QLineEdit(self)
        self.new_name_text.setPlaceholderText("Name")
        self.new_name_text.setFixedHeight(60)
        self.new_name_text.setAlignment(Qt.AlignCenter)
        self.new_name_text.setFont(QFont("Times New Roman", 20))
        self.new_name_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid black; border-radius: 14px")

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

        # -- element 2 --
        self.new_month_text = QLineEdit(self)
        self.new_month_text.setPlaceholderText("MM")
        self.new_month_text.setFixedHeight(60)
        self.new_month_text.setFixedWidth(146)
        self.new_month_text.setAlignment(Qt.AlignCenter)
        self.new_month_text.setFont(QFont("Times New Roman", 20))
        self.new_month_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid black; border-radius: 14px")

        # -- element 3 --
        self.new_year_text = QLineEdit(self)
        self.new_year_text.setPlaceholderText("YYYY")
        self.new_year_text.setFixedHeight(60)
        self.new_year_text.setFixedWidth(296)
        self.new_year_text.setAlignment(Qt.AlignCenter)
        self.new_year_text.setFont(QFont("Times New Roman", 20))
        self.new_year_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid black; border-radius: 14px")

        #Center column - Row 4 - Gender
            
            #elements left to right

        # -- element 1 --
        self.gender_male_button = QPushButton("Male", self)
        self.gender_male_button.setFixedHeight(60)
        self.gender_male_button.setFixedWidth(297)
        self.gender_male_button.setFont(QFont("Times New Roman", 20))
        self.gender_male_button.setStyleSheet("""
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
        self.gender_male_button.clicked.connect(lambda: self.gender_state("Male"))
        
        #self.gender_male_button.clicked.connect()

        # -- element 2 --
        self.gender_female_button = QPushButton("Female", self)
        self.gender_female_button.setFixedHeight(60)
        self.gender_female_button.setFixedWidth(297)
        self.gender_female_button.setFont(QFont("Times New Roman", 20))
        self.gender_female_button.setStyleSheet("""
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
        self.gender_female_button.clicked.connect(lambda: self.gender_state("Female"))
        
        #self.gender_female_button.clicked.connect()

        #Center column - Row 5 - Height
        self.new_height_text = QLineEdit(self)
        self.new_height_text.setPlaceholderText("Height (cm's)")
        self.new_height_text.setFixedHeight(60)
        self.new_height_text.setFixedWidth(600)
        self.new_height_text.setAlignment(Qt.AlignCenter)
        self.new_height_text.setFont(QFont("Times New Roman", 20))
        self.new_height_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid black; border-radius: 14px")


        #Center column - Row 6
        self.new_weight_text = QLineEdit(self)
        self.new_weight_text.setPlaceholderText("Weight (kg's)")
        self.new_weight_text.setFixedHeight(60)
        self.new_weight_text.setFixedWidth(600)
        self.new_weight_text.setAlignment(Qt.AlignCenter)
        self.new_weight_text.setFont(QFont("Times New Roman", 20))
        self.new_weight_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid black; border-radius: 14px")

        #Center column - Row 7
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
                                "▼    Very Active: intense exercise 6-7 times/week",
                                "▼    Extra Active: very intense daily exercise"
                                ])
        self.new_activity_combo.setCurrentIndex(2)

        # -- Right column - Row 1 --

        #element 1
        self.cancel_new_save_button = QPushButton("Cancel", self)
        self.cancel_new_save_button.setFixedHeight(60)
        self.cancel_new_save_button.setFixedWidth(140)
        self.cancel_new_save_button.setFont(QFont("Times New Roman", 20))
        self.cancel_new_save_button.setStyleSheet("""
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
        self.cancel_new_save_button.clicked.connect(self.cancel_new_save)
        self.cancel_new_save_button.hide()

        if self.local_profiles:
            self.cancel_new_save_button.show()

        #element 2
        new_save_button = QPushButton("Save", self)
        new_save_button.setFixedHeight(60)
        new_save_button.setFixedWidth(140)
        new_save_button.setFont(QFont("Times New Roman", 20))
        new_save_button.setStyleSheet("""
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

        new_profile_col2_row4_layout.addWidget(self.gender_male_button)
        new_profile_col2_row4_layout.addWidget(self.gender_female_button)

        new_profile_col2_row4_widget.setLayout(new_profile_col2_row4_layout)

        new_profile_col2_layout.addStretch()
        new_profile_col2_layout.addSpacing(20)
        new_profile_col2_layout.addWidget(self.new_profile_picture, alignment=Qt.AlignHCenter)
        new_profile_col2_layout.addWidget(add_new_picture_button, alignment=Qt.AlignHCenter)
        new_profile_col2_layout.addSpacing(40)
        new_profile_col2_layout.addWidget(self.new_name_text)
        new_profile_col2_layout.addWidget(new_profile_col2_row3_widget)
        new_profile_col2_layout.addWidget(new_profile_col2_row4_widget)
        new_profile_col2_layout.addWidget(self.new_height_text)
        new_profile_col2_layout.addWidget(self.new_weight_text)
        new_profile_col2_layout.addWidget(self.new_activity_combo)
        new_profile_col2_layout.addSpacing(120)
        

        new_profile_col2_widget.setLayout(new_profile_col2_layout)

        new_profile_col3_widget = QWidget()
        new_profile_col3_widget.setStyleSheet("background-color: #24201f")
        new_profile_col3_widget.setFixedWidth(400)

        new_profile_col3_layout = QVBoxLayout()
        new_profile_col3_layout.setContentsMargins(0, 0, 0, 0)
        new_profile_col3_layout.setSpacing(20)

        new_profile_col3_row1_widget = QWidget()
        new_profile_col3_row1_widget.setStyleSheet("background-color: #24201f")

        new_profile_col3_row1_layout = QHBoxLayout()
        new_profile_col3_row1_layout.setContentsMargins(0, 0, 0, 0)
        new_profile_col3_row1_layout.setSpacing(20)

        new_profile_col3_row1_layout.addStretch()
        new_profile_col3_row1_layout.addWidget(self.cancel_new_save_button)
        new_profile_col3_row1_layout.addWidget(new_save_button)
        new_profile_col3_row1_layout.addStretch()

        new_profile_col3_row1_widget.setLayout(new_profile_col3_row1_layout)

        new_profile_col3_layout.addStretch()
        new_profile_col3_layout.addSpacing(20)
        new_profile_col3_layout.addWidget(new_profile_col3_row1_widget)
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




    def gender_state(self, gender):
        self.current_gender = gender

        if self.current_gender == "Male":
            self.gender_male_button.setStyleSheet("""
                                QPushButton {
                                    color: #645e59; background-color: #171514; border: 2px solid #645e59; 
                                    border-radius: 14px; text-align: center;
                                }

                                QPushButton:Hover {
                                    background-color: #1d1a19;
                                }
                                QPushButton:pressed {
                                    background-color: #1d1a19;
                                        }
                                QPushButton:focus {
                                    border: 2px solid #645e59; outline: none; 
                                }
                            """)
            self.gender_female_button.setStyleSheet("""
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
        else: 
            self.gender_female_button.setStyleSheet("""
                                QPushButton {
                                    color: #645e59; background-color: #171514; border: 2px solid #645e59; 
                                    border-radius: 14px; text-align: center;
                                }

                                QPushButton:Hover {
                                    background-color: #1d1a19;
                                }
                                QPushButton:pressed {
                                    background-color: #1d1a19;
                                        }
                                QPushButton:focus {
                                    border: 2px solid #645e59; outline: none; 
                                }
                            """)
            self.gender_male_button.setStyleSheet("""
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




    def cancel_new_save(self):

        self.tab_switcher("Profiles")
        self.tabs_widget.show()




    def save_profile(self):

        can_save_profile = True
        
        #Check to see if the profile name exists
        name = self.new_name_text.text()
        for profiles in self.local_profiles:
            for value in profiles.values():
                if value == self.new_name_text.text():
                    can_save_profile = False
                    self.new_name_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid #841934; border-radius: 14px")
                    self.new_name_text.setText("")
                    self.new_name_text.setPlaceholderText("Name already taken")
                
        #Confirm that the day/month/year is valid
        try:
            day = int(self.new_day_text.text())

            if day < 1 or day > 31:
                can_save_profile = False
                self.new_day_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid #841934; border-radius: 14px")
                self.new_day_text.setText("")
                self.new_day_text.setPlaceholderText("(1-31)")

        except ValueError:
            can_save_profile = False
            self.new_day_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid #841934; border-radius: 14px")
            self.new_day_text.setText("")
            self.new_day_text.setPlaceholderText("(1-31)")

        try:
            month = int(self.new_month_text.text())

            if month < 1 or month > 12:
                can_save_profile = False
                self.new_month_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid #841934; border-radius: 14px")
                self.new_month_text.setText("")
                self.new_month_text.setPlaceholderText("(1-12)")

        except ValueError:
            can_save_profile = False
            self.new_month_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid #841934; border-radius: 14px")
            self.new_month_text.setText("")
            self.new_month_text.setPlaceholderText("(1-12)")

        try:
            year = int(self.new_year_text.text())

            if year < 1900 or year > 2025:
                can_save_profile = False
                self.new_year_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid #841934; border-radius: 14px")
                self.new_year_text.setText("")
                self.new_year_text.setPlaceholderText("(1900-2025)")

        except ValueError:
            can_save_profile = False
            self.new_year_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid #841934; border-radius: 14px")
            self.new_year_text.setText("")
            self.new_year_text.setPlaceholderText("(1900-2025)")

        gender = self.current_gender

        #Confirm that the height is valid
        try:
            height = int(self.new_height_text.text())

            if height <= 0 or height > 400:
                can_save_profile = False
                self.new_height_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid #841934; border-radius: 14px")
                self.new_height_text.setText("")
                self.new_height_text.setPlaceholderText("(0-400)")

        except ValueError:
            can_save_profile = False
            self.new_height_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid #841934; border-radius: 14px")
            self.new_height_text.setText("")
            self.new_height_text.setPlaceholderText("(0-400)")

        #Confirm that the height weight is valid
        try:
            weight = float(self.new_weight_text.text())

            if weight < 1 or weight > 1000:
                can_save_profile = False
                self.new_weight_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid #841934; border-radius: 14px")
                self.new_weight_text.setText("")
                self.new_weight_text.setPlaceholderText("(1-1000)")

            weight = float(f"{weight:.1f}")

        except ValueError:
            can_save_profile = False
            self.new_weight_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid #841934; border-radius: 14px")
            self.new_weight_text.setText("")
            self.new_weight_text.setPlaceholderText("(1-1000)")


        #Activity - does not require validation checking
        activity = self.new_activity_combo.currentIndex()

        if can_save_profile == True:

            dob = datetime.date(year, month, day)

            profile_update = {
                "picture": self.picture_URL,
                "name": name,
                "dob": {
                    "day": day,
                    "month": month,
                    "year": year
                },
                "gender": gender,
                "height": height, 
                "weight": weight, 
                "activity": activity
            }

            self.local_profiles.append(profile_update)

            with open('./src/data.json', 'w') as f:
                json.dump(self.data, f, indent=4)

            self.tabs_widget.show()

            self.tab_switcher("Profiles")




    def profiles(self):

        #Profiles - elements
        self.profile_picture = QLabel(self)
        self.picture_URL = self.local_profiles[0]['picture']
        pixmap = QPixmap(self.picture_URL)
        self.profile_picture.setPixmap(pixmap)
        self.profile_picture.setScaledContents(True)
        self.profile_picture.setFixedHeight(440)
        self.profile_picture.setFixedWidth(440)
        self.profile_picture.setAlignment(Qt.AlignCenter)
        self.profile_picture.setFont(QFont("Times New Roman", 20))
        self.profile_picture.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid black")

        self.preview_profile_picture = QLabel(self)
        self.preview_profile_picture.setPixmap(pixmap)
        self.preview_profile_picture.setScaledContents(True)
        self.preview_profile_picture.setFixedHeight(360)
        self.preview_profile_picture.setFixedWidth(400)
        self.preview_profile_picture.setAlignment(Qt.AlignCenter)
        self.preview_profile_picture.setFont(QFont("Times New Roman", 20))
        self.preview_profile_picture.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid black; margin-left: 40px")
        self.preview_profile_picture.hide()

        self.edit_profile_picture_button = QPushButton("Browse...", self)
        self.edit_profile_picture_button.setFixedHeight(60)
        self.edit_profile_picture_button.setFixedWidth(290)
        self.edit_profile_picture_button.setFont(QFont("Times New Roman", 18))
        self.edit_profile_picture_button.setStyleSheet("""
                                QPushButton {
                                    color: #645e59; background-color: #171514; border: 2px solid black; 
                                    border-radius: 14px; text-align: center; margin-left: 150px;
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
        self.edit_profile_picture_button.clicked.connect(lambda: self.update_profile_picture("Current Profile"))
        self.edit_profile_picture_button.hide()

        self.next_profile_button = QPushButton("Next\nProfile", self)
        self.next_profile_button.setFixedHeight(80)
        self.next_profile_button.setFixedWidth(140)
        self.next_profile_button.setFont(QFont("Times New Roman", 18))
        self.next_profile_button.setStyleSheet("""
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
        self.next_profile_button.clicked.connect(self.next_profile)

        self.delete_profile_button = QPushButton("Delete", self)
        self.delete_profile_button.setFixedHeight(80)
        self.delete_profile_button.setFixedWidth(140)
        self.delete_profile_button.setFont(QFont("Times New Roman", 20))
        self.delete_profile_button.setStyleSheet("""
                                QPushButton {
                                    color: black; background-color: #971c3c; border: 2px solid #841934; 
                                    border-radius: 14px; text-align: center;
                                }

                                QPushButton:Hover {
                                    background-color: #b22150;
                                }
                                QPushButton:pressed {
                                    background-color: #971c3c;
                                        }
                                QPushButton:focus {
                                    border: 2px solid #841934; outline: none; 
                                }
                            """)
        self.delete_profile_button.clicked.connect(self.delete_profile)
        self.delete_profile_button.hide()
                            
        self.add_profile_button = QPushButton("Add\nProfile", self)
        self.add_profile_button.setFixedHeight(80)
        self.add_profile_button.setFixedWidth(140)
        self.add_profile_button.setFont(QFont("Times New Roman", 18))
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

        self.cancel_profile_button = QPushButton("Cancel", self)
        self.cancel_profile_button.setFixedHeight(80)
        self.cancel_profile_button.setFixedWidth(140)
        self.cancel_profile_button.setFont(QFont("Times New Roman", 20))
        self.cancel_profile_button.setStyleSheet("""
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
        self.cancel_profile_button.clicked.connect(self.cancel_edit_profile)
        self.cancel_profile_button.hide()

        self.edit_profile_button = QPushButton("Edit\nProfile", self)
        self.edit_profile_button.setFixedHeight(80)
        self.edit_profile_button.setFixedWidth(140)
        self.edit_profile_button.setFont(QFont("Times New Roman", 18))
        self.edit_profile_button.setStyleSheet("""
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
        self.edit_profile_button.clicked.connect(self.edit_profile)

        self.save_profile_button = QPushButton("Save", self)
        self.save_profile_button.setFixedHeight(80)
        self.save_profile_button.setFixedWidth(140)
        self.save_profile_button.setFont(QFont("Times New Roman", 20))
        self.save_profile_button.setStyleSheet("""
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
        self.save_profile_button.clicked.connect(self.save_edit_profile)
        self.save_profile_button.hide()
        
        name = f"Name:    {self.local_profiles[0]['name']}"
        self.profile_name_label = QLabel(name, self)
        self.profile_name_label.setFixedHeight(80)
        self.profile_name_label.setFixedWidth(740)
        self.profile_name_label.setAlignment(Qt.AlignCenter)
        self.profile_name_label.setFont(QFont("Times New Roman", 20))
        self.profile_name_label.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid black; border-radius: 14px")

        self.profile_name_text = QLineEdit(self.local_profiles[0]['name'], self)
        self.profile_name_text.setFixedHeight(80)
        self.profile_name_text.setFixedWidth(740)
        self.profile_name_text.setAlignment(Qt.AlignCenter)
        self.profile_name_text.setFont(QFont("Times New Roman", 20))
        self.profile_name_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid black; border-radius: 14px")
        self.profile_name_text.hide()

        self.current_age = 0
        self.calculate_age()

        age = f"Date of Birth:    {self.local_profiles[0]['dob']['day']} - {self.local_profiles[0]['dob']['month']} - {self.local_profiles[0]['dob']['year']}    ({self.current_age} Years old)"
        self.profile_age_label = QLabel(age, self)
        self.profile_age_label.setFixedHeight(80)
        self.profile_age_label.setFixedWidth(740)
        self.profile_age_label.setAlignment(Qt.AlignCenter)
        self.profile_age_label.setFont(QFont("Times New Roman", 20))
        self.profile_age_label.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid black; border-radius: 14px")

        gender = f"Gender:    {self.local_profiles[0]['gender']}"
        self.profile_gender_label = QLabel(gender, self)
        self.profile_gender_label.setFixedHeight(80)
        self.profile_gender_label.setFixedWidth(740)
        self.profile_gender_label.setAlignment(Qt.AlignCenter)
        self.profile_gender_label.setFont(QFont("Times New Roman", 20))
        self.profile_gender_label.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid black; border-radius: 14px")

        height = f"Height:    {self.local_profiles[0]['height']} CM"
        self.profile_height_label = QLabel(height, self)
        self.profile_height_label.setFixedHeight(80)
        self.profile_height_label.setFixedWidth(740)
        self.profile_height_label.setAlignment(Qt.AlignCenter)
        self.profile_height_label.setFont(QFont("Times New Roman", 20))
        self.profile_height_label.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid black; border-radius: 14px")

        self.profile_height_text = QLineEdit(self)
        self.profile_height_text.setFixedHeight(80)
        self.profile_height_text.setFixedWidth(740)
        self.profile_height_text.setPlaceholderText("Height (cm's)")
        self.profile_height_text.setAlignment(Qt.AlignCenter)
        self.profile_height_text.setFont(QFont("Times New Roman", 20))
        self.profile_height_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid black; border-radius: 14px")
        self.profile_height_text.hide()

        
        weight = f"Weight:    {self.local_profiles[0]['weight']} KG"
        self.profile_weight_label = QLabel(weight, self)
        self.profile_weight_label.setFixedHeight(80)
        self.profile_weight_label.setFixedWidth(740)
        self.profile_weight_label.setAlignment(Qt.AlignCenter)
        self.profile_weight_label.setFont(QFont("Times New Roman", 20))
        self.profile_weight_label.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid black; border-radius: 14px")

        self.profile_weight_text = QLineEdit(self)
        self.profile_weight_text.setFixedHeight(80)
        self.profile_weight_text.setFixedWidth(740)
        self.profile_weight_text.setPlaceholderText("Weight (kg's)")
        self.profile_weight_text.setAlignment(Qt.AlignCenter)
        self.profile_weight_text.setFont(QFont("Times New Roman", 20))
        self.profile_weight_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid black; border-radius: 14px")
        self.profile_weight_text.hide()

        activity = ""
        match self.local_profiles[0]['activity']:
            case 0:
                activity = "Activity:    Sedentary - little or no exercise"
            case 1:
                activity = "Activity:    Light - exercise 1-3 times/week"
            case 2:
                activity = "Activity:    Moderate - exercise 4-5 times/week"
            case 3:
                activity = "Activity:    Very Active - intense exercise 6-7 times/week"
            case 4:
                activity = "Activity:    Extra Active - very intense daily exercise"

        self.profile_activity_label = QLabel(activity, self)
        self.profile_activity_label.setFixedHeight(80)
        self.profile_activity_label.setFixedWidth(740)
        self.profile_activity_label.setAlignment(Qt.AlignCenter)
        self.profile_activity_label.setFont(QFont("Times New Roman", 20))
        self.profile_activity_label.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid black; border-radius: 14px")

        self.profile_activity_combo = QComboBox(self)
        self.profile_activity_combo.setFixedHeight(80)
        self.profile_activity_combo.setFixedWidth(740)
        self.profile_activity_combo.setFont(QFont("Times New Roman", 20))
        self.profile_activity_combo.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid black; border-radius: 14px")
        self.profile_activity_combo.setStyleSheet("""
                                QComboBox {
                                    color: #645e59; background-color: #171514; border: 2px solid black; 
                                    border-radius: 14px; padding-left: 10 px;
                                }
                                
                                QComboBox::drop-down {
                                    border-top-right-radius: 4px; border-top-right-radius: 4px;
                                }
                            """)

        self.profile_activity_combo.addItems([
                                "▼            Sedentary: little or no exercise", 
                                "▼            Light: exercise 1-3 times/week", 
                                "▼            Moderate: exercise 4-5 times/week",
                                "▼            Very Active: intense exercise 6-7 times/week",
                                "▼            Extra Active: very intense daily exercise"
                                ])
        self.profile_activity_combo.setCurrentIndex(self.local_profiles[0]['activity'])
        self.profile_activity_combo.hide()

        self.current_TDEE = 0.00

        temp_weight = 10 * float(self.local_profiles[0]['weight'])
        temp_height = 6.25 * float(self.local_profiles[0]['height'])
        temp_age = 5 * float(self.current_age)
        
        self.current_TDEE += temp_weight
        self.current_TDEE += temp_height
        self.current_TDEE -= temp_age

        match self.local_profiles[0]['gender']:
            case "Male":
                self.current_TDEE += 5
            case "Female":
                self.current_TDEE -= 161

        match self.local_profiles[0]['activity']:
            case 0:
                self.current_TDEE *= 1.2
            case 1:
                self.current_TDEE *= 1.375
            case 2:
                self.current_TDEE *= 1.55
            case 3:
                self.current_TDEE *= 1.725
            case 4:
                self.current_TDEE *= 1.9

        gain = f"Weight Gain: {int(self.current_TDEE) + 500} calories"
        maintain = f"Maintain Weight: {int(self.current_TDEE)} calories"
        loss = f"Weight Loss: {int(self.current_TDEE) - 500} calories"
        extreme_loss = f"Extreme Weight Loss: {int(self.current_TDEE) - 1000} calories"

        self.gain_label = QLabel(gain, self)
        self.gain_label.setFixedHeight(90)
        self.gain_label.setFixedWidth(645)
        self.gain_label.setAlignment(Qt.AlignCenter)
        self.gain_label.setFont(QFont("Times New Roman", 20))
        self.gain_label.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid black; border-radius: 14px")

        self.maintain_label = QLabel(maintain, self)
        self.maintain_label.setFixedHeight(90)
        self.maintain_label.setFixedWidth(645)
        self.maintain_label.setAlignment(Qt.AlignCenter)
        self.maintain_label.setFont(QFont("Times New Roman", 20))
        self.maintain_label.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid black; border-radius: 14px")
        
        self.loss_label = QLabel(loss, self)
        self.loss_label.setFixedHeight(90)
        self.loss_label.setFixedWidth(645)
        self.loss_label.setAlignment(Qt.AlignCenter)
        self.loss_label.setFont(QFont("Times New Roman", 20))
        self.loss_label.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid black; border-radius: 14px")
        
        self.extreme_loss_label = QLabel(extreme_loss, self)
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
        profiles_row1_col1_widget.setFixedWidth(440)

        profiles_row1_col1_layout = QVBoxLayout()
        profiles_row1_col1_layout.setContentsMargins(0, 0, 0, 0)
        profiles_row1_col1_layout.setSpacing(20)

        profiles_row1_col1_layout.addWidget(self.profile_picture)
        profiles_row1_col1_layout.addWidget(self.preview_profile_picture)
        profiles_row1_col1_layout.addWidget(self.edit_profile_picture_button)

        profiles_row1_col1_buttons_widget = QWidget()

        profiles_row1_col1_buttons_layout = QHBoxLayout()
        profiles_row1_col1_buttons_layout.setContentsMargins(0, 0, 0, 0)
        profiles_row1_col1_buttons_layout.setSpacing(0)

        profiles_row1_col1_buttons_layout.addWidget(self.next_profile_button)
        profiles_row1_col1_buttons_layout.addWidget(self.delete_profile_button)
        profiles_row1_col1_buttons_layout.addStretch()
        profiles_row1_col1_buttons_layout.addWidget(self.add_profile_button)
        profiles_row1_col1_buttons_layout.addWidget(self.cancel_profile_button)
        profiles_row1_col1_buttons_layout.addStretch()
        profiles_row1_col1_buttons_layout.addWidget(self.edit_profile_button)
        profiles_row1_col1_buttons_layout.addWidget(self.save_profile_button)
        

        profiles_row1_col1_buttons_widget.setLayout(profiles_row1_col1_buttons_layout)

        profiles_row1_col1_layout.addWidget(profiles_row1_col1_buttons_widget) 

        profiles_row1_col1_widget.setLayout(profiles_row1_col1_layout)

        profiles_row1_col2_widget = QWidget(self)

        profiles_row1_col2_layout = QVBoxLayout()
        profiles_row1_col2_layout.setContentsMargins(0, 0, 0, 0)
        profiles_row1_col2_layout.setSpacing(12)

        profiles_row1_col2_layout.addWidget(self.profile_name_label)
        profiles_row1_col2_layout.addWidget(self.profile_name_text)
        profiles_row1_col2_layout.addWidget(self.profile_age_label)
        profiles_row1_col2_layout.addWidget(self.profile_gender_label)
        profiles_row1_col2_layout.addWidget(self.profile_height_label)
        profiles_row1_col2_layout.addWidget(self.profile_height_text)
        profiles_row1_col2_layout.addWidget(self.profile_weight_label)
        profiles_row1_col2_layout.addWidget(self.profile_weight_text)
        profiles_row1_col2_layout.addWidget(self.profile_activity_label)
        profiles_row1_col2_layout.addWidget(self.profile_activity_combo)

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



    def next_profile(self):
        profile = self.local_profiles.pop(0)
        self.local_profiles.append(profile)

        with open('./src/data.json', 'w') as f:
                json.dump(self.data, f, indent=4)

        self.tab_switcher("Profiles")

    


    def delete_profile(self):
        self.local_profiles.pop(0)

        with open('./src/data.json', 'w') as f:
                json.dump(self.data, f, indent=4)

        if not self.local_profiles:
            self.tab_switcher("New Profile")

        else:
            self.tab_switcher("Profiles")




    def edit_profile(self):

        self.profile_picture.hide()

        self.preview_profile_picture.show()
        self.edit_profile_picture_button.show()

        self.next_profile_button.hide()
        self.add_profile_button.hide()
        self.edit_profile_button.hide()

        self.delete_profile_button.show()
        self.cancel_profile_button.show()
        self.save_profile_button.show()

        self.profile_name_label.hide()
        self.profile_height_label.hide()
        self.profile_weight_label.hide()
        self.profile_activity_label.hide()

        self.profile_name_text.show()
        self.profile_height_text.show()
        self.profile_weight_text.show()
        self.profile_activity_combo.show()




    def cancel_edit_profile(self):

        self.profile_picture.show()

        self.preview_profile_picture.hide()
        self.edit_profile_picture_button.hide()

        self.next_profile_button.show()
        self.add_profile_button.show()
        self.edit_profile_button.show()

        self.delete_profile_button.hide()
        self.cancel_profile_button.hide()
        self.save_profile_button.hide()

        self.profile_name_label.show()
        self.profile_height_label.show()
        self.profile_weight_label.show()
        self.profile_activity_label.show()

        self.profile_name_text.hide()
        self.profile_height_text.hide()
        self.profile_weight_text.hide()
        self.profile_activity_combo.hide()




    def save_edit_profile(self):

        can_save_edit_profile = True

        #Check to see if the profile name exists
        name = self.profile_name_text.text()
        if not name:
                can_save_edit_profile = False
                self.profile_name_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid #841934; border-radius: 14px")
                self.profile_name_text.setText("")
                self.profile_name_text.setPlaceholderText("Enter a name")

        #Confirm that the height is valid
        try:
            height = int(self.profile_height_text.text())

            if height <= 0 or height > 400:
                can_save_edit_profile = False
                self.profile_height_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid #841934; border-radius: 14px")
                self.profile_height_text.setText("")
                self.profile_height_text.setPlaceholderText("(0-400)")

        except ValueError:
            can_save_edit_profile = False
            self.profile_height_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid #841934; border-radius: 14px")
            self.profile_height_text.setText("")
            self.profile_height_text.setPlaceholderText("(0-400)")

        #Confirm that the height weight is valid
        try:
            weight = float(self.profile_weight_text.text())

            if weight < 1 or weight > 1000:
                can_save_edit_profile = False
                self.profile_weight_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid #841934; border-radius: 14px")
                self.profile_weight_text.setText("")
                self.profile_weight_text.setPlaceholderText("(1-1000)")

            weight = float(f"{weight:.1f}")

        except ValueError:
            can_save_edit_profile = False
            self.profile_weight_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid #841934; border-radius: 14px")
            self.profile_weight_text.setText("")
            self.profile_weight_text.setPlaceholderText("(1-1000)")


        #Activity - does not require validation checking
        activity = self.profile_activity_combo.currentIndex()

        if can_save_edit_profile == True:

            self.local_profiles[0].pop('picture')
            self.local_profiles[0]['picture'] = self.picture_URL

            self.local_profiles[0].pop('name')
            self.local_profiles[0]['name'] = name

            birthdate = self.local_profiles[0]['dob']
            self.local_profiles[0].pop('dob')
            self.local_profiles[0]['dob'] = birthdate

            gender = self.local_profiles[0]['gender']
            self.local_profiles[0].pop('gender')
            self.local_profiles[0]['gender'] = gender

            self.local_profiles[0].pop('height')
            self.local_profiles[0]['height'] = height

            self.local_profiles[0].pop('weight')
            self.local_profiles[0]['weight'] = weight

            self.local_profiles[0].pop('activity')
            self.local_profiles[0]['activity'] = activity
            
            with open('./src/data.json', 'w') as f:
                json.dump(self.data, f, indent=4)

            self.tab_switcher("Profiles")
        



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

        for key in self.local_consumables:

            button = key['consumable']
            button = QPushButton(key['consumable'], self)
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

            button.clicked.connect(partial(self.consumable_variants, key['consumable'])) 

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




    def add_consumable(self, consumable):

        if not consumable:
            self.new_consumable_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid #841934; border-radius: 14px")
            self.new_consumable_text.setText("")
            self.new_consumable_text.setPlaceholderText("No consumable detected")
            return

        for key in self.local_consumables:
            if consumable == key['consumable']:
                self.new_consumable_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid #841934; border-radius: 14px")
                self.new_consumable_text.setText("")
                self.new_consumable_text.setPlaceholderText("Consumable already added")
                return

        new_consumable = {
                            "consumable": consumable,
                            "variants": []
        }
        self.local_consumables.append(new_consumable)

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
        self.consumable_button.clicked.connect(lambda: self.tab_switcher("Consumables"))

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
                                    color: black; background-color: #971c3c; border: 2px solid #841934; 
                                    border-radius: 14px; text-align: center;
                                }

                                QPushButton:Hover {
                                    background-color: #b22150;
                                }
                                QPushButton:pressed {
                                    background-color: #971c3c;
                                        }
                                QPushButton:focus {
                                    border: 2px solid #841934; outline: none; 
                                }
                            """)
        self.delete_consumable_button.clicked.connect(lambda: self.delete_consumable_edit(consumable))
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

        self.save_consumable_button.clicked.connect(lambda: self.save_consumable_edit(self.consumable_text.text()))   
        self.save_consumable_button.hide()

        #Row 3 - element 1
        self.brand_text = QLineEdit(self)
        self.brand_text.setFixedHeight(60)
        self.brand_text.setFixedWidth(400)
        self.brand_text.setReadOnly(False)
        self.brand_text.setPlaceholderText("Brand e.g. (Coke)")
        self.brand_text.setAlignment(Qt.AlignCenter)
        self.brand_text.setFont(QFont("Times New Roman", 20))
        self.brand_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid black; border-radius: 14px")

        #Row 3 - element 2
        self.protein_text = QLineEdit(self)
        self.protein_text.setFixedHeight(60)
        self.protein_text.setFixedWidth(280)
        self.protein_text.setReadOnly(False)
        self.protein_text.setPlaceholderText("Protein (1)g")
        self.protein_text.setAlignment(Qt.AlignCenter)
        self.protein_text.setFont(QFont("Times New Roman", 20))
        self.protein_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid black; border-radius: 14px")

        #Row 3 - element 3
        self.carbs_text = QLineEdit(self)
        self.carbs_text.setFixedHeight(60)
        self.carbs_text.setFixedWidth(280)
        self.carbs_text.setReadOnly(False)
        self.carbs_text.setPlaceholderText("Carbs (8)g")
        self.carbs_text.setAlignment(Qt.AlignCenter)
        self.carbs_text.setFont(QFont("Times New Roman", 20))
        self.carbs_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid black; border-radius: 14px")

        #Row 3 - element 4
        self.fat_text = QLineEdit(self)
        self.fat_text.setFixedHeight(60)
        self.fat_text.setFixedWidth(280)
        self.fat_text.setReadOnly(False)
        self.fat_text.setPlaceholderText("Fat (2)g")
        self.fat_text.setAlignment(Qt.AlignCenter)
        self.fat_text.setFont(QFont("Times New Roman", 20))
        self.fat_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid black; border-radius: 14px")

        #Row 4 - element 1
        self.variant_text = QLineEdit(self)
        self.variant_text.setFixedHeight(60)
        self.variant_text.setFixedWidth(400)
        self.variant_text.setReadOnly(False)
        self.variant_text.setPlaceholderText("Variant (Vanilla - 1.5L)")
        self.variant_text.setAlignment(Qt.AlignCenter)
        self.variant_text.setFont(QFont("Times New Roman", 20))
        self.variant_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid black; border-radius: 14px")

        #Row 4 - element 2
        self.servings_text = QLineEdit(self)
        self.servings_text.setFixedHeight(60)
        self.servings_text.setFixedWidth(280)
        self.servings_text.setReadOnly(False)
        self.servings_text.setPlaceholderText("Servings (6)")
        self.servings_text.setAlignment(Qt.AlignCenter)
        self.servings_text.setFont(QFont("Times New Roman", 20))
        self.servings_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid black; border-radius: 14px")

        #Row 4 - element 3
        self.price_text = QLineEdit(self)
        self.price_text.setFixedHeight(60)
        self.price_text.setFixedWidth(280)
        self.price_text.setReadOnly(False)
        self.price_text.setPlaceholderText("Price (2.99)")
        self.price_text.setAlignment(Qt.AlignCenter)
        self.price_text.setFont(QFont("Times New Roman", 20))
        self.price_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid black; border-radius: 14px")

        #Row 4 - element 4
        self.add_variant_button = QPushButton("Add" , self)
        self.add_variant_button.setFixedHeight(60)
        self.add_variant_button.setFixedWidth(120)
        self.add_variant_button.setFont(QFont("Times New Roman", 20)) 
        self.add_variant_button.setStyleSheet("""
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
        self.add_variant_button.clicked.connect(lambda: self.add_variant(consumable))                

        #Row 4 - element 4 - edit mode
        self.delete_variant_button = QPushButton("Delete" , self)
        self.delete_variant_button.setFixedHeight(60)
        self.delete_variant_button.setFixedWidth(120)
        self.delete_variant_button.setFont(QFont("Times New Roman", 20)) 
        self.delete_variant_button.setStyleSheet("""
                                QPushButton {
                                    color: black; background-color: #971c3c; border: 2px solid #841934; 
                                    border-radius: 14px; text-align: center;
                                }

                                QPushButton:Hover {
                                    background-color: #b22150;
                                }
                                QPushButton:pressed {
                                    background-color: #971c3c;
                                        }
                                QPushButton:focus {
                                    border: 2px solid #841934; outline: none; 
                                }
                            """) 
        self.delete_variant_button.clicked.connect(lambda: self.delete_variant(consumable, self.variant_text.text()))
        self.delete_variant_button.hide()  

        #Row 4 - element 5 - edit mode
        self.edit_variant_button = QPushButton("Edit" , self)
        self.edit_variant_button.setFixedHeight(60)
        self.edit_variant_button.setFixedWidth(120)
        self.edit_variant_button.setFont(QFont("Times New Roman", 20)) 
        self.edit_variant_button.setStyleSheet("""
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
        self.edit_variant_button.clicked.connect(self.edit_variant)
        self.edit_variant_button.hide() 

        #Row 4 - element 4 - edit mode 2
        self.cancel_edit_variant_button = QPushButton("Cancel" , self)
        self.cancel_edit_variant_button.setFixedHeight(60)
        self.cancel_edit_variant_button.setFixedWidth(120)
        self.cancel_edit_variant_button.setFont(QFont("Times New Roman", 20)) 
        self.cancel_edit_variant_button.setStyleSheet("""
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
        current_variant = self.variant_text.text()
        self.cancel_edit_variant_button.clicked.connect(self.cancel_edit_variant)
        self.cancel_edit_variant_button.hide()

        #Row 4 - element 5 - edit mode 2
        self.save_edit_variant_button = QPushButton("Save" , self)
        self.save_edit_variant_button.setFixedHeight(60)
        self.save_edit_variant_button.setFixedWidth(120)
        self.save_edit_variant_button.setFont(QFont("Times New Roman", 20)) 
        self.save_edit_variant_button.setStyleSheet("""
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
        self.save_edit_variant_button.clicked.connect(lambda: self.save_edit_variant(consumable, self.current_variant))
        self.save_edit_variant_button.hide()

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

        for local_consumable in self.local_consumables:

            for variant in local_consumable['variants']:

                current_button_variant = f"{variant['brand']}: {variant['variant']}"

                button = QPushButton(current_button_variant, self)
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
                button.clicked.connect(partial(self.display_variant, variant['variant']))    

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
        variants_row3_layout.addWidget(self.brand_text)
        variants_row3_layout.addWidget(self.protein_text)
        variants_row3_layout.addWidget(self.carbs_text)
        variants_row3_layout.addWidget(self.fat_text)
        variants_row3_layout.addSpacing(20)

        variants_row3_widget.setLayout(variants_row3_layout)


        #Row 4 widget/layout
        variants_row4_widget = QWidget()
        variants_row4_widget.setFixedHeight(100)

        variants_row4_layout = QHBoxLayout()
        variants_row4_layout.setContentsMargins(0, 0, 0, 0)
        variants_row4_layout.setSpacing(40)

        variants_row4_layout.addSpacing(20)
        variants_row4_layout.addWidget(self.variant_text)
        variants_row4_layout.addWidget(self.servings_text)
        variants_row4_layout.addWidget(self.price_text)
        variants_row4_layout.addWidget(self.add_variant_button)
        variants_row4_layout.addWidget(self.delete_variant_button)
        variants_row4_layout.addWidget(self.edit_variant_button)
        variants_row4_layout.addWidget(self.cancel_edit_variant_button)
        variants_row4_layout.addWidget(self.save_edit_variant_button)
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

        self.central_layout.removeWidget(self.consumables_widget)
        self.consumables_widget.setParent(None)
        self.consumables_widget.deleteLater()

        self.central_layout.insertWidget(1, self.variants_widget)

        self.current_widget = "Variants"
        



    def delete_consumable_edit(self, consumable):

        index = 0

        for consumables in self.local_consumables:

            if consumables['consumable'] == consumable:
                self.local_consumables.pop(index)

            index += 1
    
        with open('./src/data.json', 'w') as f:
                json.dump(self.data, f, indent=4)
                
        self.tab_switcher("Consumables")




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




    def save_consumable_edit(self, new):

        can_save = True

        for consumables in self.local_consumables:
            if consumables['consumable'] == new:
                can_save = False
                self.consumable_text.setText("")
                self.consumable_text.setPlaceholderText("Name taken")
                self.consumable_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid #841934; border-radius: 14px")

        if new and can_save:
            self.local_consumables['consumable'] = new

            with open('./src/data.json', 'w') as f:
                json.dump(self.data, f, indent=4)

            self.consumable_button.setText(new)

            self.cancel_consumable_edit()




    def add_variant(self, current_consumable):

        can_add_variant = True
        
        brand = self.brand_text.text()
        variant = self.variant_text.text()

        if not brand:
            can_add_variant = False
            self.brand_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid #841934; border-radius: 14px")
            self.brand_text.setText("")
            self.brand_text.setPlaceholderText("Enter Brand")

        if not variant:
            can_add_variant = False
            self.variant_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid #841934; border-radius: 14px")
            self.variant_text.setText("")
            self.variant_text.setPlaceholderText("Enter Variant")

        for consumables in self.local_consumables:
            for variants in consumables['variants']:
                if variants['variant'] == variant:
                    can_add_variant = False
                    self.variant_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid #841934; border-radius: 14px")
                    self.variant_text.setText("")
                    self.variant_text.setPlaceholderText("Variant taken")
                
        try:
            carbs = float(self.carbs_text.text())

            if carbs < 0:
                can_add_variant = False
                self.carbs_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid #841934; border-radius: 14px")
                self.carbs_text.setText("")
                self.carbs_text.setPlaceholderText("Cannot have less than 0")

        except ValueError:
            can_add_variant = False
            self.carbs_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid #841934; border-radius: 14px")
            self.carbs_text.setText("")
            self.carbs_text.setPlaceholderText("Must be a number")

        try:
            protein = float(self.protein_text.text())

            if protein < 0:
                can_add_variant = False
                self.protein_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid #841934; border-radius: 14px")
                self.protein_text.setText("")
                self.protein_text.setPlaceholderText("Cannot have less than 0")

        except ValueError:
            can_add_variant = False
            self.protein_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid #841934; border-radius: 14px")
            self.protein_text.setText("")
            self.protein_text.setPlaceholderText("Must be a number")

        try:
            fat = float(self.fat_text.text())

            if fat < 0:
                can_add_variant = False
                self.fat_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid #841934; border-radius: 14px")
                self.fat_text.setText("")
                self.fat_text.setPlaceholderText("Cannot have less than 0")

        except ValueError:
            can_add_variant = False
            self.fat_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid #841934; border-radius: 14px")
            self.fat_text.setText("")
            self.fat_text.setPlaceholderText("Must be a number")

        try:
            servings = int(self.servings_text.text())

            if servings <= 0:
                can_add_variant = False
                self.servings_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid #841934; border-radius: 14px")
                self.servings_text.setText("")
                self.servings_text.setPlaceholderText("Must be more than 0")

        except ValueError:
            can_add_variant = False
            self.servings_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid #841934; border-radius: 14px")
            self.servings_text.setText("")
            self.servings_text.setPlaceholderText("Whole numbers only")

        try:
            price = float(self.price_text.text())

            if price <= 0:
                can_add_variant = False
                self.price_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid #841934; border-radius: 14px")
                self.price_text.setText("")
                self.price_text.setPlaceholderText("Must be more than 0")

        except ValueError:
            can_add_variant = False
            self.price_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid #841934; border-radius: 14px")
            self.price_text.setText("")
            self.price_text.setPlaceholderText("Must be a number")

        if can_add_variant == True:

            temp_carbs = carbs * 4
            temp_protein = protein * 4
            temp_fat = fat * 9

            calories = temp_carbs + temp_protein + temp_fat

            variant_update = {
                "brand": brand,
                "variant": variant,
                "carbs": carbs,
                "protein": protein,
                "fat": fat, 
                "servings": servings, 
                "price": price,
                "calories": calories
            }

            index = 0

            for consumables in self.local_consumables:
                if consumables['consumable'] == current_consumable:

                    self.local_consumables[index]['variants'].append(variant_update)

                    with open('./src/data.json', 'w') as f:
                        json.dump(self.data, f, indent=4)

                    self.tab_switcher("Consumables")
                    self.consumable_variants(current_consumable)                
                
                index += 1




    def display_variant(self, variant):

        self.add_variant_button.hide()
        self.delete_variant_button.show()
        self.edit_variant_button.show()

        self.current_variant = variant
        
        for consumables in self.local_consumables:
            for variants in consumables['variants']:
                if variants['variant'] == variant:

                    if variants['calories']:
                        calories = variants['calories'] / variants['servings']
                    else:
                        calories = 0

                    variant_id = f"{variants['brand']}: {variants['variant']}"
                    calories = int(calories)
                    calories_label = f"Cals per serving: {calories}"

                    self.brand_text.setText(variant_id)
                    self.brand_text.setReadOnly(True)
                    self.variant_text.setText(calories_label)
                    self.variant_text.setReadOnly(True)
                    self.carbs_text.setText(str(variants['carbs']))
                    self.carbs_text.setReadOnly(True)
                    self.protein_text.setText(str(variants['protein']))
                    self.protein_text.setReadOnly(True)
                    self.fat_text.setText(str(variants['fat']))
                    self.fat_text.setReadOnly(True)
                    self.servings_text.setText(str(variants['servings']))
                    self.servings_text.setReadOnly(True)
                    self.price_text.setText(str(variants['price']))
                    self.price_text.setReadOnly(True)




    def delete_variant(self, consumable, variant):

        index_C = 0
        index_V = 0

        for consumables in self.local_consumables:
            for variants in consumables['variants']:
                if variants['variant'] == variant:

                    self.local_consumables[index_C]['variants'].pop(index_V)

                    with open('./src/data.json', 'w') as f:
                        json.dump(self.data, f, indent=4)

                    self.tab_switcher("Consumables")
                    self.consumable_variants(consumable)

                index_V += 1

            index_C += 1




    def edit_variant(self):

        self.brand_text.setReadOnly(False)
        self.variant_text.setReadOnly(False)
        self.carbs_text.setReadOnly(False)
        self.protein_text.setReadOnly(False)
        self.fat_text.setReadOnly(False)
        self.servings_text.setReadOnly(False)
        self.price_text.setReadOnly(False)
        

        self.delete_variant_button.hide()
        self.edit_variant_button.hide()
        self.cancel_edit_variant_button.show()
        self.save_edit_variant_button.show()



    def cancel_edit_variant(self):

        self.delete_variant_button.show()
        self.edit_variant_button.show()
        self.cancel_edit_variant_button.hide()
        self.save_edit_variant_button.hide()

        variant = self.current_variant

        for consumables in self.local_consumables:
            for variants in consumables['variants']:
                if variants['variant'] == variant:
                    self.brand_text.setText(variants['brand'])
                    self.brand_text.setReadOnly(True)
                    self.variant_text.setText(variants['variant'])
                    self.variant_text.setReadOnly(True)
                    self.carbs_text.setText(str(variants['carbs']))
                    self.carbs_text.setReadOnly(True)
                    self.protein_text.setText(str(variants['protein']))
                    self.protein_text.setReadOnly(True)
                    self.fat_text.setText(str(variants['fat']))
                    self.fat_text.setReadOnly(True)
                    self.servings_text.setText(str(variants['servings']))
                    self.servings_text.setReadOnly(True)
                    self.price_text.setText(str(variants['price']))
                    self.price_text.setReadOnly(True)




    def save_edit_variant(self, current_consumable, current_variant):
        
        can_save_variant = True
        
        brand = self.brand_text.text()
        variant = self.variant_text.text()

        if not brand:
            can_save_variant = False
            self.brand_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid #841934; border-radius: 14px")
            self.brand_text.setText("")
            self.brand_text.setPlaceholderText("Enter Brand")

        if not variant:
            can_save_variant = False
            self.variant_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid #841934; border-radius: 14px")
            self.variant_text.setText("")
            self.variant_text.setPlaceholderText("Enter Variant")
                
        try:
            carbs = float(self.carbs_text.text())

            if carbs < 0:
                can_save_variant = False
                self.carbs_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid #841934; border-radius: 14px")
                self.carbs_text.setText("")
                self.carbs_text.setPlaceholderText("Cannot have less than 0")

        except ValueError:
            can_save_variant = False
            self.carbs_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid #841934; border-radius: 14px")
            self.carbs_text.setText("")
            self.carbs_text.setPlaceholderText("Must be a number")

        try:
            protein = float(self.protein_text.text())

            if protein < 0:
                can_save_variant = False
                self.protein_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid #841934; border-radius: 14px")
                self.protein_text.setText("")
                self.protein_text.setPlaceholderText("Cannot have less than 0")

        except ValueError:
            can_save_variant = False
            self.protein_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid #841934; border-radius: 14px")
            self.protein_text.setText("")
            self.protein_text.setPlaceholderText("Must be a number")

        try:
            fat = float(self.fat_text.text())

            if fat < 0:
                can_save_variant = False
                self.fat_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid #841934; border-radius: 14px")
                self.fat_text.setText("")
                self.fat_text.setPlaceholderText("Cannot have less than 0")

        except ValueError:
            can_save_variant = False
            self.fat_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid #841934; border-radius: 14px")
            self.fat_text.setText("")
            self.fat_text.setPlaceholderText("Must be a number")

        try:
            servings = int(self.servings_text.text())

            if servings <= 0:
                can_save_variant = False
                self.servings_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid #841934; border-radius: 14px")
                self.servings_text.setText("")
                self.servings_text.setPlaceholderText("Must be more than 0")

        except ValueError:
            can_save_variant = False
            self.servings_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid #841934; border-radius: 14px")
            self.servings_text.setText("")
            self.servings_text.setPlaceholderText("Whole numbers only")

        try:
            price = float(self.price_text.text())

            if price <= 0:
                can_save_variant = False
                self.price_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid #841934; border-radius: 14px")
                self.price_text.setText("")
                self.price_text.setPlaceholderText("Must be more than 0")

        except ValueError:
            can_save_variant = False
            self.price_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid #841934; border-radius: 14px")
            self.price_text.setText("")
            self.price_text.setPlaceholderText("Must be a number")

        if can_save_variant == True:

            temp_carbs = carbs * 4
            temp_protein = protein * 4
            temp_fat = fat * 9

            calories = temp_carbs + temp_protein + temp_fat

            variant_update = {
                "brand": brand,
                "variant": variant,
                "carbs": carbs,
                "protein": protein,
                "fat": fat, 
                "servings": servings, 
                "price": price,
                "calories": calories
            }

            index_C = 0
            index_V = 0

            for consumables in self.local_consumables:
                for variants in consumables['variants']:
                    if variants['variant'] == current_variant:

                        self.local_consumables[index_C]['variants'][index_V] = variant_update

                        with open('./src/data.json', 'w') as f:
                            json.dump(self.data, f, indent=4)

                        self.tab_switcher("Consumables")
                        self.consumable_variants(current_consumable)  

                    index_V += 1

                index_C += 1


            
# carbs/protein * 4 / fat * 9
    def recipes(self):
        pass




    def pantry(self):
        pass




    def planner(self):
        pass




    def shopping(self):
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

    def update_profile_picture(self, display):
        picture, _ = QFileDialog.getOpenFileName(
                                            None,
                                            "Open file",
                                            "",
                                            "Images (*.png, *.jpg, *.jpeg);;All Files (*)"
                                            )

        if picture:
            self.picture_URL = picture

        pixmap = QPixmap(self.picture_URL)

        match display:
            case "New Profile":
                self.new_profile_picture.setPixmap(pixmap)
            case "Current Profile":
                self.preview_profile_picture.setPixmap(pixmap)


    def calculate_age(self):

        birth_date = datetime.date(self.local_profiles[0]['dob']['year'], self.local_profiles[0]['dob']['month'], self.local_profiles[0]['dob']['day'])
        current_date = datetime.datetime.now()

        birth_day = birth_date.strftime("%d-%m")
        current_day = current_date.strftime("%d-%m")

        birth_year = birth_date.strftime("%Y")
        current_year = current_date.strftime("%Y")

        self.current_age = int(current_year) - int(birth_year)

        if birth_day > current_day:
            self.current_age -= 1

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()