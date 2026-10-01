import re
import functools

import maya.cmds as cmds
import maya.mel

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QCheckBox, QComboBox, QScrollArea,
    QFrame, QSizePolicy,
)
from PySide6.QtCore import Qt

from shiboken6 import wrapInstance
import maya.app.general.mayaMixin as maya_mixin
from maya.OpenMayaUI import MQtUtil


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def _name_with_numbered_postfix(name: str, postfix: str, zerofill: int = 2) -> str:
    pattern = f".*{postfix}(?P<num>\\d*)$"
    match = re.match(pattern, name)
    if match:
        name = name[:-(len(postfix))]
        if match.groupdict()["num"]:
            num = str(int(match.groupdict()["num"]) + 1)
            num_len = len(match.groupdict()["num"])
            name = name[:-num_len]
            zerofill = zerofill or num_len
            postfix = f"{postfix}{num.zfill(num_len)}"
        else:
            postfix = f"{postfix}{'2'.zfill(zerofill)}"
    return f"{name}{postfix}"


def _get_curve_length(curve_shape: str) -> float:
    crv_info = cmds.createNode("curveInfo")
    cmds.connectAttr(f"{curve_shape}.worldSpace[0]", f"{crv_info}.inputCurve")
    length = cmds.getAttr(f"{crv_info}.arcLength")
    cmds.delete(crv_info)
    return length


def _get_joint_list(ik_handle: str) -> list:
    start_joint = cmds.ikHandle(ik_handle, q=True, startJoint=True)
    end_effector = cmds.ikHandle(ik_handle, q=True, endEffector=True)
    current = cmds.listRelatives(end_effector, parent=True, fullPath=True)[0]
    joint_list = []
    while True:
        joint_list.append(current)
        short = current.split("|")[-1]
        if short == start_joint or current == start_joint:
            break
        parents = cmds.listRelatives(current, parent=True, fullPath=True)
        if not parents:
            break
        current = parents[0]
    return list(reversed(joint_list))


def _get_free_md_channels(node: str = None, name: str = None):
    """Returns (input1_plug, input2_plug, output_plug) of first free channel."""
    channels = [
        ("input1X", "input2X", "outputX"),
        ("input1Y", "input2Y", "outputY"),
        ("input1Z", "input2Z", "outputZ"),
    ]
    if not node:
        node = cmds.createNode("multiplyDivide", name=name or "multDiv")
        i1, i2, o = channels[0]
        return f"{node}.{i1}", f"{node}.{i2}", f"{node}.{o}"
    for i1, i2, o in channels:
        if not cmds.listConnections(f"{node}.{i1}", source=True, destination=False):
            return f"{node}.{i1}", f"{node}.{i2}", f"{node}.{o}"
    return None


def _insert_normalized_scale_node(unnormalized_plug: str, scalefactor_plug: str,
                                   normalize_node: str = None, name: str = None) -> str:
    src_node = unnormalized_plug.split(".")[0]
    name = name or src_node[:-4]
    dest_plugs = cmds.listConnections(unnormalized_plug, plugs=True,
                                      source=False, destination=True) or []
    in1, in2, out = _get_free_md_channels(node=normalize_node,
                                           name=f"{name}_normalize_div")
    norm_node = in1.split(".")[0]
    cmds.setAttr(f"{norm_node}.operation", 2)
    cmds.connectAttr(unnormalized_plug, in1)
    cmds.connectAttr(scalefactor_plug, in2)
    for dst in dest_plugs:
        cmds.connectAttr(out, dst, force=True)
    return norm_node


def _get_twist_axis(jnt: str) -> tuple:
    axes = [(1,0,0), (-1,0,0), (0,1,0), (0,-1,0), (0,0,1), (0,0,-1)]
    children = cmds.listRelatives(jnt, children=True) or []
    tx, ty, tz = cmds.getAttr(f"{children[0]}.translate")[0]
    vals = [tx, ty, tz]
    best_val, best_idx = 0, None
    for i, t in enumerate(vals):
        if t > best_val:
            best_val, best_idx = t, i * 2
        elif abs(t) > best_val:
            best_val, best_idx = abs(t), i * 2 + 1
    return axes[best_idx]


def _guess_forward_axis(joint: str) -> tuple:
    children = cmds.listRelatives(joint, children=True, type="joint") or []
    tx, ty, tz = cmds.getAttr(f"{children[0]}.translate")[0]
    trans = [abs(tx), abs(ty), abs(tz)]
    m = max(trans)
    return tuple(1 if v == m else 0 for v in trans)


