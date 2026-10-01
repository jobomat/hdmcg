import maya.cmds as cmds
from maya import OpenMayaUI as omui
from PySide6 import QtWidgets, QtGui, QtCore
import shiboken6


def show_widget_name_under_cursor():
    widget = QtWidgets.QApplication.widgetAt(QtGui.QCursor.pos())
    if widget is None:
        msg = "Kein Widget unter dem Cursor gefunden."
    else:
        widget_pass = omui.MQtUtil.fullName(int(shiboken6.getCppPointer(widget)[0]))
        QtWidgets.QApplication.clipboard().setText(widget_pass)
        msg = f"{widget_pass}\nWidget-pass was copied to clipboard."
        cmds.warning(widget_pass)

    # pos, text, widget(optional), rect(optional), Anzeigedauer in ms
    QtWidgets.QToolTip.showText(QtGui.QCursor.pos(), msg, None, QtCore.QRect(), 3000)



if not cmds.runTimeCommand('show_widget_name', exists=True):
    cmds.runTimeCommand(
        'show_widget_name',
        annotation='Gibt den Namen des Widgets unter dem Mauszeiger aus',
        category='Custom Scripts',
        command="from hdmcg.maya.hotkeys import show_widget_name_under_cursor;show_widget_name_under_cursor()",
        commandLanguage='python'
    )

cmds.nameCommand(
    'show_widget_name_nameCommand',
    annotation='Startet mein Tool',
    command='show_widget_name',
    sourceType='Python'
)

cmds.hotkey(keyShortcut='w', ctrlModifier=True, altModifier=True,
            name='show_widget_name_nameCommand')