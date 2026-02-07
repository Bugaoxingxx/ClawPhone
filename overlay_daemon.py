#!/usr/bin/env python3
"""overlay_daemon.py

Runs in a *foreground* termux/tmux session and shows Termux:GUI overlay text whenever
~/overlay.txt changes.

Usage (in Termux interactive shell):
  python ~/overlay_daemon.py

Then from anywhere (including OpenClaw):
  printf '%s\n' 'hello' > ~/overlay.txt

Notes:
- This keeps the Termux:GUI connection in the "known-good" interactive context.
- Avoid emojis if you don't want the black background effect.
"""

import os
import time
import termuxgui as tg

OVERLAY_FILE = os.path.expanduser('~/overlay.txt')
POLL_SEC = 0.25
DEFAULT_SECONDS = 10.0


def show_overlay(c: tg.Connection, text: str, seconds: float = DEFAULT_SECONDS):
    a1 = tg.Activity(c)
    tid = a1.t.tid
    a1.finish()

    a = tg.Activity(c, tid=tid, overlay=True)
    tg.TextView(a, text)
    time.sleep(max(0.1, seconds))
    # Explicitly close the overlay activity so it doesn't stick around.
    try:
        a.finish()
    except Exception:
        pass


def main():
    print(f"[overlay_daemon] watching {OVERLAY_FILE}")
    print("[overlay_daemon] write text into overlay.txt to display it")
    last_mtime = None

    # Ensure file exists
    if not os.path.exists(OVERLAY_FILE):
        with open(OVERLAY_FILE, 'w', encoding='utf-8') as f:
            f.write('')

    with tg.Connection() as c:
        while True:
            try:
                st = os.stat(OVERLAY_FILE)
                if last_mtime is None:
                    last_mtime = st.st_mtime
                elif st.st_mtime != last_mtime:
                    last_mtime = st.st_mtime
                    with open(OVERLAY_FILE, 'r', encoding='utf-8') as f:
                        text = f.read().strip()
                    if text:
                        show_overlay(c, text, DEFAULT_SECONDS)
            except KeyboardInterrupt:
                print("\n[overlay_daemon] exiting")
                return
            except Exception as e:
                # Don't die on transient file/GUI hiccups
                print(f"[overlay_daemon] error: {e}")
                time.sleep(1.0)

            time.sleep(POLL_SEC)


if __name__ == '__main__':
    main()