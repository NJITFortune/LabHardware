#!/usr/bin/env python3
"""
multiTrig.py — Multi-camera triggered capture for Thorlabs UI-3240CP (IDS uEye).
Cameras are opened independently and may receive simultaneous or asynchronous triggers.
Capture stops after a user-specified duration rather than a fixed frame count.
"""

from thorTrig import (UI3240CP, enumerate_cameras, parse_roi,
                      _writer_thread, _report_stats)
import argparse
import os
import sys
import time
import threading
from queue import Queue
from threading import Thread


# Per-frame poll interval: short enough to respond quickly to stop_event,
# long enough not to burn CPU if no triggers are arriving.
_POLL_MS = 500


def _capture_loop(cam, cam_idx, stop_event, write_q, out_dir, fmt):
    """
    Capture triggered frames until stop_event is set.
    Returns (hw_ts_list, frame_num_list).
    """
    hw_ts      = []
    frame_nums = []
    count      = 0

    while not stop_event.is_set():
        try:
            frame, ts, fnum = cam.capture(timeout_ms=_POLL_MS)
        except TimeoutError:
            continue  # no trigger in this poll window — check stop_event and retry

        hw_ts.append(ts)
        frame_nums.append(fnum)
        path = os.path.join(out_dir, f"frame_{count:04d}.{fmt}")
        write_q.put((path, frame))
        count += 1
        print(f"  Cam {cam_idx}  frame {count:4d}")

    return hw_ts, frame_nums


def main():
    parser = argparse.ArgumentParser(
        description="Multi-camera triggered capture from IDS uEye cameras.")
    parser.add_argument("--cam-id", type=int, nargs="+", default=[0],
                        metavar="N",
                        help="Camera indices from --list-cameras, e.g. --cam-id 0 1")
    parser.add_argument("-d", "--duration", type=float, required=True,
                        help="Capture duration in seconds")
    parser.add_argument("-o", "--output-dir", default=".",
                        help="Root output directory; one sub-dir is created per camera "
                             "(default: current dir)")
    parser.add_argument("--roi", type=parse_roi, default=None, metavar="x,y,w,h",
                        help="ROI applied to all cameras")
    parser.add_argument("--color", action="store_true",
                        help="Capture in BGR color (default: mono8 for max speed)")
    parser.add_argument("--edge", choices=["rising", "falling"], default="rising",
                        help="Trigger edge (default: rising)")
    parser.add_argument("--exposure", type=float, default=None,
                        help="Exposure in ms (default: SDK default ~5 ms)")
    parser.add_argument("--gain", type=int, default=0,
                        help="Master hardware gain 0-100 (default: 0)")
    parser.add_argument("--fps", type=float, default=None,
                        help="Internal framerate limit (default: hardware max). "
                             "Lower values allow longer exposures.")
    parser.add_argument("--buffers", type=int, default=32,
                        help="Ring buffer count per camera (default: 32)")
    parser.add_argument("--format", choices=["tiff", "png", "bmp"], default="tiff",
                        help="Output image format (default: tiff)")
    parser.add_argument("--list-cameras", action="store_true",
                        help="Print detected cameras and exit")
    args = parser.parse_args()

    if args.list_cameras:
        enumerate_cameras()
        sys.exit(0)

    # --- Open cameras ---
    cams     = []
    out_dirs = []
    for idx in args.cam_id:
        out_dir = os.path.join(args.output_dir, f"cam{idx}")
        os.makedirs(out_dir, exist_ok=True)
        out_dirs.append(out_dir)

        try:
            cam = UI3240CP(cam_id=idx)
            cam.open(roi=args.roi, color=args.color, trigger_edge=args.edge,
                     num_buffers=args.buffers, fps=args.fps)
            cam.set_gain(args.gain)
            print(f"Master gain : {args.gain}")
            if args.exposure is not None:
                cam.set_exposure(args.exposure)
                print(f"Exposure    : {args.exposure} ms")
            cams.append(cam)
        except Exception as e:
            print(f"Failed to open camera {idx}: {e}")
            for c in cams:
                c.close()
            sys.exit(1)

    # --- Shared writer thread ---
    write_q = Queue()
    writer  = Thread(target=_writer_thread, args=(write_q,), daemon=True)
    writer.start()

    # --- Per-camera capture threads ---
    stop_event = threading.Event()
    results    = [([], [])] * len(cams)   # (hw_ts, frame_nums) per camera

    def capture_worker(i):
        try:
            results[i] = _capture_loop(
                cams[i], args.cam_id[i], stop_event,
                write_q, out_dirs[i], args.format)
        except Exception as e:
            print(f"\nCam {args.cam_id[i]} capture error: {e}")
            results[i] = ([], [])

    threads = [Thread(target=capture_worker, args=(i,), daemon=True)
               for i in range(len(cams))]

    print(f"\nCapturing for {args.duration:.1f} s — press Ctrl+C to stop early.\n")
    t_start = time.monotonic()
    for t in threads:
        t.start()

    try:
        deadline = t_start + args.duration
        while time.monotonic() < deadline:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nInterrupted.")
    finally:
        stop_event.set()
        for t in threads:
            t.join()

        print("\nWaiting for writes to complete…")
        write_q.put(None)
        writer.join()

        for cam in cams:
            cam.close()

        # --- Per-camera report ---
        elapsed = time.monotonic() - t_start
        print(f"\nTotal elapsed: {elapsed:.2f} s")
        for i, idx in enumerate(args.cam_id):
            hw_ts, frame_nums = results[i]
            n = len(hw_ts)
            print(f"\nCamera {idx} — {n} frame(s) saved to {out_dirs[i]}")
            if n >= 2:
                _report_stats(hw_ts, frame_nums)


if __name__ == "__main__":
    main()
