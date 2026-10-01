from PySide6.QtWidgets import QWidget
from shiboken6 import wrapInstance
from maya.OpenMayaUI import MQtUtil

from hdmcg.shared.cat import CatWidget


def show_cat():
    w = CatWidget(parent=wrapInstance(int(MQtUtil.mainWindow()), QWidget))
    w.show()
