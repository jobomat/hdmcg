import os
import sys

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSplitter, QTabWidget,
    QLineEdit, QListWidget, QListWidgetItem, QPushButton, QCheckBox, QComboBox,
    QFileDialog,
)
from PySide6.QtCore import Qt


class ModuleManager(QWidget):
    """Listet geladene sys.modules auf und erlaubt es, einzelne oder mehrere
    davon aus dem Modul-Cache zu entfernen (fuer schnelles Reload beim Entwickeln)."""

    def __init__(self, parent=None, filter_text: str = ''):
        super().__init__(parent=parent)

        self._filter_edit = QLineEdit(filter_text)
        self._filter_edit.setPlaceholderText('Filter...')
        self._filter_edit.textChanged.connect(self._refresh)

        refresh_btn = QPushButton('Refresh')
        refresh_btn.clicked.connect(self._refresh)

        self._list = QListWidget()

        toggle_all_btn = QPushButton('Toggle All')
        toggle_all_btn.clicked.connect(self._on_toggle_all)

        delete_checked_btn = QPushButton('Delete Checked')
        delete_checked_btn.clicked.connect(self._on_delete_checked)

        top_row = QWidget()
        top_layout = QHBoxLayout(top_row)
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.addWidget(self._filter_edit)
        top_layout.addWidget(refresh_btn)

        bottom_row = QWidget()
        bottom_layout = QHBoxLayout(bottom_row)
        bottom_layout.setContentsMargins(0, 0, 0, 0)
        bottom_layout.addWidget(toggle_all_btn)
        bottom_layout.addStretch()
        bottom_layout.addWidget(delete_checked_btn)

        layout = QVBoxLayout(self)
        layout.addWidget(top_row)
        layout.addWidget(self._list)
        layout.addWidget(bottom_row)

        self._refresh()

    def _matching_modules(self) -> list[str]:
        filter_text = self._filter_edit.text().lower()
        return sorted(name for name in sys.modules if filter_text in name.lower())

    def _refresh(self):
        self._list.clear()
        for name in self._matching_modules():
            self._add_row(name)

    def _add_row(self, name: str):
        row = QWidget()
        row_layout = QHBoxLayout(row)
        row_layout.setContentsMargins(4, 0, 4, 0)

        checkbox = QCheckBox(name)
        checkbox.setStyleSheet("""
            QCheckBox::indicator { width: 13px; height: 13px; border: 1px solid #888; border-radius: 2px; }
            QCheckBox::indicator:checked { background-color: #5a9; border-color: #5a9; }
        """)
        delete_btn = QPushButton('Delete')
        delete_btn.setFixedWidth(60)
        delete_btn.clicked.connect(lambda: self._on_delete_single(name))

        row_layout.addWidget(checkbox)
        row_layout.addStretch()
        row_layout.addWidget(delete_btn)

        item = QListWidgetItem()
        item.setData(Qt.ItemDataRole.UserRole, name)
        item.setSizeHint(row.sizeHint())
        self._list.addItem(item)
        self._list.setItemWidget(item, row)

    def _checkbox_at(self, row_index: int) -> QCheckBox:
        return self._list.itemWidget(self._list.item(row_index)).findChild(QCheckBox)

    def _on_toggle_all(self):
        checkboxes = [self._checkbox_at(i) for i in range(self._list.count())]
        if not checkboxes:
            return
        all_checked = all(cb.isChecked() for cb in checkboxes)
        for cb in checkboxes:
            cb.setChecked(not all_checked)

    def _on_delete_single(self, name: str):
        sys.modules.pop(name, None)
        self._refresh()

    def _on_delete_checked(self):
        for i in range(self._list.count()):
            item = self._list.item(i)
            if self._checkbox_at(i).isChecked():
                sys.modules.pop(item.data(Qt.ItemDataRole.UserRole), None)
        self._refresh()


