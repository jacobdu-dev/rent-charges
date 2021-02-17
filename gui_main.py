from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication
import sys
from household import House
from pathlib import Path


house = House() #global object


def getrentbreakdown():
    rentbreakdown = ""
    rentbreakdown += "Member Rent Breakdown: \n"
    for uid, amount in house.rent.items():
        rentbreakdown += "{:<15}    ${:<}\n".format(house.members[uid], amount)
    rentbreakdown += "Total Monthly Collection: ${:.2f}".format(sum(list(house.rent.values())) + house.operatorrent)
    return rentbreakdown

def getrecenttransactions(n):
    transactions = ""
    transactions += "Recent Transactions: \n"
    for date, transtype, amount, message, name in [("Date", "Transaction Type", "Amount", "Request Message", "Name")] + house.transactions[::-1]:
        n -= 1
        if n == 0: break
        transactions += "{:<12}     {:<16}    {:<10}    {:<20}    {:<}\n".format(date, transtype, amount, message, name)
    return transactions


class Ui_send_charge(object):
    def setupUi(self, send_charge):
        send_charge.setObjectName("send_charge")
        send_charge.resize(312, 388)
        self.centralwidget = QtWidgets.QWidget(send_charge)
        self.centralwidget.setObjectName("centralwidget")
        self.radio_rent = QtWidgets.QRadioButton(self.centralwidget)
        self.radio_rent.setGeometry(QtCore.QRect(100, 20, 61, 21))
        self.radio_rent.setChecked(True)
        self.radio_rent.setObjectName("radio_rent")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 20, 81, 21))
        self.label.setObjectName("label")
        self.radio_other = QtWidgets.QRadioButton(self.centralwidget)
        self.radio_other.setGeometry(QtCore.QRect(170, 20, 61, 21))
        self.radio_other.setObjectName("radio_other")
        self.check_splitbyrent = QtWidgets.QCheckBox(self.centralwidget)
        self.check_splitbyrent.setGeometry(QtCore.QRect(10, 50, 201, 20))
        self.check_splitbyrent.setObjectName("check_splitbyrent")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 110, 161, 16))
        self.label_2.setObjectName("label_2")
        self.text_requestmessage = QtWidgets.QLineEdit(self.centralwidget)
        self.text_requestmessage.setGeometry(QtCore.QRect(10, 130, 291, 21))
        self.text_requestmessage.setObjectName("text_requestmessage")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(10, 80, 101, 16))
        self.label_3.setObjectName("label_3")
        self.text_charge_amount = QtWidgets.QLineEdit(self.centralwidget)
        self.text_charge_amount.setGeometry(QtCore.QRect(120, 80, 181, 21))
        self.text_charge_amount.setObjectName("text_charge_amount")
        self.list_members_charged = QtWidgets.QListView(self.centralwidget)
        self.list_members_charged.setGeometry(QtCore.QRect(10, 180, 291, 141))
        self.list_members_charged.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.list_members_charged.setObjectName("list_members_charged")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(10, 160, 161, 16))
        self.label_4.setObjectName("label_4")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(70, 330, 171, 32))
        self.pushButton.setObjectName("pushButton")
        send_charge.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(send_charge)
        self.statusbar.setObjectName("statusbar")
        send_charge.setStatusBar(self.statusbar)

        self.retranslateUi(send_charge)
        QtCore.QMetaObject.connectSlotsByName(send_charge)

    def retranslateUi(self, send_charge):
        _translate = QtCore.QCoreApplication.translate
        send_charge.setWindowTitle(_translate("send_charge", "Rent Manager - Send Charges"))
        self.radio_rent.setText(_translate("send_charge", "Rent"))
        self.label.setText(_translate("send_charge", "Charge Type"))
        self.radio_other.setText(_translate("send_charge", "Other"))
        self.check_splitbyrent.setText(_translate("send_charge", "Split by Rent Distribution"))
        self.label_2.setText(_translate("send_charge", "Venmo Request Message"))
        self.label_3.setText(_translate("send_charge", "Charge Amount"))
        self.label_4.setText(_translate("send_charge", "Members Charged"))
        self.pushButton.setText(_translate("send_charge", "Send Venmo Request"))

