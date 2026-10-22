import re
import traceback

import maya.cmds as cmds
import maya.mel as mel

from hdmcg.shared.actions import ActionSpec, ConfigError, load_config, make_callback, parse_actions

TOOLBOX_ENV_VAR = "MAYA_TOOLBOX_CONFIG"
_PREFIX = "hdmcg_toolbox_"
_RUNTIME_COMMAND_RE = re.compile(r"^[A-Za-z_]\w*$")


def add_toolbox_buttons(env_var: str = TOOLBOX_ENV_VAR) -> None:
    """
    Haengt die Buttons aus der JSON-Config, auf die env_var zeigt, an die Maya-Toolbox.
    Bricht nie ab: Fehler werden nur im Script Editor ausgegeben.
    """
    try:
        _add_toolbox_buttons(env_var)
    except Exception:
        print("[hdmcg] toolbox: unexpected error while adding buttons:")
        traceback.print_exc()


def remove_toolbox_buttons() -> None:
    toolbox = _toolbox_layout()
    if not toolbox:
        return
    for child in cmds.layout(toolbox, query=True, childArray=True) or []:
        if child.startswith(_PREFIX):
            cmds.deleteUI(child)


def _add_toolbox_buttons(env_var: str) -> None:
    try:
        data, config_path = load_config(env_var)
    except ConfigError as e:
        print(f"[hdmcg] {e} Nothing added to Toolbox.")
        return

    toolbox = _toolbox_layout()
    if not toolbox:
        print("[hdmcg] toolbox: Maya Toolbox not available (batch mode?). Nothing added to Toolbox.")
        return

    for spec in parse_actions(data, config_path.parent, dcc_keys=("runtime_command",)):
        runtime_command = spec.extra.get("runtime_command")
        if runtime_command is not None and not (
                isinstance(runtime_command, str) and _RUNTIME_COMMAND_RE.match(runtime_command)):
            print(f"[hdmcg] buttons: skipping '{spec.id}': invalid runtime_command {runtime_command!r}")
            continue
        _add_button(toolbox, spec)


def _toolbox_layout() -> str:
    if cmds.about(batch=True):
        return ""
    toolbox = mel.eval("$tmp = $gToolBox;")
    return toolbox if toolbox and cmds.layout(toolbox, exists=True) else ""


def _add_button(toolbox: str, spec: ActionSpec) -> None:
    name = _PREFIX + spec.id
    # Den Button loeschen, falls es ihn schon gibt (z.B. bei erneutem Aufruf)
    if cmds.control(name, exists=True):
        cmds.deleteUI(name)

    cmds.iconTextButton(
        name,
        parent=toolbox,
        style="iconOnly",
        image=spec.icon or "commandButton.png",
        label=spec.label or spec.id,
        annotation=spec.tooltip or spec.label or spec.id,
        command=_maya_callback(spec),
    )


def _maya_callback(spec: ActionSpec):
    if spec.call:
        return make_callback(spec, on_error=cmds.warning)

    runtime_command = spec.extra["runtime_command"]

    def run_runtime_command(*_):
        if not cmds.runTimeCommand(runtime_command, exists=True):
            cmds.warning(f"[hdmcg] runtime command '{runtime_command}' does not exist")
            return
        mel.eval(runtime_command)
    return run_runtime_command
