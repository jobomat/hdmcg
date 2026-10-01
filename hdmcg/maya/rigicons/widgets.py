from pathlib import Path
from PySide6.QtWidgets import (
    QApplication, QWidget, QPushButton, QSizePolicy, QToolTip,
    QMenu, QColorDialog, QHBoxLayout, QLabel, QLineEdit, QSlider
)
from PySide6.QtCore import Qt, QSize, Signal, QMimeData
from PySide6.QtGui import (
    QPainter, QPen, QColor, QPainterPath, 
    QIcon, QDrag, QDoubleValidator
)

from hdmcg.qt.layouts import FlowLayout


class ColorButton(QPushButton):
    """Borderless square button representing a single color."""
 
    colorClicked = Signal(tuple)
    defaultRequested = Signal(int)
    changeColorRequested = Signal(int)
 
    def __init__(self, rgb, index, size=32, parent=None):
        super().__init__(parent)
        self.rgb = rgb  # (r, g, b) as floats 0..1
        self.index = index
        self._is_default = False
        self.setFixedSize(size, size)
        self.setCursor(Qt.PointingHandCursor)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self._apply_style()
        self.setToolTip(self._rgb_to_hex())
        self.clicked.connect(self._on_clicked)
        self.customContextMenuRequested.connect(self._show_context_menu)
 
    def set_rgb(self, rgb):
        self.rgb = rgb
        self._apply_style()
        self.setToolTip(self._rgb_to_hex())
 
    def set_size(self, size):
        self.setFixedSize(size, size)
        self._apply_style()  # border-radius doesn't depend on size, but repaint to be safe
        self.update()
 
    def set_default(self, is_default):
        if self._is_default != is_default:
            self._is_default = is_default
            self.update()
 
    def is_default(self):
        return self._is_default
 
    def _rgb_255(self):
        return tuple(round(max(0.0, min(1.0, c)) * 255) for c in self.rgb)
 
    def _rgb_to_hex(self):
        r, g, b = self._rgb_255()
        return f"#{r:02X}{g:02X}{b:02X}"
 
    def _apply_style(self):
        r, g, b = self._rgb_255()
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: rgb({r}, {g}, {b});
                border: none;
                border-radius: 2px;
            }}
            QPushButton:hover {{
                border: 1px solid #888888;
            }}
            QPushButton:pressed {{
                border: 1px solid #333333;
            }}
        """)
 
    def _on_clicked(self):
        QToolTip.showText(self.mapToGlobal(self.rect().center()), self._rgb_to_hex(), self)
        self.colorClicked.emit(self.rgb)
 
    def _show_context_menu(self, pos):
        menu = QMenu(self)
        use_action = menu.addAction("Use this on creation")
        change_action = menu.addAction("Change Color...")
        chosen = menu.exec(self.mapToGlobal(pos))
        if chosen == use_action:
            self.defaultRequested.emit(self.index)
        elif chosen == change_action:
            self.changeColorRequested.emit(self.index)
 
    def paintEvent(self, event):
        super().paintEvent(event)
        if not self._is_default:
            return
 
        # Rough brightness estimate to pick checkmark color (light/dark)
        r, g, b = self._rgb_255()
        brightness = 0.299 * r + 0.587 * g + 0.114 * b
        check_color = QColor("#202020") if brightness > 140 else QColor("#f0f0f0")
 
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        pen = QPen(check_color)
        pen.setWidthF(max(1.5, self.width() * 0.08))
        pen.setCapStyle(Qt.RoundCap)
        pen.setJoinStyle(Qt.RoundJoin)
        painter.setPen(pen)
 
        w, h = self.width(), self.height()
        path = QPainterPath()
        path.moveTo(w * 0.28, h * 0.52)
        path.lineTo(w * 0.43, h * 0.68)
        path.lineTo(w * 0.74, h * 0.32)
        painter.drawPath(path)
        painter.end()
 
 
class ColorPaletteWidget(QWidget):
    """Displays a list of RGB tuples/lists as a flow of color buttons."""

    colorSelected = Signal(tuple)
    defaultColorSet = Signal(int)        # index of the color marked as default
    colorChanged = Signal(int, tuple)    # index, new (r, g, b) color (0..1)
 
    def __init__(self, palette=None, button_size=32, parent=None):
        super().__init__(parent)
        self._layout = FlowLayout(self, margin=4, h_spacing=4, v_spacing=4)
        self.setLayout(self._layout)
        self._button_size = button_size
        self._buttons = []
        self._default_index = None
        if palette:
            self.set_palette(palette)
 
    def set_palette(self, palette):
        # remove existing buttons
        while self._layout.count():
            item = self._layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self._buttons = []
        self._default_index = None
 
        for index, rgb in enumerate(palette):
            btn = ColorButton(tuple(rgb), index, size=self._button_size)
            btn.colorClicked.connect(self.colorSelected.emit)
            btn.defaultRequested.connect(self._on_default_requested)
            btn.changeColorRequested.connect(self._on_change_color_requested)
            self._layout.addWidget(btn)
            self._buttons.append(btn)
 
    def set_default_index(self, index):
        """Marks the button at `index` as default (checkmark) and removes it from all others."""
        for i, btn in enumerate(self._buttons):
            btn.set_default(i == index)
        self._default_index = index
 
    def default_index(self):
        return self._default_index
 
    def set_button_size(self, size):
        """Changes the size of all buttons at runtime without recreating them."""
        self._button_size = size
        for btn in self._buttons:
            btn.set_size(size)
        self._layout.invalidate()  # force flow layout to recalculate
        self.updateGeometry()
 
    def _on_default_requested(self, index):
        self.set_default_index(index)
        self.defaultColorSet.emit(index)
 
    def _on_change_color_requested(self, index):
        btn = self._buttons[index]
        r, g, b = btn._rgb_255()
        initial = QColor(r, g, b)
        chosen = QColorDialog.getColor(initial, self, "Pick Color")
        if not chosen.isValid():
            return
        new_rgb = (chosen.redF(), chosen.greenF(), chosen.blueF())
        btn.set_rgb(new_rgb)
        self.colorChanged.emit(index, new_rgb)


class IconButton(QPushButton):
    """Borderless square button displaying an icon from a BMP file."""

    iconClicked = Signal(str)              # icon_name of the clicked icon
    replaceShapesRequested = Signal(str)   # "Replace selected Shapes" -> icon_name
    removeIconRequested = Signal(str)      # "Remove Icon" -> icon_name

    DRAG_MIME_TYPE = "application/x-icon-name"  # public so the container can reference it
 
    def __init__(self, icon: dict[str, Path], size=40, parent=None):
        super().__init__(parent)
        self.path = icon["bmp_path"]
        self.ma_path = icon["ma_path"]
        self.icon_name = icon["ma_path"].stem
        self.icon_size = size
        self.setFixedSize(size, size)
        self.setCursor(Qt.PointingHandCursor)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self._drag_start_pos = None
        self._hovered = False
        self._apply_style()
        self.set_icon_path(icon)
        self.setToolTip(self.icon_name)
        self.clicked.connect(self._on_clicked)
        self.customContextMenuRequested.connect(self._show_context_menu)
 
    def set_icon_path(self, icon: dict[str, Path]):
        self.path = icon["bmp_path"]
        self.ma_path = icon["ma_path"]
        self.icon_name = icon["ma_path"].stem
        self.setIcon(QIcon(str(self.path)))
        # Keep icon slightly smaller than the button so it doesn't touch the edges
        # margin = max(2, int(self.width() * 0.15))
        self.setIconSize(QSize(self.width(), self.height()))
        self.setToolTip(self.icon_name)
 
    def set_size(self, size):
        self.setFixedSize(size, size)
        margin = max(2, int(size * 0.15))
        self.setIconSize(QSize(size - margin, size - margin))
 
    def _apply_style(self):
        self.setStyleSheet("QPushButton { background-color: transparent; border: none; }")

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.isDown():
            painter = QPainter(self)
            painter.fillRect(self.rect(), QColor(0, 0, 0, 70))
            painter.end()
        elif self._hovered:
            painter = QPainter(self)
            painter.fillRect(self.rect(), QColor(255, 255, 255, 55))
            painter.end()

    def _on_clicked(self):
        QToolTip.showText(self.mapToGlobal(self.rect().center()), self.icon_name, self)
        self.iconClicked.emit(self.icon_name)

    def enterEvent(self, event):
        self._hovered = True
        self.update()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._hovered = False
        self.update()
        super().leaveEvent(event)

    def _show_context_menu(self, pos):
        menu = QMenu(self)
        replace_action = menu.addAction("Replace selected Shapes")
        remove_action = menu.addAction("Remove Icon")
        chosen = menu.exec(self.mapToGlobal(pos))
        self._hovered = False
        self.update()
        if chosen == replace_action:
            self.replaceShapesRequested.emit(self.icon_name)
        elif chosen == remove_action:
            self.removeIconRequested.emit(self.icon_name)
 
    # --- Drag & Drop: reorder by press + drag --------------------------------
 
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._drag_start_pos = event.position().toPoint()
        super().mousePressEvent(event)
 
    def mouseMoveEvent(self, event):
        if self._drag_start_pos is None or not (event.buttons() & Qt.LeftButton):
            super().mouseMoveEvent(event)
            return
 
        moved = (event.position().toPoint() - self._drag_start_pos).manhattanLength()
        if moved < QApplication.startDragDistance():
            super().mouseMoveEvent(event)
            return
 
        # threshold exceeded → start drag instead of normal click
        self._drag_start_pos = None
        self.setDown(False)  # reset visual "pressed" state
 
        drag = QDrag(self)
        mime = QMimeData()
        mime.setData(self.DRAG_MIME_TYPE, self.icon_name.encode("utf-8"))
        drag.setMimeData(mime)
 
        pixmap = self.icon().pixmap(self.iconSize())
        if not pixmap.isNull():
            drag.setPixmap(pixmap)
            drag.setHotSpot(pixmap.rect().center())
 
        drag.exec(Qt.MoveAction)
 
    def mouseReleaseEvent(self, event):
        self._drag_start_pos = None
        super().mouseReleaseEvent(event)
 
 
class IconPaletteWidget(QWidget):
    """Displays a dict of icons (icon_name -> {'bmp_path', 'ma_path'}) as a flow of icon buttons."""

    iconClicked = Signal(str)              # icon_name
    replaceShapesRequested = Signal(str)   # icon_name
    removeIconRequested = Signal(str)      # icon_name
    iconOrderChanged = Signal(list)        # new order as a list of icon_name
 
    def __init__(self, icons: dict = None, button_size=32, parent=None):
        super().__init__(parent)
        self._layout = FlowLayout(self, margin=4, h_spacing=4, v_spacing=4)
        self.setLayout(self._layout)
        self._button_size = button_size
        self._buttons = []
        self.setAcceptDrops(True)
        if icons:
            self.set_icons(icons)
 
    def set_icons(self, icons: dict):
        # Remove existing buttons
        while self._layout.count():
            item = self._layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        self._buttons = []
 
        for icon in icons.values():
            btn = IconButton(icon, size=self._button_size)
            btn.iconClicked.connect(self.iconClicked.emit)
            btn.replaceShapesRequested.connect(self.replaceShapesRequested.emit)
            btn.removeIconRequested.connect(self.removeIconRequested.emit)
            self._layout.addWidget(btn)
            self._buttons.append(btn)
 
    # --- Drag & Drop: central drop handling at container level ---------------
    # (more robust than per-button drop handling: small/closely spaced buttons
    # are more reliably hit as drop targets via childAt() + distance fallback)
 
    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat(IconButton.DRAG_MIME_TYPE):
            event.acceptProposedAction()
        else:
            event.ignore()
 
    def dragMoveEvent(self, event):
        if event.mimeData().hasFormat(IconButton.DRAG_MIME_TYPE):
            event.acceptProposedAction()
        else:
            event.ignore()
 
    def dropEvent(self, event):
        if not event.mimeData().hasFormat(IconButton.DRAG_MIME_TYPE):
            event.ignore()
            return
 
        source_name = bytes(event.mimeData().data(IconButton.DRAG_MIME_TYPE)).decode("utf-8")
        drop_pos = event.position().toPoint()
        target_btn = self._button_at(drop_pos)
 
        if target_btn is not None and target_btn.icon_name != source_name:
            self._on_reorder_requested(source_name, target_btn.icon_name)
 
        event.acceptProposedAction()
 
    def _button_at(self, pos):
        """Returns the IconButton at position `pos` (container coordinates).
        Falls back to the nearest button if dropped exactly between two
        buttons or within the margin area."""
        child = self.childAt(pos)
        while child is not None and not isinstance(child, IconButton):
            child = child.parent()
        if isinstance(child, IconButton):
            return child
 
        if not self._buttons:
            return None
        return min(
            self._buttons,
            key=lambda b: (b.geometry().center() - pos).manhattanLength(),
        )
 
    def _on_reorder_requested(self, source_name, target_name):
        btn_map = {b.icon_name: b for b in self._buttons}
        if source_name not in btn_map or target_name not in btn_map:
            return
        source_btn = btn_map[source_name]
        target_index = self._buttons.index(btn_map[target_name])
 
        self._buttons.remove(source_btn)
        self._buttons.insert(target_index, source_btn)
        self._rebuild_layout()
        self.iconOrderChanged.emit([b.icon_name for b in self._buttons])
 
    def _rebuild_layout(self):
        """Reorders the existing button widgets in the FlowLayout according to self._buttons
        without recreating them (widgets are kept, only their order changes)."""
        while self._layout.count():
            self._layout.takeAt(0)
        for btn in self._buttons:
            self._layout.addWidget(btn)
        self._layout.invalidate()  # notify Qt that geometry needs to be recalculated
        self.updateGeometry()
        self.update()
 
    def icon_order(self):
        """Current order as a list of icon_name."""
        return [b.icon_name for b in self._buttons]
 
    def set_button_size(self, size):
        """Changes the size of all icon buttons at runtime without recreating them."""
        self._button_size = size
        for btn in self._buttons:
            btn.set_size(size)
        self._layout.invalidate()
        self.updateGeometry()
 
    def button_for_name(self, icon_name):
        """Liefert den Button mit gegebenem icon_name, oder None."""
        for btn in self._buttons:
            if btn.icon_name == icon_name:
                return btn
        return None
 
    def remove_icon_by_name(self, icon_name):
        """Entfernt den Button mit gegebenem icon_name aus der UI (z.B. nach 'Remove Icon')."""
        btn = self.button_for_name(icon_name)
        if btn is None:
            return False
        self._layout.removeWidget(btn)
        self._buttons.remove(btn)
        btn.deleteLater()
        return True
    

class RotateWidget(QWidget):
    """Single-row widget to rotate shapes by a given angle around X, Y, or Z."""

    rotateRequested = Signal(list, float)  # axis e.g. [1,0,0], angle in degrees

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        layout.addWidget(QLabel("Rotate"))

        self._angle_edit = QLineEdit("90")
        self._angle_edit.setValidator(QDoubleValidator())
        self._angle_edit.setFixedWidth(24)
        layout.addWidget(self._angle_edit)

        for label, axis in [("X", [1, 0, 0]), ("Y", [0, 1, 0]), ("Z", [0, 0, 1])]:
            btn = QPushButton(label)
            btn.setFixedWidth(34)
            btn.clicked.connect(lambda *_, a=axis: self._emit(a))
            layout.addWidget(btn)

        layout.addStretch()

    def _emit(self, axis: list):
        try:
            angle = float(self._angle_edit.text().replace(",", "."))
        except ValueError:
            return
        self.rotateRequested.emit(axis, angle)


class ScaleShapesWidget(QWidget):
    """Slider to interactively scale shapes of selected objects.
    Three signals let the caller manage Maya's undo state so only one
    undo step is recorded for the entire drag gesture."""

    scaleStarted = Signal()
    scaleChanged = Signal(float)   # factor relative to state at drag start
    scaleFinished = Signal(float)  # final factor

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        layout.addWidget(QLabel("Scale:"))

        self._slider = QSlider(Qt.Horizontal)
        self._slider.setRange(10, 300)
        self._slider.setValue(100)
        layout.addWidget(self._slider)

        self._slider.sliderPressed.connect(self.scaleStarted.emit)
        self._slider.valueChanged.connect(self._on_change)
        self._slider.sliderReleased.connect(self._on_release)

    def _on_change(self, value):
        factor = value / 100.0
        self.scaleChanged.emit(factor)

    def _on_release(self):
        factor = self._slider.value() / 100.0
        self.scaleFinished.emit(factor)
        self._slider.blockSignals(True)
        self._slider.setValue(100)
        self._slider.blockSignals(False)


class ExpandableRowWidget(QWidget):
    """Places `first` at its natural width and `second` fills the remaining space.
    When the available width drops below their combined minimum, `second` wraps
    to a full-width row below `first`."""

    def __init__(self, first: QWidget, second: QWidget, spacing: int = 4, parent=None):
        super().__init__(parent)
        self._first = first
        self._second = second
        self._spacing = spacing
        first.setParent(self)
        second.setParent(self)

    @staticmethod
    def _eff_min_w(widget: QWidget) -> int:
        """Effective minimum width: the larger of the natural hint and any explicitly set minimum."""
        return max(widget.minimumSizeHint().width(), widget.minimumWidth())

    def _fits_in_one_row(self, w: int) -> bool:
        return (self._first.sizeHint().width() + self._spacing
                + self._eff_min_w(self._second)) <= w

    def hasHeightForWidth(self) -> bool:
        return True

    def heightForWidth(self, w: int) -> int:
        if self._fits_in_one_row(w):
            return max(self._first.sizeHint().height(), self._second.sizeHint().height())
        return (self._first.sizeHint().height() + self._spacing
                + self._second.sizeHint().height())

    def sizeHint(self) -> QSize:
        fw = self._first.sizeHint().width()
        sw = self._second.sizeHint().width()
        h = max(self._first.sizeHint().height(), self._second.sizeHint().height())
        return QSize(fw + self._spacing + sw, h)

    def minimumSizeHint(self) -> QSize:
        w = max(self._eff_min_w(self._first), self._eff_min_w(self._second))
        return QSize(w, self.heightForWidth(w))

    def resizeEvent(self, event):
        super().resizeEvent(event)
        w = event.size().width()
        if self._fits_in_one_row(w):
            first_w = self._first.sizeHint().width()
            h = max(self._first.sizeHint().height(), self._second.sizeHint().height())
            self._first.setGeometry(0, 0, first_w, h)
            self._second.setGeometry(first_w + self._spacing, 0,
                                     max(0, w - first_w - self._spacing -6), h)
        else:
            fh = self._first.sizeHint().height()
            sh = self._second.sizeHint().height()
            self._first.setGeometry(0, 0, w-6, fh)
            self._second.setGeometry(0, fh + self._spacing, w-6, sh)


class ToggleLockHideWidget(QWidget):
    """Four buttons (T/R/S/V) that each emit the matching channels list for toggle_lock_hide."""

    toggled = Signal(list)  # [T, R, S, V] as bools

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        label = QLabel("Toggle Lock/Hide:")
        label.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        label.setMinimumWidth(96)
        layout.addWidget(label)

        for text, channels in [
            ("T", [True, False, False, False]),
            ("R", [False, True, False, False]),
            ("S", [False, False, True, False]),
            ("V", [False, False, False, True]),
        ]:
            btn = QPushButton(text)
            btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
            btn.clicked.connect(lambda *_, ch=channels: self.toggled.emit(ch))
            layout.addWidget(btn, stretch=1)


class ToggleRenderableSelectableWidget(QWidget):
    toggle_renderable = Signal()
    toggle_selectable = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        label = QLabel("Toggle ")
        label.setStyleSheet("QLabel {font-size:10px; margin-left:0px;}")
        label.setMaximumWidth(30)
        layout.addWidget(label)

        renderable_btn = QPushButton("Renderable")
        selectable_btn = QPushButton("Selectable")

        renderable_btn.clicked.connect(self.toggle_renderable.emit)
        selectable_btn.clicked.connect(self.toggle_selectable.emit)
        layout.addWidget(renderable_btn)
        layout.addWidget(selectable_btn)