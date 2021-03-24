from PyQt5 import QtWidgets


class ListDialog(QtWidgets.QDialog):
    def __init__(self, di: dict):
        QtWidgets.QDialog.__init__(self)
        self.result = ""
        self.dictionary = di
        layout = QtWidgets.QVBoxLayout()
        self.array = list(di.keys())

        for i in di.keys():
            radio_button = QtWidgets.QRadioButton(i)
            radio_button.toggled.connect(self.radioToggle)
            layout.addWidget(radio_button)
        confirm_button = QtWidgets.QPushButton("Bestätigen")
        confirm_button.clicked.connect(self.confirm)
        layout.addWidget(confirm_button)
        self.setLayout(layout)

    def radioToggle(self):
        rb = self.sender()
        txt = rb.text()
        self.result = self.array.index(txt)

    def confirm(self):
        if self.result == "":
            QtWidgets.QMessageBox.information(self, "Error", "One item must be selected")
            return
        self.done(self.result)
        return self.result

