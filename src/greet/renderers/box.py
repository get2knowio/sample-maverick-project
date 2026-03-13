def render_box(lines: list[str]) -> str:
    """Surround text lines with Unicode box-drawing characters."""
    if not lines:
        return "┌┐\n└┘"
    width = max(len(line) for line in lines)
    top = f"┌{'─' * (width + 2)}┐"
    bottom = f"└{'─' * (width + 2)}┘"
    body = "\n".join(f"│ {line:<{width}} │" for line in lines)
    return f"{top}\n{body}\n{bottom}"
