import os
import subprocess

from PyQt5.QtCore import QEvent, QObject, Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QCloseEvent, QIcon, QKeyEvent
from PyQt5.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
                             QLineEdit, QListWidget, QListWidgetItem,
                             QPushButton, QSpacerItem, QVBoxLayout, QWidget)

from cfg import Cfg


class MyApp(QApplication):
    def __init__(self, argv: list[str]) -> None:
        super().__init__(argv)

        if not os.path.exists("lib"): 
            self.setWindowIcon(QIcon("icon.icns"))

        self.installEventFilter(self)

    def eventFilter(self, a0: QObject | None, a1: QEvent | None) -> bool:
        if a1.type() == QEvent.Type.ApplicationActivate:
            for i in self.topLevelWidgets():
                i.show()
        return super().eventFilter(a0, a1)


class SafeWidget(QWidget):
    on_text_changed = pyqtSignal(str)
    on_removed = pyqtSignal()

    def __init__(self, parent: QWidget = None, text: str = None):
        super().__init__(parent=parent)

        self.v_layout = QVBoxLayout()
        self.v_layout.setContentsMargins(5, 15, 5, 15)
        self.setLayout(self.v_layout)

        h_wid = QWidget()
        self.v_layout.addWidget(h_wid)

        h_layout = QHBoxLayout()
        h_layout.setContentsMargins(0, 0, 0, 0)
        h_wid.setLayout(h_layout)

        self.input_widget = QLineEdit(parent=self)
        self.input_widget.setPlaceholderText("Введите любой текст")
        self.input_widget.setStyleSheet("padding-left: 5px;")
        self.input_widget.setFixedHeight(30)
        self.input_widget.textChanged.connect(self.on_text_changed_cmd)
        h_layout.addWidget(self.input_widget)

        self.copy_btn = QPushButton(parent=self, text="Копировать")
        self.copy_btn.setFixedWidth(130)
        self.copy_btn.clicked.connect(lambda: self.copy_text(self.input_widget.text()))
        h_layout.addWidget(self.copy_btn)

        self.remove_btn = QPushButton(parent=self, text="Удалить")
        self.remove_btn.setFixedWidth(130)
        self.remove_btn.clicked.connect(self.remove_cmd)
        self.v_layout.addWidget(self.remove_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        sep = QFrame(parent=self)
        sep.setStyleSheet("background-color: black;")
        sep.setFixedHeight(1)
        self.v_layout.addWidget(sep)

        if text:
            self.input_widget.setText(text)

        else:
            self.input_widget.setStyleSheet("padding-left: 5px; background-color: #3b590d;")
            QTimer.singleShot(500, lambda: self.remove_temp(self.input_widget))

    def remove_temp(self, widget: QFrame):
        widget.setStyleSheet("padding-left: 5px;")

    def on_text_changed_cmd(self, txt: str):
        self.on_text_changed.emit(txt)

    def remove_cmd(self):
        self.on_removed.emit()

    def copy_text(self, text: str):
        text_bytes = text.encode('utf-8')
        subprocess.run(['pbcopy'], input=text_bytes, check=True)
        return True

class MainWin(QWidget):
    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent=parent)
        self.setWindowTitle(Cfg.app_name)
        self.setMinimumSize(450, 400)

        self.v_layout = QVBoxLayout()
        self.v_layout.setContentsMargins(0, 15, 0, 5)
        self.setLayout(self.v_layout)

        self.add_btn = QPushButton(parent=self, text="Добавить")
        self.add_btn.setFixedWidth(200)
        self.add_btn.clicked.connect(self.add_safe)
        self.v_layout.addWidget(self.add_btn)

        self.list_widget = QListWidget(parent=self)
        self.list_widget.setSelectionMode(QListWidget.SelectionMode.NoSelection)
        self.v_layout.addWidget(self.list_widget)

        self.save_timer = QTimer(self)
        self.save_timer.setSingleShot(True)
        self.save_timer.timeout.connect(self.save_json_file)

        self.input_widgets: dict[SafeWidget: str] = {}

        for i in Cfg.data:
            self.add_safe(text=i)

    def add_safe(self, text: str = None):
        wid = SafeWidget(parent=self, text=text)
        wid.on_text_changed.connect(lambda text: self.safe_text_changed(wid, text))
        self.input_widgets[wid] = text

        list_item = QListWidgetItem()
        list_item.setSizeHint(wid.sizeHint())
        wid.on_removed.connect(lambda: self.on_removed(list_item, wid))

        self.list_widget.addItem(list_item)
        self.list_widget.setItemWidget(list_item, wid)

    def safe_text_changed(self, wid: SafeWidget, text: str):
        self.save_timer.stop()
        self.input_widgets[wid] = text
        self.save_timer.start(1000)

    def save_json_file(self):
        data = [
            text
            for widget, text in self.input_widgets.items()
            if text is not None
            ]
        Cfg.save_json(data)

    def on_removed(self, list_item: QListWidgetItem, wid: SafeWidget):
        self.input_widgets.pop(wid)

        item_index = self.list_widget.row(list_item)
        item = self.list_widget.takeItem(item_index)
        self.list_widget.removeItemWidget(item)
        del item

        self.save_json_file()

    def keyPressEvent(self, a0: QKeyEvent | None) -> None:
        if a0.modifiers() == Qt.KeyboardModifier.ControlModifier:
            if a0.key() == Qt.Key.Key_W:
                self.hide()
            elif a0.key() == Qt.Key.Key_Q:
                self.save_json_file()
                quit()
        return super().keyPressEvent(a0)
    
    def closeEvent(self, a0: QCloseEvent | None) -> None:
        self.hide()
        a0.ignore()
        # return super().closeEvent(a0)
