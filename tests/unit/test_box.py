from greet.renderers.box import render_box


def test_single_line_has_box_corners() -> None:
    result = render_box(["Hello"])
    assert "┌" in result
    assert "┐" in result
    assert "└" in result
    assert "┘" in result


def test_single_line_contains_text() -> None:
    result = render_box(["Hello"])
    assert "Hello" in result


def test_single_line_has_borders() -> None:
    result = render_box(["Hi"])
    assert "│" in result
    assert "─" in result


def test_multiple_lines_all_present() -> None:
    result = render_box(["line one", "line two"])
    assert "line one" in result
    assert "line two" in result


def test_multiple_lines_aligned_to_widest() -> None:
    lines = ["short", "a longer line"]
    result = render_box(lines)
    width = max(len(line) for line in lines)
    # top border should span the widest line + 2 padding
    assert "─" * (width + 2) in result


def test_empty_list_returns_minimal_box() -> None:
    result = render_box([])
    assert "┌┐" in result
    assert "└┘" in result


def test_structure_is_three_parts() -> None:
    result = render_box(["text"])
    lines = result.splitlines()
    assert len(lines) == 3  # top, body, bottom
