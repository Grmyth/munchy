import sys
import json
import datetime
import math
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QLabel, QLineEdit, QComboBox, QPushButton
from PyQt5.QtGui import QFont


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

        #Creating the profiles instance from the Profiles class
            #This is one instance that will hold all of the user profiles
        self.local_profiles = Profiles()

        #Initiation methods
        self.read_data_file()
        self.initUI()
        if not self.local_profiles.profile:
            self.new_profile()

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
            self.json_profiles = self.data['profiles']

        #Creating a local Profiles instance with a .profile for all stored profiles
        if self.json_profiles:
            for profile in self.json_profiles:
                for profile_name, profile_values in profile.items():
                    self.local_profiles.add_profile(
                        profile_name, 
                        profile_values['dob'], 
                        profile_values['height'], 
                        profile_values['weight'], 
                        str(profile_values['activity'])
                        )

            #self.consumables = data['consumables']
            #self.recipes = data['recipes']

    def initUI(self):

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


        #Central application widget - This is the widget that covers the full application
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        #Central application layout
        self.central_layout = QVBoxLayout()
        self.central_layout.setContentsMargins(0, 0, 0, 0)
        self.central_layout.setSpacing(0)

        #Titlebar Widget - Also setting the layout of the titlebar elements within the widget
        titlebar_widget = QWidget()
        titlebar_widget.setStyleSheet("background-color: #161515")

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
                                    background-color: #161515;
                                }
                            """)

        self.consumables_tab = QPushButton("Consumables", self)
        self.consumables_tab.setFixedHeight(106)
        self.consumables_tab.setFixedWidth(230)

        self.recipes_tab = QPushButton("Recipes", self)
        self.recipes_tab.setFixedHeight(106)
        self.recipes_tab.setFixedWidth(230)

        self.pantry_tab = QPushButton("Pantry", self)
        self.pantry_tab.setFixedHeight(106)
        self.pantry_tab.setFixedWidth(230)

        self.planner_tab = QPushButton("Planner", self)
        self.planner_tab.setFixedHeight(106)
        self.planner_tab.setFixedWidth(230)

        self.shopping_tab = QPushButton("Shopping", self)
        self.shopping_tab.setFixedHeight(106)
        self.shopping_tab.setFixedWidth(230)

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
        self.tabs_widget.hide()


        #Center column - Row 1 - Profile picture
        self.profile_picture = QLabel(self)
        self.profile_picture.setFixedHeight(260)
        self.profile_picture.setFixedWidth(260)
        self.profile_picture.setFocusPolicy(Qt.StrongFocus)
        self.profile_picture.setStyleSheet("background-color: #171514; border: 2px solid black; border-radius: 20px")

        #Center column - Row 2 - Name
        self.name_text = QLineEdit(self)
        self.name_text.setPlaceholderText("Name")
        self.name_text.setFixedHeight(60)
        self.name_text.setAlignment(Qt.AlignCenter)
        self.name_text.setFont(QFont("Times New Roman", 20))
        self.name_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid black; border-radius: 14px")
        self.name_text.textEdited.connect(lambda: self.is_empty(self.name_text))

        #Center column - Row 3 - D.O.B
            
            #elements left to right
            
        # -- element 1 --
        self.day_text = QLineEdit(self)
        self.day_text.setPlaceholderText("DD")
        self.day_text.setFixedHeight(60)
        self.day_text.setFixedWidth(146)
        self.day_text.setAlignment(Qt.AlignCenter)
        self.day_text.setFont(QFont("Times New Roman", 20))
        self.day_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid black; border-radius: 14px")
        self.day_text.textEdited.connect(lambda: self.is_empty(self.day_text))

        # -- element 2 --
        self.month_text = QLineEdit(self)
        self.month_text.setPlaceholderText("MM")
        self.month_text.setFixedHeight(60)
        self.month_text.setFixedWidth(146)
        self.month_text.setAlignment(Qt.AlignCenter)
        self.month_text.setFont(QFont("Times New Roman", 20))
        self.month_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid black; border-radius: 14px")
        self.month_text.textEdited.connect(lambda: self.is_empty(self.month_text))

        # -- element 3 --
        self.year_text = QLineEdit(self)
        self.year_text.setPlaceholderText("YYYY")
        self.year_text.setFixedHeight(60)
        self.year_text.setFixedWidth(296)
        self.year_text.setAlignment(Qt.AlignCenter)
        self.year_text.setFont(QFont("Times New Roman", 20))
        self.year_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid black; border-radius: 14px")
        self.year_text.textEdited.connect(lambda: self.is_empty(self.year_text))

        #Center column - Row 4 - Height
            
            #elements left to right

        # -- element 1 --
        self.foot_height_text = QLineEdit(self)
        self.foot_height_text.setPlaceholderText("Height (Feet)")
        self.foot_height_text.setFixedHeight(60)
        self.foot_height_text.setFixedWidth(297)
        self.foot_height_text.setAlignment(Qt.AlignCenter)
        self.foot_height_text.setFont(QFont("Times New Roman", 20))
        self.foot_height_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid black; border-radius: 14px")
        self.foot_height_text.textEdited.connect(lambda: self.is_empty(self.foot_height_text))

        # -- element 2 --
        self.inch_height_text = QLineEdit(self)
        self.inch_height_text.setPlaceholderText("Height (Inches)")
        self.inch_height_text.setFixedHeight(60)
        self.inch_height_text.setFixedWidth(297)
        self.inch_height_text.setAlignment(Qt.AlignCenter)
        self.inch_height_text.setFont(QFont("Times New Roman", 20))
        self.inch_height_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid black; border-radius: 14px")
        self.inch_height_text.textEdited.connect(lambda: self.is_empty(self.inch_height_text))

        #Center column - Row 5
            
            #elements left to right

        # -- element 1 --
        self.weight_text = QLineEdit(self)
        self.weight_text.setPlaceholderText("Weight")
        self.weight_text.setFixedHeight(60)
        self.weight_text.setFixedWidth(297)
        self.weight_text.setAlignment(Qt.AlignCenter)
        self.weight_text.setFont(QFont("Times New Roman", 20))
        self.weight_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid black; border-radius: 14px")
        self.weight_text.textEdited.connect(lambda: self.is_empty(self.weight_text))

        # -- element 2 --
        self.weight_combo = QComboBox(self)
        self.weight_combo.setFixedHeight(60)
        self.weight_combo.setFixedWidth(297)
        self.weight_combo.setFont(QFont("Times New Roman", 20))
        self.weight_combo.setStyleSheet("""
                                QComboBox {
                                    color: #645e59; background-color: #171514; border: 2px solid black; 
                                    border-radius: 14px; padding-left: 64px;
                                }
                                
                                QComboBox::drop-down {
                                    border-top-right-radius: 4px; border-top-right-radius: 4px;
                                }""")

        self.weight_combo.addItems([
                                "▼    KG's    ▼", 
                                "▼    LB's    ▼"
                                ])
        self.weight_combo.setCurrentIndex(0)

        #Center column - Row 6
        self.activity_combo = QComboBox(self)
        self.activity_combo.setFixedHeight(60)
        self.activity_combo.setFixedWidth(600)
        self.activity_combo.setPlaceholderText("Activity")
        self.activity_combo.setFont(QFont("Times New Roman", 20))
        self.activity_combo.setStyleSheet("""
                                QComboBox {
                                    color: #645e59; background-color: #171514; border: 2px solid black; 
                                    border-radius: 14px; padding-left: 10 px;
                                }
                                
                                QComboBox::drop-down {
                                    border-top-right-radius: 4px; border-top-right-radius: 4px;
                                }
                            """)

        self.activity_combo.addItems([
                                "▼    Sedentary: little or no exercise", 
                                "▼    Light: exercise 1-3 times/week", 
                                "▼    Moderate: exercise 4-5 times/week", 
                                "▼    Active: intense exercise 3-4 times/week",
                                "▼    Very Active: intense exercise 6-7 times/week",
                                "▼    Extra Active: very intense daily exercise"
                                ])
        self.activity_combo.setCurrentIndex(2)

        #Right column
        save_btn = QPushButton("Save", self)
        save_btn.setFixedHeight(60)
        save_btn.setFixedWidth(280)
        save_btn.setFont(QFont("Times New Roman", 20))
        save_btn.setStyleSheet("""
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
        
        save_btn.clicked.connect(self.save_profile)

        #Create profile widget containing form for first profile
        self.new_profile_widget = QWidget()

        profile_col_left_widget = QWidget()
        profile_col_left_widget.setStyleSheet("background-color: #24201f")

        profile_col_center_widget = QWidget()
        profile_col_center_widget.setFixedWidth(600)
        profile_col_center_widget.setStyleSheet("background-color: #24201f")

        profile_col_center_layout = QVBoxLayout()
        profile_col_center_layout.setContentsMargins(0, 0, 0, 0)
        profile_col_center_layout.setSpacing(20)

        profile_row3_center_widget = QWidget()
        profile_row3_center_widget.setFixedHeight(60)

        profile_row3_center_layout = QHBoxLayout()
        profile_row3_center_layout.setContentsMargins(0, 0, 0, 0)
        profile_row3_center_layout.setSpacing(6)

        profile_row3_center_layout.addWidget(self.day_text)
        profile_row3_center_layout.addWidget(self.month_text)
        profile_row3_center_layout.addWidget(self.year_text)

        profile_row3_center_widget.setLayout(profile_row3_center_layout)

        profile_row4_center_widget = QWidget()
        profile_row4_center_widget.setFixedHeight(60)

        profile_row4_center_layout = QHBoxLayout()
        profile_row4_center_layout.setContentsMargins(0, 0, 0, 0)
        profile_row4_center_layout.setSpacing(6)

        profile_row4_center_layout.addWidget(self.foot_height_text)
        profile_row4_center_layout.addWidget(self.inch_height_text)

        profile_row4_center_widget.setLayout(profile_row4_center_layout)

        profile_row5_center_widget = QWidget()
        profile_row5_center_widget.setFixedHeight(60)

        profile_row5_center_layout = QHBoxLayout()
        profile_row5_center_layout.setContentsMargins(0, 0, 0, 0)
        profile_row5_center_layout.setSpacing(6)

        profile_row5_center_layout.addWidget(self.weight_text)
        profile_row5_center_layout.addWidget(self.weight_combo)

        profile_row5_center_widget.setLayout(profile_row5_center_layout)


        profile_col_center_layout.addStretch()
        profile_col_center_layout.addSpacing(120)
        profile_col_center_layout.addWidget(self.profile_picture, alignment=Qt.AlignHCenter)
        profile_col_center_layout.addSpacing(140)
        profile_col_center_layout.addWidget(self.name_text)
        profile_col_center_layout.addWidget(profile_row3_center_widget)
        profile_col_center_layout.addWidget(profile_row4_center_widget)
        profile_col_center_layout.addWidget(profile_row5_center_widget)
        profile_col_center_layout.addWidget(self.activity_combo)
        profile_col_center_layout.addSpacing(140)
        

        profile_col_center_widget.setLayout(profile_col_center_layout)

        profile_col_right_widget = QWidget()
        profile_col_right_widget.setStyleSheet("background-color: #24201f")

        profile_col_right_layout = QVBoxLayout()
        profile_col_right_layout.setContentsMargins(0, 0, 0, 0)
        profile_col_right_layout.setSpacing(20)

        profile_col_right_layout.addStretch()
        profile_col_right_layout.addSpacing(20)
        profile_col_right_layout.addWidget(save_btn)
        profile_col_right_layout.addSpacing(140)

        profile_col_right_widget.setLayout(profile_col_right_layout)

        new_profile_layout = QHBoxLayout()
        new_profile_layout.setContentsMargins(0, 0, 0, 0)
        new_profile_layout.setSpacing(0)

        new_profile_layout.addWidget(profile_col_left_widget)
        new_profile_layout.addWidget(profile_col_center_widget)
        new_profile_layout.addWidget(profile_col_right_widget)
        self.new_profile_widget.setLayout(new_profile_layout)

        self.central_layout.insertWidget(1, self.new_profile_widget)
        self.central_widget.setLayout(self.central_layout)


    #Check if the current text field is empty and show error color on border - only after typing and removing input
    def is_empty(self, text):
        if not text.text():
            self.can_save_profile = False
            text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid #c32157; border-radius: 14px")
        else:
            self.can_save_profile = True
            text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid #000000; border-radius: 14px")

    def save_profile(self):

        #Check to see if the profile name exists
        name = self.name_text.text()
        for profile_name in self.local_profiles.profile:
            if profile_name == self.name_text.text():
                self.can_save_profile = False
                self.name_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid #c32157; border-radius: 14px")
                
        #Confirm that the day/month/year is valid
        
        try:
            day = int(self.day_text.text())

            if day < 1 or day > 31:
                self.can_save_profile = False
                self.day_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid #c32157; border-radius: 14px")

        except ValueError:
            self.can_save_profile = False
            self.day_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid #c32157; border-radius: 14px")

        try:
            month = int(self.month_text.text())

            if month < 1 or month > 12:
                self.can_save_profile = False
                self.month_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid #c32157; border-radius: 14px")

        except ValueError:
            self.can_save_profile = False
            self.month_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid #c32157; border-radius: 14px")

        try:
            year = int(self.year_text.text())

            if year < 1900 or year > 2025:
                self.can_save_profile = False
                self.year_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid #c32157; border-radius: 14px")

        except ValueError:
            self.can_save_profile = False
            self.year_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid #c32157; border-radius: 14px")

        dob = []
        dob.append(day)
        dob.append(month)
        dob.append(year)

        #Confirm that the height Ft/In is valid
        ft = ""
        inch = ""

        try:
            ft = int(self.foot_height_text.text())

            if ft < 0 or ft > 9:
                self.can_save_profile = False
                self.foot_height_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid #c32157; border-radius: 14px")

        except ValueError:
            self.can_save_profile = False
            self.foot_height_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid #c32157; border-radius: 14px")

        try:
            inch = int(self.inch_height_text.text())

            if inch < 0 or inch > 11:
                self.can_save_profile = False
                self.inch_height_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid #c32157; border-radius: 14px")

        except ValueError:
            self.can_save_profile = False
            self.inch_height_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid #c32157; border-radius: 14px")

        height = []
        height.append(ft)
        height.append(inch)

        #Confirm that the height weight is valid
        weight_number = ""
        try:
            weight_number = float(self.weight_text.text())

            if weight_number < 1 or weight_number > 2000:
                self.can_save_profile = False
                self.weight_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid #c32157; border-radius: 14px")

            weight_number = float(f"{weight_number:.1f}")

        except ValueError:
            self.can_save_profile = False
            self.weight_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid #c32157; border-radius: 14px")

        weight = []
        weight.append(weight_number)
        weight.append(self.weight_combo.currentIndex())

        #Activity - does not require validation checking
        activity = self.activity_combo.currentIndex()

        if self.can_save_profile == True:
            self.local_profiles.add_profile(
                name, 
                dob, 
                height, 
                weight, 
                activity
                )

            profile_update = {
                name: {
                    "dob": {
                        "day": self.local_profiles.profile[name].dob[0],
                        "month": self.local_profiles.profile[name].dob[1],
                        "year": self.local_profiles.profile[name].dob[2]
                    }, 
                    "height": {
                        "ft": self.local_profiles.profile[name].height[0],
                        "inch": self.local_profiles.profile[name].height[1]
                    }, 
                    "weight": {
                        "unit": self.local_profiles.profile[name].weight[0],
                        "kg/lb": self.local_profiles.profile[name].weight[1]
                    }, 
                    "activity": self.local_profiles.profile[name].activity
                }
            }

            self.json_profiles.append(profile_update)

            with open('./src/data.json', 'w') as f:
                json.dump(self.data, f, indent=4)

            self.central_layout.removeWidget(self.new_profile_widget)
            self.new_profile_widget.setParent(None)
            self.new_profile_widget.deleteLater()

            self.tabs_widget.show()

    def tab_switcher(self):
        #TODO - Logic for switching widgets when a tab is pressed to call a new page
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


class Profile:
    def __init__(self, dob, height, weight, activity):
        self.dob = dob
        self.height = height
        self.weight = weight
        self.activity = activity

class Profiles:
    def __init__(self):
        self.profile = {}

    def add_profile(self, name, dob, height, weight, activity):
        self.profile[name] = Profile(dob, height, weight, activity)   

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()