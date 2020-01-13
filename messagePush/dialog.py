# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'text01.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(285, 267)
        self.list_view_message = QtWidgets.QListView(Dialog)
        self.list_view_message.setGeometry(QtCore.QRect(0, 0, 291, 271))
        self.list_view_message.setObjectName("list_view_message")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Message"))
