import maya.cmds as cmds

from ayon_core.lib import get_ayon_username
from ayon_core.pipeline.workfile import save_next_version


def bump_workfile_version():
    # Enter speichert mit Default-Description, Escape/Cancel bricht ab
    result = cmds.promptDialog(
        title="Version Bump",
        message="Description (optional):",
        button=["OK", "Cancel"],
        defaultButton="OK",
        cancelButton="Cancel",
        dismissString="Cancel",
    )
    if result != "OK":
        return

    description = cmds.promptDialog(query=True, text=True).strip()
    if not description:
        description = f"Version-Bump von {get_ayon_username()}"
    save_next_version(description=description)
