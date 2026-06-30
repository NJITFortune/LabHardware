#! /home/eric/PyEnvs/ThorCam/bin/python3
"""
fishTracker.py — Track the head of a fish in a long thin refuge.

Interactive setup (first run)
------------------------------
A single window collects 4 clicks on the first frame:
  1 & 2  Two opposite corners of the fish zone (excludes black end caps).
  3      Fish HEAD (fat / blunt end).
  4      Fish TAIL (thin / pointed end).

The head and tail clicks serve two purposes:
  • Threshold  — patch intensity at both points is the fish baseline; scanning
                 outward in 4 directions from each seed locates the
                 fish→background boundary.  Threshold = midpoint.
  • Orientation — head position in frame 0 initialises a proximity tracker.
                  Each frame, the fish end nearest the previous head position
                  is called the head.  This survives the fish turning around.

Pass --roi / --head / --tail on subsequent runs to skip the window.

Outputs
-------
  fish_track.csv   frame, head_x, head_y, tail_x, tail_y,
                   centroid_x, centroid_y, angle_deg, area_px2
  annotated video  (optional --output-video)
    cyan rect  = fish zone
    green      = fish outline
    red dot    = head
    blue dot   = tail
    cyan arrow = tail → head
"""

import cv2
import numpy as np
import argparse
import csv
import os
from pathlib import Path


# ── background model ──────────────────────────────────────────────────────────

def build_background(source, total, n_samples=150):
    """Per-pixel maximum across n_samples frames.

    The fish occupies any given pixel only some of the time, so the maximum
    over enough frames recovers the unoccluded background for every pixel.
    Returns a uint8 grayscale image the same size as the source frames.
    """
    step = max(1, total // n_samples)
    if isinstance(source, list):          # TIFF / PNG directory
        bg = cv2.imread(str(source[0]), cv2.IMREAD_GRAYSCALE).astype(np.uint16)
        for i in range(0, total, step):
            g = cv2.imread(str(source[i]), cv2.IMREAD_GRAYSCALE)
            if g is None:
                continue
            np.maximum(bg, g, out=bg)
    else:                                 # VideoCapture
        source.set(cv2.CAP_PROP_POS_FRAMES, 0)
        _, f0 = source.read()
        bg = cv2.cvtColor(f0, cv2.COLOR_BGR2GRAY).astype(np.uint16)
        for i in range(0, total, step):
            source.set(cv2.CAP_PROP_POS_FRAMES, i)
            ret, f = source.read()
            if not ret:
                continue
            g = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY).astype(np.uint16)
            np.maximum(bg, g, out=bg)
        source.set(cv2.CAP_PROP_POS_FRAMES, 0)
    return bg.astype(np.uint8)


