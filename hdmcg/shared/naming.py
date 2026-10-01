import re


def hash_rename(pattern: str, names: list[str], start: int = 1) -> list[str]:
    """
    Resolves a naming pattern with '#' placeholders into a list of new names,
    one per entry in `names` (old names are used only for their count).

    The first contiguous run of '#' characters marks the insertion point;
    its length determines the zero-fill width.
    If no '#' is present, the counter is appended as _{n} with enough
    digits for len(names) (minimum 3).
    More than one '#'-block raises ValueError.

    Args:
        pattern:  e.g. "name_##_geo", "joint_###", "mesh"
        names:    list of existing names (determines count and order)
        start:    first counter value (default 1)

    Returns:
        list[str] of new names, same length and order as `names`

    Examples:
        resolve_names("name_##_geo", ["a", "b", "c"])
            → ["name_01_geo", "name_02_geo", "name_03_geo"]
        resolve_names("mesh", ["x", "y"], start=0)
            → ["mesh_000", "mesh_001"]
    """
    blocks = list(re.finditer(r'#+', pattern))
    if len(blocks) > 1:
        raise ValueError(
            f"Pattern contains {len(blocks)} '#'-blocks; exactly 0 or 1 is allowed."
        )
    count = len(names)
    if blocks:
        m = blocks[0]
        width = len(m.group())
        prefix, suffix = pattern[:m.start()], pattern[m.end():]
        return [f"{prefix}{str(i).zfill(width)}{suffix}"
                for i in range(start, start + count)]
    else:
        width = max(len(str(start + count - 1)), 3)
        return [f"{pattern}_{str(i).zfill(width)}"
                for i in range(start, start + count)]
