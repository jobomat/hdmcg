import json
import os
from shutil import copytree, copyfile
from pathlib import Path

from PySide6.QtWidgets import *
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QDoubleValidator

from shiboken6 import wrapInstance
import maya.app.general.mayaMixin as maya_mixin
from maya.OpenMayaUI import MQtUtil
import maya.cmds as cmds

from hdmcg.maya.rigicons.widgets import (
    ColorPaletteWidget, IconPaletteWidget, RotateWidget, ScaleShapesWidget,
    ExpandableRowWidget, ToggleLockHideWidget, ToggleRenderableSelectableWidget
)
from hdmcg.qt.widgets import QHLine
from hdmcg.maya.color import set_wireframe_color
from hdmcg.maya.shape import (
    add_shape, rotate_shapes,
    capture_shape_points, apply_shape_points, scale_shapes_from_capture,
)
from hdmcg.maya.transform import (
    add_group, toggle_lock_hide, toggle_renderable, toggle_selectable
)


class RigIcons(maya_mixin.MayaQWidgetDockableMixin, QMainWindow):
    def __init__(self, settings_folder:str=None):
        super().__init__(parent=wrapInstance(int(MQtUtil.mainWindow()), QWidget))

        self.settings:dict = {}
        self.settings_file:Path = None
        self.bmp_folder:Path = None
        self.ma_folder:Path = None
        
        self._load_settings(settings_folder)
        self.setWindowTitle("Rig Icons")
        self.setContentsMargins(0, 0, 0, 0)

        self._create_widgets()
        self._connect_widgets()
        self._create_layout()
        self._create_menu()

        mb = self.menuBar().sizeHint().height()
        regular_size = self.settings["window_sizes"][0]
        self.resize(regular_size[1], regular_size[2] + mb)
        self.show(dockable=True)

    def _create_widgets(self):
        self.color_palette_widget = ColorPaletteWidget(self.settings["palette"], self.settings["color_button_size"])
        self.color_palette_widget.set_default_index(self.settings["default_color_index"])
        self.icon_palette_widget = IconPaletteWidget(self.icons, self.settings["icon_button_size"])
        self.rotate_widget = RotateWidget()
        self.scale_widget = ScaleShapesWidget()
        self.scale_widget.setMinimumWidth(80)
        self.toggle_lock_hide_widget = ToggleLockHideWidget()
        self.toggle_render_select_widget = ToggleRenderableSelectableWidget()
        self.auto_add_grp_lineedit = QLineEdit("2")
        self.auto_add_grp_lineedit.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.auto_add_grp_lineedit.setMaximumWidth(40)
        self.auto_add_grp_lineedit.setValidator(QDoubleValidator())
        self.add_grp_btn = QPushButton("Add Groups above Selection")

        self._scale_captures: dict = {}

    def _connect_widgets(self):
        self.color_palette_widget.colorSelected.connect(self._color_clicked)
        self.color_palette_widget.defaultColorSet.connect(self.set_default_color)
        self.color_palette_widget.colorChanged.connect(self._color_changed)

        self.icon_palette_widget.iconClicked.connect(self._on_icon_clicked)
        self.icon_palette_widget.iconOrderChanged.connect(self._on_icon_order_changed)
        self.icon_palette_widget.replaceShapesRequested.connect(self._replace_shapes)

        self.rotate_widget.rotateRequested.connect(self._rotate_shapes)

        self.scale_widget.scaleStarted.connect(self._on_scale_started)
        self.scale_widget.scaleChanged.connect(self._on_scale_changed)
        self.scale_widget.scaleFinished.connect(self._on_scale_finished)

        self.toggle_lock_hide_widget.toggled.connect(self._on_toggle_lock_hide_changed)
        self.toggle_render_select_widget.toggle_renderable.connect(self._on_toggle_renderable_clicked)
        self.toggle_render_select_widget.toggle_selectable.connect(self._on_toggle_selectable_clicked)

        self.add_grp_btn.clicked.connect(self._on_add_group_clicked)
    
    def _create_layout(self):
        vbox = QVBoxLayout()
        vbox.setContentsMargins(4, 0, 4, 0)
        vbox.setSpacing(3)

        vbox.addWidget(self.icon_palette_widget)
        vbox.addWidget(QHLine())
        vbox.addWidget(self.color_palette_widget)
        vbox.addWidget(QHLine())
        vbox.addWidget(ExpandableRowWidget(self.rotate_widget, self.scale_widget, spacing=8))
        vbox.addWidget(QHLine())
        vbox.addWidget(ExpandableRowWidget(
            self.toggle_lock_hide_widget, self.toggle_render_select_widget, spacing=8
        ))

        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.addWidget(QLabel("Add Groups on Creation: "))
        hbox.addWidget(self.auto_add_grp_lineedit)
        container = QWidget()
        container.setLayout(hbox)
        vbox.addWidget(QHLine())
        vbox.addWidget(ExpandableRowWidget(container, self.add_grp_btn, spacing=8))
        vbox.addStretch()
        
        container = QWidget()
        container.setLayout(vbox)

        scroll = QScrollArea()
        scroll.setWidget(container)
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setFrameShape(QFrame.NoFrame)

        self.setCentralWidget(scroll)

    def _create_menu(self):
        menu = self.menuBar().addMenu("Window")
        for label, w, h in self.settings["window_sizes"]:
            action = QAction(label, self)
            action.triggered.connect(
                lambda *_, _w=w, _h=h: self._apply_window_size(_w, _h)
            )
            menu.addAction(action)

        sliders_folder = Path(__file__).parent / "template" / "sliders"
        extras = self.menuBar().addMenu("Extras")
        for label, filename in [
            ("Slider 0 to 1",       "slider_zero_one.ma"),
            ("Slider -1 to 1",      "slider_neg_pos.ma"),
            ("Four Corner Control", "four_corner_control.ma"),
        ]:
            action = QAction(label, self)
            action.triggered.connect(
                lambda *_, p=sliders_folder / filename: self._import_ma(p)
            )
            extras.addAction(action)

        text_action = QAction("Text", self)
        text_action.triggered.connect(self._open_text_dialog)
        extras.addAction(text_action)

    def _import_ma(self, path: Path):
        new_nodes = cmds.file(str(path), rnn=True, i=True)
        top_nodes = [n for n in new_nodes if n.count("|") == 1]
        if top_nodes:
            cmds.select(top_nodes, r=True)

    def _open_text_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Create Text Curves")
        layout = QVBoxLayout(dialog)

        line_edit = QLineEdit()
        line_edit.setPlaceholderText("Enter text…")
        layout.addWidget(line_edit)

        btn_row = QHBoxLayout()
        cancel_btn = QPushButton("Cancel")
        create_btn = QPushButton("Create")
        create_btn.setEnabled(False)
        btn_row.addWidget(cancel_btn)
        btn_row.addWidget(create_btn)
        layout.addLayout(btn_row)

        def _try_create():
            if line_edit.text():
                dialog.accept()

        line_edit.textChanged.connect(lambda t: create_btn.setEnabled(bool(t)))
        line_edit.returnPressed.connect(_try_create)
        create_btn.clicked.connect(_try_create)
        cancel_btn.clicked.connect(dialog.reject)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            txt = line_edit.text()
            result = cmds.textCurves(text=txt)
            if not result:
                return
            top = cmds.ls(result[0], long=True)[0]
            all_xforms = cmds.listRelatives(top, ad=True, fullPath=True, type='transform') or []
            nurbs_xforms = [t for t in all_xforms if cmds.listRelatives(t, shapes=True, type='nurbsCurve')]
            if not nurbs_xforms:
                return
            target = cmds.ls(cmds.parent(nurbs_xforms[0], world=True)[0], long=True)[0]
            cmds.makeIdentity(target, a=True)
            for src in nurbs_xforms[1:]:
                src = cmds.parent(src, world=True)[0]
                cmds.makeIdentity(src, a=True)
                shape = cmds.listRelatives(src, shapes=True, path=True)[0]
                cmds.parent(shape, target, shape=True, add=True)
                cmds.delete(src)
            cmds.delete(top)
            cmds.select(target)
            set_wireframe_color([target], self.settings["palette"][self.settings["default_color_index"]])
            cmds.rename(target, f"{txt}_crv")

    def _apply_window_size(self, w: int, h: int):
        mb_h = self.menuBar().sizeHint().height()
        total_h = h + mb_h + 10
        self.window().resize(w + 5, total_h)
        self.resize(w + 5, total_h - 10)


    def _on_icon_clicked(self, icon_name:str):
        sel = cmds.ls(sl=True, long=True)
        if not sel:
            self._create_icon(icon_name)
            return
        top_nodes = []
        new_nodes = []
        groups = []
        for obj in sel:
            nn, tn, grps = self._create_icon(icon_name, obj)
            top_nodes.append(tn)
            new_nodes.extend(nn)
            groups.extend(grps)
        cmds.select(top_nodes)


    def _create_icon(self, icon_name:str, match_obj:str=None):
        new_nodes, top_nodes = self._import_icon(icon_name)
        tn:str = top_nodes[0] if not match_obj else cmds.rename(top_nodes[0], f"{match_obj.split('|')[-1]}_ctrl")
        if match_obj:
            cmds.matchTransform(tn, match_obj)
        groups = []
        grps_to_add = min(max(int(self.auto_add_grp_lineedit.text()), 0), 3)
        grp = ""
        for i in range(grps_to_add):
            grp = add_group(f"{grp}|{tn}")
            tn = tn[1:] if tn.startswith("|") else tn
            grp = cmds.rename(grp, f"{tn}_bfg_{i}")
            groups.append(grp)
        return new_nodes, tn, groups

    def _import_icon(self, icon_name:str):
        icon = self.icons.get(icon_name)
        if not icon:
            cmds.warning(f"Icon '{icon_name}' not found.")
            return
        
        ma_path = str(icon["ma_path"])
        new_nodes = cmds.file(ma_path, rnn=True, i=True)
        top_nodes = list(filter(lambda x: x.count("|") == 1, new_nodes))

        set_wireframe_color(top_nodes, self.settings["palette"][self.settings["default_color_index"]])
        return new_nodes, top_nodes
        
    def _replace_shapes(self, icon_name:str):
        sel = cmds.ls(sl=True, long=True)

        if not sel:
            cmds.warning("No objects selected.")
            return
        
        new_nodes, top_nodes = self._import_icon(icon_name)

        for obj in sel:
            if not cmds.objectType(obj, isType="transform"):
                cmds.warning(f"Object '{obj}' is not a transform. Skipping.")
                continue
            add_shape(top_nodes[0], obj)

        cmds.delete(top_nodes)
        cmds.select(sel, r=True)

    def _color_clicked(self, rgb:tuple):
        sel = cmds.ls(sl=True, long=True)
        if not sel:
            cmds.warning("No objects selected.")
            return
        set_wireframe_color(sel, rgb)

    def set_default_color(self, index:int):
        self.settings["default_color_index"] = index
        self._save_settings()
    
    def _color_changed(self, index:int, rgb:tuple):
        self.settings["palette"][index] = rgb
        self._save_settings()

    def _rotate_shapes(self, axis: list, angle: float):
        sel = cmds.ls(sl=True, long=True)
        if not sel:
            cmds.warning("No objects selected.")
            return
        for obj in sel:
            rotate_shapes(obj, axis, angle)

    def _on_scale_started(self):
        sel = cmds.ls(sl=True, long=True) or []
        self._scale_captures = {}
        for obj in sel:
            try:
                self._scale_captures.update(capture_shape_points(obj))
            except (ValueError, RuntimeError):
                pass
        if self._scale_captures:
            cmds.undoInfo(stateWithoutFlush=False)

    def _on_scale_changed(self, factor: float):
        if self._scale_captures:
            scale_shapes_from_capture(self._scale_captures, factor)

    def _on_scale_finished(self, factor: float):
        if not self._scale_captures:
            return
        try:
            apply_shape_points(self._scale_captures)  # restore originals (undo still off)
            cmds.undoInfo(stateWithoutFlush=True)      # re-enable undo
            cmds.undoInfo(openChunk=True)
            # cmds.xform goes through Maya's DG → gets recorded in undo queue
            # (om API calls do not, even inside a chunk)
            for shape, orig_pts in self._scale_captures.items():
                shape_type = cmds.objectType(shape)
                if shape_type == "nurbsCurve":
                    components = cmds.ls(f"{shape}.cv[*]", flatten=True)
                elif shape_type == "mesh":
                    components = cmds.ls(f"{shape}.vtx[*]", flatten=True)
                else:
                    continue
                for i, comp in enumerate(components):
                    p = orig_pts[i]
                    cmds.xform(comp, os=True, t=(p.x * factor, p.y * factor, p.z * factor))
            cmds.undoInfo(closeChunk=True)
        except Exception:
            cmds.undoInfo(stateWithoutFlush=True)
            raise
        finally:
            self._scale_captures = {}

    def _on_toggle_lock_hide_changed(self, channels:list[bool, bool, bool, bool]):
        sel = cmds.ls(sl=True, long=True)
        if not sel:
            cmds.warning("No objects selected.")
            return
        for obj in sel:
            toggle_lock_hide(obj, channels)

    def _on_toggle_renderable_clicked(self):
        sel = cmds.ls(sl=True, long=True)
        if not sel:
            cmds.warning("No objects selected.")
            return
        for obj in sel:
            toggle_renderable(obj)

    def _on_toggle_selectable_clicked(self):
        sel = cmds.ls(sl=True, long=True)
        if not sel:
            cmds.warning("No objects selected.")
            return
        for obj in sel:
            toggle_selectable(obj)

    def _on_add_group_clicked(self):
        sel = cmds.ls(sl=True, long=True)
        if not sel:
            cmds.warning("No objects selected.")
            return
        for obj in sel:
            add_group(obj)

    def _on_icon_order_changed(self, new_order:list):
        """Called when the user changes the order of the icons. new_order is a list of icon names in the new order."""
        self.settings["icon_order"] = new_order
        self._save_settings()

    def _load_settings(self, folder:str | None):
        """Try to load settings from the provided folder.
        Be as fail safe as possible...
        """
        template_folder = Path(__file__).parent / "template"

        # if nothing is provided, try to load from MAYA_APP_DIR/rig_icons,
        if folder is None:
            maya_dir = Path(os.environ.get("MAYA_APP_DIR"))
            self.folder = maya_dir / "rig_icons"
            # if MAYA_APP_DIR/rig_icons doesn't exist, copy there from template.
            if not self.folder.exists():
                cmds.warning(f"No folder provided, copy template to {self.folder}")
                copytree(str(template_folder), str(self.folder))
        # If a folder was provided but it doesn't exist, copy template to that location.
        elif not Path(folder).exists():
            cmds.warning(f"Folder {folder} does not exist, copy default folder to this location.")
            self.folder = Path(folder)
            self.folder.parent.mkdir(parents=True, exist_ok=True)
            copytree(str(template_folder), str(self.folder), dirs_exist_ok=True)
        # If it exists, load from there, but if some files are missing, copy them from template.
        else:
            i = Path(folder)
            if not (i / "ma").exists():
                copytree(str(template_folder / "ma"), str(i / "ma"))
            if not (i / "bmp").exists():
                copytree(str(template_folder / "bmp"), str(i / "bmp"))
            if not (i / "settings.json").exists():
                copyfile(str(template_folder / "settings.json"), str(i / "settings.json"))
            self.folder = i

        self.settings_file = Path(self.folder) / "settings.json"
        self.bmp_folder = Path(self.folder) / "bmp"
        self.ma_folder = Path(self.folder) / "ma"

        self.icons = {}
        
        for ma_file in self.ma_folder.glob("*.ma"):
            bmp_file = self.bmp_folder / f"{ma_file.stem}.bmp"
            bmp_path = bmp_file if bmp_file.exists() else self.bmp_folder / "default.bmp"
            self.icons[ma_file.stem] = {
                "ma_path": ma_file,
                "bmp_path": bmp_path
            }

        self.settings = json.loads(self.settings_file.read_text())

        if self.settings["icon_order"] and set(self.settings["icon_order"]) == set(self.icons.keys()):
            # Reorder icons according to settings
            ordered_icons = {name: self.icons[name] for name in self.settings["icon_order"]}
            self.icons = ordered_icons
        else:
            # If the order in settings doesn't match the available icons, reset to default order
            self.settings["icon_order"] = list(self.icons.keys())
            self._save_settings()

        print(f"Loaded settings from {self.folder}")
        
    def _save_settings(self, silent=True):
        """Save the current settings to the settings.json file."""
        if self.settings_file:
            self.settings_file.write_text(json.dumps(self.settings, indent=4))
            if not silent:
                print(f"Settings saved to {self.settings_file}")
        else:
            cmds.warning("No settings file found. Cannot save settings.")