def _place_along_curve(objects: list, curve: str, front_axis: str = "x",
                        up_axis: str = "y", up_vector: tuple = (0, 1, 0),
                        up_object: str = None):
    axis_map = {"x": 0, "y": 1, "z": 2}
    u_step = 1.0 / (len(objects) - 1)
    u_values = [x * u_step for x in range(len(objects))]

    shapes = cmds.listRelatives(curve, shapes=True) or []
    curve_shape = shapes[0] if shapes else curve

    mp = cmds.createNode("motionPath")
    cmds.connectAttr(f"{curve_shape}.worldSpace[0]", f"{mp}.geometryPath")
    cmds.setAttr(f"{mp}.fractionMode", True)
    cmds.setAttr(f"{mp}.follow", True)
    cmds.setAttr(f"{mp}.frontAxis", axis_map.get(front_axis, 0))

    if up_object:
        cmds.setAttr(f"{mp}.worldUpType", 2)
        cmds.setAttr(f"{mp}.worldUpVector", *up_vector)
        cmds.setAttr(f"{mp}.upAxis", axis_map.get(up_axis, 1))
        cmds.connectAttr(f"{up_object}.worldMatrix[0]", f"{mp}.worldUpMatrix")

    for obj, u_val in zip(objects, u_values):
        cmds.setAttr(f"{mp}.uValue", u_val)
        pos = cmds.getAttr(f"{mp}.allCoordinates")[0]
        rot = cmds.getAttr(f"{mp}.rotate")[0]
        cmds.xform(obj, translation=pos, worldSpace=True)
        cmds.xform(obj, rotation=rot, worldSpace=True)

    cmds.delete(mp)


def _add_group(transform: str, name: str = None) -> str:
    if name is None:
        name = transform.split("|")[-1]
    name = _name_with_numbered_postfix(name, "_grp")
    parent = (cmds.listRelatives(transform, parent=True) or [None])[0]
    grp = cmds.group(empty=True, name=name)
    cnstr = cmds.parentConstraint(transform, grp)
    cmds.delete(cnstr)
    if parent:
        cmds.parent(grp, parent)
    cmds.parent(transform, grp)
    return grp


def _single_joint_ctrl(name: str, postfix: str = "_bnd") -> str:
    jnt = cmds.joint(name=f"{name}{postfix}", p=(0, 0, 0))
    cmds.setAttr(f"{jnt}.visibility", False)
    ctrl = cmds.circle(ch=False, normal=(1, 0, 0), name=f"{name}_ctrl")[0]
    _add_group(_add_group(ctrl, f"{name}_offset"), f"{name}_null")
    cmds.parent(jnt, ctrl)
    return jnt


def _create_joint_controls_along_curve(curve: str, up_object: str,
                                        num_controls: int, name: str = None) -> list:
    name = name or "_".join(curve.split("_")[:-1])
    jnt_list = [_single_joint_ctrl(f"{name}_{i + 1}") for i in range(num_controls)]
    null_list = []
    for jnt in jnt_list:
        ctrl = cmds.listRelatives(jnt, parent=True)[0]
        offset = cmds.listRelatives(ctrl, parent=True)[0]
        null = cmds.listRelatives(offset, parent=True)[0]
        null_list.append(null)
    _place_along_curve(null_list, curve, up_object=up_object)
    return jnt_list


def get_selected_channelbox_attributes() -> list:
    return maya.mel.eval("selectedChannelBoxAttributes();") or []


# ---------------------------------------------------------------------------
# public rig functions
# ---------------------------------------------------------------------------

def create_spline_ik(start_joint: str, end_joint: str,
                     name: str = None, curve_spans: int = 4):
    name = name or start_joint.split("|")[-1][:-1]
    result = cmds.ikHandle(
        n=f"{name}_spline_ik", sol="ikSplineSolver",
        sj=start_joint, ee=end_joint, pcv=False, ns=curve_spans,
    )
    ik_handle, ik_effector, ik_curve = result[0], result[1], result[2]
    ik_curve = cmds.rename(ik_curve, f"{name}_ik_crv")
    cmds.rename(ik_effector, f"{name}_spline_effector")
    cmds.setAttr(f"{ik_handle}.visibility", False)
    if not cmds.attributeQuery("scale_power", node=ik_handle, exists=True):
        cmds.addAttr(ik_handle, ln="scale_power", keyable=True)
    curve_shape = (cmds.listRelatives(ik_curve, shapes=True) or [ik_curve])[0]
    cmds.addAttr(ik_handle, ln="initial_curve_length", at="float")
    cmds.setAttr(f"{ik_handle}.initial_curve_length", _get_curve_length(curve_shape))
    cmds.setAttr(f"{ik_curve}.visibility", False)
    return ik_handle, ik_curve, name


def recommend_up_vector(ik_handle: str, spline_ik_joint: str, up_object: str) -> tuple:
    axes_map = (
        (0, 1, 0), (0, -1, 0), (0, 1, 0),
        (0, 0, 1), (0, 0, -1), (0, 0, 1),
        (1, 0, 0), (-1, 0, 0), (1, 0, 0),
    )
    translate_values = axes_map[cmds.getAttr(f"{ik_handle}.dWorldUpAxis")]

    ref_loc = cmds.spaceLocator(p=(0, 0, 0))[0]
    cmds.delete(cmds.pointConstraint(up_object, ref_loc, mo=False))
    cmds.delete(cmds.orientConstraint(spline_ik_joint, ref_loc, mo=False))

    loc = cmds.spaceLocator(p=(0, 0, 0))[0]
    cmds.parent(loc, ref_loc)
    cmds.setAttr(f"{loc}.translate", *translate_values)
    cmds.parent(loc, up_object, absolute=True)
    new_translate = cmds.getAttr(f"{loc}.translate")[0]

    cmds.delete(loc, ref_loc)
    return new_translate


