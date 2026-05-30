thorTrig.py / multiTrig.py — Thorlabs UI-3240CP External Trigger Capture
=========================================================================

OVERVIEW
--------
Two scripts for capturing triggered frames from one or more Thorlabs UI-3240CP
cameras.  The UI-3240CP is a rebranded IDS Imaging uEye camera, so both scripts
use the IDS uEye SDK rather than the Thorlabs ThorCam SDK.

  thorTrig.py   — single-camera capture; stops after a fixed frame count.
  multiTrig.py  — multi-camera capture; stops after a fixed duration (seconds).
                  Cameras may receive simultaneous or asynchronous triggers.
                  Each camera runs in its own thread; a shared background thread
                  handles all disk writes.

Both scripts use a ring buffer + image queue so the camera can accept the next
trigger while the CPU is still copying the previous frame, and a background
writer thread so disk I/O does not stall the capture loop.

Performance statistics (mean fps, jitter, dropped triggers) are printed at the
end of each run using hardware timestamps from the camera itself, which are
immune to OS scheduling jitter.


HARDWARE TRIGGER WIRING
-----------------------
The UI-3240CP has a 6-pin GPIO connector (Hirose HR10A-7P-6S or compatible).

  Pin 1 — GND
  Pin 2 — Trigger IN  (3.3 V – 5 V TTL, ~1 kΩ internal pull-up)
  Pin 3 — Flash/strobe OUT (optional output to synchronize other devices)
  Pin 4 — GPIO
  Pin 5 — GPIO
  Pin 6 — +5 V (if enabled in firmware)

Connect your trigger source (function generator, DAQ card, microcontroller,
etc.) between Pin 2 (signal) and Pin 1 (GND).  By default the scripts fire on
the RISING edge; pass --edge falling to use the falling edge instead.

The maximum trigger rate is set by the camera's readout time, which depends on
pixel clock, ROI size, and color mode (see MAXIMIZING FRAMERATE).


PLATFORM SUPPORT
----------------
  Ubuntu x86_64 (recommended)
  Windows 10/11 (x64)
  macOS (Intel or Apple Silicon via Rosetta)

The IDS uEye SDK and pyueye wrapper support all three platforms with identical
Python code.


INSTALLATION
------------

1. Install the IDS uEye SDK
   Download the correct package for your OS from:
     https://en.ids-imaging.com/downloads.html
     (search for "uEye SDK")

   Linux:
     chmod +x ueye_4.xx.x_amd64.run
     sudo ./ueye_4.xx.x_amd64.run
     sudo systemctl start ueyeusbdrc        # start the uEye USB daemon

   Windows:
     Run the installer .exe and follow the wizard.
     The uEye driver is installed automatically.

   macOS:
     Run the .pkg installer.

2. Install Python dependencies
     pip install pyueye numpy opencv-python

   Python 3.8 or newer is recommended.

3. Connect the camera(s)
   Plug each UI-3240CP into a USB 3.x port (not a hub if avoidable).
   On Linux, verify cameras are detected:
     sudo ueyesetid          # assign camera IDs (run once after first connection)
     ueyedemo                # optional GUI to confirm a camera works

4. Verify the uEye daemon is running (Linux only)
     sudo systemctl status ueyeusbdrc
   If it is not running:
     sudo systemctl start ueyeusbdrc


CAMERA SELECTION
----------------
Both scripts identify cameras by their 0-based position in the enumerated
camera list, NOT by the configurable camera ID stored in firmware (which may
not be unique if multiple cameras have never had IDs assigned).

Always run --list-cameras first to see which index maps to which device:

  python thorTrig.py --list-cameras
  python multiTrig.py --list-cameras

Example output for two cameras:
  Detected 2 camera(s):  (use [N] as --cam-id)
    [0] Serial=4102989570  Model=UI324xCP-NIR  dev_id=1  cam_id=1  Status=0
    [1] Serial=4102989568  Model=UI324xCP-NIR  dev_id=2  cam_id=1  Status=0

Pass the [N] index to --cam-id:
  python thorTrig.py --cam-id 1          # open the second camera
  python multiTrig.py --cam-id 0 1       # open both cameras

If both cameras show cam_id=1 (factory default), run `sudo ueyesetid` to
assign distinct IDs.  The scripts use the unique dev_id internally, so
distinct cam_ids are cosmetic only.


USAGE — thorTrig.py
-------------------
Captures a fixed number of triggered frames from a single camera.

Basic — 10 frames, full resolution, mono8, rising edge:
  python thorTrig.py

Capture 50 frames and save to a subfolder:
  python thorTrig.py -n 50 -o ./captures

Use a reduced ROI to increase the maximum trigger rate:
  python thorTrig.py --roi 0,0,640,512

Set exposure and gain:
  python thorTrig.py --exposure 10 --gain 0

