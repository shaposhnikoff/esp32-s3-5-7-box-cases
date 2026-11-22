# Acrylic cases for Waveshare displays and Raspberry Pi 4

[Інструкція для майстерні українською](docs/instruction-for-cutting-uk.md)

Prototype cutting files for **two display enclosures**, each with six panels and two supports cut from nominal 3 mm cast acrylic. The metal display body passes through the front opening; the outer coloured rim rests on the acrylic and attaches with the display's adhesive tape. Wall tabs enter matching slots in the front and rear plates. The four corner fasteners remain removable.

## Dimensions

All dimensions are in millimetres. Opening coordinates are measured from the top-left corner of the front plate, viewed from the front.

| Feature | 5-inch | 7B |
| --- | ---: | ---: |
| Front and rear plate | 160 × 115 | 224 × 140 |
| Front opening | 121.7 × 80.6 | 168.3 × 102.8 |
| Opening left, top | 19.15, 17.2 | 27.85, 18.6 |
| Protruding body in the supplied STEP model | 120.7 × 75.8 | 164.0 × 97.0 |
| Outer touch glass | 127.7 × 87.45 | 192.96 × 110.76 |
| Minimum nominal glass overlap around opening | 3.0 | 3.98 |
| Assembled outer depth | 36 | 36 |
| Support base length | 152 | 188 |
| Support slot center X from left edge | 16, 144 | 26, 198 |
| Support slot center Y from bottom edge | 20, 42 | 20, 42 |

The 7B dimensional drawing calls out 97.60 mm across its backing; the prototype opening accounts for this larger value and the body offset. The supplied five-inch archive is named `ESP32-S3-Touch-LCD-5_Drawing.zip`, without `B`. Its fit to a 5B module has **not** been physically verified.

The panel sizes, opening clearances, wall depth, and corner fastener positions are design choices. The display dimensions and mount positions were derived from the manufacturer's PDF and STEP files supplied for this project.

## Cutting and fit files

Each enclosure has eight individual SVG parts, one millimetre-unit DXF sheet, an eight-page A4 PDF with one part per page, and a single-page 1:1 front-plate PDF.

- **5-inch:** [front plate 1:1](output/finger-joint/waveshare-5b/front-panel-1to1.pdf) · [A4 templates](output/finger-joint/waveshare-5b/a4-fit-templates.pdf) · [DXF sheet](output/finger-joint/waveshare-5b/prototype-cut-sheet.dxf)
- **7B:** [front plate 1:1](output/finger-joint/waveshare-7b/front-panel-1to1.pdf) · [A4 templates](output/finger-joint/waveshare-7b/a4-fit-templates.pdf) · [DXF sheet](output/finger-joint/waveshare-7b/prototype-cut-sheet.dxf)
- **7B and 5B together:** [combined DXF sheet, 16 parts](output/finger-joint/waveshare-7b-5b-cut-sheet.dxf)
- **All three cases:** [workshop DXF with Raspberry Pi 4, 22 parts](output/finger-joint/workshop-all-cases.dxf)
- **Joint calibration:** [fit coupon PDF](output/finger-joint/fit-coupon/fit-coupon.pdf) · [fit coupon DXF](output/finger-joint/fit-coupon/fit-coupon.dxf)

Print PDF templates at **100% / Actual size**, with page fitting disabled. Check the 50 mm control line with a ruler. The DXF and SVG files are cutting geometry. The PDFs are paper fit templates. All eight parts have separate outlines on each DXF sheet.

The walls have 12 × 3 mm tabs. Front and rear plates have ten nominal 12.1 × 3.1 mm wall slots each. The rear plate has four additional 3.1 × 12.1 mm through slots. Each triangular support has two 12 mm tabs that enter the rear plate by 3 mm for gluing. The supports hold the enclosure at 15° from vertical. The separate coupon has four slot widths from 3.0 to 3.3 mm in 0.1 mm increments. Test the actual acrylic and laser kerf on this coupon before choosing a case slot width. Edit `SLOT_CLEARANCE` in `generate.py` and regenerate if a different fit is needed.

## Waveshare 3D previews

- **5-inch** · [Rotate on GitHub](visualization/waveshare-5b/waveshare-5b-acrylic-showcase.stl) · [Photoreal render, Blender projects and colour GLB](visualization/README.md#waveshare-5-inch)
- **7B** · [Rotate on GitHub](visualization/waveshare-7b/waveshare-7b-acrylic-showcase.stl) · [Photoreal render, Blender projects and colour GLB](visualization/README.md#waveshare-7b)

## Generate

```sh
uv sync --locked
uv run python generate.py
```

The project uses Python 3.13, with dependencies pinned by `uv.lock`.

## Prototype status

These files are **not approved for final cutting**. First check the paper front/rear templates against both physical modules, including the adhesive rim, mount holes, and orientation. The USB/power openings in the side walls, board spacer heights, actual acrylic thickness, laser kerf, and physical assembly fit remain unverified. The side walls currently have no connector openings. Dry-fit the enclosure before applying tape, and avoid loading the touch glass through the rear fasteners.

See the [generation and fit-check flow](docs/diagrams/acrylic-case-generation-flow.md).

## Raspberry Pi 4 Model B

The separate [Raspberry/V4 prototype](Raspberry/V4/README.md) is a six-part acrylic case with an open GPIO service window and side openings for the Pi 4 ports. It includes its own [DXF cut sheet](Raspberry/V4/output/prototype-cut-sheet.dxf), [single-page A4 layout at 1:1](Raspberry/V4/output/a4-cut-layout.pdf), fit coupon, SVG parts, and generator. Check the physical board, plug clearance, and laser kerf before a final cut.

The [3D showcase](Raspberry/V4/visualization/README.md) includes a Blender scene with transparent acrylic, a detailed Raspberry Pi 4 board, a colour GLB, a GitHub-rotatable STL, and a rendered preview.
