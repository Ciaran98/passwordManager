# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

from tkinter import dialog
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QVBoxLayout, QHBoxLayout, QLineEdit, QTabWidget
from PyQt5.QtCore import QRect, QTimer
import pm

# PyQt Class for the Main Window
class Ui_MainWindow(object):
	def setupMainUi(self, MainWindow):
		MainWindow.setObjectName("MainWindow")
		MainWindow.resize(585, 505)
		self.centralwidget = QtWidgets.QWidget(MainWindow)
		self.centralwidget.setObjectName("centralwidget")
		self.inputDialogButton = QtWidgets.QPushButton(self.centralwidget)
		self.inputDialogButton.setObjectName("inputDialogButton")
		self.inputDialogButton.clicked.connect(self.dialog)
		self.inputDialogButton.move(0,5)
		self.refresh_button = QtWidgets.QPushButton(self.centralwidget)
		self.refresh_button.clicked.connect(self.refresh)
		self.refresh_button.move(100,5)
		self.refresh_button.setObjectName("inputDialogButton")
		MainWindow.setCentralWidget(self.centralwidget)
		self.statusbar = QtWidgets.QStatusBar(MainWindow)
		self.statusbar.setObjectName("statusbar")
		MainWindow.setStatusBar(self.statusbar)
		self.tableWidget = QTableWidget(self.centralwidget)
		count = pm.get_password_count(pm.get_filepath())
		self.tableWidget.setRowCount(count)
		self.tableWidget.setGeometry(QRect(0,35,350,350))
		self.tableWidget.setColumnCount(3)
		namlist = ["Email","Platform","Password"]
		self.tableWidget.setHorizontalHeaderLabels(namlist)
		for x in range(count):
			data = pm.get_data_from_index(pm.get_filepath(), x)
			self.tableWidget.setItem(x,0, QTableWidgetItem(data['email']))
			self.tableWidget.item(x,0).setFlags(QtCore.Qt.ItemIsEnabled)
			self.tableWidget.setItem(x,1, QTableWidgetItem(data['platform']))
			self.tableWidget.item(x,1).setFlags(QtCore.Qt.ItemIsEnabled)
			self.tableWidget.setItem(x,2, QTableWidgetItem(data['encrypted']))
			self.tableWidget.item(x,2).setFlags(QtCore.Qt.ItemIsEnabled)
		self.tableWidget.itemClicked.connect(lambda: self.unhidePassword(self.tableWidget.currentColumn(),self.tableWidget.currentRow()))
		self.retranslateMainUi(MainWindow)
		QtCore.QMetaObject.connectSlotsByName(MainWindow)

	def retranslateMainUi(self, MainWindow):
		_translate = QtCore.QCoreApplication.translate
		MainWindow.setWindowTitle(_translate("MainWindow", "PMPro"))
		self.inputDialogButton.setText(_translate("MainWindow", "Add New Password"))
		self.refresh_button.setText(_translate("Main Window", "Refresh"))

	def refresh(self):
		print("Refresh")

	# Function to open dialog window
	def dialog(self):
		self.dialogWindow = QtWidgets.QDialog()
		self.dialog = Ui_Dialog()
		self.dialog.setupDialogUi(self.dialogWindow)
		self.dialogWindow.show()

	# Function to rehide the password after the user clicked to show it, called by a QTimer singleShot signal
	def rehidePassword(self,clicked_row,clicked_col,item_file):
		self.tableWidget.setItem(clicked_row,clicked_col,QTableWidgetItem(item_file))
		self.tableWidget.item(clicked_row,clicked_col).setFlags(QtCore.Qt.ItemIsEnabled)

	# If the clicked item is a password, decrypt the password and show it for 2000 miliseconds, then call the function to rehide the password
	def unhidePassword(self,clicked_col,clicked_row):
		if clicked_col == 2:
			item_table = self.tableWidget.item(clicked_row,clicked_col).text()
			item_file = pm.get_password_from_index(pm.get_filepath(),clicked_row).decode('UTF-8')
			if item_table == item_file:
				item_decrypted = pm.decrypt_password(bytes(item_table,'UTF-8'))
				self.tableWidget.setItem(clicked_row,clicked_col,QTableWidgetItem(item_decrypted))
				self.tableWidget.item(clicked_row,clicked_col).setFlags(QtCore.Qt.ItemIsEnabled)
				QTimer.singleShot(2000, lambda : self.rehidePassword(clicked_row,clicked_col,item_file))

# PyQt Dialog class
class Ui_Dialog(object):
	# Function to write the user data into the JSON file
	def buttonClick(self,email,password,platform):
		filepath = pm.get_filepath()
		data = pm.prepare_input(email,platform,password)
		pm.write_data(data, filepath)
		self.textEdit.clear()
		self.textEdit_2.clear()
		self.textEdit_3.clear()

	def setupDialogUi(self, Dialog):
		Dialog.setObjectName("Dialog")
		Dialog.resize(400, 400)
		self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
		self.buttonBox.setGeometry(QtCore.QRect(30, 240, 341, 32))
		self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
		self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel)
		self.buttonBox.setObjectName("buttonBox")
		self.addDataButton = QtWidgets.QPushButton("Add",Dialog, clicked = lambda: self.buttonClick(self.textEdit.text(), self.textEdit_2.text(), self.textEdit_3.text()))
		self.addDataButton.move(220,244)
		self.textEdit = QtWidgets.QLineEdit(Dialog)
		self.textEdit.setGeometry(QtCore.QRect(140, 50, 101, 31))
		self.textEdit.setObjectName("textEdit")
		self.textEdit_2 = QtWidgets.QLineEdit(Dialog)
		self.textEdit_2.setGeometry(QtCore.QRect(140, 90, 101, 31))
		self.textEdit_2.setObjectName("textEdit_2")
		self.textEdit_3 = QtWidgets.QLineEdit(Dialog)
		self.textEdit_3.setGeometry(QtCore.QRect(140, 130, 101, 31))
		self.textEdit_3.setObjectName("textEdit_3")
		self.label = QtWidgets.QLabel(Dialog)
		self.label.setGeometry(QtCore.QRect(60, 60, 47, 13))
		self.label.setObjectName("label")
		self.label_2 = QtWidgets.QLabel(Dialog)
		self.label_2.setGeometry(QtCore.QRect(60, 100, 47, 13))
		self.label_2.setObjectName("label_2")
		self.label_3 = QtWidgets.QLabel(Dialog)
		self.label_3.setGeometry(QtCore.QRect(60, 140, 47, 13))
		self.label_3.setObjectName("label_3")
		self.retranslateDialogUi(Dialog)
		self.buttonBox.accepted.connect(Dialog.accept)
		self.buttonBox.rejected.connect(Dialog.reject)
		QtCore.QMetaObject.connectSlotsByName(Dialog)

	def retranslateDialogUi(self, Dialog):
		_translate = QtCore.QCoreApplication.translate
		Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
		self.label.setText(_translate("Dialog", "Email:"))
		self.label_2.setText(_translate("Dialog", "Password:"))
		self.label_3.setText(_translate("Dialog", "Platform:"))

if __name__ == "__main__":
	import sys
	app = QtWidgets.QApplication(sys.argv)
	MainWindow = QtWidgets.QMainWindow()
	ui = Ui_MainWindow()
	ui.setupMainUi(MainWindow)
	MainWindow.show()
	sys.exit(app.exec_())
