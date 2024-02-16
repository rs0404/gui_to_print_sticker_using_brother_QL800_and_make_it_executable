import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox
from PyQt5.QtGui import QRegExpValidator, QPalette
from PyQt5.QtCore import QRegExp, Qt
from create_sale_sticker import print_ID

class LabelPrinterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.userData = []

    def initUI(self):
        # Layouts
        mainLayout = QVBoxLayout()
        formLayout = QVBoxLayout()
        buttonLayout = QHBoxLayout()

        # Validators
        nameRegExp = QRegExp("^[a-zA-Z]+(?:[-'\\s][a-zA-Z]+)*$")
        addressRegExp = QRegExp("^[a-zA-Z0-9\\s,.-]+$")
        phoneRegExp = QRegExp("^(\+\d{1,3})?\s?(9\d{9}|0\d{8})$")

        # Form fields
        self.nameInput = QLineEdit(self)
        self.addressInput = QLineEdit(self)
        self.phoneInput = QLineEdit(self)
        self.paymentComboBox = QComboBox(self)
        self.paymentComboBox.addItems(['COD (2500)', "Esewa (2500)", "Bank(200)"])


        # Set validators
        self.nameInput.setValidator(QRegExpValidator(nameRegExp, self.nameInput))
        self.addressInput.setValidator(QRegExpValidator(addressRegExp, self.addressInput))
        self.phoneInput.setValidator(QRegExpValidator(phoneRegExp, self.phoneInput))

        # Add widgets to form layout
        formLayout.addWidget(QLabel('Name:'))
        formLayout.addWidget(self.nameInput)
        formLayout.addWidget(QLabel('Address:'))
        formLayout.addWidget(self.addressInput)
        formLayout.addWidget(QLabel('Phone:'))
        formLayout.addWidget(self.phoneInput)
        formLayout.addWidget(QLabel('Payment:'))
        formLayout.addWidget(self.paymentComboBox)

        # Buttons
        self.printButton = QPushButton('Print', self)
        self.clearButton = QPushButton('Clear', self)
        self.exitButton = QPushButton('Exit', self)
        self.printButton.clicked.connect(self.printLabel)
        self.clearButton.clicked.connect(self.clearData)
        self.exitButton.clicked.connect(self.exit)


        # Add buttons to button layout
        buttonLayout.addWidget(self.printButton)
        buttonLayout.addWidget(self.clearButton)
        buttonLayout.addWidget(self.exitButton)

        # Add layouts to main layout
        mainLayout.addLayout(formLayout)
        mainLayout.addLayout(buttonLayout)

        self.setLayout(mainLayout)
        self.setWindowTitle('Label Printer')
        
        # Connect signal for phone input text changed
        self.phoneInput.textChanged.connect(self.validatePhone)

    def validatePhone(self, text):
        """
        Changes the background color of the phone input field to green if the text matches the phone number pattern.
        """
        palette = self.phoneInput.palette()
        if self.phoneInput.hasAcceptableInput():
            palette.setColor(QPalette.Base, Qt.green)
        else:
            palette.setColor(QPalette.Base, Qt.white)
        self.phoneInput.setPalette(palette)



    def collectData(self):
        """
        Collects data from input fields, validates it, and stores in a dictionary.
        This method could also generate a preview of the label.
        """
        self.userData = [
            self.nameInput.text(),
            self.addressInput.text(),
            self.phoneInput.text(),
            self.paymentComboBox.currentText(),
        ]
        # Here, you could also call a method to generate and display a preview of the label
        print("Data collected: ", self.userData)  # For debugging

    def clearData(self):
        """
        Clears all the input fields in the form.
        """
        self.nameInput.clear()
        self.addressInput.clear()
        self.phoneInput.clear()
        self.paymentComboBox.setCurrentIndex(0)
        self.userData = []
    def exit(self):
        sys.exit()

    def printLabel(self):
        self.collectData()
        print_ID(self.userData)

def main():
    app = QApplication(sys.argv)
    ex = LabelPrinterApp()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