def estimate_threshold_bg(diff_roi, head_roi_pt, tail_roi_pt, patch=8):
    """Threshold on the background-difference image.

    diff_roi = (background − frame).clip(0) in the fish zone.
    Fish pixels are bright (large diff); background pixels are ~0.

    Uses 10 % of the peak fish-diff value as the threshold, floored at 8.
    This is low enough to capture even the faint tail while staying above
    the noise floor (background diff ≈ 0–5).
    Returns (threshold_int, fish_diff_val).
    """
    roi_h, roi_w = diff_roi.shape

    def pm(cx, cy):
        p = patch
        x1, x2 = max(0, cx - p // 2), min(roi_w, cx + p // 2 + 1)
        y1, y2 = max(0, cy - p // 2), min(roi_h, cy + p // 2 + 1)
        sub = diff_roi[y1:y2, x1:x2]
        return float(sub.mean()) if sub.size else float(diff_roi[cy, cx])

    head_diff = pm(head_roi_pt[0], head_roi_pt[1])
    tail_diff  = pm(tail_roi_pt[0], tail_roi_pt[1])
    fish_diff  = max(head_diff, tail_diff)   # higher = more reliable fish pixel

    threshold = max(8, int(round(fish_diff * 0.10)))
    return threshold, fish_diff


# ── interactive setup ─────────────────────────────────────────────────────────

def select_fish_points(frame, scale=3.0):
    """
    Show frame at `scale`× and collect 4 clicks:
      clicks 0,1 → zone corners
      click  2   → head
      click  3   → tail
    Returns (x_min, y_min, x_max, y_max, head_pt, tail_pt)
    in full-frame pixel coordinates.
    Controls: left-click to place, R to restart all clicks, Enter/Space to confirm.
    """
    h, w = frame.shape[:2]
    dw, dh = int(w * scale), int(h * scale)
    base = cv2.resize(frame, (dw, dh), interpolation=cv2.INTER_LINEAR)

    PROMPTS = [
        "1/4  Click CORNER 1 of the fish zone",
        "2/4  Click CORNER 2 of the fish zone  (opposite corner)",
        "3/4  Click the FISH HEAD  (fat / blunt end)",
        "4/4  Click the FISH TAIL  (thin / pointed end)",
        "Confirm: Enter or Space     Redo all: R",
    ]
    # colours per click: corner1, corner2, head, tail
    COLORS = [(200, 120, 0), (200, 120, 0), (0, 0, 220), (30, 180, 0)]

    clicks = []   # list of (orig_x, orig_y)

    def on_mouse(event, mx, my, _flags, _param):
        if event == cv2.EVENT_LBUTTONDOWN and len(clicks) < 4:
            clicks.append((int(mx / scale + 0.5), int(my / scale + 0.5)))

    win = "Fish tracker setup"
    cv2.namedWindow(win, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(win, dw, dh)
    cv2.setMouseCallback(win, on_mouse)

    font  = cv2.FONT_HERSHEY_SIMPLEX
    fs    = max(0.45, scale / 5.5)
    thick = max(1, int(scale / 2))
    mk_sz = int(22 * scale / 3)

    while True:
        img  = base.copy()
        step = min(len(clicks), 4)
        cv2.putText(img, PROMPTS[step], (10, dh - 10),
                    font, fs, (0, 230, 230), thick, cv2.LINE_AA)

        for idx, (ox, oy) in enumerate(clicks):
            sx, sy = int(ox * scale), int(oy * scale)
            col = COLORS[idx]
            if idx < 2:                           # zone corners → crosshair
                cv2.drawMarker(img, (sx, sy), col,
                               cv2.MARKER_CROSS, mk_sz, thick + 1)
            elif idx == 2:                        # head → filled circle + H
                cv2.circle(img, (sx, sy), mk_sz // 2, col, -1)
                cv2.putText(img, "H", (sx + mk_sz // 2 + 2, sy + mk_sz // 4),
                            font, fs * 0.9, (255, 255, 255), thick)
            else:                                 # tail → filled circle + T
                cv2.circle(img, (sx, sy), mk_sz // 2, col, -1)
                cv2.putText(img, "T", (sx + mk_sz // 2 + 2, sy + mk_sz // 4),
                            font, fs * 0.9, (255, 255, 255), thick)

        # zone rectangle after 2 clicks
        if len(clicks) >= 2:
            p1 = (int(clicks[0][0] * scale), int(clicks[0][1] * scale))
            p2 = (int(clicks[1][0] * scale), int(clicks[1][1] * scale))
            cv2.rectangle(img, p1, p2, COLORS[0], thick)

        # tail→head arrow after 4 clicks
        if len(clicks) == 4:
            hp = (int(clicks[2][0] * scale), int(clicks[2][1] * scale))
            tp = (int(clicks[3][0] * scale), int(clicks[3][1] * scale))
            cv2.arrowedLine(img, tp, hp, (0, 200, 200), thick + 1,
                            tipLength=0.06)

        cv2.imshow(win, img)
        key = cv2.waitKey(30) & 0xFF
        if key in (13, 32) and len(clicks) == 4:   # Enter / Space → confirm
            break
        if key in (ord('r'), ord('R')):             # R → redo all
            clicks.clear()

    cv2.destroyWindow(win)

    x_min = min(clicks[0][0], clicks[1][0])
    x_max = max(clicks[0][0], clicks[1][0])
    y_min = min(clicks[0][1], clicks[1][1])
    y_max = max(clicks[0][1], clicks[1][1])
    return x_min, y_min, x_max, y_max, clicks[2], clicks[3]


# ── threshold estimation from clicked fish pixels ─────────────────────────────

def estimate_threshold(gray_full, x_min, y_min, x_max, y_max,
                       head_pt, tail_pt, patch=8):
    """
    Derive an intensity threshold from the user-clicked fish points.

    1. Sample a small patch at each click → fish baseline per point.
    2. Use the DARKER of the two as the scan seed (most reliably on fish body).
    3. Scan outward from that seed in 4 cardinal directions until intensity
       jumps well above the fish baseline → fish/background boundary samples.
       (Requiring a large jump avoids stopping at wall-transition pixels.)
    4. bg_val = median of boundary samples; fall back to the 85th-percentile
       of all ROI pixels if fewer than 2 boundary samples are found (the
       background dominates the zone area so the high percentile is reliable).
    5. threshold = midpoint(fish_val, bg_val).

    Returns (threshold_int, fish_val, bg_val).
    """
    roi = gray_full[y_min:y_max, x_min:x_max].astype(np.float32)
    roi_h, roi_w = roi.shape

    def to_roi(pt):
        return pt[0] - x_min, pt[1] - y_min

    def patch_mean(cx, cy):
        p = patch
        x1, x2 = max(0, cx - p // 2), min(roi_w, cx + p // 2 + 1)
        y1, y2 = max(0, cy - p // 2), min(roi_h, cy + p // 2 + 1)
        sub = roi[y1:y2, x1:x2]
        return float(sub.mean()) if sub.size else float(roi[cy, cx])

    hx, hy = to_roi(head_pt)
    tx, ty = to_roi(tail_pt)
    head_fish = patch_mean(hx, hy)
    tail_fish  = patch_mean(tx, ty)

    # Scan from whichever click is darker — that one is more reliably on fish
    if head_fish <= tail_fish:
        seed_x, seed_y, fish_val = hx, hy, head_fish
    else:
        seed_x, seed_y, fish_val = tx, ty, tail_fish

    # Require a large intensity jump so wall-transition pixels are not mistaken
    # for background.  jump = at least 50 counts, or 70 % of the fish value.
    jump = max(50, fish_val * 0.70)
    rise = fish_val + jump

    bg_samples = []
    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        x, y = float(seed_x), float(seed_y)
        for _ in range(max(roi_w, roi_h)):
            x += dx;  y += dy
            xi, yi = int(x), int(y)
            if not (0 <= xi < roi_w and 0 <= yi < roi_h):
                break
            if float(roi[yi, xi]) > rise:
                bg_samples.append(float(roi[yi, xi]))
                break

    # 75th-pct of the ROI (clipped at 240 to avoid fully-saturated highlights
    # inflating the estimate).  Fish occupies << 50 % of the zone area, so
    # the 75th-pct lands solidly in the bright interior background.
    roi_clipped    = np.clip(roi, 0, 240)
    bg_percentile  = float(np.percentile(roi_clipped, 75))

    # Take the higher of the directional scan and the area percentile so that
    # wall-transition pixels (darker than true background) don't drag bg_val down.
    bg_scan = float(np.median(bg_samples)) if len(bg_samples) >= 2 else 0.0
    bg_val  = max(bg_scan, bg_percentile, fish_val + 60)
    bg_val  = min(bg_val, 230)   # never let a saturated zone pull threshold too high

    # Place the threshold 50 % of the way from fish to background.
    # This captures the full fish body without pulling in much background.
    threshold = int(round(fish_val + (bg_val - fish_val) * 0.50))
    return threshold, fish_val, bg_val


# ── per-frame detection ───────────────────────────────────────────────────────

def process_frame(gray_full, x_min, y_min, x_max, y_max,
                  threshold, min_area, prev_head, bg_gray=None):
    """
    Detect the fish inside the crop [y_min:y_max, x_min:x_max].

    When bg_gray is provided, thresholding is done on the background-difference
    image (bg − frame, clipped to 0–255) so that fish pixels are bright and
    background is near-zero.  This mode is insensitive to absolute grey level
    and works for both dark and translucent fish.

    Without bg_gray, the raw frame is thresholded (inverted) as before.

    Head/tail orientation is resolved by proximity to prev_head (a (x,y)
    tuple in full-frame coords) — whichever fish end is nearer is the head.

    Returns a dict with full-frame coordinates, or None if no fish found.
    Keys: head_x, head_y, tail_x, tail_y, centroid_x, centroid_y,
          angle_deg, area, contour (ROI-space).
    """
    roi = gray_full[y_min:y_max, x_min:x_max]

    if bg_gray is not None:
        bg_roi = bg_gray[y_min:y_max, x_min:x_max]
        work   = cv2.subtract(bg_roi, roi)          # fish → bright; bg → ~0
        _, binary = cv2.threshold(work, threshold, 255, cv2.THRESH_BINARY)
    else:
        _, binary = cv2.threshold(roi, threshold, 255, cv2.THRESH_BINARY_INV)

    close_k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
    open_k  = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    binary  = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, close_k)
    binary  = cv2.morphologyEx(binary, cv2.MORPH_OPEN,  open_k)

    contours, _ = cv2.findContours(
        binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    candidates = [(cv2.contourArea(c), c)
                  for c in contours if cv2.contourArea(c) >= min_area]
    if not candidates:
        return None

    # Select the blob whose contour is nearest to prev_head (ROI coords).
    # This keeps us on the fish even when a larger dark blob (e.g. an end-cap
    # fixture inside the zone) competes for largest-area honours.
    ph_roi = (float(prev_head[0] - x_min), float(prev_head[1] - y_min))
    def dist_to_contour(c):
        # pointPolygonTest returns +dist if inside, -dist if outside
        return -cv2.pointPolygonTest(c, ph_roi, measureDist=True)
    area, fish_c = min(candidates, key=lambda t: dist_to_contour(t[1]))

    roi_h, roi_w = roi.shape
    fish_mask = np.zeros((roi_h, roi_w), np.uint8)
    cv2.drawContours(fish_mask, [fish_c], -1, 255, cv2.FILLED)

    bx, by, bw, bh = cv2.boundingRect(fish_c)

    # ── centroid of each end (innermost 25 % of the bounding box) ────────────
    n25 = max(1, bw // 4)

    def end_centroid(col_start, col_end):
        sub = fish_mask[:, col_start:col_end]
        ys, xs = np.where(sub > 0)
        if len(xs) == 0:
            return None
        return (int(round(float(xs.mean()))) + col_start + x_min,
                int(round(float(ys.mean()))) + y_min)

    right_pos = end_centroid(bx + bw - n25, bx + bw)
    left_pos  = end_centroid(bx,            bx + n25)
    if right_pos is None or left_pos is None:
        return None

    # ── head = end closer to prev_head ────────────────────────────────────────
    def dist2(a, b):
        return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2

    if dist2(right_pos, prev_head) <= dist2(left_pos, prev_head):
        head_pos, tail_pos = right_pos, left_pos
    else:
        head_pos, tail_pos = left_pos, right_pos

    # ── body centroid ─────────────────────────────────────────────────────────
    M = cv2.moments(fish_c)
    if M["m00"] == 0:
        return None
    cx = int(round(M["m10"] / M["m00"])) + x_min
    cy = int(round(M["m01"] / M["m00"])) + y_min

    # ── body angle via PCA ────────────────────────────────────────────────────
    ys_all, xs_all = np.where(fish_mask > 0)
    if len(xs_all) > 1:
        pts = np.column_stack([xs_all, ys_all]).astype(np.float32)
        _, eigvec = cv2.PCACompute(pts, mean=None)
        angle_deg = float(np.degrees(np.arctan2(eigvec[0, 1], eigvec[0, 0])))
    else:
        angle_deg = float("nan")

    return dict(head_x=head_pos[0], head_y=head_pos[1],
                tail_x=tail_pos[0], tail_y=tail_pos[1],
                centroid_x=cx,      centroid_y=cy,
                angle_deg=angle_deg, area=area,
                contour=fish_c)


# ── argument helpers ──────────────────────────────────────────────────────────

def parse_xy(s, name):
    try:
        vals = [int(v) for v in s.split(",")]
        if len(vals) != 2:
            raise ValueError
        return tuple(vals)
    except ValueError:
        raise argparse.ArgumentTypeError(f"--{name} requires x,y")


def parse_roi(s):
    try:
        vals = [int(v) for v in s.split(",")]
        if len(vals) != 4:
            raise ValueError
        return vals
    except ValueError:
        raise argparse.ArgumentTypeError("--roi requires x1,y1,x2,y2")


# ── main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Track fish head in a long thin refuge.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "First run — omit --roi/--head/--tail to click interactively.\n"
            "The script prints reuse coordinates so subsequent runs can skip\n"
            "the selection window.\n\n"
            "Example:\n"
            "  ./fishTracker.py Eigen25jun26-j --output-video out.mp4\n"
            "  ./fishTracker.py Eigen25jun26-j \\\n"
            "      --roi 72,27,1207,145 --head 1115,84 --tail 570,82 \\\n"
            "      --output-video out.mp4"
        ))
    parser.add_argument("input", nargs="?", default="output.mp4",
                        help="MP4 file or directory of TIFFs (default: output.mp4)")
    parser.add_argument("-o", "--output-csv", default="fish_track.csv")
    parser.add_argument("--output-video", default=None, metavar="PATH")
    parser.add_argument("--roi",  type=parse_roi, default=None,
                        metavar="x1,y1,x2,y2",
                        help="Fish zone corners (skips interactive selection)")
    parser.add_argument("--head", type=lambda s: parse_xy(s, "head"),
                        default=None, metavar="x,y",
                        help="Head click in full-frame pixels")
    parser.add_argument("--tail", type=lambda s: parse_xy(s, "tail"),
                        default=None, metavar="x,y",
                        help="Tail click in full-frame pixels")
    parser.add_argument("--scale", type=float, default=3.0,
                        help="Display zoom for selection window (default: 3.0)")
    parser.add_argument("--threshold", type=int, default=None,
                        help="Override auto-computed threshold.  In background "
                             "mode this is the minimum diff value (fish darker "
                             "than background); in raw mode it is the intensity "
                             "below which a pixel is considered fish.")
    parser.add_argument("--gamma", type=float, default=1.0,
                        help="Gamma applied before thresholding (default: 1.0). "
                             "Only relevant in raw (no-background) mode; has "
                             "little effect when background subtraction is used.")
    parser.add_argument("--background", default=None, metavar="PATH",
                        help="Path to a pre-computed background image (grayscale). "
                             "If omitted, the background is built automatically "
                             "from the source and saved next to the output CSV.")
    parser.add_argument("--no-background", action="store_true",
                        help="Disable background subtraction and use raw intensity "
                             "thresholding (the original mode).")
    parser.add_argument("--min-area", type=int, default=None,
                        help="Min fish blob area in px² "
                             "(default: 1000 in background mode, 3000 in raw mode)")
    args = parser.parse_args()

    # ── open source ───────────────────────────────────────────────────────────
    use_files = os.path.isdir(args.input)
    if use_files:
        files = (sorted(Path(args.input).glob("*.tiff")) +
                 sorted(Path(args.input).glob("*.tif")))
        if not files:
            files = sorted(Path(args.input).glob("*.png"))
        total, src_fps = len(files), 60.0
    else:
        cap     = cv2.VideoCapture(args.input)
        total   = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        src_fps = cap.get(cv2.CAP_PROP_FPS) or 60.0

    # first frame for setup
    if use_files:
        first = cv2.imread(str(files[0]))
    else:
        ret, first = cap.read()
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        if not ret:
            raise RuntimeError("Cannot read first frame.")

    frame_h, frame_w = first.shape[:2]
    gray0 = cv2.cvtColor(first, cv2.COLOR_BGR2GRAY)

    # Gamma LUT (only meaningful in raw/no-background mode)
    if args.gamma != 1.0:
        gamma_lut = np.array(
            [min(255, int(round((i / 255.0) ** args.gamma * 255)))
             for i in range(256)], dtype=np.uint8)
        gray0 = cv2.LUT(gray0, gamma_lut)
    else:
        gamma_lut = None

    # ── background model ──────────────────────────────────────────────────────
    use_bg = not args.no_background
    bg_gray = None
    bg_path = None

    if use_bg:
        if args.background:
            bg_gray = cv2.imread(args.background, cv2.IMREAD_GRAYSCALE)
            if bg_gray is None:
                raise RuntimeError(f"Cannot read background image: {args.background}")
            bg_path = args.background
            print(f"Background   : loaded from {bg_path}")
        else:
            print("Building background model (per-pixel max across sampled frames)…")
            bg_gray = build_background(files if use_files else cap, total)
            # reset VideoCapture position after background scan
            if not use_files:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            bg_path = args.output_csv.replace(".csv", "_bg.png")
            cv2.imwrite(bg_path, bg_gray)
            print(f"             saved → {bg_path}")
        if gamma_lut is not None:
            bg_gray = cv2.LUT(bg_gray, gamma_lut)

    # ── define fish zone + orientation ────────────────────────────────────────
    have_all = args.roi and args.head and args.tail
    if have_all:
        raw = args.roi
        x_min = min(raw[0], raw[2]);  x_max = max(raw[0], raw[2])
        y_min = min(raw[1], raw[3]);  y_max = max(raw[1], raw[3])
        head_pt, tail_pt = args.head, args.tail
    else:
        print("Opening setup window — 4 clicks needed.")
        print("  Clicks 1+2 : opposite corners of the fish zone")
        print("  Click  3   : fish HEAD (fat/blunt end)")
        print("  Click  4   : fish TAIL (thin/pointed end)")
        x_min, y_min, x_max, y_max, head_pt, tail_pt = \
            select_fish_points(first, scale=args.scale)

    # ── min-area default depends on detection mode ────────────────────────────
    min_area = args.min_area if args.min_area is not None \
               else (1000 if use_bg else 3000)

    # ── compute threshold from clicked fish pixels ────────────────────────────
    fish_diff = fish_val = bg_val = None
    if args.threshold is not None:
        threshold = args.threshold
    elif use_bg and bg_gray is not None:
        hx, hy = head_pt[0] - x_min, head_pt[1] - y_min
        tx, ty = tail_pt[0] - x_min, tail_pt[1] - y_min
        diff0 = cv2.subtract(bg_gray[y_min:y_max, x_min:x_max],
                             gray0[y_min:y_max, x_min:x_max]).astype(np.float32)
        threshold, fish_diff = estimate_threshold_bg(diff0, (hx, hy), (tx, ty))
    else:
        threshold, fish_val, bg_val = estimate_threshold(
            gray0, x_min, y_min, x_max, y_max, head_pt, tail_pt)

    print(f"\nSource       : {args.input}  ({total} frames @ {src_fps:.0f} fps)")
    print(f"Fish zone    : ({x_min},{y_min}) → ({x_max},{y_max})  "
          f"[{x_max-x_min} × {y_max-y_min} px]")
    print(f"Head click   : {head_pt}   Tail click: {tail_pt}")
    if use_bg:
        print(f"Mode         : background subtraction")
        if fish_diff is not None:
            print(f"Fish diff    : {fish_diff:.1f}  (at clicked points vs background)")
    else:
        print(f"Mode         : raw intensity  gamma={args.gamma}")
        if fish_val is not None:
            print(f"Fish px val  : {fish_val:.1f}   Background: {bg_val:.1f}")
    print(f"Threshold    : {threshold}   min-area: {min_area} px²")
    reuse = (f"--roi {x_min},{y_min},{x_max},{y_max} "
             f"--head {head_pt[0]},{head_pt[1]} "
             f"--tail {tail_pt[0]},{tail_pt[1]}")
    if bg_path:
        reuse += f" --background {bg_path}"
    if args.no_background:
        reuse += " --no-background"
    if args.gamma != 1.0:
        reuse += f" --gamma {args.gamma}"
    print(f"Reuse        : {reuse}")

    # ── optional video writer ─────────────────────────────────────────────────
    vout = None
    if args.output_video:
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        vout   = cv2.VideoWriter(args.output_video, fourcc,
                                 src_fps, (frame_w, frame_h))

    # ── tracking loop ─────────────────────────────────────────────────────────
    rows      = []
    tracked   = 0
    prev_head = head_pt            # proximity seed from user click

    for i in range(total):
        if use_files:
            frame = cv2.imread(str(files[i]))
        else:
            ret, frame = cap.read()
            if not ret or frame is None:
                break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if gamma_lut is not None:
            gray = cv2.LUT(gray, gamma_lut)
        result = process_frame(gray, x_min, y_min, x_max, y_max,
                               threshold, min_area, prev_head, bg_gray=bg_gray)

        if result:
            tracked  += 1
            prev_head = (result["head_x"], result["head_y"])
            rows.append([i,
                         result["head_x"],     result["head_y"],
                         result["tail_x"],     result["tail_y"],
                         result["centroid_x"], result["centroid_y"],
                         round(result["angle_deg"], 2),
                         int(result["area"])])

            if vout is not None:
                vis = frame.copy()
                cv2.rectangle(vis, (x_min, y_min), (x_max, y_max),
                              (200, 200, 0), 1)
                c = result["contour"].copy()
                c[:, :, 0] += x_min;  c[:, :, 1] += y_min
                cv2.drawContours(vis, [c], -1, (0, 200, 0), 1)
                hp = (result["head_x"], result["head_y"])
                tp = (result["tail_x"], result["tail_y"])
                cv2.arrowedLine(vis, tp, hp, (200, 200, 0), 1, tipLength=0.06)
                cv2.circle(vis, tp, 5, (180, 80,  0), -1)   # tail  — orange
                cv2.circle(vis, hp, 8, (0,   0, 220), -1)   # head  — red
                vout.write(vis)
        else:
            rows.append([i] + [None] * 8)
            if vout is not None:
                vout.write(frame)

        if i % 100 == 0:
            tag = (f"head=({result['head_x']},{result['head_y']})"
                   if result else "NO FISH")
            print(f"  {i:4d}/{total}  {tag}")

    if not use_files:
        cap.release()
    if vout is not None:
        vout.release()

    # ── write CSV ─────────────────────────────────────────────────────────────
    with open(args.output_csv, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["frame", "head_x", "head_y", "tail_x", "tail_y",
                         "centroid_x", "centroid_y", "angle_deg", "area_px2"])
        writer.writerows(rows)

    print(f"\nTracked {tracked}/{total} frames  →  {args.output_csv}")
    if args.output_video:
        print(f"Annotated video → {args.output_video}")


if __name__ == "__main__":
    main()
