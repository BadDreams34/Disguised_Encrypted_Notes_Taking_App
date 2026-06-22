'''Encrypted Notes Taking App
Program to secretly take notes and store them with no clues left behind'''

import sys
from encodings import utf_8
import datetime
import encryption
import PySide6
from PySide6 import QtCore , QtGui , QtWidgets

# after encrypting IF THE PASSWORD IS RIGHT HOW DO I KNOW
# just check if the previous decryption is passing on with the current password !


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.password = ''

        self.setWindowTitle("Unsevered")
        layout = QtWidgets.QVBoxLayout()
        self.box = QtWidgets.QComboBox()
        self.box.addItems(["Access used","Password"])
        self.box.setCurrentIndex(-1)
        layout.addWidget(self.box)
        self.box.hide()

        self.lineedit = QtWidgets.QLineEdit()

        self.lineedit.setPlaceholderText("Use Me !")
        self.used = QtWidgets.QPushButton("save it !!!")




        layout.addWidget(self.lineedit)
        layout.addWidget(self.used)


        #the top text
        label = QtWidgets.QLabel("Its not a guarentee that you are gonna never forget this program ! ")
        font = label.font()
        font.setPointSize(30)
        label.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(label)

        #lets make it super ugly
        g_search = QtWidgets.QLabel()
        g_search.setPixmap(QtGui.QPixmap("img_1.png"))
        g_search.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)

        #checkbox
        self.checkbox = QtWidgets.QCheckBox("You gotta check it !")

        layout.addWidget(self.checkbox, alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)

        self.checkbox.clicked.connect(self.checkbox_state)
        self.used.clicked.connect(self.on_save_data)

        layout.addWidget(g_search)
        central_widget = QtWidgets.QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        self.box.currentTextChanged.connect(self.opt_selected)

    def checkbox_state(self,state):
        self.checkbox.setEnabled(False)
        self.box.show()
    def on_save_data(self):
        text = self.lineedit.text() #pass password before ,
        if text:
            dt = datetime.datetime.now()
            line = f"{dt.strftime("%d %b, %Y %H:%M:%S")} {text}"
            password = text.split(',')[0]

            with open("enc.txt", "rb") as file:
                text = file.read()
            if len(text) != 0:
                if encryption.decrypt_file("enc.txt", password) == 0:
                    print("Incorrect password")
                    return

            with open("enc.txt", 'ab') as file:
                file.write((line + '\n').encode('utf-8'))

            encryption.encrypt_file("enc.txt",password)

        self.lineedit.clear()

    def opt_selected(self,text):
        if text == "Access used":
            print("Needs a pass")
            passw = input("Give the password")
            encryption.decrypt_file("enc.txt", passw)

app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()