def create_curve_based_scale_setup(ik_handle: str, name: str = None):
    joints = _get_joint_list(ik_handle)
    if name is None:
        name = joints[0].split("|")[-1]
    ik_curve = cmds.ikHandle(ik_handle, q=True, c=True)
    curve_shape = (cmds.listRelatives(ik_curve, shapes=True) or [ik_curve])[0]

    crv_info = cmds.createNode("curveInfo", name=f"{name}_ik_crvinfo")
    div_node = cmds.createNode("multiplyDivide", name=f"{name}_ik_div")
    cmds.setAttr(f"{div_node}.operation", 2)
    cmds.connectAttr(f"{curve_shape}.worldSpace[0]", f"{crv_info}.inputCurve")
    cmds.connectAttr(f"{crv_info}.arcLength", f"{div_node}.input1X")
    cmds.setAttr(f"{div_node}.input2X", cmds.getAttr(f"{ik_handle}.initial_curve_length"))

    axis_map = {(1,0,0): "scaleX", (0,1,0): "scaleY", (0,0,1): "scaleZ"}
    for joint in joints:
        scale_attr = axis_map[_guess_forward_axis(joint)]
        cmds.connectAttr(f"{div_node}.outputX", f"{joint}.{scale_attr}")

    return crv_info, f"{div_node}.outputX"


def setup_advanced_twist_control(ik_handle: str, start_up_obj: str, end_up_obj: str):
    cmds.setAttr(f"{ik_handle}.dWorldUpType", 4)
    start_joint = cmds.ikHandle(ik_handle, q=True, startJoint=True)
    end_effector = cmds.ikHandle(ik_handle, q=True, endEffector=True)
    end_joint = cmds.listRelatives(end_effector, parent=True)[0]

    twist_axis = _get_twist_axis(start_joint)
    forward_axis_map = {
        (1,0,0): 0, (-1,0,0): 1,
        (0,1,0): 2, (0,-1,0): 3,
        (0,0,1): 4, (0,0,-1): 5,
    }
    fa = forward_axis_map[twist_axis]
    cmds.setAttr(f"{ik_handle}.dForwardAxis", fa)
    up_axis_map = [0, 0, 3, 3, 6, 6]
    cmds.setAttr(f"{ik_handle}.dWorldUpAxis", up_axis_map[fa])
    cmds.setAttr(f"{ik_handle}.dWorldUpVector",
                 *recommend_up_vector(ik_handle, start_joint, start_up_obj))
    cmds.setAttr(f"{ik_handle}.dWorldUpVectorEnd",
                 *recommend_up_vector(ik_handle, end_joint, end_up_obj))
    cmds.connectAttr(f"{start_up_obj}.worldMatrix[0]", f"{ik_handle}.dWorldUpMatrix")
    cmds.connectAttr(f"{end_up_obj}.worldMatrix[0]", f"{ik_handle}.dWorldUpMatrixEnd")
    cmds.setAttr(f"{ik_handle}.dTwistControlEnable", True)


def setup_squash_stretch(ik_handle: str, scale_factor_plug: str, name: str):
    joint_list = _get_joint_list(ik_handle)
    if not cmds.attributeQuery("scale_power", node=ik_handle, exists=True):
        cmds.addAttr(ik_handle, ln="scale_power", at="float")

    sp = f"{ik_handle}.scale_power"
    cmds.setKeyframe(sp, t=1, v=0)
    cmds.setKeyframe(sp, t=len(joint_list), v=0)
    anim_curve = (cmds.listConnections(sp, type="animCurve") or [None])[0]
    if anim_curve:
        cmds.keyTangent(anim_curve, weightedTangents=True)
        cmds.keyTangent(anim_curve, e=True, absolute=True, t=(1, 1), outAngle=50)
        cmds.keyTangent(anim_curve, e=True, absolute=True,
                        t=(len(joint_list), len(joint_list)), inAngle=-50)

    axes_map = {
        (1,0,0): ("sx", "sy", "sz"),
        (0,1,0): ("sy", "sx", "sz"),
        (0,0,1): ("sz", "sy", "sx"),
    }
    frame_caches = []
    expr_lines = [f"$scale = {scale_factor_plug};", "$sqrt = 1 / sqrt($scale);"]
    for i, joint in enumerate(joint_list, 1):
        fc = cmds.createNode("frameCache", n=f"{name}_{joint.split('|')[-1]}_fcache")
        cmds.setAttr(f"{fc}.varyTime", i)
        cmds.connectAttr(sp, f"{fc}.stream")
        fw = _guess_forward_axis(joint)
        j_short = joint.split("|")[-1]
        a1, a2 = axes_map[fw][1], axes_map[fw][2]
        expr_lines.append(f"{j_short}.{a1} = pow($sqrt, {fc}.varying);")
        expr_lines.append(f"{j_short}.{a2} = pow($sqrt, {fc}.varying);")
        frame_caches.append(fc)

    expression_node = cmds.expression(s="\n".join(expr_lines), n=f"{name}_expr")
    return expression_node, frame_caches


# ---------------------------------------------------------------------------
# SplineIKRig
# ---------------------------------------------------------------------------

