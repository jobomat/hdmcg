from PySide6.QtWidgets import QWidget
from shiboken6 import wrapInstance
from maya.OpenMayaUI import MQtUtil

from hdmcg.shared.dev import DevTools


def show_dev_tools(mod="hdmcg", env="PYTHONPATH") -> DevTools:
    parent = wrapInstance(int(MQtUtil.mainWindow()), QWidget)
    tools = DevTools(module_filter=mod, envvar_filter=env, parent=parent)
    tools.show()
    return tools
