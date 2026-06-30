#! /home/eric/PyEnvs/ThorCam/bin/python3

### #!/usr/bin/env python3
"""
thorAuto.py — Thorlabs UI-3240CP internal-trigger (free-running) capture at
a user-specified framerate.
Requires: IDS uEye SDK (Linux/Windows/macOS) + pip install pyueye numpy opencv-python
"""

from pyueye import ueye
import numpy as np
import ctypes
import cv2
import argparse
import os
import sys
from queue import Queue
from threading import Thread


def check(ret, label=""):
    if ret != ueye.IS_SUCCESS:
        raise RuntimeError(f"uEye error {ret} [{label}]")


_INIT_ERROR_HINTS = {
    3:   "Cannot open device — unplug/replug camera then:\n"
         "  sudo systemctl restart ueyeusbdrc",
    9:   "Camera is already open in another process.\n"
         "  Close IDS uEye Cockpit (or any other IDS application) and retry.",
    212: "Camera paired to a stale daemon session (IS_DEVICE_ALREADY_PAIRED).\n"
         "  1. Close IDS uEye Cockpit completely.\n"
         "  2. sudo systemctl restart ueyeusbdrc\n"
         "  3. sudo ueyesetid\n"
         "  4. Re-run this script.",
}


def enumerate_cameras():
    """Print available cameras and return list of camera IDs."""
    n = ueye.INT(0)
    ueye.is_GetNumberOfCameras(n)
    count = int(n)
    if count == 0:
        print("No IDS uEye cameras detected.")
        return []

    class _CamList(ctypes.Structure):
        _fields_ = [("dwCount", ueye.ULONG),
                    ("uci",     ueye.UEYE_CAMERA_INFO * count)]

    cam_list = _CamList()
    cam_list.dwCount = count
    ueye.is_GetCameraList(cam_list)

    dev_ids = []
    print(f"Detected {count} camera(s):  (use [N] as --cam-id)")
    for i in range(count):
        info   = cam_list.uci[i]
        dev_id = int(info.dwDeviceID)
        dev_ids.append(dev_id)
        print(f"  [{i}] Serial={info.SerNo.decode()}  "
              f"Model={info.Model.decode()}  "
              f"dev_id={dev_id}  cam_id={int(info.dwCameraID)}  "
              f"Status={info.dwStatus}")
    return dev_ids


def _report_stats(hw_ts, frame_nums):
    """Print inter-frame interval statistics from camera hardware timestamps."""
    n = len(hw_ts)
    # u64TimestampDevice is in 100 ns units
    ts_ms = [t / 10_000.0 for t in hw_ts]
    intervals = [ts_ms[i+1] - ts_ms[i] for i in range(n - 1)]
    mean   = sum(intervals) / len(intervals)
    var    = sum((x - mean)**2 for x in intervals) / len(intervals)
    std    = var ** 0.5
    dropped = sum(frame_nums[i+1] - frame_nums[i] - 1 for i in range(n - 1))

    print(f"\n--- Capture statistics (camera hardware timestamps) ---")
    print(f"Frames captured  : {n}  |  Dropped frames: {dropped}")
    print(f"Mean frame period: {mean:.3f} ms  ({1000/mean:.2f} fps)")
    print(f"Jitter (1σ)      : ±{std:.3f} ms")
    print(f"Min / Max period : {min(intervals):.3f} / {max(intervals):.3f} ms")


def _writer_thread(q):
    while True:
        item = q.get()
        if item is None:
            break
        path, frame = item
        cv2.imwrite(path, frame)
        q.task_done()


