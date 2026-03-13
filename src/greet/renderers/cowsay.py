_COW = r"""        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||"""


def render_cowsay(text: str) -> str:
    """Wrap text in an ASCII speech bubble with adjacent cow art."""
    width = max(len(text), 1)
    border = "-" * (width + 2)
    bubble = f" {border}\n< {text} >\n {border}"
    return f"{bubble}\n{_COW}"
