import sys
import json
import datetime
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton
from PyQt5.QtGui import QFont

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.profiles = True

        #Initiation methods
        self.read_data_file()
        self.initUI()
        self.initGrid()

        #Setting window properties
        self.setWindowTitle("Munchy")
        self.setGeometry(800, 800, 1400, 900)
        self.setStyleSheet("background-color: #3c3c3c")

    def read_data_file(self):
        #TODO - read profile/theme/data from json
        with open('./src/data.json', 'r') as f:
            data = json.load(f)
            self.profiles = data['profiles']
            self.consumables = data['consumables']
            self.recipes = data['recipes']

    def initUI(self):
        #TODO - 
            #Create UI for:
                #Titlebar and tabs
                #Profile page
                #Consumables page
                #Recipes page
                #Planner page
                #Pantry page
                #Shopping list page

        #title bar

        self.title_label = QLabel("Munchy", self)
        self.title_label.setFont(QFont("Arial", 14))
        self.title_label.setStyleSheet("text-align: center")

        self.min_button = QPushButton("_", self)
        self.min_button.setFont(QFont("Arial", 14))
        self.min_button.setFixedWidth(40)
        self.min_button.setFixedHeight(28)
        self.min_button.clicked.connect(self.showMinimized)

        self.max_button = QPushButton("O", self)
        self.max_button.setFont(QFont("Arial", 14))
        self.max_button.setFixedWidth(40)
        self.max_button.setFixedHeight(28)
        self.max_button.clicked.connect(self.showMaximized)

        self.exit_button = QPushButton("X", self)
        self.exit_button.setFont(QFont("Arial", 14))
        self.exit_button.setFixedWidth(40)
        self.exit_button.setFixedHeight(28)
        self.exit_button.clicked.connect(QApplication.instance().quit)

        self.blank_space = QLabel("")


        #Application widget is the container shown in the window 
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        #Application grid(custom - vbox and hbox) is the layout structure of internal widgets
        vbox = QVBoxLayout()
        titlebar = QHBoxLayout()
        test = QHBoxLayout()
        test2 = QHBoxLayout()

        titlebar.addStretch()
        titlebar.addWidget(self.title_label)
        titlebar.addStretch()
        titlebar.addWidget(self.min_button)
        titlebar.addWidget(self.max_button)
        titlebar.addWidget(self.exit_button)
        vbox.addLayout(titlebar)

        vbox.addStretch()

        central_widget.setLayout(vbox)

        if not self.profiles:
            #initial_login()
            print("no created profiles")
        
        else:
            pass

    def initGrid(self):
        #TODO - Set up the initial grid with titlebar, profile page and tabs
        pass

    def tab_switcher(self):
        #TODO - Logic for switching widgets when a tab is pressed to call a new page
        pass

    def initial_login(self):
        #TODO - Logic called by default when there is no saved profiles
        #Sets an overlay allowing user to create a profile
        save_profile()
        #Then remove the overlay
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