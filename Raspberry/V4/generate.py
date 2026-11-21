"""Generate a prototype laser-cut enclosure for Raspberry Pi 4 Model B."""

from dataclasses import dataclass
from pathlib import Path
from xml.etree import ElementTree as ET

import ezdxf
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "output"
THICKNESS = 3.0
CASE_WIDTH = 110.0
CASE_HEIGHT = 86.0
CASE_DEPTH = 40.0
TAB_LENGTH = 12.0
SLOT_EXTRA = 0.1
BOARD_X = 12.5
BOARD_Y = 15.0
BOARD_HOLES = ((3.5, 3.5), (61.5, 3.5), (3.5, 52.5), (61.5, 52.5))
LONG_TABS = (16.0, 46.0, 76.0)
SHORT_TABS = (13.0, 49.0)


@dataclass(frozen=True)
class Rect:
    x: float
    y: float
    width: float
    height: float


@dataclass(frozen=True)
class Hole:
    x: float
    y: float
    radius: float


@dataclass(frozen=True)
class Part:
    name: str
    width: float
    height: float
    outline: tuple[tuple[float, float], ...]
    cutouts: tuple[Rect, ...] = ()
    holes: tuple[Hole, ...] = ()


def wall_outline(
    length: float, tabs: tuple[float, ...]
) -> tuple[tuple[float, float], ...]:
    """Return a wall contour with 3 mm tabs on both long edges."""
    points = [(0.0, THICKNESS)]
    for start in tabs:
        points.extend(
            (
                (start, THICKNESS),
                (start, 0.0),
                (start + TAB_LENGTH, 0.0),
                (start + TAB_LENGTH, THICKNESS),
            )
        )
    points.extend(((length, THICKNESS), (length, CASE_DEPTH - THICKNESS)))
    for start in reversed(tabs):
        end = start + TAB_LENGTH
        points.extend(
            (
                (end, CASE_DEPTH - THICKNESS),
                (end, CASE_DEPTH),
                (start, CASE_DEPTH),
                (start, CASE_DEPTH - THICKNESS),
            )
        )
    points.append((0.0, CASE_DEPTH - THICKNESS))
    return tuple(points)


def face_slots() -> tuple[Rect, ...]:
    """Place face slots opposite every wall tab."""
    pad = SLOT_EXTRA / 2
    slots = []
    for start in LONG_TABS:
        for y in (THICKNESS, CASE_HEIGHT - 2 * THICKNESS):
            slots.append(
                Rect(
                    THICKNESS + start - pad,
                    y - pad,
                    TAB_LENGTH + SLOT_EXTRA,
                    THICKNESS + SLOT_EXTRA,
                )
            )
    for start in SHORT_TABS:
        for x in (THICKNESS, CASE_WIDTH - 2 * THICKNESS):
            slots.append(
                Rect(
                    x - pad,
                    2 * THICKNESS + start - pad,
                    THICKNESS + SLOT_EXTRA,
                    TAB_LENGTH + SLOT_EXTRA,
                )
            )
    return tuple(slots)


def make_parts() -> tuple[Part, ...]:
    """Build two faces and four labelled side walls."""
    face = (
        (0.0, 0.0),
        (CASE_WIDTH, 0.0),
        (CASE_WIDTH, CASE_HEIGHT),
        (0.0, CASE_HEIGHT),
    )
    corners = tuple(
        Hole(x, y, 1.65)
        for x in (10.0, CASE_WIDTH - 10.0)
        for y in (10.0, CASE_HEIGHT - 10.0)
    )
    mounts = tuple(Hole(BOARD_X + x, BOARD_Y + y, 1.35) for x, y in BOARD_HOLES)
    slots = face_slots()
    bottom = Part("bottom", CASE_WIDTH, CASE_HEIGHT, face, slots, corners + mounts)
    top = Part(
        "top-open-gpio",
        CASE_WIDTH,
        CASE_HEIGHT,
        face,
        slots + (Rect(13.0, 14.0, 84.0, 58.0),),
        corners,
    )
    long_wall = wall_outline(CASE_WIDTH - 2 * THICKNESS, LONG_TABS)
    short_wall = wall_outline(CASE_HEIGHT - 4 * THICKNESS, SHORT_TABS)
    return (
        bottom,
        top,
        Part(
            "power-hdmi-av", 104.0, CASE_DEPTH, long_wall, (Rect(9.0, 8.0, 64.0, 24.0),)
        ),
        Part("gpio-side", 104.0, CASE_DEPTH, long_wall),
        Part(
            "microsd-side", 74.0, CASE_DEPTH, short_wall, (Rect(24.0, 7.0, 26.0, 12.0),)
        ),
        Part(
            "usb-ethernet", 74.0, CASE_DEPTH, short_wall, (Rect(5.0, 8.0, 64.0, 24.0),)
        ),
    )


