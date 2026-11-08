def render_snbt(obj) -> str:
    if isinstance(obj, dict):
        items = ", ".join("{}: {}".format("\"{}\"".format(k) if " " in k else k, render_snbt(v)) for k, v in obj.items())
        return "{" + items + "}"
    elif isinstance(obj, list):
        return "[" + ", ".join(render_snbt(v) for v in obj) + "]"
    elif isinstance(obj, str):
        return "\"{}\"".format("{}".format(obj).replace("\\", "\\\\").replace("\"", "\\\""))
    elif isinstance(obj, bool):
        return "true" if obj else "false"
    elif isinstance(obj, float):
        return "{}f".format(obj)
    elif isinstance(obj, int):
        return str(obj)
    else:
        raise TypeError("Invalid type {} in SNBT: {}".format(type(obj), obj))