class ProfileSelection(QtWidgets.QMainWindow, Ui_send_charge):
    def __init__(self, parent=None):
        super(ProfileSelection, self).__init__(parent)
        self.setupUi(self)

class Ui_main_view(object):
    def setupUi(self, main_view):
        main_view.setObjectName("main_view")
        main_view.resize(480, 483)
        main_view.setMinimumSize(QtCore.QSize(480, 483))
        main_view.setMaximumSize(QtCore.QSize(480, 483))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        main_view.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(main_view)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 20, 131, 16))
        self.label.setObjectName("label")
        self.rent_burden = QtWidgets.QLineEdit(self.centralwidget)
        self.rent_burden.setGeometry(QtCore.QRect(160, 20, 113, 20))
        self.rent_burden.setText(str(round(float(house.totalrent), 2)))
        self.rent_burden.setMaxLength(8)
        self.rent_burden.setReadOnly(True)
        self.rent_burden.setPlaceholderText("")
        self.rent_burden.setObjectName("rent_burden")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 50, 101, 20))
        self.label_2.setObjectName("label_2")
        self.oprent = QtWidgets.QLineEdit(self.centralwidget)
        self.oprent.setGeometry(QtCore.QRect(130, 50, 113, 20))
        self.oprent.setText(str(round(float(house.operatorrent), 2)))
        self.oprent.setMaxLength(8)
        self.oprent.setReadOnly(True)
        self.oprent.setPlaceholderText("")
        self.oprent.setObjectName("oprent")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(20, 80, 121, 16))
        self.label_3.setObjectName("label_3")
        self.rent_breakdown = QtWidgets.QTextEdit(self.centralwidget)
        self.rent_breakdown.setGeometry(QtCore.QRect(20, 100, 441, 131))
        self.rent_breakdown.setText(getrentbreakdown())
        self.rent_breakdown.setReadOnly(True)
        self.rent_breakdown.setObjectName("rent_breakdown")
        self.recent_transactions = QtWidgets.QTextEdit(self.centralwidget)
        self.recent_transactions.setGeometry(QtCore.QRect(20, 260, 441, 131))
        self.recent_transactions.setText(getrecenttransactions(10))
        self.recent_transactions.setReadOnly(True)
        self.recent_transactions.setObjectName("recent_transactions")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(20, 240, 161, 16))
        self.label_4.setObjectName("label_4")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(20, 410, 111, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(190, 410, 101, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(350, 410, 111, 23))
        self.pushButton_3.setObjectName("pushButton_3")
        main_view.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(main_view)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 480, 22))
        self.menubar.setObjectName("menubar")
        self.menuProfile = QtWidgets.QMenu(self.menubar)
        self.menuProfile.setObjectName("menuProfile")
        main_view.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(main_view)
        self.statusbar.setObjectName("statusbar")
        main_view.setStatusBar(self.statusbar)
        self.actionSave = QtWidgets.QAction(main_view)
        self.actionSave.setObjectName("actionSave")
        self.menuProfile.addAction(self.actionSave)
        self.menubar.addAction(self.menuProfile.menuAction())

        self.retranslateUi(main_view)
        QtCore.QMetaObject.connectSlotsByName(main_view)

    def retranslateUi(self, main_view):
        _translate = QtCore.QCoreApplication.translate
        main_view.setWindowTitle(_translate("main_view", "Rent Manager"))
        self.label.setText(_translate("main_view", "Monthly Rent Burden"))
        self.label_2.setText(_translate("main_view", "Operator Rent"))
        self.label_3.setText(_translate("main_view", "Rent Breakdown"))
        self.label_4.setText(_translate("main_view", "Recent Transactions"))
        self.pushButton.setText(_translate("main_view", "Send Charges"))
        self.pushButton_2.setText(_translate("main_view", "Edit Profile"))
        self.pushButton_3.setText(_translate("main_view", "Save and Quit"))
        self.menuProfile.setTitle(_translate("main_view", "Profile"))
        self.actionSave.setText(_translate("main_view", "Save"))