class SplineIKRig:
    """Manages a spline IK rig. All node references are plain string names."""

    def __init__(self, ik_handle: str):
        self.ik_handle = ik_handle
        self._tag = "spline_ik_handle"
        self.initial_dropoff_rate: float = 4.0

        for attr in ("control_joints", "controls", "stretch_div", "skin_cluster", "curve_info"):
            if not cmds.attributeQuery(attr, node=ik_handle, exists=True):
                cmds.addAttr(ik_handle, ln=attr, at="message")
        if not cmds.attributeQuery("world_scale_attr", node=ik_handle, exists=True):
            cmds.addAttr(ik_handle, ln="world_scale_attr", at="float")
        if not cmds.attributeQuery("prefix", node=ik_handle, exists=True):
            cmds.addAttr(ik_handle, ln="prefix", dt="string")
        if not cmds.attributeQuery("scale_power", node=ik_handle, exists=True):
            cmds.addAttr(ik_handle, ln="scale_power", at="float")
        if not cmds.attributeQuery("initial_curve_length", node=ik_handle, exists=True):
            crv = cmds.ikHandle(ik_handle, q=True, c=True)
            shape = (cmds.listRelatives(crv, shapes=True) or [crv])[0]
            cmds.addAttr(ik_handle, ln="initial_curve_length", at="float")
            cmds.setAttr(f"{ik_handle}.initial_curve_length", _get_curve_length(shape))

        stored = cmds.getAttr(f"{ik_handle}.prefix")
        self._prefix = stored if stored else ik_handle.split("|")[-1]
        cmds.setAttr(f"{ik_handle}.visibility", False)

    # --- rig operations ---

    def rebuild_curve(self, number_of_spans: int):
        cmds.rebuildCurve(self.curve, s=number_of_spans, ch=0, rpo=1, rt=0,
                          end=1, kr=0, kcp=0, kep=1, kt=0, d=3, tol=0.01)

    def add_stretch(self):
        sel = cmds.ls(sl=True)
        crv_info, stretch_div_plug = create_curve_based_scale_setup(
            self.ik_handle, name=self.prefix)
        stretch_div = stretch_div_plug.split(".")[0]
        self.tag_node_and_connect(crv_info, "curve_info")
        self.tag_node_and_connect(stretch_div, "stretch_div")
        if self.skin_cluster:
            crv = self.curve
            shapes = cmds.listRelatives(crv, shapes=True) or []
            main_shape = shapes[0] if shapes else None
            orig_shapes = [s for s in shapes if s != main_shape]
            if orig_shapes:
                cmds.setAttr(f"{stretch_div}.input2X",
                             _get_curve_length(orig_shapes[0]))
        if sel:
            cmds.select(sel)

    def remove_stretch(self):
        self.remove_volume()
        self.remove_world_scale()
        sd = self.stretch_div
        if sd:
            cmds.delete(sd)
            axis_map = {(1,0,0): "scaleX", (0,1,0): "scaleY", (0,0,1): "scaleZ"}
            for jnt in self.joints:
                cmds.setAttr(f"{jnt}.{axis_map[_guess_forward_axis(jnt)]}", 1)

    def add_controllers(self, number_of_controls: int):
        joints = self.joints
        bind_joints = _create_joint_controls_along_curve(
            self.curve, joints[0], number_of_controls, name=self.prefix)
        for i, jnt in enumerate(bind_joints):
            self.tag_node_and_connect(jnt, "control_joints")
            ctrl = cmds.listRelatives(jnt, parent=True)[0]
            self.tag_node_and_connect(ctrl, "controls")
            if not cmds.attributeQuery("order", node=jnt, exists=True):
                cmds.addAttr(jnt, ln="order", at="byte")
            cmds.setAttr(f"{jnt}.order", i + 1)
            if not cmds.attributeQuery("dropoff_rate", node=jnt, exists=True):
                cmds.addAttr(jnt, ln="dropoff_rate", at="float")
            cmds.setAttr(f"{jnt}.dropoff_rate", self.initial_dropoff_rate)

        def _null(jnt):
            ctrl = cmds.listRelatives(jnt, parent=True)[0]
            offset = cmds.listRelatives(ctrl, parent=True)[0]
            return cmds.listRelatives(offset, parent=True)[0]

        cmds.delete(cmds.orientConstraint(joints[0], _null(bind_joints[0])))
        cmds.delete(cmds.orientConstraint(joints[-1], _null(bind_joints[-1])))
        setup_advanced_twist_control(self.ik_handle, bind_joints[0], bind_joints[-1])
        self.bind_curve()

    def remove_controllers(self, delete_parents: bool = True):
        self.unbind_curve()
        for ctrl in self.controls:
            offset_grp = (cmds.listRelatives(ctrl, parent=True) or [None])[0]
            null_grp = (cmds.listRelatives(offset_grp, parent=True)
                        if offset_grp else [None])[0] if offset_grp else None
            if cmds.objExists(ctrl):
                cmds.delete(ctrl)
            if delete_parents:
                if offset_grp and cmds.objExists(offset_grp) and \
                        offset_grp.endswith("_offset_grp"):
                    cmds.delete(offset_grp)
                if null_grp and cmds.objExists(null_grp) and \
                        null_grp.endswith("_null_grp"):
                    cmds.delete(null_grp)

    def bind_curve(self):
        sc = cmds.skinCluster(
            *self.control_joints, self.curve,
            bindMethod=0, name=f"{self.prefix}_skinCluster",
            dropoffRate=self.initial_dropoff_rate,
        )[0]
        self.tag_node_and_connect(sc, "skin_cluster")

    def unbind_curve(self):
        sc = self.skin_cluster
        if sc:
            cmds.delete(sc)

    def adjust_dropoff(self, jnt: str, dropoff_delta: float):
        val = max(0.1, min(cmds.getAttr(f"{jnt}.dropoff_rate") + dropoff_delta, 10.0))
        cmds.setAttr(f"{jnt}.dropoff_rate", val)
        cmds.skinCluster(self.skin_cluster, e=True, inf=jnt, dr=val)

    def reset_dropoff(self):
        for jnt in self.control_joints:
            cmds.setAttr(f"{jnt}.dropoff_rate", self.initial_dropoff_rate)
            cmds.skinCluster(self.skin_cluster, e=True, inf=jnt,
                             dr=self.initial_dropoff_rate)

    def add_volume(self):
        sel = cmds.ls(sl=True)
        setup_squash_stretch(self.ik_handle, self.scale_factor_attr, self.prefix)
        if sel:
            cmds.select(sel)

    def remove_volume(self):
        exp = self.expression
        if exp:
            cmds.delete(exp)
            axis_map = {
                (1,0,0): ("scaleY", "scaleZ"),
                (0,1,0): ("scaleX", "scaleZ"),
                (0,0,1): ("scaleX", "scaleY"),
            }
            for jnt in self.joints:
                a1, a2 = axis_map[_guess_forward_axis(jnt)]
                cmds.setAttr(f"{jnt}.{a1}", 1)
                cmds.setAttr(f"{jnt}.{a2}", 1)

    def add_world_scale(self, attr_plug: str):
        sel = cmds.ls(sl=True)
        ci = self.curve_info
        _insert_normalized_scale_node(f"{ci}.arcLength", attr_plug, name=self._prefix)
        cmds.connectAttr(attr_plug, f"{self.ik_handle}.world_scale_attr", force=True)
        if sel:
            cmds.select(sel)

    def remove_world_scale(self):
        wsd = self.world_scale_div
        if wsd:
            ci = self.curve_info
            sd = self.stretch_div
            cmds.connectAttr(f"{ci}.arcLength", f"{sd}.input1X", force=True)
            wsa = self.world_scale_attr
            if wsa:
                cmds.disconnectAttr(wsa, f"{self.ik_handle}.world_scale_attr")
            cmds.delete(wsd)

    def is_stretchy(self) -> bool:
        return self.curve_info is not None

    def is_volume_maintaining(self) -> bool:
        return bool(self.frame_caches)

    def list_all_nodes(self) -> list:
        nodes = []
        for ctrl in self.controls:
            nodes.append(ctrl)
            offset = (cmds.listRelatives(ctrl, parent=True) or [None])[0]
            if offset and offset.endswith("_offset_grp"):
                nodes.append(offset)
                null = (cmds.listRelatives(offset, parent=True) or [None])[0]
                if null and null.endswith("_null_grp"):
                    nodes.append(null)
        nodes.extend(self.control_joints)
        nodes.extend(self.frame_caches)
        if self.curve:
            nodes.append(self.curve)
        if self.curve_info:
            nodes.append(self.curve_info)
        if self.world_scale_div:
            nodes.append(self.world_scale_div)
        if self.stretch_div:
            nodes.append(self.stretch_div)
        if self.skin_cluster:
            nodes.append(self.skin_cluster)
        return nodes

    def tag_node(self, node: str):
        if not cmds.attributeQuery(self._tag, node=node, exists=True):
            cmds.addAttr(node, ln=self._tag, at="message")

    def tag_node_and_connect(self, node: str, plug: str):
        self.tag_node(node)
        cmds.connectAttr(f"{self.ik_handle}.{plug}", f"{node}.{self._tag}", force=True)

    # --- properties ---

    @property
    def frame_caches(self) -> list:
        return cmds.listConnections(f"{self.ik_handle}.scale_power",
                                    type="frameCache") or []

    @property
    def joints(self) -> list:
        return _get_joint_list(self.ik_handle)

    @property
    def curve(self) -> str:
        return cmds.ikHandle(self.ik_handle, q=True, c=True)

    @property
    def curve_info(self):
        nodes = cmds.listConnections(f"{self.ik_handle}.curve_info",
                                     type="curveInfo") or []
        return None if not nodes else nodes[0]

    @property
    def controls(self) -> list:
        return cmds.listConnections(f"{self.ik_handle}.controls") or []

    @property
    def control_joints(self) -> list:
        joints = cmds.listConnections(f"{self.ik_handle}.control_joints",
                                      type="joint") or []
        return sorted(joints, key=lambda j: cmds.getAttr(f"{j}.order"))

    @property
    def world_scale_attr(self):
        plugs = cmds.listConnections(f"{self.ik_handle}.world_scale_attr",
                                     plugs=True, source=True, destination=False) or []
        return None if not plugs else plugs[0]

    @property
    def scale_factor_attr(self):
        sd = self.stretch_div
        return None if not sd else f"{sd}.outputX"

    @property
    def world_scale_object(self):
        wsa = self.world_scale_attr
        return None if not wsa else wsa.split(".")[0]

    @property
    def world_scale_div(self):
        wsa = self.world_scale_attr
        if not wsa:
            return None
        divs = cmds.listConnections(wsa, type="multiplyDivide") or []
        return None if not divs else divs[0]

    @property
    def stretch_div(self):
        divs = cmds.listConnections(f"{self.ik_handle}.stretch_div",
                                    type="multiplyDivide") or []
        return None if not divs else divs[0]

    @property
    def expression(self):
        sd = self.stretch_div
        if not sd:
            return None
        exprs = cmds.listConnections(sd, type="expression") or []
        return None if not exprs else exprs[0]

    @property
    def skin_cluster(self):
        scs = cmds.listConnections(f"{self.ik_handle}.skin_cluster",
                                   type="skinCluster") or []
        return None if not scs else scs[0]

    @property
    def prefix(self) -> str:
        return self._prefix

    def change_prefix(self, name: str):
        for node in self.list_all_nodes():
            short = node.split("|")[-1]
            new_name = short.replace(self.prefix, name)
            if new_name != short:
                cmds.rename(node, new_name)
        crv = self.curve
        crv_shape = (cmds.listRelatives(crv, shapes=True) or [None])[0]
        if crv_shape:
            cmds.rename(crv_shape, f"{name}_ik_crvShape")
        cmds.rename(crv, f"{name}_ik_crv")
        cmds.rename(self.ik_handle, f"{name}_ik_hndl")
        self.ik_handle = f"{name}_ik_hndl"
        self._prefix = name
        cmds.setAttr(f"{self.ik_handle}.prefix", name, type="string")


