"""
Seeed XIAO ESP32S3 long case: board at one end, FPC antenna at the other.
Parametric CadQuery model -> STEP (for Onshape) + STL (for printing).

Coordinates: X = length (USB-C end at x=0), Y = width (centred), Z = up.
All dimensions in mm. VERIFY the *_VERIFY values with calipers before printing.
"""
import cadquery as cq

# ---------------- parameters ----------------
WALL = 1.6          # side wall thickness
FLOOR = 1.6         # floor thickness
LID_T = 1.6         # lid plate thickness
FIT = 0.3           # board clearance per side
LIP_CLR = 0.15      # lid lip clearance per side
LIP_H = 1.5         # lid lip depth
LIP_T = 1.0         # lid lip wall thickness

PCB_L = 20.95       # along X (USB edge to antenna-connector edge)  [from Seeed STEP]
PCB_W = 17.78       # along Y
PCB_T = 1.0
STANDOFF = 1.0      # board sits on ledges this high (clears bottom pads)
TOP_STACK = 3.4     # USB-C shell 3.21 above PCB; u.FL plug ~2.5; shield 2.0

USB_W, USB_H = 9.4, 4.6     # USB-C shell 8.94 x 4.20 + clearance
USB_Z_ABOVE_PCB = 1.11      # USB-C centre height above PCB top
USB_OVERHANG = 1.53          # USB-C shell sticks past PCB edge (sits inside end wall)
UFL_Y = -4.73                # u.FL connector centre (Y) at antenna end of board

GAP = 12.0          # empty space board -> antenna (pigtail loop)
ANT_L, ANT_W = 46.0, 15.0   # FPC antenna footprint + ~1 mm margin (VERIFY)
ANT_RECESS = 0.3

# Buttons (B = BOOT, R = RESET) flank the USB-C on the top side  (VERIFY)
BTN_X = 1.59        # from PCB USB edge to button centre  [from STEP]
BTN_Y = 5.93        # +/- from centreline
BTN_TOP = 0.73      # button top above PCB
FLEX_W, FLEX_L, FLEX_SLOT = 3.6, 7.0, 0.7   # flexure tab size & slot width
NUB_D, NUB_GAP = 1.8, 0.3                   # plunger dia, rest gap above button

WIRE_SLOT = False   # sensor-wire exit in side wall at board end
WIRE_W, WIRE_H = 6.0, 3.0

CORNER_R = 2.0

# LED window: white light-pipe insert (print as a second material)
LED_X = 4.0         # LEDs sit just inboard of B and R buttons, from PCB USB edge  [from photos, +/-0.3]
LED_Y = BTN_Y       # same line as the buttons
LED_SIDES = (1, -1) # +1 = user LED by B (orange), -1 = charge LED by R (red)
LED_TOP = 0.5       # LED height above PCB
PIPE_D = 1.8        # white pipe diameter (visible dot on lid)
PIPE_GAP = 0.8      # pipe bottom to LED top
PIPE_RECESS = 0.0   # 0 = lid top dead flat (face-down print). >0 recesses the pipe top

# pry notch (antenna end, top edge of base)
PRY_W, PRY_D = 8.0, 1.0

# grip: vertical V-grooves down both long sides
GRIP = True
GRIP_X = (30.0, 78.0)     # start/end along length
GRIP_PITCH = 1.6
GRIP_DEPTH = 0.5
GRIP_W = 1.2              # groove width at surface

# lid snaps: half-round ridges on the lid lip click into grooves in the base walls
SNAP_X = (16.0, 50.0, 75.0)   # along length (both sides)
SNAP_LEN = 6.0
SNAP_R = 0.45                 # ridge radius (protrudes SNAP_R - LIP_CLR past the lip)
SNAP_Z = 0.9                  # below lid underside
# board hold-down ribs (from lid onto PCB long edges) and u.FL plug retainer
HOLD_X = (13.0, 20.9)
HOLD_Y = 8.3
HOLD_GAP = 0.1
UFL_X = 19.18                 # u.FL centre from PCB USB edge [from STEP]
UFL_PLUG_TOP = 2.4            # mated u.FL plug top above PCB
UFL_GAP = 0.2
BOTTOM_CHAMFER = 0.4

