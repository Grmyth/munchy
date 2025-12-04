import sys
import json
import datetime
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QLabel, QLineEdit, QComboBox, QPushButton
from PyQt5.QtGui import QFont

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        #Initiation methods
        self.read_data_file()
        self.initUI()

        #Setting window properties
        self.setWindowTitle("Munchy")
        self.setMinimumSize(1400, 1100)
        self.setMaximumSize(1400, 1100)
        self.setStyleSheet("background-color: #24201f")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.oldPos = self.pos()

    def mousePressEvent(self, event):
        x = event.pos().x()
        y = event.pos().y()

        width = self.width()

        if (0 < x < width - 96 and 0 < y < 44):
            self.dragging = True
            self.oldPos = event.globalPos()
        else:
            self.dragging = False

    def mouseMoveEvent(self, event):

        if self.dragging:
            delta = QPoint(event.globalPos() - self.oldPos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPos()
    
    def mouseReleaseEvent(self, event):
        self.dragging = False

    def read_data_file(self):
        #TODO - read profile/theme/data from json
        with open('./src/data.json', 'r') as f:
            data = json.load(f)
            self.profiles = data['profiles']
            self.consumables = data['consumables']
            self.recipes = data['recipes']

    def initUI(self):

        #title bar elements
        self.title_label = QLabel("", self)
        self.title_label.setFixedWidth(280)
        self.title_label.setFixedHeight(44)
        self.title_label.setStyleSheet("image: url(./assets/titlebar/title.png)")

        self.min_button = QPushButton("", self)
        self.min_button.setFixedWidth(48)
        self.min_button.setFixedHeight(44)
        self.min_button.setFocusPolicy(Qt.NoFocus)
        self.min_button.clicked.connect(self.showMinimized)
        self.min_button.setStyleSheet("""
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

        self.exit_button = QPushButton("", self)
        self.exit_button.setFixedWidth(48)
        self.exit_button.setFixedHeight(44)
        self.exit_button.setFocusPolicy(Qt.NoFocus)
        self.exit_button.clicked.connect(QApplication.instance().quit)
        self.exit_button.setStyleSheet("""
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
        titlebar_layout.addWidget(self.title_label)
        titlebar_layout.addStretch()
        titlebar_layout.addWidget(self.min_button)
        titlebar_layout.addWidget(self.exit_button)

        #Applying the titlebar layout to the titlebar widget
        titlebar_widget.setLayout(titlebar_layout)

        #Adding the titlebar as a widget of the central widget layout
        self.central_layout.addWidget(titlebar_widget, 0)

        if not self.profiles:
            self.initial_login()
            pass

    def initial_login(self):
        #TODO - Logic called by default when there is no saved profiles


        #Profile widget elements

        #Center column - Row 1 - Profile picture
        profile_picture = QLabel(self)
        profile_picture.setFixedHeight(260)
        profile_picture.setFixedWidth(260)
        profile_picture.setStyleSheet("background-color: #171514; border: 2px solid black; border-radius: 20px")

        #Center column - Row 2 - Name
        name_text = QLineEdit(self)
        name_text.setPlaceholderText("Name")
        name_text.setFixedHeight(60)
        name_text.setAlignment(Qt.AlignCenter)
        name_text.setFont(QFont("Times New Roman", 20))
        name_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid black; border-radius: 14px")

        #Center column - Row 3 - D.O.B
            
            #elements left to right
            
        # -- element 1 --
        day_text = QLineEdit(self)
        day_text.setPlaceholderText("DD")
        day_text.setFixedHeight(60)
        day_text.setFixedWidth(146)
        day_text.setAlignment(Qt.AlignCenter)
        day_text.setFont(QFont("Times New Roman", 20))
        day_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid black; border-radius: 14px")

        # -- element 2 --
        month_text = QLineEdit(self)
        month_text.setPlaceholderText("MM")
        month_text.setFixedHeight(60)
        month_text.setFixedWidth(146)
        month_text.setAlignment(Qt.AlignCenter)
        month_text.setFont(QFont("Times New Roman", 20))
        month_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid black; border-radius: 14px")

        # -- element 3 --
        year_text = QLineEdit(self)
        year_text.setPlaceholderText("YYYY")
        year_text.setFixedHeight(60)
        year_text.setFixedWidth(296)
        year_text.setAlignment(Qt.AlignCenter)
        year_text.setFont(QFont("Times New Roman", 20))
        year_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid black; border-radius: 14px")

        #Center column - Row 4 - Height
            
            #elements left to right

        # -- element 1 --
        height_label = QLabel("Height:", self)
        height_label.setFixedHeight(60)
        height_label.setFixedWidth(296)
        height_label.setAlignment(Qt.AlignCenter)
        height_label.setFont(QFont("Times New Roman", 20))
        height_label.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid black; border-radius: 14px")

        # -- element 2 --
        foot_height_text = QLineEdit(self)
        foot_height_text.setPlaceholderText("FT")
        foot_height_text.setFixedHeight(60)
        foot_height_text.setFixedWidth(146)
        foot_height_text.setAlignment(Qt.AlignCenter)
        foot_height_text.setFont(QFont("Times New Roman", 20))
        foot_height_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid black; border-radius: 14px")

        # -- element 3 --
        inch_height_text = QLineEdit(self)
        inch_height_text.setPlaceholderText("IN")
        inch_height_text.setFixedHeight(60)
        inch_height_text.setFixedWidth(146)
        inch_height_text.setAlignment(Qt.AlignCenter)
        inch_height_text.setFont(QFont("Times New Roman", 20))
        inch_height_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid black; border-radius: 14px")

        #Center column - Row 5
            
            #elements left to right

        # -- element 1 --
        weight_text = QLineEdit(self)
        weight_text.setPlaceholderText("Weight")
        weight_text.setFixedHeight(60)
        weight_text.setFixedWidth(297)
        weight_text.setAlignment(Qt.AlignCenter)
        weight_text.setFont(QFont("Times New Roman", 20))
        weight_text.setStyleSheet("color: #645e59; background-color: #171514; border: 2px solid black; border-radius: 14px")

        # -- element 2 --
        weight_combo = QComboBox(self)
        weight_combo.setFixedHeight(60)
        weight_combo.setFixedWidth(297)
        weight_combo.setFont(QFont("Times New Roman", 20))
        weight_combo.setStyleSheet("""
                                QComboBox {
                                    color: #645e59; background-color: #171514; border: 2px solid black; 
                                    border-radius: 14px; radius: 14px; padding-left: 114 px;
                                }
                                
                                QComboBox::drop-down {
                                    border-top-right-radius: 4px; border-top-right-radius: 4px;
                                }""")

        weight_combo.addItems([
                                "KG's", 
                                "LB's"
                                ])

        #Center column - Row 6
        activity_combo = QComboBox(self)
        activity_combo.setFixedHeight(60)
        activity_combo.setFixedWidth(600)
        activity_combo.setPlaceholderText("Activity")
        activity_combo.setFont(QFont("Times New Roman", 20))
        activity_combo.setStyleSheet("""
                                QComboBox {
                                    color: #645e59; background-color: #171514; border: 2px solid black; 
                                    border-radius: 14px; radius: 14px; padding-left: 40 px;
                                }
                                
                                QComboBox::drop-down {
                                    border-top-right-radius: 4px; border-top-right-radius: 4px;
                                }""")

        activity_combo.addItems([
                                "Sedentary: little or no exercise", 
                                "Light: exercise 1-3 times/week", 
                                "Moderate: exercise 4-5 times/week", 
                                "Active: intense exercise 3-4 times/week",
                                "Very Active: intense exercise 6-7 times/week",
                                "Extra Active: very intense daily exercise"
                                ])

        #Right column - save button
        save_btn = QPushButton("Save", self)
        save_btn.setFixedHeight(60)
        save_btn.setFixedWidth(280)
        save_btn.setFont(QFont("Times New Roman", 20))
        save_btn.setStyleSheet("""
                                color: #645e59; background-color: #171514; border: 2px solid black; 
                                border-radius: 14px; margin-left: 130px; text-align: center;
                            """)

        #Create profile widget containing form for first profile
        profile_widget = QWidget()

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

        profile_row3_center_layout.addWidget(day_text)
        profile_row3_center_layout.addWidget(month_text)
        profile_row3_center_layout.addWidget(year_text)

        profile_row3_center_widget.setLayout(profile_row3_center_layout)

        profile_row4_center_widget = QWidget()
        profile_row4_center_widget.setFixedHeight(60)

        profile_row4_center_layout = QHBoxLayout()
        profile_row4_center_layout.setContentsMargins(0, 0, 0, 0)
        profile_row4_center_layout.setSpacing(6)

        profile_row4_center_layout.addWidget(height_label)
        profile_row4_center_layout.addStretch()
        profile_row4_center_layout.addWidget(foot_height_text)
        profile_row4_center_layout.addWidget(inch_height_text)

        profile_row4_center_widget.setLayout(profile_row4_center_layout)

        profile_row5_center_widget = QWidget()
        profile_row5_center_widget.setFixedHeight(60)

        profile_row5_center_layout = QHBoxLayout()
        profile_row5_center_layout.setContentsMargins(0, 0, 0, 0)
        profile_row5_center_layout.setSpacing(6)

        profile_row5_center_layout.addWidget(weight_text)
        profile_row5_center_layout.addWidget(weight_combo)

        profile_row5_center_widget.setLayout(profile_row5_center_layout)


        profile_col_center_layout.addStretch()
        profile_col_center_layout.addSpacing(120)
        profile_col_center_layout.addWidget(profile_picture, alignment=Qt.AlignHCenter)
        profile_col_center_layout.addSpacing(140)
        profile_col_center_layout.addWidget(name_text)
        profile_col_center_layout.addWidget(profile_row3_center_widget)
        profile_col_center_layout.addWidget(profile_row4_center_widget)
        profile_col_center_layout.addWidget(profile_row5_center_widget)
        profile_col_center_layout.addWidget(activity_combo)
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

        profile_layout = QHBoxLayout()
        profile_layout.setContentsMargins(0, 0, 0, 0)
        profile_layout.setSpacing(0)

        profile_layout.addWidget(profile_col_left_widget)
        profile_layout.addWidget(profile_col_center_widget, alignment=Qt.AlignHCenter)
        profile_layout.addWidget(profile_col_right_widget)
        profile_widget.setLayout(profile_layout)

        self.central_layout.addWidget(profile_widget, stretch=1)
        
        self.central_widget.setLayout(self.central_layout)

        #save_profile()
        #Then remove the overlay
            #pass

    def tab_switcher(self):
        #TODO - Logic for switching widgets when a tab is pressed to call a new page
        pass

    def save_profile(self):
        #TODO - Logic for saving a profile, as this will need to be written to json
        pass
    
    def delete_profile(self):
        #TODO - Logic for deleting a profile
        if not profiles.default:
            #Delete if not the default profile
            pass
        else:
            if profiles.additional:
                #Choose a new default profile
                pass
            else:
                #Delete profile
                profiles.exists == False
                initial_login()
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

    


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()