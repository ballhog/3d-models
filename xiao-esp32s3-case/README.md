# XIAO ESP32S3 Case

A slim two-part case for the **Seeed Studio XIAO ESP32S3** with the included FPC (flex) antenna. Comes in two versions:

| Version | For | Outer size |
|---|---|---|
| [`standard/`](standard/) | Bare board, no headers. Power and data over USB-C. | 83.5 × 21.6 × 8.9 mm |
| [`breakout/`](breakout/) | Pin headers soldered **underneath**. The 14 pins come out the bottom for a breadboard or female Dupont jumpers. | 83.5 × 21.6 × 9.2 mm |

## Features (both versions)

- **Antenna in its own bay**, about 12 mm away from the board's ground plane and with no metal nearby, which gives better range than stacking the antenna under the board
- **Flexure buttons** in the lid for BOOT (B) and RESET (R)
- **Light pipes** over both onboard LEDs (orange user LED, red charge LED), built into the button tabs. Paint them white in the slicer.
- **USB-C** port flush with the end wall; the stop behind the board keeps it in place when you plug in a cable
- **Snap-fit lid** with three pairs of snaps and a pry notch at the antenna end. No screws, so no metal near the antenna.
- **Antenna-plug retainer** under the lid
- Floor and lid **vents** over the module; V-groove **grip** on both sides
- Flat lid top for **face-down printing with no supports**

### Breakout version differences

- Standard 2.54 mm male headers (2 × 7) are soldered with the **plastic body under the board** and the long pins pointing down.
- The header bodies sit in pockets in the floor, which locate and support the board. The pins pass through a 0.4 mm floor web and stick out about **5.6 mm** below the case.
- The short pin ends sticking up above the board don't need trimming; the lid clears them by up to 3 mm.
- Tip: solder the headers with the board seated in the base, so the pins line up with the floor holes.

## Files

Each version folder contains:

| Folder | Contents |
|---|---|
| `stl/` | Print-ready parts. The `lid_print.stl` file is already flipped face-down. |
| `step/` | Base, lid, and assembly for editing in Onshape / Fusion / etc. |
| `fit-test/` | First 30 mm of the case (board end only). Print this first to check fit. |

`source/xiao_s3_case.py` generates both versions.

## Printing

- **Material:** PETG or ASA recommended. The button flexures can creep or crack in PLA over time.
- **Base:** as-is, open side up.
- **Lid:** `lid_print.stl`, top face on the bed. No supports needed.
- **Light pipes:** in Bambu Studio or OrcaSlicer, paint the two pipe columns white (underside view) and a 1.8 mm circle over each on the top face. A dark lid colour makes them stand out.
- 0.2 mm layers and 3 walls work well.

## Assembly

1. Peel the backing off the flex antenna and stick it in the recess in the floor at the far end.
2. Snap the antenna plug onto the board's u.FL connector before installing the board. The connector is rated for about 30 mating cycles, so plug it in once and leave it.
3. Tilt the board so the USB-C goes into the end-wall opening first, then lower the back of the board behind the stop (breakout: lower the header pins into the floor holes). Route the antenna cable through the notch in the stop.
4. Press the lid on until all snaps click.

## Customizing

Edit the parameters at the top of `source/xiao_s3_case.py` and run it with [CadQuery](https://github.com/CadQuery/cadquery):

```bash
pip install cadquery
python xiao_s3_case.py                          # standard
XIAO_VARIANT=breakout python xiao_s3_case.py    # breakout
```

Output goes to a `standard/` or `breakout/` folder next to the script.

Common tweaks: `ANT_L` / `ANT_W` (antenna size, since generic flex antennas vary), `VENTS`, `GRIP`, `SNAP_R` (snap stiffness), `LED_SIDES`, `HDR_BODY_H` (header plastic height, if yours isn't 2.5 mm).

## Notes

- The case is designed around the Seeed antenna that ships with the XIAO ESP32S3. Measure your antenna if you're using a different one.
- The board model used for fit-checking is Seeed's and isn't included here; it's available from Seeed's wiki.

## License

Design files: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Credit: Joe ([ballhog](https://github.com/ballhog)).
`source/xiao_s3_case.py`: MIT. See the repo [LICENSE](../LICENSE).