# vents
VENTS = True
VENT_W = 1.2
FLOOR_VENTS_Y = (-4.5, -1.5, 1.5, 4.5)   # under board, between ledges
FLOOR_VENT_X = (6.0, 18.0)                # from PCB USB edge
LID_VENTS_Y = (-4.0, -1.5, 1.5, 4.0)      # over the shield can
LID_VENT_X = (12.5, 17.5)

# ---------------- derived ----------------
IN_W = PCB_W + 2 * FIT
IN_L = (PCB_L + FIT) + GAP + ANT_L + 1.0
IN_H = STANDOFF + PCB_T + TOP_STACK + 0.3
OUT_L, OUT_W, OUT_H = IN_L + 2 * WALL, IN_W + 2 * WALL, IN_H + FLOOR
assert ANT_W <= IN_W, "antenna wider than interior - widen case"

pcb_x0 = WALL + 0.05                # PCB USB edge against inner wall; USB-C pokes into the wall
pcb_z = FLOOR + STANDOFF            # PCB bottom z
pcb_top = pcb_z + PCB_T

# ---------------- base ----------------
base = (cq.Workplane("XY")
        .box(OUT_L, OUT_W, OUT_H, centered=(False, True, False))
        .edges("|Z").fillet(CORNER_R)
        .faces("<Z").edges().chamfer(BOTTOM_CHAMFER))
cavity = cq.Workplane("XY").box(IN_L, IN_W, IN_H, centered=(False, True, False)) \
    .translate((WALL, 0, FLOOR))
base = base.cut(cavity)

# board ledges along both long sides (leave centre open for bottom pads)
for s in (1, -1):
    ledge = cq.Workplane("XY").box(PCB_L, 2.0, STANDOFF, centered=(False, True, False)) \
        .translate((pcb_x0, s * (IN_W / 2 - 1.0), FLOOR))
    base = base.union(ledge)
# end stop behind the board so it can't slide back
stop = cq.Workplane("XY").box(1.2, IN_W, STANDOFF + PCB_T + 1.0, centered=(False, True, False)) \
    .translate((pcb_x0 + PCB_L + FIT, 0, FLOOR))
# notch the stop so the pigtail can pass over/around it
notch = cq.Workplane("XY").box(1.4, 6.0, 5, centered=(False, True, False)) \
    .translate((pcb_x0 + PCB_L + FIT - 0.1, UFL_Y, pcb_top - 0.2))
base = base.union(stop).cut(notch)

# USB-C opening
usb_z = pcb_top + USB_Z_ABOVE_PCB
usb = (cq.Workplane("YZ").center(0, usb_z).rect(USB_W, USB_H)
       .extrude(WALL + 1).translate((-0.5, 0, 0)).edges("|X").fillet(1.0))
base = base.cut(usb)

if VENTS:
    for vy in FLOOR_VENTS_Y:
        L = FLOOR_VENT_X[1] - FLOOR_VENT_X[0]
        base = base.cut(cq.Workplane("XY").slot2D(L, VENT_W, 0).extrude(FLOOR + 0.2)
                        .translate((pcb_x0 + sum(FLOOR_VENT_X) / 2, vy, -0.1)))

# antenna recess in floor
ant_x0 = pcb_x0 + PCB_L + FIT + 1.2 + GAP
recess = cq.Workplane("XY").box(ANT_L, ANT_W, ANT_RECESS + 0.01, centered=(False, True, False)) \
    .translate((ant_x0, 0, FLOOR - ANT_RECESS))
base = base.cut(recess)

if WIRE_SLOT:
    slot = cq.Workplane("XY").box(WIRE_W, WALL + 1, WIRE_H, centered=(True, True, False)) \
        .translate((pcb_x0 + PCB_L - WIRE_W / 2 - 1, IN_W / 2 + WALL / 2, OUT_H - WIRE_H))
    base = base.cut(slot)

# pry notch in the antenna-end wall
base = base.cut(cq.Workplane("XY").box(WALL + 0.2, PRY_W, PRY_D + 0.1, centered=(False, True, False))
                .translate((OUT_L - WALL - 0.1, 0, OUT_H - PRY_D)))