Use a falling-edge trigger:
  python thorTrig.py --edge falling

Lower the internal framerate limit to allow longer exposures with a small ROI
(see EXPOSURE AND FRAMERATE below):
  python thorTrig.py --roi 0,0,1000,100 --fps 30 --exposure 20

Select a specific camera:
  python thorTrig.py --cam-id 1

Increase the ring buffer to handle high trigger rates:
  python thorTrig.py --buffers 32

Set a per-frame trigger timeout (milliseconds, default 5000):
  python thorTrig.py --timeout 10000

Save as PNG instead of TIFF:
  python thorTrig.py --format png

Full option list:
  python thorTrig.py --help


USAGE — multiTrig.py
--------------------
Captures triggered frames from one or more cameras simultaneously.
Capture stops after --duration seconds rather than a fixed frame count.
Each camera saves to its own subdirectory under --output-dir.

Capture from two cameras for 30 seconds:
  python multiTrig.py --cam-id 0 1 -d 30 -o ./captures

Single camera for 10 seconds (same interface as thorTrig.py):
  python multiTrig.py --cam-id 0 -d 10 -o ./captures

With ROI, exposure, and gain applied to all cameras:
  python multiTrig.py --cam-id 0 1 -d 30 --roi 0,0,1280,512 --exposure 5 --gain 0

Full option list:
  python multiTrig.py --help

Output layout:
  ./captures/
    cam0/
      frame_0000.tiff
      frame_0001.tiff
      ...
    cam1/
      frame_0000.tiff
      frame_0001.tiff
      ...


MAXIMIZING FRAMERATE
--------------------
Both scripts apply all of these automatically; the notes explain the tradeoffs.

  1. Mono8 color mode (default)
     Color requires 3x the USB bandwidth.  Mono8 is the fastest mode.
     Full 1280x1024 mono8 reaches ~60–90 fps depending on pixel clock.

  2. Maximum pixel clock
     The script queries and sets the highest clock the camera supports.
     Higher pixel clock = faster sensor readout = higher max trigger rate.

  3. Reduced ROI (--roi x,y,w,h)
     Cutting sensor height roughly doubles maximum framerate.
     Approximate max rates (full pixel clock, mono8):
       1280x1024  →  ~60–90 fps
       1280x512   →  ~130–160 fps
       1280x256   →  ~220–280 fps
       640x512    →  ~160–200 fps

  4. Ring buffer (--buffers, default 8 for thorTrig / 32 for multiTrig)
     The camera writes each triggered frame into the next available ring buffer
     slot while the CPU copies the previous frame.  Increase --buffers if
     triggers arrive faster than the CPU can drain them.

  5. Background writer thread
     Disk writes happen in a separate thread so the capture loop is never
     stalled waiting for the filesystem.  Use --format tiff or bmp for fastest
     writes (uncompressed); --format png adds CPU-side compression.

  6. USB 3.x port
     Use a port connected directly to an xHCI controller, not a USB 2.0 hub or
     USB-C adapter.  On Linux, confirm with:
       lsusb -t
     Each camera should appear under a separate xhci_hcd host controller if
     possible; two cameras on the same controller share bandwidth.


EXPOSURE AND FRAMERATE
----------------------
Exposure is capped at just below one frame period (1 / internal_fps).  With the
internal framerate set to the hardware maximum, the exposure ceiling shrinks
sharply as the ROI gets smaller.

If images are dark at a small ROI, reduce the internal framerate with --fps:

  python thorTrig.py --roi 0,0,1000,100 --fps 30 --exposure 20

  --fps 30 sets the frame period to ~33 ms, allowing exposures up to ~30 ms
  regardless of ROI size.  Set --fps to just above your actual trigger rate;
  there is no benefit to allowing a higher internal rate than the trigger rate,
  and doing so shrinks the exposure window unnecessarily.

The available exposure range for the current settings is always printed at
startup:
  Exposure range: 0.0291 – 31.847 ms  (use --exposure to set)


PERFORMANCE REPORTING
---------------------
At the end of each run, both scripts print capture statistics derived from the
camera's internal hardware timestamps (100 ns resolution, stamped at capture
time before USB transfer).  These are accurate regardless of OS scheduling
jitter.

Example output:
  --- Capture statistics (camera hardware timestamps) ---
  Frames captured  : 50  |  Dropped triggers: 0
  Mean frame period: 25.003 ms  (39.99 fps)
  Jitter (1σ)      : ±0.009 ms
  Min / Max period : 24.981 / 25.031 ms

  Dropped triggers: detected by gaps in the camera's frame counter.  A value
    greater than 0 means some triggers were received but no buffer was available
    to store the frame (increase --buffers or reduce trigger rate).

  Jitter: inter-frame interval standard deviation.  Large jitter with an
    otherwise correct mean fps indicates the trigger source is uneven.
    Jitter near zero with an incorrect mean fps indicates missed triggers.