def make_fit_coupon() -> tuple[Part, Part]:
    """Provide trial slots and a matching 12 by 3 mm tab."""
    slots = tuple(
        Rect(x, 9.5, TAB_LENGTH + SLOT_EXTRA, width)
        for x, width in zip((6.0, 25.0, 44.0, 63.0), (3.0, 3.1, 3.2, 3.3), strict=True)
    )
    plate = Part(
        "fit-slots",
        82.0,
        23.0,
        ((0.0, 0.0), (82.0, 0.0), (82.0, 23.0), (0.0, 23.0)),
        slots,
    )
    tab = Part(
        "fit-tab",
        30.0,
        16.0,
        (
            (0.0, 3.0),
            (9.0, 3.0),
            (9.0, 0.0),
            (21.0, 0.0),
            (21.0, 3.0),
            (30.0, 3.0),
            (30.0, 16.0),
            (0.0, 16.0),
        ),
    )
    return plate, tab


def rect_points(rect: Rect) -> tuple[tuple[float, float], ...]:
    """Return clockwise corners for a rectangular cutout."""
    return (
        (rect.x, rect.y),
        (rect.x + rect.width, rect.y),
        (rect.x + rect.width, rect.y + rect.height),
        (rect.x, rect.y + rect.height),
    )


def assert_clear(part: Part) -> None:
    """Check cutouts against edges and each other."""
    for index, a in enumerate(part.cutouts):
        assert a.width > 0 and a.height > 0
        assert 0 < a.x and 0 < a.y
        assert a.x + a.width < part.width
        assert a.y + a.height < part.height
        for b in part.cutouts[index + 1 :]:
            assert (
                a.x + a.width <= b.x
                or b.x + b.width <= a.x
                or a.y + a.height <= b.y
                or b.y + b.height <= a.y
            ), part.name
        for hole in part.holes:
            closest_x = max(a.x, min(hole.x, a.x + a.width))
            closest_y = max(a.y, min(hole.y, a.y + a.height))
            assert (hole.x - closest_x) ** 2 + (hole.y - closest_y) ** 2 > (
                hole.radius + 0.5
            ) ** 2, part.name


def validate(parts: tuple[Part, ...]) -> None:
    """Check the board pitch and matching tab/slot count."""
    assert len(parts) == 6
    assert BOARD_HOLES[1][0] - BOARD_HOLES[0][0] == 58.0
    assert BOARD_HOLES[2][1] - BOARD_HOLES[0][1] == 49.0
    assert len(face_slots()) == 2 * len(LONG_TABS) + 2 * len(SHORT_TABS)
    assert all(len(part.outline) >= 4 for part in parts)
    for part in parts:
        assert_clear(part)


def svg_element(tag: str, **attributes: str) -> ET.Element:
    """Create a namespaced SVG element."""
    return ET.Element(f"{{http://www.w3.org/2000/svg}}{tag}", attributes)


def write_svg(part: Part, path: Path) -> None:
    """Write one millimetre-scaled SVG cutting part."""
    root = svg_element(
        "svg",
        width=f"{part.width:g}mm",
        height=f"{part.height:g}mm",
        viewBox=f"0 0 {part.width:g} {part.height:g}",
    )
    group = ET.SubElement(
        root,
        "{http://www.w3.org/2000/svg}g",
        {"fill": "none", "stroke": "#000000", "stroke-width": "0.1"},
    )
    ET.SubElement(
        group,
        "{http://www.w3.org/2000/svg}polygon",
        {
            "points": " ".join(f"{x:g},{y:g}" for x, y in part.outline),
        },
    )
    for cutout in part.cutouts:
        ET.SubElement(
            group,
            "{http://www.w3.org/2000/svg}rect",
            {
                "x": f"{cutout.x:g}",
                "y": f"{cutout.y:g}",
                "width": f"{cutout.width:g}",
                "height": f"{cutout.height:g}",
            },
        )
    for hole in part.holes:
        ET.SubElement(
            group,
            "{http://www.w3.org/2000/svg}circle",
            {
                "cx": f"{hole.x:g}",
                "cy": f"{hole.y:g}",
                "r": f"{hole.radius:g}",
            },
        )
    ET.ElementTree(root).write(path, encoding="utf-8", xml_declaration=True)


def write_dxf(
    parts: tuple[Part, ...], path: Path, positions: tuple[tuple[float, float], ...]
) -> None:
    """Write a single DXF cut sheet using millimetres."""
    drawing = ezdxf.new("R2000")
    drawing.units = ezdxf.units.MM
    drawing.layers.new("CUT", dxfattribs={"color": 7})
    model = drawing.modelspace()
    for part, (dx, dy) in zip(parts, positions, strict=True):
        model.add_lwpolyline(
            [(x + dx, y + dy) for x, y in part.outline],
            close=True,
            dxfattribs={"layer": "CUT"},
        )
        for rect in part.cutouts:
            model.add_lwpolyline(
                [(x + dx, y + dy) for x, y in rect_points(rect)],
                close=True,
                dxfattribs={"layer": "CUT"},
            )
        for hole in part.holes:
            model.add_circle(
                (hole.x + dx, hole.y + dy), hole.radius, dxfattribs={"layer": "CUT"}
            )
    drawing.saveas(path)