if GRIP:
    z0, z1 = 1.0, OUT_H - 0.8
    x = GRIP_X[0]
    while x <= GRIP_X[1]:
        for s_ in (1, -1):
            y = s_ * OUT_W / 2
            tri = (cq.Workplane("XY").polyline([(x - GRIP_W / 2, y + s_ * 0.05), (x + GRIP_W / 2, y + s_ * 0.05),
                                                 (x, y - s_ * GRIP_DEPTH)]).close()
                   .extrude(z1 - z0).translate((0, 0, z0)))
            base = base.cut(tri)
        x += GRIP_PITCH

# snap grooves in inner wall faces
for sx in SNAP_X:
    for s_ in (1, -1):
        g = (cq.Workplane("YZ").circle(SNAP_R + 0.1).extrude(SNAP_LEN + 0.6)
             .translate((sx - (SNAP_LEN + 0.6) / 2, s_ * (IN_W / 2 - LIP_CLR), OUT_H - SNAP_Z)))
        base = base.cut(g)

# ---------------- lid ----------------
lid = (cq.Workplane("XY")
       .box(OUT_L, OUT_W, LID_T, centered=(False, True, False))
       .edges("|Z").fillet(CORNER_R))
lip_o = cq.Workplane("XY").box(IN_L - 2 * LIP_CLR, IN_W - 2 * LIP_CLR, LIP_H,
                               centered=(False, True, False)).translate((WALL + LIP_CLR, 0, -LIP_H))
lip_i = cq.Workplane("XY").box(IN_L - 2 * LIP_CLR - 2 * LIP_T, IN_W - 2 * LIP_CLR - 2 * LIP_T, LIP_H,
                               centered=(False, True, False)).translate((WALL + LIP_CLR + LIP_T, 0, -LIP_H))
lid = lid.union(lip_o.cut(lip_i))
# clear the lip where the USB opening is
lid = lid.cut(cq.Workplane("XY").box(LIP_T + LIP_CLR + 0.2, USB_W + 1, LIP_H + 0.1,
                                     centered=(False, True, False)).translate((WALL, 0, -LIP_H - 0.05)))

# remove the lip at the board end so it can't stiffen the flexures
lid = lid.cut(cq.Workplane("XY").box(BTN_X + FLEX_L + 2.0, IN_W + 1, LIP_H + 0.1,
                                     centered=(False, True, False)).translate((WALL - 0.1, 0, -LIP_H - 0.05)))

# flexure buttons: U-slot around a tab hinged toward the antenna end, plunger underneath
lid_under_z = OUT_H                      # lid underside sits on top of walls
btn_top_z = pcb_top + BTN_TOP
nub_len = (lid_under_z - btn_top_z) - NUB_GAP
for s in (1, -1):
    cx, cy = pcb_x0 + BTN_X, s * BTN_Y
    # tab spans from (cx - FLEX_W/2 .. ) along X, hinge at +X end
    x0 = cx - FLEX_SLOT - 1.0
    outer = cq.Workplane("XY").box(FLEX_L + FLEX_SLOT, FLEX_W + 2 * FLEX_SLOT, LID_T + 0.2,
                                   centered=(False, True, False)).translate((x0 - FLEX_SLOT, cy, -0.1))
    inner = cq.Workplane("XY").box(FLEX_L + FLEX_SLOT + 0.01, FLEX_W, LID_T + 0.4,
                                   centered=(False, True, False)).translate((x0, cy, -0.2))
    lid = lid.cut(outer.cut(inner))
    # thin the hinge for flex (cut from the UNDERSIDE so the top face stays flat for face-down printing)
    lid = lid.cut(cq.Workplane("XY").box(1.2, FLEX_W, 0.8, centered=(False, True, False))
                  .translate((x0 + FLEX_L - 1.2, cy, -0.01)))
    nub = cq.Workplane("XY").circle(NUB_D / 2).extrude(nub_len + 0.5).translate((cx, cy, -nub_len))
    lid = lid.union(nub)

if VENTS:
    for vy in LID_VENTS_Y:
        L = LID_VENT_X[1] - LID_VENT_X[0]
        lid = lid.cut(cq.Workplane("XY").slot2D(L, VENT_W, 0).extrude(LID_T + 0.2)
                      .translate((pcb_x0 + sum(LID_VENT_X) / 2, vy, -0.1)))

