import uuid

from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLineEdit, QMenu
from PySide6.QtCore import Qt

from shiboken6 import wrapInstance
import maya.app.general.mayaMixin as maya_mixin
from maya.OpenMayaUI import MQtUtil
import maya.cmds as cmds

from hdmcg.shared.naming import hash_rename


def _rename_safe(old_names: list[str], new_names: list[str]):
    """Renames old_names[i] → new_names[i], robust against path changes and collisions.

    Tracks each node via a message-attribute connection on a temporary network node —
    connections survive renames so nodes are always findable regardless of path changes.
    A two-phase approach (temp names first, then final names) avoids collisions where
    a target name is already held by another node in the rename set.
    """
    net = cmds.createNode('network', name='__hash_rename_tmp__', skipSelect=True)
    try:
        for i, obj in enumerate(old_names):
            cmds.addAttr(net, longName=f'obj_{i}', attributeType='message')
            cmds.connectAttr(f'{obj}.message', f'{net}.obj_{i}')

        token = uuid.uuid4().hex[:8]
        for i in range(len(old_names)):
            current = cmds.listConnections(f'{net}.obj_{i}',
                                           source=True, destination=False)[0]
            cmds.rename(current, f'__tmp_{i}_{token}__')

        for i, final in enumerate(new_names):
            current = cmds.listConnections(f'{net}.obj_{i}',
                                           source=True, destination=False)[0]
            cmds.rename(current, final)
    finally:
        cmds.delete(net)


class HashRename(maya_mixin.MayaQWidgetDockableMixin, QMainWindow):
    MAX_RECENT = 10

    def __init__(self):
        super().__init__(parent=wrapInstance(int(MQtUtil.mainWindow()), QWidget))
        self._recent: list[str] = []

        self._pattern_edit = QLineEdit()
        self._pattern_edit.setPlaceholderText("name_##_suffix   (# = counter position & width)")
        self._pattern_edit.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self._pattern_edit.customContextMenuRequested.connect(self._show_recent_menu)
        self._pattern_edit.textChanged.connect(self._validate)
        self._pattern_edit.returnPressed.connect(self._on_return_pressed)

        central = QWidget()
        layout = QVBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self._pattern_edit)
        self.setCentralWidget(central)

        self.setWindowTitle("Hash Rename")
        self.setMinimumWidth(300)
        self.setMaximumHeight(20)
        self.show(dockable=True, width=300, height=20)

    def _validate(self):
        pattern = self._pattern_edit.text().strip()
        if not pattern:
            self._set_error(False)
            return
        try:
            hash_rename(pattern, ["_"])   # dummy list — only checks for structural errors
            self._set_error(False)
        except ValueError:
            self._set_error(True)

    def _on_return_pressed(self):
        pattern = self._pattern_edit.text().strip()
        if not pattern:
            return
        old_names = cmds.ls(sl=True, long=True)
        if not old_names:
            cmds.warning("HashRename: nothing selected.")
            return
        try:
            new_names = hash_rename(pattern, old_names)
        except ValueError as e:
            cmds.warning(f"HashRename: {e}")
            return
        _rename_safe(old_names, new_names)
        self._add_to_recent(pattern)

    def _add_to_recent(self, pattern: str):
        if pattern in self._recent:
            self._recent.remove(pattern)
        self._recent.insert(0, pattern)
        self._recent = self._recent[:self.MAX_RECENT]

    def _set_error(self, error: bool):
        if error:
            self._pattern_edit.setStyleSheet(
                "QLineEdit { border: 1px solid #cc3333; background: rgba(200, 0, 0, 25); }"
            )
        else:
            self._pattern_edit.setStyleSheet("")

    def _show_recent_menu(self, pos):
        if not self._recent:
            return
        menu = QMenu(self)
        for pattern in self._recent:
            action = menu.addAction(pattern)
            action.triggered.connect(lambda *_, p=pattern: self._pattern_edit.setText(p))
        menu.exec(self._pattern_edit.mapToGlobal(pos))