class UI3240CP:
    def __init__(self, cam_id=0):
        self._cam_id = cam_id  # 0-based index into enumerated camera list
        self.hCam   = None
        self.width  = 0
        self.height = 0
        self.bpp    = 8
        self._bufs  = []  # (ptr, id) pairs for ring buffer

    def open(self, roi=None, color=False, num_buffers=8, fps=10.0):
        ids = enumerate_cameras()
        if not ids:
            raise RuntimeError(
                "No cameras found. Check USB connection and uEye daemon:\n"
                "  sudo systemctl status ueyeusbdrc")
        if self._cam_id >= len(ids):
            raise RuntimeError(
                f"--cam-id {self._cam_id} is out of range — "
                f"only {len(ids)} camera(s) detected (0–{len(ids)-1}).")
        dev_id = ids[self._cam_id]
        self.hCam = ueye.HIDS(dev_id | ueye.IS_USE_DEVICE_ID)
        ret = ueye.is_InitCamera(self.hCam, None)
        if ret != ueye.IS_SUCCESS:
            hint = _INIT_ERROR_HINTS.get(ret, "")
            msg  = f"is_InitCamera failed with error {ret} (dev_id={dev_id})."
            if hint:
                msg += f"\n{hint}"
            else:
                msg += f"\n  Available camera indices: {list(range(len(ids)))}"
            raise RuntimeError(msg)

        if color:
            self.bpp = 24
            check(ueye.is_SetColorMode(
                self.hCam, ueye.IS_CM_BGR8_PACKED), "SetColorMode color")
        else:
            self.bpp = 8
            check(ueye.is_SetColorMode(
                self.hCam, ueye.IS_CM_MONO8), "SetColorMode mono")

        # Maximize pixel clock
        clk_range = (ueye.UINT * 3)()
        check(ueye.is_PixelClock(
            self.hCam, ueye.IS_PIXELCLOCK_CMD_GET_RANGE,
            clk_range, 3 * ctypes.sizeof(ueye.UINT)), "PixelClock range")
        max_clk = ueye.UINT(clk_range[1].value)
        check(ueye.is_PixelClock(
            self.hCam, ueye.IS_PIXELCLOCK_CMD_SET,
            max_clk, ctypes.sizeof(ueye.UINT)), "PixelClock set")
        print(f"Pixel clock : {clk_range[1]} MHz")

        # Optional ROI
        if roi:
            rect = ueye.IS_RECT()
            rect.s32X      = roi[0]
            rect.s32Y      = roi[1]
            rect.s32Width  = roi[2]
            rect.s32Height = roi[3]
            check(ueye.is_AOI(
                self.hCam, ueye.IS_AOI_IMAGE_SET_AOI,
                rect, ctypes.sizeof(rect)), "AOI set")
            self.width, self.height = roi[2], roi[3]
        else:
            sinfo = ueye.SENSORINFO()
            check(ueye.is_GetSensorInfo(self.hCam, sinfo), "GetSensorInfo")
            self.width  = int(sinfo.nMaxWidth)
            self.height = int(sinfo.nMaxHeight)

        # Set the requested framerate
        actual_fps = ueye.double()
        check(ueye.is_SetFrameRate(
            self.hCam, ueye.double(fps), actual_fps), "SetFrameRate")
        print(f"Framerate   : {float(actual_fps):.1f} fps")

        # Query and report exposure range
        exp_min = ueye.double()
        exp_max = ueye.double()
        check(ueye.is_Exposure(
            self.hCam, ueye.IS_EXPOSURE_CMD_GET_EXPOSURE_RANGE_MIN,
            exp_min, ctypes.sizeof(ueye.double)), "Exposure get min")
        check(ueye.is_Exposure(
            self.hCam, ueye.IS_EXPOSURE_CMD_GET_EXPOSURE_RANGE_MAX,
            exp_max, ctypes.sizeof(ueye.double)), "Exposure get max")
        print(f"Exposure range: {float(exp_min):.4f} – {float(exp_max):.4f} ms "
              f"(use --exposure to set)")

        # Ring buffer
        self._bufs = []
        for _ in range(num_buffers):
            ptr = ueye.c_mem_p()
            mid = ueye.INT()
            check(ueye.is_AllocImageMem(
                self.hCam, self.width, self.height, self.bpp, ptr, mid),
                "AllocImageMem")
            check(ueye.is_AddToSequence(self.hCam, ptr, mid), "AddToSequence")
            self._bufs.append((ptr, mid))
        check(ueye.is_ImageQueue(
            self.hCam, ueye.IS_IMAGE_QUEUE_CMD_INIT, None, 0), "ImageQueue INIT")

        # Internal (free-running) trigger — camera generates frames at the set rate
        check(ueye.is_SetExternalTrigger(
            self.hCam, ueye.IS_SET_TRIGGER_OFF), "SetExternalTrigger OFF")

        # Arm the capture engine
        check(ueye.is_CaptureVideo(self.hCam, ueye.IS_DONT_WAIT), "CaptureVideo")

        print(f"Trigger     : internal (free-running)")
        print(f"Resolution  : {self.width}x{self.height} "
              f"({'color' if color else 'mono'})")
        print(f"Ring buffers: {num_buffers}")
        print("Ready — capturing.")

    def capture(self, timeout_ms=5000):
        """Return (image, hw_timestamp_100ns, frame_number) for the next frame.

        hw_timestamp is the camera's internal hardware counter in 100 ns units.
        Raises TimeoutError if no frame arrives within timeout_ms.
        """
        img_ptr = ueye.c_char_p()
        img_id  = ueye.c_int()
        wait_buf = ueye.IMAGEQUEUEWAITBUFFER()
        wait_buf.timeout = timeout_ms
        wait_buf.ppcMem  = ctypes.pointer(img_ptr)
        wait_buf.pnMemId = ctypes.pointer(img_id)
        ret = ueye.is_ImageQueue(
            self.hCam, ueye.IS_IMAGE_QUEUE_CMD_WAIT,
            wait_buf, ctypes.sizeof(ueye.IMAGEQUEUEWAITBUFFER))
        if ret == ueye.IS_TIMED_OUT:
            raise TimeoutError(f"No frame received within {timeout_ms} ms")
        if ret == ueye.IS_IMAGE_QUEUE_CMD_CANCEL_WAIT:
            ueye.is_ImageQueue(self.hCam, ueye.IS_IMAGE_QUEUE_CMD_FLUSH, None, 0)
            ueye.is_CaptureVideo(self.hCam, ueye.IS_DONT_WAIT)
            raise TimeoutError("image queue cancelled — flushed and re-armed")
        check(ret, "ImageQueue WAIT")

        img_info = ueye.UEYEIMAGEINFO()
        check(ueye.is_GetImageInfo(
            self.hCam, img_id.value, img_info,
            ctypes.sizeof(ueye.UEYEIMAGEINFO)), "GetImageInfo")

        shape = (self.height, self.width) if self.bpp == 8 \
                else (self.height, self.width, 3)
        img = np.empty(shape, dtype=np.uint8)
        check(ueye.is_CopyImageMem(
            self.hCam, img_ptr, img_id.value,
            img.ctypes.data_as(ctypes.POINTER(ctypes.c_char))), "CopyImageMem")
        check(ueye.is_UnlockSeqBuf(self.hCam, img_id.value, img_ptr), "UnlockSeqBuf")

        return img, int(img_info.u64TimestampDevice), int(img_info.u64FrameNumber)

    def set_gain(self, master=0):
        check(ueye.is_SetHardwareGain(
            self.hCam, master,
            ueye.IS_IGNORE_PARAMETER, ueye.IS_IGNORE_PARAMETER,
            ueye.IS_IGNORE_PARAMETER), "SetHardwareGain")

    def set_exposure(self, ms):
        exp = ueye.double(ms)
        check(ueye.is_Exposure(
            self.hCam, ueye.IS_EXPOSURE_CMD_SET_EXPOSURE,
            exp, ctypes.sizeof(ueye.double)), "Exposure set")
        actual = ueye.double()
        check(ueye.is_Exposure(
            self.hCam, ueye.IS_EXPOSURE_CMD_GET_EXPOSURE,
            actual, ctypes.sizeof(ueye.double)), "Exposure get")
        return float(actual)

    def close(self):
        ueye.is_StopLiveVideo(self.hCam, ueye.IS_WAIT)
        ueye.is_ImageQueue(self.hCam, ueye.IS_IMAGE_QUEUE_CMD_EXIT, None, 0)
        ueye.is_ClearSequence(self.hCam)
        for ptr, mid in self._bufs:
            ueye.is_FreeImageMem(self.hCam, ptr, mid)
        self._bufs = []
        ueye.is_ExitCamera(self.hCam)
        print("Camera closed.")