# snap ridges on lip outer faces
for sx in SNAP_X:
    for s_ in (1, -1):
        r = (cq.Workplane("YZ").circle(SNAP_R).extrude(SNAP_LEN)
             .translate((sx - SNAP_LEN / 2, s_ * (IN_W / 2 - LIP_CLR), -SNAP_Z)))
        lid = lid.union(r)
# board hold-down ribs on PCB long edges (behind the flexures)
hold_len = OUT_H - (pcb_top + HOLD_GAP)
for s_ in (1, -1):
    lid = lid.union(cq.Workplane("XY").box(HOLD_X[1] - HOLD_X[0], 0.8, hold_len + 0.3, centered=(False, True, False))
                    .translate((pcb_x0 + HOLD_X[0], s_ * HOLD_Y, -hold_len)))
# u.FL retainer pad
ufl_len = OUT_H - (pcb_top + UFL_PLUG_TOP + UFL_GAP)
lid = lid.union(cq.Workplane("XY").box(2.2, 2.2, ufl_len + 0.3).translate((pcb_x0 + UFL_X, UFL_Y, -(ufl_len) / 2 + 0.15)))

# LED light pipes: solid columns, part of the lid (paint white in the slicer).
# They hang from the B/R flexure tabs; extra gap so a press can't touch the LED.
pipe_bot = (pcb_top + LED_TOP + PIPE_GAP) - OUT_H        # lid coords (lid underside = 0)
for side in LED_SIDES:
    led_cx, led_cy = pcb_x0 + LED_X, side * LED_Y
    lid = lid.union(cq.Workplane("XY").circle(PIPE_D / 2).extrude(-pipe_bot + 0.5)
                    .translate((led_cx, led_cy, pipe_bot)))
    if PIPE_RECESS > 0:
        lid = lid.cut(cq.Workplane("XY").circle(PIPE_D / 2).extrude(PIPE_RECESS + 0.1)
                      .translate((led_cx, led_cy, LID_T - PIPE_RECESS)))

# lid is modelled in its installed position; also export flipped for printing
lid_installed = lid.translate((0, 0, OUT_H))

if __name__ == "__main__":
    import os
    out = os.path.dirname(os.path.abspath(__file__))
    cq.exporters.export(base, f"{out}/xiao_s3_case_base.step")
    cq.exporters.export(lid_installed, f"{out}/xiao_s3_case_lid.step")
    cq.exporters.export(base, f"{out}/xiao_s3_case_base.stl")
    flip = lambda w: w.rotate((0, 0, 0), (1, 0, 0), 180).translate((0, 0, LID_T))
    cq.exporters.export(flip(lid), f"{out}/xiao_s3_case_lid_print.stl")

    cq.Assembly().add(base, name="base").add(lid_installed, name="lid").save(f"{out}/xiao_s3_case_assembly.step")
    # fit-test coupon: board end only
    cut = cq.Workplane("XY").box(30, 60, 60, centered=(False, True, True))
    cq.exporters.export(base.intersect(cut), f"{out}/fittest_base.stl")
    cq.exporters.export(flip(lid.intersect(cut.translate((0, 0, 0)))), f"{out}/fittest_lid_print.stl")
    asm = cq.Assembly().add(base, name="base").add(lid_installed, name="lid")
    board_step = os.environ.get("XIAO_STEP")
    if board_step:
        b = cq.importers.importStep(board_step)
        # Seeed STEP axes: X along board (USB at +X, edge 12.28), Y up (PCB 0..1), Z across (centre -6.11)
        b = b.rotate((0, 0, 0), (1, 0, 0), 90).rotate((0, 0, 0), (0, 0, 1), 180)
        b = b.translate((pcb_x0 + 12.28, 6.11, pcb_z))
        asm.add(b, name="xiao_esp32s3", color=cq.Color(0.1, 0.4, 0.15))
        globals()["board_placed"] = b
    asm.save(f"{out}/PRIVATE_assembly_with_seeed_board.step")
    print(f"Outer: {OUT_L:.1f} x {OUT_W:.1f} x {OUT_H + LID_T:.1f} mm, nub length {nub_len:.2f}")