# ---------------------------------------------------------------------------
# SplineIKManager (PySide6)
# ---------------------------------------------------------------------------

class SplineIKManager(maya_mixin.MayaQWidgetDockableMixin, QMainWindow):

    def __init__(self):
        super().__init__(parent=wrapInstance(int(MQtUtil.mainWindow()), QWidget))
        self.rig = None
        self._script_jobs = []
        self._num_handles = 0

        # --- combo ---
        self._combo = QComboBox()
        self._combo.currentTextChanged.connect(self._on_combo_changed)

        # --- edit area ---
        self._edit_widget = QWidget()
        self._edit_widget.setEnabled(False)
        edit_layout = QVBoxLayout(self._edit_widget)
        edit_layout.setContentsMargins(0, 0, 0, 0)
        edit_layout.setSpacing(4)

        self._prefix_edit, self._prefix_btn = self._make_row(
            edit_layout, "Prefix", "Change", self._change_prefix)
        self._prefix_edit.textChanged.connect(self._on_prefix_changed)

        self._spans_edit, self._spans_btn = self._make_row(
            edit_layout, "Curve Spans", "Change", self._change_spans)
        self._spans_edit.textChanged.connect(self._on_spans_changed)

        self._ctrl_edit, self._ctrl_btn = self._make_row(
            edit_layout, "Controllers", "Create", self._create_controllers)
        self._ctrl_edit.setText("3")
        self._ctrl_edit.textChanged.connect(self._on_ctrl_count_changed)

        # joint list
        self._scroll_area = QScrollArea()
        self._scroll_area.setWidgetResizable(True)
        # self._scroll_area.setFixedHeight(120)
        self._joints_widget = QWidget()
        self._joints_layout = QVBoxLayout(self._joints_widget)
        self._joints_layout.setContentsMargins(2, 2, 2, 2)
        self._joints_layout.setSpacing(4)
        self._scroll_area.setWidget(self._joints_widget)
        edit_layout.addWidget(self._scroll_area)

        reset_btn = QPushButton("Reset Dropoff")
        reset_btn.clicked.connect(self._reset_dropoff)
        edit_layout.addWidget(reset_btn)

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        edit_layout.addWidget(sep)

        cb_row = QWidget()
        cb_layout = QHBoxLayout(cb_row)
        cb_layout.setContentsMargins(0, 0, 0, 0)
        self._stretchy_cb = QCheckBox("Stretchy")
        self._volume_cb = QCheckBox("Maintain Volume")
        self._stretchy_cb.toggled.connect(self._toggle_stretchy)
        self._volume_cb.toggled.connect(self._toggle_volume)
        cb_layout.addWidget(self._stretchy_cb)
        cb_layout.addWidget(self._volume_cb)
        edit_layout.addWidget(cb_row)

        sep2 = QFrame()
        sep2.setFrameShape(QFrame.Shape.HLine)
        edit_layout.addWidget(sep2)

        ws_row = QWidget()
        ws_layout = QHBoxLayout(ws_row)
        ws_layout.setContentsMargins(0, 0, 0, 0)
        ws_lbl = QLabel("World Scale:")
        ws_lbl.setFixedWidth(self._LBL_W)
        ws_layout.addWidget(ws_lbl)
        self._ws_edit = QLineEdit()
        self._ws_edit.setReadOnly(True)
        self._ws_edit.setPlaceholderText("Select attr in Channel Box →")
        self._ws_btn = QPushButton("Set")
        self._ws_btn.setFixedWidth(self._BTN_W)
        self._ws_btn.clicked.connect(self._set_world_scale)
        ws_layout.addWidget(self._ws_edit)
        ws_layout.addWidget(self._ws_btn)
        edit_layout.addWidget(ws_row)

        # --- main layout ---
        central = QWidget()
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(4, 4, 4, 4)
        main_layout.setSpacing(4)
        main_layout.addWidget(self._combo)
        main_layout.addWidget(self._edit_widget)
        self.setCentralWidget(central)

        self.setWindowTitle("Spline IK Manager")
        self.setMinimumWidth(280)
        self.show(dockable=True, width=280, height=460)

        self._register_script_jobs()
        self._update_combo()

    # --- helpers ---

    _LBL_W = 70
    _BTN_W = 60

    def _make_row(self, layout, label: str, btn_label: str, callback) -> tuple:
        row = QWidget()
        rl = QHBoxLayout(row)
        rl.setContentsMargins(0, 0, 0, 0)
        lbl = QLabel(label)
        lbl.setFixedWidth(self._LBL_W)
        rl.addWidget(lbl)
        edit = QLineEdit()
        btn = QPushButton(btn_label)
        btn.setFixedWidth(self._BTN_W)
        btn.setEnabled(False)
        btn.clicked.connect(callback)
        rl.addWidget(edit)
        rl.addWidget(btn)
        layout.addWidget(row)
        return edit, btn

    def _register_script_jobs(self):
        self._script_jobs = [
            cmds.scriptJob(event=["DagObjectCreated", self._update_combo]),
            cmds.scriptJob(event=["NameChanged", self._update_combo]),
            cmds.scriptJob(event=["idleVeryLow", self._check_handle_deletion]),
        ]

    def closeEvent(self, event):
        self._kill_script_jobs()
        super().closeEvent(event)

    def _kill_script_jobs(self):
        for job in self._script_jobs:
            if cmds.scriptJob(exists=job):
                cmds.scriptJob(kill=job, force=True)
        self._script_jobs = []

    # --- combo / scene sync ---

    def _list_spline_handles(self) -> list:
        result = []
        for h in cmds.ls(type="ikHandle") or []:
            solver = (cmds.listConnections(f"{h}.ikSolver") or [None])[0]
            if solver and cmds.nodeType(solver) == "ikSplineSolver":
                result.append(h)
        return result

    def _update_combo(self, *_):
        handles = self._list_spline_handles()
        self._num_handles = len(handles)
        current = self._combo.currentText()
        self._combo.blockSignals(True)
        self._combo.clear()
        self._combo.addItem("-- choose IK handle --")
        for h in handles:
            self._combo.addItem(h)
        if current in handles:
            self._combo.setCurrentText(current)
        self._combo.blockSignals(False)

    def _check_handle_deletion(self):
        handles = self._list_spline_handles()
        if len(handles) != self._num_handles:
            self._num_handles = len(handles)
            current = self._combo.currentText()
            self._update_combo()
            if current not in handles:
                self.rig = None
                self._edit_widget.setEnabled(False)

    def _on_combo_changed(self, text: str):
        self._edit_widget.setEnabled(False)
        if not cmds.objExists(text):
            self.rig = None
            return
        self.rig = SplineIKRig(text)
        self._stretchy_cb.blockSignals(True)
        self._volume_cb.blockSignals(True)
        self._edit_widget.setEnabled(True)

        self._prefix_edit.blockSignals(True)
        self._prefix_edit.setText(self.rig.prefix)
        self._prefix_edit.blockSignals(False)
        self._prefix_btn.setEnabled(True)

        crv = self.rig.curve
        spans = cmds.getAttr(f"{crv}.spans") if crv else ""
        self._spans_edit.blockSignals(True)
        self._spans_edit.setText(str(spans))
        self._spans_edit.blockSignals(False)
        self._spans_btn.setEnabled(True)

        n_ctrls = len(self.rig.controls)
        self._ctrl_edit.blockSignals(True)
        self._ctrl_edit.setText(str(n_ctrls) if n_ctrls else "3")
        self._ctrl_edit.blockSignals(False)
        self._ctrl_btn.setText("Change" if n_ctrls else "Create")
        self._ctrl_btn.setEnabled(True)

        self._update_joints_list()

        stretchy = self.rig.is_stretchy()
        self._stretchy_cb.setChecked(stretchy)
        self._stretchy_cb.blockSignals(False)

        self._volume_cb.setChecked(self.rig.is_volume_maintaining())
        self._volume_cb.setEnabled(stretchy)
        self._volume_cb.blockSignals(False)

        wsa = self.rig.world_scale_attr
        self._ws_edit.setText(wsa if wsa else "")
        self._ws_btn.setEnabled(stretchy)
        if wsa:
            self._ws_btn.setText("Remove")
            self._ws_btn.clicked.disconnect()
            self._ws_btn.clicked.connect(self._remove_world_scale)
        else:
            self._ws_btn.setText("Set")
            self._ws_btn.clicked.disconnect()
            self._ws_btn.clicked.connect(self._set_world_scale)

    # --- joint list ---

    def _update_joints_list(self):
        while self._joints_layout.count():
            item = self._joints_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        for jnt in self.rig.control_joints:
            row = QWidget()
            rl = QHBoxLayout(row)
            rl.setContentsMargins(0, 0, 0, 0)
            rl.addWidget(QLabel(jnt.split("|")[-1]))
            m_btn = QPushButton("+")
            m_btn.setFixedWidth(24)
            p_btn = QPushButton("-")
            p_btn.setFixedWidth(24)
            m_btn.clicked.connect(functools.partial(self.rig.adjust_dropoff, jnt, -0.2))
            p_btn.clicked.connect(functools.partial(self.rig.adjust_dropoff, jnt, 0.2))
            rl.addWidget(m_btn)
            rl.addWidget(p_btn)
            self._joints_layout.addWidget(row)
        self._joints_layout.addStretch()

    # --- prefix ---

    def _on_prefix_changed(self, text: str):
        self._prefix_btn.setEnabled(bool(self.rig) and text != self.rig.prefix)

    def _change_prefix(self):
        if not self.rig:
            return
        name = self._prefix_edit.text().strip()
        if name:
            self.rig.change_prefix(name)
            self._update_combo()
            self._combo.blockSignals(True)
            self._combo.setCurrentText(self.rig.ik_handle)
            self._combo.blockSignals(False)
            self._update_joints_list()
        self._prefix_btn.setEnabled(False)

    # --- spans ---

    def _on_spans_changed(self, text: str):
        digits = "".join(c for c in text if c.isdigit())
        if not digits or not self.rig:
            self._spans_btn.setEnabled(False)
            return
        crv = self.rig.curve
        cur_spans = cmds.getAttr(f"{crv}.spans") if crv else None
        self._spans_btn.setEnabled(int(digits) > 2 and int(digits) != cur_spans)

    def _change_spans(self):
        if not self.rig:
            return
        text = self._spans_edit.text().strip()
        if not text.isdigit():
            return
        num = int(text)
        if num <= 2:
            return
        crv = self.rig.curve
        if cmds.getAttr(f"{crv}.spans") == num:
            return
        num_ctrls = 0
        if self.rig.skin_cluster:
            answer = cmds.confirmDialog(
                title="Warning",
                message="Spline is already bound!\nChanging spans deletes controllers and binding.\nContinue?",
                button=["OK", "Cancel"], defaultButton="Cancel", cancelButton="Cancel",
            )
            if answer != "OK":
                return
            num_ctrls = len(self.rig.controls)
            self.rig.remove_controllers()
        self.rig.rebuild_curve(num)
        cmds.delete(self.rig.curve, ch=True)
        if num_ctrls:
            self.rig.add_controllers(num_ctrls)
            self._update_joints_list()
        self._spans_btn.setEnabled(False)

    # --- controllers ---

    def _on_ctrl_count_changed(self, text: str):
        digits = "".join(c for c in text if c.isdigit())
        if not digits or not self.rig:
            self._ctrl_btn.setEnabled(False)
            return
        self._ctrl_btn.setEnabled(int(digits) >= 2 and int(digits) != len(self.rig.controls))

    def _create_controllers(self):
        if not self.rig:
            return
        text = self._ctrl_edit.text().strip()
        if not text.isdigit():
            return
        num = int(text)
        if self.rig.skin_cluster:
            answer = cmds.confirmDialog(
                title="Warning",
                message="Spline is already bound!\nChanging controllers deletes current bind.\nContinue?",
                button=["OK", "Cancel"], defaultButton="Cancel", cancelButton="Cancel",
            )
            if answer != "OK":
                return
            self.rig.remove_controllers()
        self.rig.add_controllers(num)
        self._ctrl_btn.setText("Change")
        self._ctrl_btn.setEnabled(False)
        self._update_joints_list()

    def _reset_dropoff(self):
        if self.rig:
            self.rig.reset_dropoff()

    # --- stretchy / volume ---

    def _toggle_stretchy(self, checked: bool):
        if not self.rig:
            return
        if checked:
            self.rig.add_stretch()
            self._volume_cb.setEnabled(True)
            self._ws_btn.setEnabled(True)
        else:
            self.rig.remove_stretch()
            self._volume_cb.blockSignals(True)
            self._volume_cb.setChecked(False)
            self._volume_cb.setEnabled(False)
            self._volume_cb.blockSignals(False)
            self._ws_edit.clear()
            self._ws_btn.setText("Set")
            self._ws_btn.clicked.disconnect()
            self._ws_btn.clicked.connect(self._set_world_scale)
            self._ws_btn.setEnabled(False)

    def _toggle_volume(self, checked: bool):
        if not self.rig:
            return
        if checked:
            self.rig.add_volume()
        else:
            self.rig.remove_volume()

    # --- world scale ---

    def _set_world_scale(self):
        if not self.rig:
            return
        attrs = get_selected_channelbox_attributes()
        if not attrs:
            cmds.warning("Please select exactly one attribute in the Channel Box.")
            return
        sel = cmds.ls(sl=True)
        if not sel:
            return
        attr_plug = f"{sel[0]}.{attrs[0]}"
        self.rig.add_world_scale(attr_plug)
        self._ws_edit.setText(attr_plug)
        self._ws_btn.setText("Remove")
        self._ws_btn.clicked.disconnect()
        self._ws_btn.clicked.connect(self._remove_world_scale)

    def _remove_world_scale(self):
        if not self.rig:
            return
        self.rig.remove_world_scale()
        self._ws_edit.clear()
        self._ws_btn.setText("Set")
        self._ws_btn.clicked.disconnect()
        self._ws_btn.clicked.connect(self._set_world_scale)
