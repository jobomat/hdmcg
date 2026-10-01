import maya.cmds as cmds

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QListWidget, QListWidgetItem, QPushButton, QAbstractItemView,
)
from PySide6.QtCore import Qt

from shiboken6 import wrapInstance
import maya.app.general.mayaMixin as maya_mixin
from maya.OpenMayaUI import MQtUtil


def _get_alembic_nodes() -> list[str]:
    return cmds.ls(type='AlembicNode') or []


def _get_shading_groups(alembic_node: str) -> set[str]:
    """Collect all SGs assigned to the meshes driven by this AlembicNode."""
    transforms = cmds.listConnections(alembic_node, type='transform') or []
    sgs = set()
    for t in transforms:
        shapes = cmds.listRelatives(t, shapes=True, noIntermediate=True, path=True) or []
        for s in shapes:
            for sg in cmds.listConnections(s, type='shadingEngine') or []:
                sgs.add(sg)
    return sgs


def _get_namespaces() -> list[str]:
    ns = cmds.namespaceInfo(':', listOnlyNamespaces=True, recurse=True) or []
    return [n for n in ns if n not in ('UI', 'shared')]


def _find_look_matches(sg_names: set[str]) -> dict[str, list[str]]:
    """Returns {namespace: [matching_ns_sg_nodes]} for namespaces with at least one SG match."""
    result = {}
    for ns in _get_namespaces():
        ns_sgs = cmds.ls(f'{ns}:*', type='shadingEngine') or []
        matches = [sg for sg in ns_sgs if sg[len(ns) + 1:] in sg_names]
        if matches:
            result[ns] = matches
    return result


def assign_look(abc_sgs: set[str], namespace: str):
    """Connect surfaceShader/volumeShader/displacementShader from namespace SGs to alembic SGs."""
    plugs = ('surfaceShader', 'volumeShader', 'displacementShader')
    for abc_sg in abc_sgs:
        ns_sg = f'{namespace}:{abc_sg}'
        if not cmds.objExists(ns_sg):
            continue
        for plug in plugs:
            srcs = cmds.listConnections(f'{ns_sg}.{plug}', plugs=True, source=True)
            if srcs:
                cmds.connectAttr(srcs[0], f'{abc_sg}.{plug}', force=True)


class LookManager(maya_mixin.MayaQWidgetDockableMixin, QMainWindow):
    def __init__(self):
        super().__init__(parent=wrapInstance(int(MQtUtil.mainWindow()), QWidget))

        self._current_sgs: set[str] = set()

        refresh_btn = QPushButton('Refresh')
        refresh_btn.clicked.connect(self._refresh)

        abc_label = QLabel('Alembic Nodes')
        self._abc_list = QListWidget()
        self._abc_list.currentItemChanged.connect(self._on_alembic_selected)

        looks_label = QLabel('Available Looks')
        self._looks_list = QListWidget()
        self._looks_list.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)

        left = QWidget()
        left_layout = QVBoxLayout(left)
        left_layout.setContentsMargins(0, 0, 4, 0)
        left_layout.addWidget(abc_label)
        left_layout.addWidget(self._abc_list)

        right = QWidget()
        right_layout = QVBoxLayout(right)
        right_layout.setContentsMargins(4, 0, 0, 0)
        right_layout.addWidget(looks_label)
        right_layout.addWidget(self._looks_list)

        lists_widget = QWidget()
        lists_layout = QHBoxLayout(lists_widget)
        lists_layout.setContentsMargins(0, 0, 0, 0)
        lists_layout.addWidget(left)
        lists_layout.addWidget(right)

        assign_btn = QPushButton('Assign Selected')
        assign_btn.clicked.connect(self._on_assign)

        bottom_row = QWidget()
        bottom_layout = QHBoxLayout(bottom_row)
        bottom_layout.setContentsMargins(0, 0, 0, 0)
        bottom_layout.addStretch()
        bottom_layout.addWidget(assign_btn)

        central = QWidget()
        layout = QVBoxLayout(central)
        layout.addWidget(refresh_btn)
        layout.addWidget(lists_widget)
        layout.addWidget(bottom_row)
        self.setCentralWidget(central)

        self.setWindowTitle('Look Manager')
        self._refresh()
        self.show(dockable=True, width=500, height=300)

    def _refresh(self):
        self._abc_list.clear()
        self._looks_list.clear()
        self._current_sgs = set()
        for node in _get_alembic_nodes():
            self._abc_list.addItem(node)

    def _on_alembic_selected(self, current, _previous):
        self._looks_list.clear()
        self._current_sgs = set()
        if current is None:
            return
        self._current_sgs = _get_shading_groups(current.text())
        total = len(self._current_sgs)
        matches = _find_look_matches(self._current_sgs)
        for ns, ns_sgs in matches.items():
            item = QListWidgetItem(f'{ns}  ({len(ns_sgs)}/{total} matched)')
            item.setData(Qt.ItemDataRole.UserRole, ns)
            self._looks_list.addItem(item)

    def _on_assign(self):
        selected = self._looks_list.selectedItems()
        if not selected or not self._current_sgs:
            return
        namespaces = [item.data(Qt.ItemDataRole.UserRole) for item in selected]
        assign_look(self._current_sgs, namespaces[0])
        cmds.inViewMessage(
            assistMessage=f'Assigned look {namespaces[0]}',
            pos='midCenter',
            fade=True,
        )