class EnvVarBrowser(QWidget):
    """Zeigt os.environ als zwei-spaltige Ansicht: links Keys, rechts die
    aufgesplitteten Pfadeinträge des gewählten Keys. Filter sucht in Key und Value."""

    def __init__(self, parent=None, filter_text: str = ''):
        super().__init__(parent=parent)

        self._filter_edit = QLineEdit(filter_text)
        self._filter_edit.setPlaceholderText('Filter...')
        self._filter_edit.textChanged.connect(self._refresh)

        self._scope_combo = QComboBox()
        self._scope_combo.addItems(['Search in keys only', 'Search in values only', 'Search in keys and values'])
        self._scope_combo.currentIndexChanged.connect(self._refresh)

        refresh_btn = QPushButton('Refresh')
        refresh_btn.clicked.connect(self._refresh)

        self._key_list = QListWidget()
        self._key_list.currentItemChanged.connect(self._on_key_selected)

        self._value_list = QListWidget()

        splitter = QSplitter()
        splitter.addWidget(self._key_list)
        splitter.addWidget(self._value_list)

        top_row = QWidget()
        top_layout = QHBoxLayout(top_row)
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.addWidget(self._filter_edit)
        top_layout.addWidget(self._scope_combo)
        top_layout.addWidget(refresh_btn)

        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 3)

        layout = QVBoxLayout(self)
        layout.addWidget(top_row)
        layout.addWidget(splitter, stretch=1)

        self._refresh()

    def _matching_keys(self) -> list[str]:
        f = self._filter_edit.text().lower()
        scope = self._scope_combo.currentIndex()
        def match(k, v):
            if not f:
                return True
            if scope == 0:
                return f in k.lower()
            if scope == 1:
                return f in v.lower()
            return f in k.lower() or f in v.lower()
        return sorted(k for k, v in os.environ.items() if match(k, v))

    def _refresh(self):
        current = self._key_list.currentItem()
        current_key = current.text() if current else None

        self._key_list.clear()
        self._value_list.clear()

        keys = self._matching_keys()
        for key in keys:
            self._key_list.addItem(key)

        if current_key and current_key in keys:
            hits = self._key_list.findItems(current_key, Qt.MatchFlag.MatchExactly)
            if hits:
                self._key_list.setCurrentItem(hits[0])

    def _on_key_selected(self, current, _previous):
        self._value_list.clear()
        if current is None:
            return
        value = os.environ.get(current.text(), '')
        for entry in value.split(os.pathsep):
            if entry:
                self._value_list.addItem(entry)


class SysPathBrowser(QWidget):
    """Zeigt sys.path als gefilterte Liste und erlaubt das Hinzufügen von Verzeichnissen."""

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self._filter_edit = QLineEdit()
        self._filter_edit.setPlaceholderText('Filter...')
        self._filter_edit.textChanged.connect(self._refresh)

        refresh_btn = QPushButton('Refresh')
        refresh_btn.clicked.connect(self._refresh)

        self._list = QListWidget()

        add_btn = QPushButton('Add Directory...')
        add_btn.clicked.connect(self._on_add)

        top_row = QWidget()
        top_layout = QHBoxLayout(top_row)
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.addWidget(self._filter_edit)
        top_layout.addWidget(refresh_btn)

        bottom_row = QWidget()
        bottom_layout = QHBoxLayout(bottom_row)
        bottom_layout.setContentsMargins(0, 0, 0, 0)
        bottom_layout.addStretch()
        bottom_layout.addWidget(add_btn)

        layout = QVBoxLayout(self)
        layout.addWidget(top_row)
        layout.addWidget(self._list, stretch=1)
        layout.addWidget(bottom_row)

        self._refresh()

    def _refresh(self):
        f = self._filter_edit.text().lower()
        self._list.clear()
        for entry in sys.path:
            if f in entry.lower():
                self._list.addItem(entry)

    def _on_add(self):
        directory = QFileDialog.getExistingDirectory(self, 'Add Directory to sys.path')
        if directory and directory not in sys.path:
            sys.path.append(directory)
            self._refresh()


class DevTools(QMainWindow):
    def __init__(self, module_filter=None, envvar_filter=None, parent=None):
        super().__init__(parent=parent)
        self.setWindowFlags(Qt.WindowType.Window)

        tabs = QTabWidget()
        tabs.addTab(ModuleManager(filter_text=module_filter), 'Modules')
        tabs.addTab(EnvVarBrowser(filter_text=envvar_filter), 'Env Vars')
        tabs.addTab(SysPathBrowser(), 'sys.path')

        self.setCentralWidget(tabs)
        self.setWindowTitle('Dev Tools')
        self.resize(700, 500)
