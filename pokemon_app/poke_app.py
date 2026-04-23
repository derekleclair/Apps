import os
import sys
import json
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QFontDatabase, QFont, QGuiApplication, Qt
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QLineEdit,
    QListWidget,
    QMainWindow,
    QSlider,
    QSpinBox,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QSpacerItem,
    QSizePolicy,
    QWidget,
    QFrame,
)
from PySide6.QtWidgets import QSizePolicy
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pokedex App")
        font_id = QFontDatabase.addApplicationFont("pkmn_font.ttf")
        if font_id != -1:
            font_families = QFontDatabase.applicationFontFamilies(font_id)
            pokemon_font = QFont(font_families[0],24)
        else:
            print("loading failed")
            pokemon_font = QFont("Arial", 16)
        poke_font = QFont(pokemon_font)
        poke_font.setPointSize(10)
        self.poke_image = QLabel()
        self.poke_desc = QLabel()
        self.poke_desc.setWordWrap(True)
        self.poke_desc.setFixedWidth(700)
        self.poke_desc.setFont(poke_font)
        self.lineedit = QLineEdit()
        self.lineedit.setMaxLength(12)
        self.lineedit.setFont(poke_font)
        self.lineedit.setPlaceholderText("Enter Pokemon Name")

        self.lineedit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout = QVBoxLayout()
        self.frame = QFrame()
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.lineedit.returnPressed.connect(self.return_pressed)
        self.setCentralWidget(self.lineedit)
        layout = QVBoxLayout()
        layout.addStretch()
        layout.addWidget(self.poke_image, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.poke_desc, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(self.lineedit, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()
        layout.setSpacing(10)
        layout.setContentsMargins(10,10,10,10)
        self.frame.setLayout(layout)
        main_layout.addWidget(self.frame)
        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

#size policy for widgets

        self.lineedit.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        self.poke_image.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        self.poke_desc.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)






    def return_pressed(self):
        print("return pressed")
        search_mon = self.lineedit.text()
        self.lineedit.setText("")        
        
        try:
            with open("dex.json","r") as file:
                pokemon_data = json.load(file)

            for pokemon in pokemon_data:
                if pokemon["name"]["english"].lower() == search_mon.lower():
                    print(f"{pokemon["id"]}")           
                    print(f"{search_mon}, the {pokemon["species"]}")
                    print(f"{pokemon["description"]}")
                    description = pokemon["description"]
                    pokedex_number = pokemon["id"]
                    species = pokemon["species"]

                    folder = "poke_sprites"
                    file_name = f"{folder}/{pokedex_number:03}.png"
                    pixmap = QPixmap(file_name)
            self.poke_image.setPixmap(pixmap.scaled(300,300, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.FastTransformation))
            self.poke_desc.setText(f"{search_mon}, the {species} \n \n {description}")
            self.poke_desc.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        except UnboundLocalError:
            self.poke_desc.setText("Pokemon or Image not found")
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    with open("style.qss", "r") as f:
        style = f.read()
    app.setStyleSheet(style)
    window.show()
    app.exec()