def parse_roi(s):
    try:
        x, y, w, h = map(int, s.split(","))
        return (x, y, w, h)
    except Exception:
        raise argparse.ArgumentTypeError(
            "ROI must be x,y,width,height (e.g. 0,0,640,512)")


def main():
    parser = argparse.ArgumentParser(
        description="Capture N frames from a Thorlabs UI-3240CP using the "
                    "internal (free-running) trigger at a specified FPS.")
    parser.add_argument("-n", "--num-frames", type=int, default=10,
                        help="Number of frames to capture (default: 10)")
    parser.add_argument("--fps", type=float, default=10.0,
                        help="Capture framerate in fps (default: 10.0)")
    parser.add_argument("-o", "--output-dir", default=".",
                        help="Directory to save frames (default: current dir)")
    parser.add_argument("--cam-id", type=int, default=0,
                        help="Camera ID (default: 0)")
    parser.add_argument("--roi", type=parse_roi, default=None,
                        metavar="x,y,w,h",
                        help="Region of interest")
    parser.add_argument("--color", action="store_true",
                        help="Capture in BGR color (default: mono8)")
    parser.add_argument("--exposure", type=float, default=None,
                        help="Exposure in ms (default: SDK default)")
    parser.add_argument("--gain", type=int, default=0,
                        help="Master hardware gain 0-100 (default: 0)")
    parser.add_argument("--buffers", type=int, default=8,
                        help="Ring buffer count (default: 8)")
    parser.add_argument("--format", choices=["tiff", "png", "bmp"], default="tiff",
                        help="Output image format (default: tiff)")
    parser.add_argument("--list-cameras", action="store_true",
                        help="Print detected cameras and exit")
    args = parser.parse_args()

    if args.list_cameras:
        enumerate_cameras()
        sys.exit(0)

    # Allow 3 missed frames worth of time before declaring a stall
    timeout_ms = max(5000, int(3000.0 / args.fps))

    os.makedirs(args.output_dir, exist_ok=True)

    # In free-running mode fps directly controls both frame rate AND the
    # exposure ceiling.  Warn if the requested exposure exceeds one frame period.
    if args.exposure is not None and args.exposure >= 1000.0 / args.fps:
        print(f"Warning: --exposure {args.exposure} ms ≥ frame period "
              f"{1000.0/args.fps:.1f} ms at --fps {args.fps}.  "
              f"SDK will clamp exposure.  Consider lowering --fps.")

    cam = UI3240CP(cam_id=args.cam_id)
    cam.open(roi=args.roi, color=args.color, num_buffers=args.buffers, fps=args.fps)

    cam.set_gain(args.gain)
    print(f"Master gain : {args.gain}")
    if args.exposure is not None:
        actual_exp = cam.set_exposure(args.exposure)
        if abs(actual_exp - args.exposure) > 0.05:
            print(f"WARNING: requested {args.exposure} ms exposure but SDK "
                  f"set {actual_exp:.3f} ms  "
                  f"(use --fps ≤ {1000.0/args.exposure:.1f} to widen the window)")
        else:
            print(f"Exposure    : {actual_exp:.3f} ms")

    # Background writer — disk I/O runs in parallel with capture
    write_q = Queue()
    writer = Thread(target=_writer_thread, args=(write_q,), daemon=True)
    writer.start()

    hw_ts      = []
    frame_nums = []
    captured   = 0
    try:
        for i in range(args.num_frames):
            frame, ts, fnum = cam.capture(timeout_ms=timeout_ms)
            hw_ts.append(ts)
            frame_nums.append(fnum)
            path = os.path.join(args.output_dir, f"frame_{i:04d}.{args.format}")
            write_q.put((path, frame))
            captured += 1
            print(f"  Frame {captured:3d}/{args.num_frames} captured")
    except TimeoutError as e:
        print(f"\nTimeout after {captured} frames: {e}")
    except KeyboardInterrupt:
        print(f"\nInterrupted after {captured} frames.")
    finally:
        print("Waiting for writes to complete…")
        write_q.put(None)
        writer.join()
        cam.close()
        print(f"Saved {captured} frame(s) to {args.output_dir}")
        if captured >= 2:
            _report_stats(hw_ts, frame_nums)


if __name__ == "__main__":
    main()