OUTPUT FILES
------------
thorTrig.py saves frames as frame_0000.tiff, frame_0001.tiff, etc. in the
directory specified by --output-dir (default: current directory).

multiTrig.py saves frames into per-camera subdirectories cam0/, cam1/, etc.
under --output-dir, each with independent sequential numbering.

TIFF is the default because it is lossless, preserves full 8-bit depth, and
writes fastest (no compression).


TROUBLESHOOTING
---------------

No cameras detected / "uEye error 3 [InitCamera]"
  - Check USB connection and try a different port.
  - On Linux, ensure the uEye daemon is running:
      sudo systemctl start ueyeusbdrc
  - Run `sudo ueyesetid` if this is the first connection.
  - Try `ueyedemo` to confirm the camera is recognized by the SDK.

"Camera is already open in another process"
  - Close IDS uEye Cockpit or any other IDS application and retry.

"Camera paired to a stale daemon session"
  - Close IDS uEye Cockpit completely.
  - sudo systemctl restart ueyeusbdrc
  - sudo ueyesetid
  - Re-run the script.

Images are black or very dark
  - Check that --exposure is set to a value within the printed exposure range.
  - If using a small ROI, lower --fps to widen the exposure ceiling (see
    EXPOSURE AND FRAMERATE above).
  - Verify --gain is set appropriately (0 = no hardware gain, higher = brighter).
  - Confirm the illumination source is on and synced to the trigger.

Trigger not being received (timeout)
  - Verify wiring on Pin 2 (trigger IN) and Pin 1 (GND).
  - Confirm signal voltage is 3.3 V – 5 V; signals below ~2.5 V may not be
    recognized as a logic high.
  - Increase --timeout (milliseconds) if triggers arrive infrequently.
  - Check --edge matches the polarity of your signal.

Reported fps differs significantly from trigger frequency
  - Small frame counts (< 50) amplify timing noise; use more frames.
  - Check "Dropped triggers" in the statistics output.  If > 0, increase
    --buffers so the ring buffer doesn't fill between CPU drain cycles.
  - Large jitter (> 1 ms) usually points to an uneven trigger source, not a
    software issue.

Both cameras open but only one captures frames (multiTrig.py)
  - Increase --buffers (default 32); if ring buffers fill faster than they are
    drained, the SDK cancels the pending wait and the script auto-recovers with
    a flush and re-arm, which drops the in-flight trigger.
  - Check that each camera is on a separate USB host controller (lsusb -t).
  - Verify both cameras are listed by --list-cameras with distinct dev_id values.

Low framerate despite small ROI
  - Confirm the pixel clock is printed correctly at startup.
  - Check the USB host controller (see USB 3.x note above).
  - On Linux: sudo cpupower frequency-set -g performance

ImportError: No module named 'pyueye'
  - Run: pip install pyueye
  - Install the IDS uEye SDK first; pyueye needs the underlying ueye_api
    shared library.

ImportError when running multiTrig.py
  - multiTrig.py imports from thorTrig.py; both files must be in the same
    directory.

Permission denied on /dev/ueyeusb* (Linux)
  - Add your user to the plugdev group:
      sudo usermod -aG plugdev $USER
    Then log out and back in.


MATLAB ALTERNATIVE
------------------
IDS ships a MATLAB wrapper with the uEye SDK.  After installing the SDK, add
the MATLAB folder to your path (typically /usr/local/share/ueye/matlab/ on
Linux or C:\Program Files\IDS\uEye\MATLAB\ on Windows), then:

  cam = ids_cam(0);
  cam.SetColorMode('MONO8');
  cam.SetPixelClock('MAX');
  cam.SetFrameRate(1000);          % SDK caps to hardware maximum
  cam.SetExposure(10);             % ms — adjust to your lighting
  cam.SetExternalTrigger('LO_HI'); % rising edge
  cam.AllocImageMem();
  cam.SetImageMem();

  for k = 1:20
      cam.FreezeVideo('WAIT');
      img = cam.GetImageData();
      imwrite(img, sprintf('frame_%04d.tiff', k));
  end
  cam.Close();

Alternatively, call thorTrig.py from MATLAB using the system() or
pyenv/py.* interface.


REFERENCES
----------
  IDS uEye SDK documentation:
    https://en.ids-imaging.com/manuals/ids-software-suite/ueye-manual/

  pyueye GitHub and documentation:
    https://github.com/morefigs/pyueye

  Thorlabs UI-3240CP product page and datasheet:
    https://www.thorlabs.com  (search "UI-3240CP")

  IDS uEye camera selector / downloads:
    https://en.ids-imaging.com/downloads.html