class MainView(QtWidgets.QMainWindow, Ui_main_view):
    def __init__(self, parent=None):
        super(MainView, self).__init__(parent)
        self.setupUi(self)

class Ui_Rent_Manager_ProfileSelect(object):
    def setupUi(self, Rent_Manager_ProfileSelect):
        Rent_Manager_ProfileSelect.setObjectName("Rent_Manager_ProfileSelect")
        Rent_Manager_ProfileSelect.resize(441, 248)
        Rent_Manager_ProfileSelect.setMinimumSize(QtCore.QSize(441, 248))
        Rent_Manager_ProfileSelect.setMaximumSize(QtCore.QSize(441, 248))
        Rent_Manager_ProfileSelect.setMouseTracking(False)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Rent_Manager_ProfileSelect.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(Rent_Manager_ProfileSelect)
        self.centralwidget.setObjectName("centralwidget")
        self.new_profile = QtWidgets.QPushButton(self.centralwidget)
        self.new_profile.setGeometry(QtCore.QRect(50, 150, 121, 51))
        self.new_profile.setObjectName("new_profile")
        self.import_profile = QtWidgets.QPushButton(self.centralwidget)
        self.import_profile.setGeometry(QtCore.QRect(270, 150, 121, 51))
        self.import_profile.setObjectName("import_profile")
        self.import_profile.clicked.connect(self.importprofile)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(150, 30, 251, 51))
        font = QtGui.QFont()
        font.setPointSize(26)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 10, 141, 121))
        self.label_2.setPixmap(QtGui.QPixmap("icon.png"))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(310, 90, 91, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        Rent_Manager_ProfileSelect.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(Rent_Manager_ProfileSelect)
        self.statusbar.setObjectName("statusbar")
        Rent_Manager_ProfileSelect.setStatusBar(self.statusbar)

        self.retranslateUi(Rent_Manager_ProfileSelect)
        QtCore.QMetaObject.connectSlotsByName(Rent_Manager_ProfileSelect)

    def importprofile(self):
        home_dir = str(Path.home())
        file_path, ext = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', home_dir, "prex(*.prex)")
        if file_path != '':
            house.importf(file_path)
            mainView = MainView(self)
            mainView.show()

    def retranslateUi(self, Rent_Manager_ProfileSelect):
        _translate = QtCore.QCoreApplication.translate
        Rent_Manager_ProfileSelect.setWindowTitle(_translate("Rent_Manager_ProfileSelect", "Rent Manager - Profile Selection"))
        Rent_Manager_ProfileSelect.setWhatsThis(_translate("Rent_Manager_ProfileSelect", "<html><head/><body><p>Rent Manager - Profile Selection</p><p><br/></p></body></html>"))
        self.new_profile.setText(_translate("Rent_Manager_ProfileSelect", "New Profile"))
        self.import_profile.setText(_translate("Rent_Manager_ProfileSelect", "Import Profile"))
        self.label.setText(_translate("Rent_Manager_ProfileSelect", "Rent Manager"))
        self.label_3.setText(_translate("Rent_Manager_ProfileSelect", "by Jacob Du"))



class ProfileSelection(QtWidgets.QMainWindow, Ui_Rent_Manager_ProfileSelect):
    def __init__(self, parent=None):
        super(ProfileSelection, self).__init__(parent)
        self.setupUi(self)


#defining windows
app = QApplication(sys.argv)
profileSelect = ProfileSelection()
profileSelect.show()
app.exec_()
