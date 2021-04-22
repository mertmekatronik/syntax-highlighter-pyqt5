import importlib
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from pygments.styles import get_style_by_name
from style import Style
from design import *
import os


class Window(QMainWindow,Ui_MainWindow):
    def __init__(self) -> None:
        super().__init__()
        QMainWindow.__init__(self)
        super().setupUi(MainWindow)
        self.stylesPygments = Style()
        self.hightlight_text = "  "

    def setupUi(self, MainWindow):    
        self.pushButton.setEnabled(False)
        self.codeArea.setAcceptRichText(False)

        self.setLanguageBox()
        self.setThemeBox()
        self.setButtonFunctions()
    


    def setLanguageBox(self):
        self.comboBox.addItem(QIcon(os.path.join(os.getcwd(), 'assets', 'python_logo.png')), 'Python')
        for lexer in self.stylesPygments.get_all_lexers():
            self.comboBox.addItem(lexer[0])

    def setThemeBox(self):
        self.listWidget.addItems(self.stylesPygments.get_all_styles())
        self.listWidget.setCurrentRow(0)
    
    def setButtonFunctions(self):
        self.pushButton.clicked.connect(self.copy_clipboard)
        self.pushButton_2.clicked.connect(self.setHightlightText)
        self.pushButton_3.clicked.connect(self.changeBgColor)
        self.actionLoad.triggered.connect(self.LoadFile)
        self.actionClear_Code.triggered.connect(self.clearCode)
        self.actionReset.triggered.connect(self.reload)
        

    def setHightlightText(self):
        self.pushButton.setEnabled(True)
        self.hightlight_text = self.stylesPygments.highlight_code(self.codeArea.toPlainText(), self.comboBox.currentText(),self.dots_checkbox.isChecked(),self.checkBox.isChecked() ,self.listWidget.currentItem().text())
        self.result.setStyleSheet(self.hightlight_text[1])
        self.result.setHtml(self.hightlight_text[0])

    def copy_clipboard(self):
        cb = QApplication.clipboard()
        cb.clear(mode=cb.Clipboard)
        cb.setText(self.hightlight_text[0], mode=cb.Clipboard)
        self.statusbar.showMessage('Source code coppied to clipboard.', 5000)
    
    def changeBgColor(self):
        color = QColorDialog.getColor()
        style = get_style_by_name(self.listWidget.currentItem().text())
        style.background_color = color.name()
        self.colorcode.setText(color.name())
    
    def LoadFile(self):
        try:
            file = QFileDialog.getOpenFileName(self, 'Open file')
            self.codeArea.setText(open(file[0],"r").read())
        except FileNotFoundError:
            self.statusbar.showMessage("No file selected",5000)
        except:
            self.statusbar.showMessage("Something went wrong",5000)
        
    def clearCode(self):
        self.codeArea.clear()
    
    def reload(self):
        self.codeArea.clear()
        self.result.clear()
        self.result.setStyleSheet("")
        self.colorcode.clear()
        self.listWidget.setCurrentRow(0)

            

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Window()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


