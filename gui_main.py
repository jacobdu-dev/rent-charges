from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMessageBox, QInputDialog
import sys
from household import House
from pathlib import Path
from gui_overview import Ui_main_view


house = House() #global object


def getrentbreakdown():
    rentbreakdown = ""
    rentbreakdown += "Member Rent Breakdown: \n"
    for uid, amount in house.rent.items():
        rentbreakdown += "{:<15}    ${:<}\n".format(house.members[uid], amount)
    rentbreakdown += "Operator Rent: ${:.2f}\n".format(house.operatorrent)
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



class MainView(QtWidgets.QMainWindow, Ui_main_view):
    def __init__(self, parent=None):
        super(MainView, self).__init__(parent)
        self.setupUi(self)
        self.action_import.triggered.connect(self.importprofile)
        self.radio_rent.toggled.connect(self.set_rent)
        self.radio_other.toggled.connect(self.set_other)
        self.btn_sendrequest.clicked.connect(self.requestcharge)
        self.action_export.triggered.connect(self.export)
        self.action_newprofile.triggered.connect(self.newprofile)
        self.action_addmember.triggered.connect(self.addmember)
        self.action_delmember.triggered.connect(self.delmember)
        self.rent_burden.setValidator(QtGui.QDoubleValidator())
        self.oprent.setValidator(QtGui.QDoubleValidator())
        self.rent_burden.returnPressed.connect(self.updaterent)
        self.oprent.returnPressed.connect(self.updateoprent)
        self.btn_sq.clicked.connect(self.exportq)

    def exportq(self):
        self.export(q=True)
        
    def delmember(self):
        name, ok_pressed = QInputDialog.getItem(self, "Which Member to Remove?", "Select Member", [name for uid, name in house.members.items()], 0, False)
        if ok_pressed:
            for i, j in house.members.items():
                if j == name:
                    house.delmembers(i)
                    break
            msgBox = QtWidgets.QMessageBox(self)
            msgBox.setText('Success!')
            msgBox.setInformativeText("Successfully removed member!")
            msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msgBox.show()
            self.updateview()
    def addmember(self):
        name, ok_pressed = QInputDialog.getText(self, 'Name of New Member', 'Please enter your the name of the new member.')
        if ok_pressed:
            rent, ok_pressed = QInputDialog.getDouble(self, 'Member Rent', 'Please enter monthly rent to be collected from this member.')
            if ok_pressed:
                venmo, ok_pressed = QInputDialog.getText(self, 'Venmo Username', "Please enter {}'s Venmo Username.".format(name))
                if ok_pressed:
                    uid = 1
                    while True:
                        if uid in house.members.keys():
                            uid += 1
                        else:
                            break
                    re = house.addmembers(uid, name, float(rent), venmo)
                    if re:
                        msgBox = QtWidgets.QMessageBox(self)
                        msgBox.setText('Success!')
                        msgBox.setInformativeText("Successfully added member!")
                        msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                        msgBox.show()
                        self.updateview()

    def updaterent(self):
        house.totalrent = float(self.rent_burden.text())
        self.updateview()

    def updateoprent(self):
        house.operatorrent = float(self.oprent.text())
        self.updateview()

    def requestcharge(self):
        if self.radio_rent.isChecked():
            venmomsg = str(self.text_requestmessage.text())
            re = house.chargerent(venmomsg)
            if re != True:
                error_dialog = QtWidgets.QErrorMessage(self)
                boolval, error = re
                error_dialog.showMessage(error)
            else:
                self.updateview()
        elif self.radio_other.isChecked():
            splitbyrent = self.check_splitbyrent.isChecked()
            venmomsg = str(self.text_requestmessage.text())
            uids = [int(i.text()[0]) for i in self.list_members_charged.selectedItems()]
            if len(uids) != 0 :
                if self.text_charge_amount.text() != '':
                    if float(self.text_charge_amount.text()) > 0:
                        re = house.chargeothers(float(self.text_charge_amount.text()), uids, venmomsg, splitbyrent)
                        if re != True:
                            error_dialog = QtWidgets.QErrorMessage(self)
                            boolval, error = re
                            error_dialog.showMessage(error)
                        else:
                            self.updateview()


    def set_rent(self):
        self.check_splitbyrent.setEnabled(False)
        self.text_charge_amount.setText(str(round(float(house.totalrent), 2)))
        self.text_charge_amount.setReadOnly(True)
        self.list_members_charged.clear()
        self.list_members_charged.addItem("All members will be charged.")

    def set_other(self):
        self.check_splitbyrent.setEnabled(True)
        self.text_charge_amount.setText(str(round(float(0), 2)))
        self.text_charge_amount.setReadOnly(False)
        self.list_members_charged.clear()
        for uid, member in house.members.items():
            self.list_members_charged.addItem("{}    {}".format(uid, member))

    def newprofile(self):
        token, ok_pressed = QInputDialog.getText(self, 'Access Token', 'Please enter your venmo access token.')
        if ok_pressed:
            totalrent, ok_pressed = QInputDialog.getDouble(self, 'Rent Burden', 'Please enter the total monthly rent burden.')
            if ok_pressed:
                operatorrent, ok_pressed = QInputDialog.getDouble(self, 'Operator Rent', 'Please enter the operator rent (How much your rent is per month).')
                if ok_pressed:
                    house.token = token
                    house.totalrent = totalrent
                    house.operatorrent = operatorrent
                    msgBox = QtWidgets.QMessageBox(self)
                    msgBox.setText('Success!')
                    msgBox.setInformativeText("Profile was created. Please do not forget to save profile when you're finished adding members")
                    msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                    msgBox.show()
                    house.startclient()
                    self.updateview()

    def export(self, q = False):
        home_dir = str(Path.home())
        file_path, ext = QtWidgets.QFileDialog.getSaveFileName(self, 'Export file', home_dir, "prex(*.prex)")
        if file_path != '':
            house.export(file_path)
            if q:
                sys.exit()
            else:
                self.updateview()

    def importprofile(self):
        home_dir = str(Path.home())
        file_path, ext = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', home_dir, "prex(*.prex)")
        if file_path != '':
            house.importf(file_path)
            house.startclient()
            self.updateview()

    def updateview(self):
        self.rent_burden.setText(str(round(float(house.totalrent), 2)))
        self.oprent.setText(str(round(float(house.operatorrent), 2)))
        self.rent_breakdown.setText(getrentbreakdown())
        self.recent_transactions.setText(getrecenttransactions(10))
        self.text_charge_amount.setText(str(round(float(0), 2)))
        self.check_splitbyrent.setChecked(False)
        self.text_requestmessage.setText("")

#defining windows
app = QApplication(sys.argv)
mainView = MainView()
mainView.show()
app.exec_()
