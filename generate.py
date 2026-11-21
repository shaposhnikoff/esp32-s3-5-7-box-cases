"""Generate 1:1 acrylic enclosure prototypes from measured board dimensions."""

from dataclasses import dataclass
from pathlib import Path
from xml.sax.saxutils import escape

import ezdxf
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas


@dataclass(frozen=True)
class Rect:
    """A cut rectangle in millimetres, measured from a part's upper-left corner."""

    x: float
    y: float
    width: float
    height: float


@dataclass(frozen=True)
class Circle:
    """A circular cut with its centre in millimetres."""

    x: float
    y: float
    diameter: float


@dataclass(frozen=True)
class Polygon:
    """A closed contour whose vertices are in millimetres."""

    points: tuple[tuple[float, float], ...]


@dataclass(frozen=True)
class Part:
    """A flat acrylic part and its internal cutouts."""

    name: str
    width: float
    height: float
    cutouts: tuple[Rect | Circle, ...] = ()
    outer: Polygon | None = None


@dataclass(frozen=True)
class Case:
    """A six-part case intended for three-millimetre acrylic."""

    name: str
    width: float
    height: float
    wall_depth: float
    window: Rect
    mount_x: tuple[float, float]
    mount_y: tuple[float, float]
    mount_diameter: float


CASES = (
    Case(
        name="waveshare-5b",
        width=160,
        height=115,
        wall_depth=30,
        window=Rect(19.15, 17.2, 121.7, 80.6),
        mount_x=(24.5, 135.5),
        mount_y=(26.225, 89.225),
        mount_diameter=3.2,
    ),
    Case(
        name="waveshare-7b",
        width=224,
        height=140,
        wall_depth=30,
        window=Rect(27.85, 18.6, 168.3, 102.8),
        mount_x=(50.43, 176.63),
        mount_y=(36.20, 101.85),
        mount_diameter=3.6,
    ),
)

ACRYLIC_THICKNESS = 3.0
SLOT_CLEARANCE = 0.1
TAB_LENGTH = 12.0


def tab_intervals(length: float, count: int) -> tuple[tuple[float, float], ...]:
    """Space equal tabs away from the ends of a wall."""
    return tuple(
        (
            length * i / (count + 1) - TAB_LENGTH / 2,
            length * i / (count + 1) + TAB_LENGTH / 2,
        )
        for i in range(1, count + 1)
    )


def wall_outline(
    length: float, depth: float, tabs: tuple[tuple[float, float], ...]
) -> Polygon:
    """Add three-millimetre tabs at both ends of a wall's depth."""
    front = ACRYLIC_THICKNESS
    rear = front + depth
    points = [(0.0, front)]
    for start, end in tabs:
        points.extend(((start, front), (start, 0.0), (end, 0.0), (end, front)))
    points.extend(((length, front), (length, rear)))
    for start, end in reversed(tabs):
        points.extend(
            ((end, rear), (end, rear + front), (start, rear + front), (start, rear))
        )
    points.append((0.0, rear))
    return Polygon(tuple(points))


def face_slots(spec: Case) -> tuple[Rect, ...]:
    """Cut clearance slots matching each wall tab in both face plates."""
    half_gap = SLOT_CLEARANCE / 2
    top_tabs = tab_intervals(spec.width - 2 * ACRYLIC_THICKNESS, 3)
    side_tabs = tab_intervals(spec.height - 4 * ACRYLIC_THICKNESS, 2)
    slots = []
    for y in (ACRYLIC_THICKNESS, spec.height - 2 * ACRYLIC_THICKNESS):
        slots.extend(
            Rect(
                ACRYLIC_THICKNESS + start - half_gap,
                y - half_gap,
                end - start + SLOT_CLEARANCE,
                ACRYLIC_THICKNESS + SLOT_CLEARANCE,
            )
            for start, end in top_tabs
        )
    for x in (ACRYLIC_THICKNESS, spec.width - 2 * ACRYLIC_THICKNESS):
        slots.extend(
            Rect(
                x - half_gap,
                2 * ACRYLIC_THICKNESS + start - half_gap,
                ACRYLIC_THICKNESS + SLOT_CLEARANCE,
                end - start + SLOT_CLEARANCE,
            )
            for start, end in side_tabs
        )
    return tuple(slots)


