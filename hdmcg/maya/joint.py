import maya.cmds as cmds

from PySide6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QLabel, QSpinBox, QSlider, QPushButton
from PySide6.QtCore import Qt

from shiboken6 import wrapInstance
import maya.app.general.mayaMixin as maya_mixin
from maya.OpenMayaUI import MQtUtil


def split(joint: str, num_segments: int = 2):
    """Splits a joint segment into num_segments equal parts using maya.cmds.

    `joint` is the parent of the segment to split. The child joint's local
    translation defines the full segment vector; each inserted joint steps
    by 1/num_segments of that vector.
    """
    child_joints = cmds.listRelatives(joint, children=True, fullPath=True, type='joint') or []

    if not child_joints:
        cmds.warning("Joint has no child-joint. Split cannot be performed.")
        return
    if len(child_joints) > 1:
        cmds.warning("Joint has more than one child-joint. Aborted.")
        return

    radius = cmds.getAttr(f'{joint}.radius')
    name = joint.split('|')[-1]

    child_joint = child_joints[0]
    child_name = child_joint.split('|')[-1]
    tx, ty, tz = cmds.getAttr(f'{child_joint}.translate')[0]
    deltas = [tx / num_segments, ty / num_segments, tz / num_segments]

    for i in range(1, num_segments):
        new_joint = cmds.insertJoint(joint)
        joint = cmds.joint(new_joint, edit=True, relative=True, position=deltas,
                           radius=radius, name=f'{name}_seg_{i}')

    cmds.setAttr(f'{child_name}.translate', *deltas, type='double3')


class SplitSelected(maya_mixin.MayaQWidgetDockableMixin, QMainWindow):

    def __init__(self):
        super().__init__(parent=wrapInstance(int(MQtUtil.mainWindow()), QWidget))

        self._spinbox = QSpinBox()
        self._spinbox.setRange(2, 9999)
        self._spinbox.setValue(3)
        self._spinbox.setFixedWidth(40)

        self._slider = QSlider(Qt.Orientation.Horizontal)
        self._slider.setRange(2, 20)
        self._slider.setValue(3)

        self._spinbox.valueChanged.connect(self._on_spinbox_changed)
        self._slider.valueChanged.connect(self._on_spinbox_from_slider)

        btn = QPushButton("Split")
        btn.clicked.connect(self._on_split)

        row = QWidget()
        layout = QHBoxLayout(row)
        layout.setContentsMargins(4, 0, 4, 0)
        layout.addWidget(QLabel("Segments:"))
        layout.addWidget(self._spinbox)
        layout.addWidget(self._slider)
        layout.addWidget(btn)
        self.setCentralWidget(row)

        self.setWindowTitle("Split Selected \"Bone\"")
        self.setMinimumWidth(250)
        self.setMaximumHeight(50)
        self.show(dockable=True, width=300, height=30)

    def _on_spinbox_changed(self, value):
        self._slider.blockSignals(True)
        self._slider.setValue(value)
        self._slider.blockSignals(False)

    def _on_spinbox_from_slider(self, value):
        self._spinbox.blockSignals(True)
        self._spinbox.setValue(value)
        self._spinbox.blockSignals(False)

    def _on_split(self):
        joints = cmds.ls(sl=True, type='joint', long=True)
        if not joints:
            cmds.warning("SplitSelected: no joints selected.")
            return
        n = self._spinbox.value()
        for jnt in joints:
            split(jnt, n)

