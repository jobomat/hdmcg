from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QListWidget, QListWidgetItem, QPushButton, QLabel,
)
from PySide6.QtCore import Qt

import shiboken6
from shiboken6 import wrapInstance
from maya.OpenMayaUI import MQtUtil


def _list_windows() -> list[dict]:
    main_ptr = int(MQtUtil.mainWindow())
    result = []
    for w in QApplication.instance().topLevelWidgets():
        if not w.isVisible() or not w.isWindow():
            continue
        title = w.windowTitle()
        if not title:
            continue
        if shiboken6.getCppPointer(w)[0] == main_ptr:
            continue
        result.append({'title': title, 'widget': w})
    return result


class WindowManager(QMainWindow):
    _BTN_W = 72

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setWindowFlags(Qt.WindowType.Window)
        self.setWindowTitle('Window Manager')

        self._filter_edit = QLineEdit()
        self._filter_edit.setPlaceholderText('Filter...')
        self._filter_edit.textChanged.connect(self._refresh)

        refresh_btn = QPushButton('Refresh')
        refresh_btn.setFixedWidth(self._BTN_W)
        refresh_btn.clicked.connect(self._refresh)

        gather_btn = QPushButton('Gather All')
        gather_btn.setFixedWidth(self._BTN_W)
        gather_btn.clicked.connect(self._on_gather_all)

        self._list = QListWidget()

        top_row = QWidget()
        top_layout = QHBoxLayout(top_row)
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.addWidget(self._filter_edit)
        top_layout.addWidget(refresh_btn)
        top_layout.addWidget(gather_btn)

        central = QWidget()
        layout = QVBoxLayout(central)
        layout.addWidget(top_row)
        layout.addWidget(self._list)
        self.setCentralWidget(central)

        self.resize(480, 400)
        self._refresh()

    def _matching_windows(self) -> list[dict]:
        f = self._filter_edit.text().lower()
        return [e for e in _list_windows() if f in e['title'].lower()]

    def _refresh(self):
        self._list.clear()
        for entry in self._matching_windows():
            self._add_row(entry)

    def _add_row(self, entry: dict):
        w = entry['widget']
        row = QWidget()
        row_layout = QHBoxLayout(row)
        row_layout.setContentsMargins(4, 0, 4, 0)

        lbl = QLabel(entry['title'])

        front_btn = QPushButton('To Front')
        front_btn.setFixedWidth(self._BTN_W)
        front_btn.clicked.connect(lambda *_, _w=w: (_w.showNormal(), _w.raise_(), _w.activateWindow()))

        min_btn = QPushButton('Minimize')
        min_btn.setFixedWidth(self._BTN_W)
        min_btn.clicked.connect(lambda *_, _w=w: _w.showMinimized())

        origin_btn = QPushButton('To (0, 0)')
        origin_btn.setFixedWidth(self._BTN_W)
        origin_btn.clicked.connect(lambda *_, _w=w: _w.move(0, 0))

        row_layout.addWidget(lbl)
        row_layout.addStretch()
        row_layout.addWidget(front_btn)
        row_layout.addWidget(min_btn)
        row_layout.addWidget(origin_btn)

        item = QListWidgetItem()
        item.setSizeHint(row.sizeHint())
        self._list.addItem(item)
        self._list.setItemWidget(item, row)

    def _on_gather_all(self):
        for entry in _list_windows():
            entry['widget'].move(0, 0)


def show_window_manager() -> WindowManager:
    parent = wrapInstance(int(MQtUtil.mainWindow()), QWidget)
    w = WindowManager(parent=parent)
    w.show()
    return w