def make_parts(spec: Case) -> tuple[Part, ...]:
    """Build two slotted faces and four walls with through-tabs."""
    corner_holes = tuple(
        Circle(x, y, 3.3) for x in (8, spec.width - 8) for y in (8, spec.height - 8)
    )
    board_holes = tuple(
        Circle(x, y, spec.mount_diameter) for x in spec.mount_x for y in spec.mount_y
    )
    vents = tuple(
        Rect(spec.width / 2 - 48 + 24 * i, y, 18, 3)
        for y in (13, spec.height - 16)
        for i in range(4)
    )
    slots = face_slots(spec)
    top_length = spec.width - 2 * ACRYLIC_THICKNESS
    side_length = spec.height - 4 * ACRYLIC_THICKNESS
    wall_height = spec.wall_depth + 2 * ACRYLIC_THICKNESS
    top_outline = wall_outline(
        top_length, spec.wall_depth, tab_intervals(top_length, 3)
    )
    side_outline = wall_outline(
        side_length, spec.wall_depth, tab_intervals(side_length, 2)
    )
    return (
        Part("front", spec.width, spec.height, (spec.window, *slots, *corner_holes)),
        Part(
            "rear",
            spec.width,
            spec.height,
            (*slots, *corner_holes, *board_holes, *vents),
        ),
        Part("top", top_length, wall_height, outer=top_outline),
        Part("bottom", top_length, wall_height, outer=top_outline),
        Part("left", side_length, wall_height, outer=side_outline),
        Part("right", side_length, wall_height, outer=side_outline),
    )


def make_fit_coupon() -> tuple[Part, Part]:
    """Provide four candidate slot widths and one sample wall tab."""
    slots = tuple(
        Rect(x, 10, TAB_LENGTH + SLOT_CLEARANCE, width)
        for x, width in zip((6, 27, 48, 69), (3.0, 3.1, 3.2, 3.3), strict=True)
    )
    female = Part("slot-gauge", 90, 25, slots)
    male = Part(
        "tab-gauge",
        25,
        20,
        outer=Polygon(
            (
                (0, 3),
                (6.5, 3),
                (6.5, 0),
                (18.5, 0),
                (18.5, 3),
                (25, 3),
                (25, 20),
                (0, 20),
            )
        ),
    )
    return female, male


def outlines(part: Part) -> tuple[Rect | Circle | Polygon, ...]:
    """Return the outside edge followed by every internal cut."""
    return (part.outer or Rect(0, 0, part.width, part.height), *part.cutouts)


def validate(parts: tuple[Part, ...]) -> None:
    """Reject cuts outside their parent panel."""
    for part in parts:
        if part.outer:
            for x, y in part.outer.points:
                if not (0 <= x <= part.width and 0 <= y <= part.height):
                    raise ValueError(f"Outer contour outside {part.name}: {(x, y)}")
        for cut in part.cutouts:
            if isinstance(cut, Rect):
                bounds = (cut.x, cut.y, cut.x + cut.width, cut.y + cut.height)
            else:
                radius = cut.diameter / 2
                bounds = (
                    cut.x - radius,
                    cut.y - radius,
                    cut.x + radius,
                    cut.y + radius,
                )
            if not (0 <= bounds[0] < bounds[2] <= part.width):
                raise ValueError(f"Cut outside {part.name}: {cut}")
            if not (0 <= bounds[1] < bounds[3] <= part.height):
                raise ValueError(f"Cut outside {part.name}: {cut}")


def svg_contours(part: Part) -> str:
    """Serialize a part's cut contours as SVG elements."""
    shapes = []
    for cut in outlines(part):
        if isinstance(cut, Rect):
            shapes.append(
                f'<rect x="{cut.x}" y="{cut.y}" width="{cut.width}" '
                f'height="{cut.height}" />'
            )
        elif isinstance(cut, Circle):
            shapes.append(
                f'<circle cx="{cut.x}" cy="{cut.y}" r="{cut.diameter / 2}" />'
            )
        else:
            points = " ".join(f"{x},{y}" for x, y in cut.points)
            shapes.append(f'<polygon points="{points}" />')
    return "\n".join(shapes)


def svg(part: Part) -> str:
    """Serialize one part as an SVG using millimetre units."""
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{part.width}mm" '
        f'height="{part.height}mm" viewBox="0 0 {part.width} {part.height}">\n'
        f"<title>{escape(part.name)}</title>\n"
        '<g fill="none" stroke="#000" stroke-width="0.1">\n'
        + svg_contours(part)
        + "\n</g>\n</svg>\n"
    )


def sheet_positions(
    spec: Case, parts: tuple[Part, ...]
) -> tuple[tuple[Part, float, float], ...]:
    """Place six separate panels without nesting parts inside the front window."""
    gap = 8
    front, rear, top, bottom, left, right = parts
    return (
        (front, 0, 0),
        (rear, front.width + gap, 0),
        (top, 0, spec.height + gap),
        (bottom, 0, spec.height + top.height + 2 * gap),
        (left, spec.width + gap, spec.height + gap),
        (right, spec.width + gap, spec.height + left.height + 2 * gap),
    )


