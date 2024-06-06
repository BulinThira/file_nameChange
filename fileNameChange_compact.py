import sys, os
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidget, QListWidgetItem, QWidget, QCheckBox, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import Qt, QUrl
from pathlib import Path
from PyQt5 import uic

moduleDir = os.path.dirname(sys.modules[__name__].__file__)

class AppDemo(QMainWindow):
    def __init__(self, parent=None):
        super(AppDemo, self).__init__(parent)
        uiFile = '%s\\ui.ui' %moduleDir
        self.main_ui = uic.loadUi(uiFile, QWidget())

        self.listbox_view = ListBoxWidget(self)
        self.main_ui.verticalLayout.addWidget(self.listbox_view)

        self.setCentralWidget(self.main_ui)
        self.setWindowTitle('Files Name Changer')

        self.msgBox = QMessageBox()
        self.msgBox.setDefaultButton(QMessageBox.No)
        self.msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

        self.main_ui.newname_line.textChanged.connect(self.check_and_set_default)
        self.main_ui.newname_ordering_line.textChanged.connect(self.check_and_set_default)


        self.main_ui.newname_checkbox.clicked.connect(lambda: self.main_ui.newname_line.setEnabled(self.main_ui.newname_checkbox.isChecked()))
        self.main_ui.prefix_checkbox.clicked.connect(lambda: self.main_ui.prefix_line.setEnabled(self.main_ui.prefix_checkbox.isChecked()))
        self.main_ui.suffix_checkbox.clicked.connect(lambda: self.main_ui.suffix_line.setEnabled(self.main_ui.suffix_checkbox.isChecked()))

        self.main_ui.newname_radbtn.clicked.connect(lambda: self.main_ui.newname_ordering_line.setEnabled(self.main_ui.newname_radbtn.isChecked()))
        self.main_ui.only_radbtn.clicked.connect(lambda: self.main_ui.newname_ordering_line.setEnabled(self.main_ui.newname_radbtn.isChecked()))
        self.main_ui.custom_radbtn.clicked.connect(lambda: self.main_ui.newname_ordering_line.setEnabled(self.main_ui.newname_radbtn.isChecked()))

        self.main_ui.rename_button.clicked.connect(lambda: self.rename_files(True))
        self.main_ui.preview_button.clicked.connect(lambda: self.rename_files(False))

    def getSelectedItem(self, name_lst=[], mode=True):
        # items = [self.listbox_view.item(i).text() for i in range(self.listbox_view.count())]
        preview_txt = ""
        index = self.main_ui.startswith_spinbox.value()
        for each_file in name_lst:
            file_path = Path(each_file)
            directory = os.path.dirname(each_file)
            file_name = file_path.name
            _, file_extension = os.path.splitext(file_path)
            check_sign_prefix = self.main_ui.prefix_checkbox.isChecked()
            check_sign_suffix = self.main_ui.suffix_checkbox.isChecked()
            new_file_name = 'newname'
            if self.main_ui.custom_radbtn.isChecked():
                if self.main_ui.newname_checkbox.isChecked():
                    file_name = self.main_ui.suffix_line.text()
                if check_sign_prefix and check_sign_suffix:
                    new_file_name = '{}_{}_{}'.format(self.main_ui.prefix_line.text(), file_name, self.main_ui.suffix_line.text())
                elif check_sign_prefix and not check_sign_suffix:
                    new_file_name = '{}_{}'.format(self.main_ui.prefix_line.text(), file_name)
                elif not check_sign_prefix and check_sign_suffix:
                    new_file_name = '{}_{}'.format(file_name, self.main_ui.suffix_line.text())
                else:
                    new_file_name = file_name
                if self.main_ui.prenumber_checkbox.isChecked():
                    new_file_name = str(index).zfill(self.main_ui.padding_spinbox.value()) + '_' + new_file_name
            elif self.main_ui.newname_radbtn.isChecked():
                new_file_name = self.main_ui.newname_ordering_line.text() + "_" + (str(index).zfill(self.main_ui.padding_spinbox.value())) + file_extension
            else:
                new_file_name = str(index).zfill(self.main_ui.padding_spinbox.value()) + file_extension

            new_path = os.path.join(directory, new_file_name)
            if mode:
                os.rename(file_path, new_path)
            else:
                self.main_ui.preview_line.setText(new_path)
                break
            index += 1
    
    def rename_files(self, state):
        items = [self.listbox_view.item(i).text() for i in range(self.listbox_view.count())]
        rename_list = self.getSelectedItem(items, state)

    def check_and_set_default(self, text):
        sender = self.sender()
        if text == "":
            sender.setText("default")

class ListBoxWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setDragDropMode(QListWidget.InternalMove)
        self.setSelectionMode(QListWidget.ExtendedSelection)
        # self.resize(600, 600)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.accept()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.accept()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()

            links = []
            for url in event.mimeData().urls():
                # https://doc.qt.io/qt-5/qurl.html
                if url.isLocalFile():
                    links.append(str(url.toLocalFile()))
                else:
                    links.append(str(url.toString()))
            self.addItems(links)
        else:
            super().dropEvent(event)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    demo = AppDemo()
    demo.show()

    sys.exit(app.exec_())
