import re

import maya.cmds as cmds
import maya.api.OpenMaya as om

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QListWidget, QPushButton, QInputDialog, QAbstractItemView,
)

from shiboken6 import wrapInstance
import maya.app.general.mayaMixin as maya_mixin
from maya.OpenMayaUI import MQtUtil

_PREF_PREFIX = "mtoa_varying_"


def normalize_shader_assignments(transform):
    """Erzwingt explizite Per-Face-Assignment für alle SGs eines Meshes,
    damit AbcExport -writeFaceSets sie garantiert erfasst."""
    
    shape = cmds.listRelatives(transform, shapes=True, noIntermediate=True, path=True)[0]
    plugs = cmds.listConnections(shape, type="shadingEngine", plugs=True)
    
    # eingesteckte wireframecolors -> indiz für per face assignment: exit
    if [p for p in plugs if p.endswith(".memberWireframeColor")]:
        return
    
    sgs = list(set(cmds.listConnections(shape, type="shadingEngine")))
    num_faces = cmds.polyEvaluate(shape, face=True)
    faces = f"{shape}.f[0:{num_faces - 1}]"
    # erst ein face mit per face assignment, sonst funktioniert es nicht...
    cmds.sets(f"{shape}.f[0]", edit=True, forceElement="initialShadingGroup")
    cmds.sets(faces, edit=True, forceElement=sgs[0])


# # z.B. so als pre-run vor dem publishen:

# for obj in cmds.ls(sl=True):
#     normalize_shader_assignments(obj)


def bake_pref(shape, rest_frame=None, name="Pref", world=True):
    """Speichert die aktuellen Vertexpositionen als mtoa_varying_<name> am Shape.
    shape = cmds.listRelatives(cmds.ls(sl=True)[0], shapes=True)[0]
    bake_pref(shape, rest_frame=1)
    """
    if rest_frame is not None:
        cmds.currentTime(rest_frame)

    sel = om.MSelectionList()
    sel.add(shape)
    dag = sel.getDagPath(0)
    space = om.MSpace.kWorld if world else om.MSpace.kObject
    pts = om.MFnMesh(dag).getPoints(space)          # MPointArray, deformierter Zustand!

    attr = _PREF_PREFIX + name
    if not cmds.attributeQuery(attr, node=shape, exists=True):
        cmds.addAttr(shape, longName=attr, dataType="pointArray")

    data = om.MFnPointArrayData().create(pts)
    plug = om.MFnDependencyNode(dag.node()).findPlug(attr, False)
    plug.setMObject(data)
    print("{}: {} Punkte nach .{} geschrieben".format(shape, len(pts), attr))


def _selected_mesh_shape() -> str | None:
    """Erstes selektiertes Mesh-Shape - direkt selektiert oder als Kind eines Transforms."""
    for node in cmds.ls(sl=True, long=True, objectsOnly=True) or []:
        if cmds.nodeType(node) == "mesh":
            if not cmds.getAttr(node + ".intermediateObject"):
                return node
            continue
        shapes = cmds.listRelatives(node, shapes=True, type="mesh", noIntermediate=True, fullPath=True)
        if shapes:
            return shapes[0]
    return None


class PrefBaker(maya_mixin.MayaQWidgetDockableMixin, QMainWindow):
    """Zeigt die mtoa_varying-Attribute des selektierten Meshes und legt sie per bake_pref an."""

    def __init__(self):
        super().__init__(parent=wrapInstance(int(MQtUtil.mainWindow()), QWidget))

        self._shape = None

        self._shape_label = QLabel()

        self._list = QListWidget()
        self._list.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self._list.itemSelectionChanged.connect(self._update_buttons)

        self._add_btn = QPushButton("Add...")
        self._add_btn.clicked.connect(self._on_add)
        self._update_btn = QPushButton("Update")
        self._update_btn.clicked.connect(self._on_update)
        self._delete_btn = QPushButton("Delete")
        self._delete_btn.clicked.connect(self._on_delete)

        bottom_row = QWidget()
        bottom_layout = QHBoxLayout(bottom_row)
        bottom_layout.setContentsMargins(0, 0, 0, 0)
        bottom_layout.addWidget(self._add_btn)
        bottom_layout.addWidget(self._update_btn)
        bottom_layout.addWidget(self._delete_btn)

        description_label = QLabel("Bake Arnold Pref Attributes to fixate procedural Arnold textures on deforming meshes.")
        description_label.setWordWrap(True)
        central = QWidget()
        layout = QVBoxLayout(central)
        layout.addWidget(description_label)
        layout.addWidget(self._shape_label)
        layout.addWidget(self._list)
        layout.addWidget(bottom_row)
        self.setCentralWidget(central)

        self.setWindowTitle("Pref Baker")
        self._script_job = cmds.scriptJob(event=["SelectionChanged", self._refresh])
        self._refresh()
        self.show(dockable=True, width=300, height=250)

    def closeEvent(self, event):
        self._kill_script_job()
        super().closeEvent(event)

    def dockCloseEventTriggered(self):
        # wird beim Schliessen des (gedockten) workspaceControls statt closeEvent gerufen
        self._kill_script_job()
        super().dockCloseEventTriggered()

    def _kill_script_job(self):
        if self._script_job is not None and cmds.scriptJob(exists=self._script_job):
            cmds.scriptJob(kill=self._script_job, force=True)
        self._script_job = None

    def _refresh(self, *_):
        self._shape = _selected_mesh_shape()
        self._list.clear()
        if self._shape is None:
            self._shape_label.setText("Select a mesh")
        else:
            self._shape_label.setText(self._shape.split("|")[-1])
            self._list.addItems(cmds.listAttr(self._shape, string=_PREF_PREFIX + "*") or [])
        self._add_btn.setEnabled(self._shape is not None)
        self._update_buttons()

    def _update_buttons(self):
        has_selection = bool(self._list.selectedItems())
        self._update_btn.setEnabled(has_selection)
        self._delete_btn.setEnabled(has_selection)

    def _selected_attrs(self) -> list[str]:
        return [item.text() for item in self._list.selectedItems()]

    def _shape_exists(self) -> bool:
        if self._shape and cmds.objExists(self._shape):
            return True
        self._refresh()
        return False

    def _on_add(self):
        if not self._shape_exists():
            return
        name, ok = QInputDialog.getText(self, "Add Pref", "Name (mtoa_varying_<name>):", text="Pref")
        name = name.strip()
        if not ok or not name:
            return
        if not re.match(r"^\w+$", name):
            cmds.warning(f"Invalid attribute name '{name}': only letters, digits and '_' allowed")
            return
        bake_pref(self._shape, name=name)
        self._refresh()

    def _on_update(self):
        if not self._shape_exists():
            return
        # loeschen und neu anlegen, damit auch Attribute mit falschem Typ ersetzt werden
        for attr in self._selected_attrs():
            cmds.deleteAttr(self._shape, attribute=attr)
            bake_pref(self._shape, name=attr[len(_PREF_PREFIX):])
        self._refresh()

    def _on_delete(self):
        if not self._shape_exists():
            return
        for attr in self._selected_attrs():
            cmds.deleteAttr(self._shape, attribute=attr)
        self._refresh()