def write_dxf(path: Path, positions: tuple[tuple[Part, float, float], ...]) -> None:
    """Write an AutoCAD 2000 DXF with one closed contour per cut."""
    drawing = ezdxf.new("R2000")
    drawing.units = 4
    drawing.layers.new("CUT")
    modelspace = drawing.modelspace()
    for part, offset_x, offset_y in positions:
        for cut in outlines(part):
            if isinstance(cut, Circle):
                modelspace.add_circle(
                    (cut.x + offset_x, cut.y + offset_y),
                    cut.diameter / 2,
                    dxfattribs={"layer": "CUT"},
                )
            elif isinstance(cut, Rect):
                x = cut.x + offset_x
                y = cut.y + offset_y
                points = (
                    (x, y),
                    (x + cut.width, y),
                    (x + cut.width, y + cut.height),
                    (x, y + cut.height),
                )
                modelspace.add_lwpolyline(
                    points, close=True, dxfattribs={"layer": "CUT"}
                )
            else:
                modelspace.add_lwpolyline(
                    ((x + offset_x, y + offset_y) for x, y in cut.points),
                    close=True,
                    dxfattribs={"layer": "CUT"},
                )
    drawing.saveas(path)


def draw_pdf_part(pdf: canvas.Canvas, part: Part) -> None:
    """Draw a part on an A4 landscape page at true 1:1 scale."""
    page_width, page_height = landscape(A4)
    x0 = (page_width / mm - part.width) / 2
    y0 = (page_height / mm - part.height) / 2 - 2
    pdf.setLineWidth(0.15 * mm)
    for cut in outlines(part):
        if isinstance(cut, Rect):
            pdf.rect(
                (x0 + cut.x) * mm,
                (y0 + part.height - cut.y - cut.height) * mm,
                cut.width * mm,
                cut.height * mm,
            )
        elif isinstance(cut, Circle):
            pdf.circle(
                (x0 + cut.x) * mm,
                (y0 + part.height - cut.y) * mm,
                cut.diameter / 2 * mm,
            )
        else:
            path = pdf.beginPath()
            first_x, first_y = cut.points[0]
            path.moveTo((x0 + first_x) * mm, (y0 + part.height - first_y) * mm)
            for x, y in cut.points[1:]:
                path.lineTo((x0 + x) * mm, (y0 + part.height - y) * mm)
            path.close()
            pdf.drawPath(path)
    pdf.setFont("Helvetica", 9)
    pdf.drawString(
        12 * mm,
        page_height - 10 * mm,
        f"{part.name}: {part.width} x {part.height} mm | 1:1",
    )
    if part.name == "front":
        window = part.cutouts[0]
        assert isinstance(window, Rect)
        pdf.drawString(
            12 * mm,
            page_height - 15 * mm,
            f"Metal opening: {window.width} x {window.height} mm | left {window.x}, top {window.y} mm",
        )
    elif part.name == "rear":
        pdf.drawString(
            12 * mm,
            page_height - 15 * mm,
            "Coordinates face case front; flip paper to check from rear",
        )
    elif part.name == "slot-gauge":
        pdf.setFont("Helvetica", 7)
        for slot in part.cutouts:
            assert isinstance(slot, Rect)
            pdf.drawCentredString(
                (x0 + slot.x + slot.width / 2) * mm,
                (y0 + 3) * mm,
                f"{slot.height:.1f}",
            )
    pdf.line(12 * mm, 12 * mm, 62 * mm, 12 * mm)
    pdf.drawString(12 * mm, 14 * mm, "50 mm control line")
    pdf.showPage()


def main() -> None:
    """Generate machine vectors and A4 fit templates for both display boards."""
    root = Path(__file__).parent / "output" / "finger-joint"
    for spec in CASES:
        folder = root / spec.name
        folder.mkdir(parents=True, exist_ok=True)
        parts = make_parts(spec)
        validate(parts)
        for part in parts:
            (folder / f"{part.name}.svg").write_text(svg(part))
        positions = sheet_positions(spec, parts)
        write_dxf(folder / "prototype-cut-sheet.dxf", positions)
        pdf = canvas.Canvas(
            str(folder / "a4-fit-templates.pdf"), pagesize=landscape(A4)
        )
        for part in parts:
            draw_pdf_part(pdf, part)
        pdf.save()
        front_pdf = canvas.Canvas(
            str(folder / "front-panel-1to1.pdf"), pagesize=landscape(A4)
        )
        draw_pdf_part(front_pdf, parts[0])
        front_pdf.save()
        print(f"Generated {spec.name}: {len(parts)} parts")

    coupon_folder = root / "fit-coupon"
    coupon_folder.mkdir(parents=True, exist_ok=True)
    coupon_parts = make_fit_coupon()
    validate(coupon_parts)
    for part in coupon_parts:
        (coupon_folder / f"{part.name}.svg").write_text(svg(part))
    write_dxf(
        coupon_folder / "fit-coupon.dxf",
        ((coupon_parts[0], 0, 0), (coupon_parts[1], 0, 35)),
    )
    pdf = canvas.Canvas(str(coupon_folder / "fit-coupon.pdf"), pagesize=landscape(A4))
    for part in coupon_parts:
        draw_pdf_part(pdf, part)
    pdf.save()
    print("Generated fit coupon: 2 parts")


if __name__ == "__main__":
    main()