def write_pdf(parts: tuple[Part, ...], path: Path) -> None:
    """Write one 1:1 A4 landscape template page per part."""
    document = canvas.Canvas(str(path), pagesize=landscape(A4))
    for part in parts:
        document.setFont("Helvetica-Bold", 13)
        document.drawString(20 * mm, 188 * mm, part.name)
        document.setFont("Helvetica", 9)
        document.drawString(
            20 * mm, 180 * mm, f"{part.width:g} x {part.height:g} mm | print at 100%"
        )
        document.saveState()
        document.translate(24 * mm, 45 * mm)
        document.setLineWidth(0.2 * mm)
        contour = document.beginPath()
        contour.moveTo(*[v * mm for v in part.outline[0]])
        for x, y in part.outline[1:]:
            contour.lineTo(x * mm, y * mm)
        contour.close()
        document.drawPath(contour)
        for rect in part.cutouts:
            document.rect(rect.x * mm, rect.y * mm, rect.width * mm, rect.height * mm)
        for hole in part.holes:
            document.circle(hole.x * mm, hole.y * mm, hole.radius * mm)
        if part.name == "bottom":
            document.setStrokeColorRGB(0.55, 0.55, 0.55)
            document.setDash(2 * mm, 1 * mm)
            document.rect(BOARD_X * mm, BOARD_Y * mm, 85 * mm, 56 * mm)
            document.setDash()
        document.restoreState()
        if part.name in ("bottom", "top-open-gpio"):
            document.setFont("Helvetica", 8)
            document.drawString(150 * mm, 102 * mm, "Power / HDMI / AV: lower edge")
            document.drawString(150 * mm, 96 * mm, "USB / Ethernet: right edge")
            document.drawString(150 * mm, 90 * mm, "microSD: left edge")
            document.drawString(150 * mm, 84 * mm, "GPIO: upper edge")
            if part.name == "bottom":
                document.drawString(
                    150 * mm, 72 * mm, "Dashed Pi outline: reference only"
                )
        document.setLineWidth(0.2 * mm)
        document.line(20 * mm, 24 * mm, 70 * mm, 24 * mm)
        document.setFont("Helvetica", 8)
        document.drawString(20 * mm, 18 * mm, "50 mm calibration line")
        document.showPage()
    document.save()


def write_a4_cut_layout(parts: tuple[Part, ...], path: Path) -> None:
    """Place all six cut profiles at 1:1 on one text-free A4 page."""
    assert len(parts) == 6
    positions = ((10, 114), (125, 114), (10, 69), (119, 69), (10, 24), (89, 24))
    page_width, page_height = landscape(A4)
    bounds = []
    document = canvas.Canvas(str(path), pagesize=(page_width, page_height))
    document.setLineWidth(0.15 * mm)
    for part, (x_offset, y_offset) in zip(parts, positions, strict=True):
        assert 10 <= x_offset and 10 <= y_offset
        assert (x_offset + part.width) * mm <= page_width - 10 * mm
        assert (y_offset + part.height) * mm <= page_height - 10 * mm
        for left, bottom, right, top in bounds:
            assert (
                x_offset >= right + 5
                or x_offset + part.width + 5 <= left
                or y_offset >= top + 5
                or y_offset + part.height + 5 <= bottom
            )
        bounds.append(
            (x_offset, y_offset, x_offset + part.width, y_offset + part.height)
        )
        document.saveState()
        document.translate(x_offset * mm, y_offset * mm)
        contour = document.beginPath()
        contour.moveTo(part.outline[0][0] * mm, part.outline[0][1] * mm)
        for x, y in part.outline[1:]:
            contour.lineTo(x * mm, y * mm)
        contour.close()
        document.drawPath(contour)
        for rect in part.cutouts:
            document.rect(rect.x * mm, rect.y * mm, rect.width * mm, rect.height * mm)
        for hole in part.holes:
            document.circle(hole.x * mm, hole.y * mm, hole.radius * mm)
        document.restoreState()
    document.setStrokeColorRGB(0.5, 0.5, 0.5)
    document.line(10 * mm, 10 * mm, 60 * mm, 10 * mm)
    document.showPage()
    document.save()


def main() -> None:
    """Validate and generate all case files."""
    parts = make_parts()
    coupon = make_fit_coupon()
    validate(parts)
    for part in coupon:
        assert_clear(part)
    OUT.mkdir(exist_ok=True)
    for part in parts:
        write_svg(part, OUT / f"{part.name}.svg")
    for part in coupon:
        write_svg(part, OUT / f"{part.name}.svg")
    write_dxf(
        parts,
        OUT / "prototype-cut-sheet.dxf",
        ((0, 0), (125, 0), (0, 105), (120, 105), (0, 160), (90, 160)),
    )
    write_dxf(coupon, OUT / "fit-coupon.dxf", ((0, 0), (100, 0)))
    write_pdf(parts, OUT / "a4-fit-templates.pdf")
    write_pdf(coupon, OUT / "fit-coupon.pdf")
    write_a4_cut_layout(parts, OUT / "a4-cut-layout.pdf")


if __name__ == "__main__":
    main()
