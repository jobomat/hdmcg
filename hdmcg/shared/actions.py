"""
DCC-unabhaengiges Laden von Button-/Menue-Aktionen aus einer JSON-Config.

Eine Aktion verweist auf ein Callable im Format "modul.pfad:attribut" (z.B.
"hdmcg.maya.cat:show_cat") statt auf auszufuehrenden Code. Importiert wird erst beim
Ausloesen der Aktion, sodass der DCC-Start schnell bleibt und kaputte Eintraege den
Start nie abbrechen. Die DCC-Adapter (z.B. hdmcg.maya.toolbox) bauen daraus nur die UI.

Beispiel-Config:
    {
      "version": 1,
      "buttons": [
        {"id": "cat", "icon": "cat.png", "tooltip": "I need a cat",
         "call": "hdmcg.maya.cat:show_cat"}
      ]
    }
"""
import importlib
import importlib.util
import json
import os
import re
import traceback
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

_ID_RE = re.compile(r"^\w+$")
_CALL_RE = re.compile(r"^[A-Za-z_][\w.]*:[A-Za-z_][\w.]*$")
_COMMON_KEYS = {"id", "label", "icon", "tooltip", "call", "args", "kwargs", "requires"}


class ConfigError(Exception):
    """Config konnte nicht geladen werden (Env-Var fehlt, Datei fehlt, JSON kaputt)."""


@dataclass
class ActionSpec:
    id: str
    label: str = ""
    icon: str = ""
    tooltip: str = ""
    call: str = ""
    args: list = field(default_factory=list)
    kwargs: dict = field(default_factory=dict)
    extra: dict = field(default_factory=dict)  # DCC-spezifische Keys, z.B. runtime_command


def load_config(env_var: str) -> tuple[dict, Path]:
    """Liest die JSON-Datei, auf die env_var zeigt. Wirft ConfigError mit lesbarer Meldung."""
    raw_path = os.environ.get(env_var)
    if not raw_path:
        raise ConfigError(f"Environment Variable {env_var} not set.")

    path = Path(os.path.expandvars(raw_path)).expanduser()
    if not path.is_file():
        raise ConfigError(f"Config file '{path}' (from {env_var}) does not exist.")

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise ConfigError(f"Config file '{path}' is not valid JSON: {e}") from None
    except OSError as e:
        raise ConfigError(f"Config file '{path}' could not be read: {e}") from None

    if not isinstance(data, dict):
        raise ConfigError(f"Config file '{path}' must contain a JSON object at top level.")
    return data, path


def parse_actions(data: dict, config_dir: Path, section: str = "buttons",
                  dcc_keys: tuple[str, ...] = ()) -> list[ActionSpec]:
    """
    Wandelt data[section] in ActionSpecs um. Fehlerhafte Eintraege werden mit einer Meldung
    uebersprungen, der Rest wird trotzdem zurueckgegeben. dcc_keys sind zusaetzliche
    Aktions-Keys, die der DCC-Adapter selbst ausfuehrt (landen in ActionSpec.extra).
    """
    entries = data.get(section, [])
    if not isinstance(entries, list):
        print(f"[hdmcg] {section}: '{section}' must be a list - nothing loaded.")
        return []

    specs = []
    seen_ids = set()
    for index, entry in enumerate(entries, start=1):
        try:
            spec = _parse_entry(entry, config_dir, dcc_keys)
            if spec.id in seen_ids:
                raise ValueError("duplicate id")
        except ValueError as e:
            entry_id = entry.get("id", "?") if isinstance(entry, dict) else "?"
            print(f"[hdmcg] {section}: skipping entry #{index} ('{entry_id}'): {e}")
            continue
        seen_ids.add(spec.id)
        specs.append(spec)
    return specs


