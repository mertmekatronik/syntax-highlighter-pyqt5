from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from style import Style

import sys, os


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.set_settings()
        self.stylesPygments = Style()
        self.setUI()

    def set_settings(self):
        self.setWindowTitle("Mert Mekatronik Highlighter v1.0")
        self.setMaximumSize(QSize(900, 600))
        self.setMinimumSize(QSize(900, 600))
        self.show()

    def setUI(self):
        Widget = QWidget()
        LWidget = QWidget()
        LWidget.setMaximumWidth(300)

        self.general_box = QHBoxLayout()

        self.left_section_box = QVBoxLayout()
        self.right_section_box = QVBoxLayout()

        self.general_box.addWidget(LWidget)
        self.general_box.addLayout(self.right_section_box)

        LWidget.setLayout(self.left_section_box)

        self.right_section_box.addWidget(self.main_code_area())
        self.right_section_box.addWidget(self.highlighter_area())
        self.right_section_box.addLayout(self.convert_area())

        self.left_section_box.addLayout(self.language_box())
        self.left_section_box.addWidget(self.theme_box())

        Widget.setLayout(self.general_box)

        self.setCentralWidget(Widget)

    def language_box(self):
        h_box = QHBoxLayout()
        h_box.setAlignment(Qt.AlignHCenter)

        self.combo_box = QComboBox()
        self.combo_box.addItem(QIcon(os.path.join(os.getcwd(), 'assets', 'python_logo.png')), 'Python')
        for lexer in self.stylesPygments.get_all_lexers():
            self.combo_box.addItem(lexer[0])


        h_box.addWidget(QLabel('Hightlighting Language: '))
        h_box.addWidget(self.combo_box)

        return h_box

    def theme_box(self):
        group_box = QGroupBox("Select Theme")

        v_box = QVBoxLayout()

        self.theme_list = QListWidget()
        self.theme_list.addItems(self.stylesPygments.get_all_styles())
        self.theme_list.setCurrentRow(0)

        v_box.addWidget(self.theme_list)

        group_box.setLayout(v_box)

        return group_box

    def main_code_area(self):
        group_box = QGroupBox("Code")

        v_box = QVBoxLayout()
        self.code_area = QTextEdit()
        self.code_area.setAcceptRichText(False)

        v_box.addWidget(self.code_area)

        group_box.setLayout(v_box)

        return group_box

    def highlighter_area(self):
        group_box = QGroupBox("Highlight Code Preview")

        v_box = QVBoxLayout()
        self.hightlightarea = QTextBrowser()
        self.hightlightarea.setAcceptRichText(False)
        v_box.addWidget(self.hightlightarea)

        group_box.setLayout(v_box)

        return group_box

    def convert_area(self):
        h_box = QHBoxLayout()
        h_box.setAlignment(Qt.AlignRight)

        self.copy_source_code_button = QPushButton("Copy Source Code")
        self.copy_source_code_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.copy_source_code_button.setEnabled(False)
        self.copy_source_code_button.clicked.connect(self.copy_clipboard)



        convert_button = QPushButton("Highlight Code!")
        convert_button.setCursor(QCursor(Qt.PointingHandCursor))
        convert_button.clicked.connect(self.setHightlightText)

        h_box.addWidget(convert_button)
        h_box.addWidget(self.copy_source_code_button)


        return h_box

    ################## FUNCTIONS ########################

    def setHightlightText(self):
        self.copy_source_code_button.setEnabled(True)
        self.hightlight_text = self.stylesPygments.highlight_code(self.code_area.toPlainText(), self.combo_box.currentText(), self.theme_list.currentItem().text())
        self.hightlightarea.setStyleSheet(self.hightlight_text[1])
        self.hightlightarea.setHtml(self.hightlight_text[0])

    def copy_clipboard(self):
        cb = QApplication.clipboard()
        cb.clear(mode=cb.Clipboard)
        cb.setText(self.hightlight_text[0], mode=cb.Clipboard)
        self.statusBar().showMessage('Source code coppied to clipboard.', 5000)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
