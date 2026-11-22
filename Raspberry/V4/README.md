# Raspberry Pi 4 Model B acrylic case prototype

This folder contains a separate six-part, flat-pack case for one bare Raspberry Pi 4 Model B without a HAT. The top has an open service window for the GPIO header and other board connectors. No fan is assumed. It is a **fit-check prototype**, not a final laser order.

## Manufacturer references

- [Raspberry Pi 4 Model B datasheet](https://pip-assets.raspberrypi.com/categories/545-raspberry-pi-4-model-b/documents/RP-008341-DS-1-raspberry-pi-4-datasheet.pdf), section 3.
- [Official mechanical drawing PDF](https://pip-assets.raspberrypi.com/categories/559-mechanical/documents/RP-001185-MD-1-Mechanical%20Drawing.pdf).
- [Official board DXF](https://pip.raspberrypi.com/documents/RP-008342-DS), also linked from the [Raspberry Pi computer documentation](https://www.raspberrypi.com/documentation/computers/sbcs.html#raspberry-pi-4-model-b).

The board is 85 × 56 mm. Its four mounting holes are Ø2.7 mm on a 58 × 49 mm pitch. With the mechanical DXF origin at the board's lower-left in the component-side view, their centres are `(3.5, 3.5)`, `(61.5, 3.5)`, `(3.5, 52.5)`, and `(61.5, 52.5)` mm. The DXF also labels the port and connector sides. These are manufacturer dimensions; the enclosure dimensions below are design choices.

## Case layout

| Feature | Prototype size |
| --- | ---: |
| Outer assembled size | 110 × 86 × 40 mm |
| Acrylic thickness | 3 mm |
| Bottom and top plate | 110 × 86 mm each |
| Power and GPIO wall blanks, including tabs | 104 × 40 mm each |
| microSD and USB/Ethernet wall blanks, including tabs | 74 × 40 mm each |
| Top service opening | 84 × 58 mm, from `(13, 14)` to `(97, 72)` |
| Pi mounting-hole centres on bottom plate | `(16, 18.5)`, `(74, 18.5)`, `(16, 67.5)`, `(74, 67.5)` mm |
| Pi screw clearance in bottom plate | Ø2.7 mm, for M2.5 hardware |
| Case corner holes | Ø3.3 mm, at x=`10/100`, y=`10/76` mm |
| Port wall apertures | Power/HDMI/AV 64 × 24 mm; USB/Ethernet 64 × 24 mm; microSD 26 × 12 mm |

Coordinates are in millimetres from the bottom plate's lower-left in the component-side view. The power/HDMI/AV wall lies along `y=3..6`, the GPIO wall along `y=80..83`, the microSD wall along `x=3..6`, and the USB/Ethernet wall along `x=104..107`. The Pi PCB starts at `(12.5, 15)`.

The bottom and top are held by tabs from all four walls, with four removable M3 case screws through the corners. The Pi mounts on four 8 mm M2.5 insulating spacers above the bottom plate. The top opening exposes GPIO, camera CSI, display DSI, RUN/GLOBAL_EN, and other contacts; the top plate can be removed for ribbon insertion. With an 8 mm spacer and 1.6 mm PCB, the highest 16 mm connector in the manufacturer's drawing is nominally below the inner top surface by about 8 mm. Added headers, plug shells, heat sinks, or cables can change that clearance.

## Files

- [`output/prototype-cut-sheet.dxf`](output/prototype-cut-sheet.dxf): all six case parts, `CUT` layer, millimetres.
- [`output/a4-cut-layout.pdf`](output/a4-cut-layout.pdf): all six case parts on one A4 landscape page at 1:1, with no text. The separate grey line at the lower edge is 50 mm long for print calibration and is not a cut contour.
- [`output/a4-fit-templates.pdf`](output/a4-fit-templates.pdf): six A4 landscape pages, one part per page at 1:1, each with a 50 mm scale line. The bottom page includes a dashed PCB footprint for reference only; it is not a cut contour.
- `output/*.svg`: individual 1:1 case parts.
- [`output/fit-coupon.dxf`](output/fit-coupon.dxf) and [`output/fit-coupon.pdf`](output/fit-coupon.pdf): four test slots plus one 12 × 3 mm test tab. Slot widths are 3.0, 3.1, 3.2, and 3.3 mm from left to right; all have 12.1 mm length.
- [`visualization/`](visualization/README.md): Blender project, colour GLB, GitHub-rotatable STL, and rendered preview of the exploded case with a detailed Pi 4 board.

Regenerate with `uv run python generate.py`. Dependencies are locked in `uv.lock` and Python is pinned in `.python-version`.

## Before cutting the case

1. Print either PDF at **Actual size / 100%**, with page fitting disabled, and measure the 50 mm line. Use the new one-page layout when all six parts are needed together.
2. Lay the real Pi 4 on the bottom paper template. Confirm all four M2.5 holes, board orientation, and the microSD side.
3. Check the port-wall paper openings against the actual USB-C, micro-HDMI, AV, USB, Ethernet, and microSD plugs you intend to use. The factory drawing gives board locations and connector heights; the cable plug bodies and bend radii are not specified in it.
4. Check that the top window gives enough hand and cable access to the GPIO, CSI, DSI, and any other contacts needed in the intended installation.
5. Cut only the fit coupon from the actual 3 mm cast acrylic. Try the tab in each slot without forcing or cracking. Adjust `SLOT_EXTRA` in `generate.py` to match the cutter's kerf before cutting the six case parts.
6. Dry-assemble without the Pi, then mount the Pi on insulating spacers and check every connector again before treating the drawing as final.

The side-wall openings and standoff height are prototype allowances. No physical board, cable plug, acrylic sheet, or laser-cut sample was available for an actual fit test in this iteration.