def _parse_entry(entry, config_dir: Path, dcc_keys: tuple[str, ...]) -> ActionSpec:
    if not isinstance(entry, dict):
        raise ValueError("entry must be a JSON object")

    entry_id = entry.get("id")
    if not isinstance(entry_id, str) or not _ID_RE.match(entry_id):
        raise ValueError("'id' is required and may only contain letters, digits and '_'")

    unknown = set(entry) - _COMMON_KEYS - set(dcc_keys)
    if unknown:
        print(f"[hdmcg] entry '{entry_id}': ignoring unknown keys {sorted(unknown)}")

    action_keys = [k for k in ("call", *dcc_keys) if k in entry]
    if len(action_keys) != 1:
        raise ValueError(f"exactly one of {['call', *dcc_keys]} is required")

    # Optionale Abhaengigkeiten (z.B. "ayon_core"), die erst innerhalb des Calls importiert werden
    requires = entry.get("requires", [])
    if isinstance(requires, str):
        requires = [requires]
    if not isinstance(requires, list) or not all(isinstance(r, str) for r in requires):
        raise ValueError("'requires' must be a module name or a list of module names")
    missing = [r for r in requires if not _module_available(r)]
    if missing:
        raise ValueError(f"required module(s) {missing} not available")

    call = entry.get("call", "")
    if call:
        _validate_call(call)

    args = entry.get("args", [])
    kwargs = entry.get("kwargs", {})
    if not isinstance(args, list):
        raise ValueError("'args' must be a list")
    if not isinstance(kwargs, dict):
        raise ValueError("'kwargs' must be an object")

    return ActionSpec(
        id=entry_id,
        label=str(entry.get("label", "")),
        icon=_resolve_icon(str(entry.get("icon", "")), config_dir),
        tooltip=str(entry.get("tooltip", "")),
        call=call,
        args=args,
        kwargs=kwargs,
        extra={k: entry[k] for k in dcc_keys if k in entry},
    )


def _validate_call(call) -> None:
    """Prueft Format und Existenz des Moduls, ohne es zu importieren."""
    if not isinstance(call, str) or not _CALL_RE.match(call):
        raise ValueError(f"'call' must look like 'package.module:function', got {call!r}")
    module_name = call.partition(":")[0]
    if not _module_available(module_name):
        raise ValueError(f"module '{module_name}' not found")


def _module_available(module_name: str) -> bool:
    """Sucht das Modul, ohne es selbst zu importieren (Elternpakete werden aber importiert)."""
    try:
        return importlib.util.find_spec(module_name) is not None
    except (ImportError, ValueError):
        return False


def _resolve_icon(icon: str, config_dir: Path) -> str:
    """Relative Icons werden zuerst neben der Config gesucht, sonst unveraendert ans DCC gegeben."""
    if icon and not os.path.isabs(icon):
        candidate = config_dir / icon
        if candidate.is_file():
            return candidate.as_posix()
    return icon


def resolve_callable(call: str) -> Callable:
    """'modul.pfad:attr.subattr' -> Callable. Importiert das Modul (Fehler werden durchgereicht)."""
    module_name, _, attr_path = call.partition(":")
    obj = importlib.import_module(module_name)
    for attr in attr_path.split("."):
        obj = getattr(obj, attr)
    if not callable(obj):
        raise TypeError(f"'{call}' is not callable")
    return obj


def run_action(call: str, *args, **kwargs):
    """Fuer DCCs, die Commands als String brauchen (z.B. Houdini-Shelf-Tools)."""
    return resolve_callable(call)(*args, **kwargs)


def make_callback(spec: ActionSpec, on_error: Callable[[str], None] = print) -> Callable:
    """
    Liefert ein Callback, das spec.call erst beim Ausloesen importiert und ausfuehrt.
    Fehler landen als Traceback in der Konsole und als Kurzmeldung bei on_error.
    """
    def callback(*_):
        try:
            run_action(spec.call, *spec.args, **spec.kwargs)
        except Exception as e:
            traceback.print_exc()
            on_error(f"[hdmcg] action '{spec.id}' ({spec.call}) failed: {e}")
    return callback
