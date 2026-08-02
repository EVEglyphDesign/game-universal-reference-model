#!/usr/bin/env python3
"""
verify_play.py — verifies the Live 3D page at urm/docs/play/index.html.

Primary path (used when Playwright is available):
  1. Serve urm/docs/play/ on localhost via a background HTTP server.
  2. Launch headless Chromium via Playwright.
  3. Navigate to the page, collect console messages/errors and page errors.
  4. Wait for the scene to report readiness (canvas present + a few animation
     frames elapsed) or for the visible error panel to appear.
  5. Screenshot the page and save it to urm/docs/play/_verify_screenshot.png.
  6. Print a JSON report of: page loaded, console errors, whether the error
     panel is visible, whether the loading screen is hidden, screenshot path.

Fallback path (used only if Playwright cannot be installed/imported):
  a. Serve the directory and curl it to confirm HTTP 200.
  b. Extract the inline <script type="module"> body to a .mjs file and run
     `node --check` on it to validate syntax.
  c. Validate that the two pinned importmap URLs
     (three.module.js, GLTFLoader.js) return HTTP 200.
  This fallback CANNOT confirm the scene actually renders geometry — that
  requires a real browser. This limitation is reported explicitly.

Usage:
  python3 verify_play.py
"""

import http.server
import io
import json
import os
import re
import socket
import subprocess
import sys
import threading
import time
import urllib.request

PLAY_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "docs", "play"))
PORT = 8791
BASE_URL = f"http://127.0.0.1:{PORT}/"
SCREENSHOT_PATH = os.path.join(PLAY_DIR, "_verify_screenshot.png")

IMPORTMAP_URLS = [
    "https://unpkg.com/three@0.160.0/build/three.module.js",
    "https://unpkg.com/three@0.160.0/examples/jsm/loaders/GLTFLoader.js",
]


def start_server():
    handler = lambda *args, **kwargs: http.server.SimpleHTTPRequestHandler(
        *args, directory=PLAY_DIR, **kwargs
    )
    httpd = http.server.ThreadingHTTPServer(("127.0.0.1", PORT), handler)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    # Wait for the socket to accept connections.
    for _ in range(50):
        try:
            with socket.create_connection(("127.0.0.1", PORT), timeout=0.2):
                break
        except OSError:
            time.sleep(0.1)
    return httpd


def check_importmap_urls():
    results = {}
    for url in IMPORTMAP_URLS:
        try:
            req = urllib.request.Request(url, method="HEAD")
            with urllib.request.urlopen(req, timeout=10) as resp:
                results[url] = resp.status
        except Exception as e:
            try:
                req = urllib.request.Request(url, method="GET")
                with urllib.request.urlopen(req, timeout=10) as resp:
                    results[url] = resp.status
            except Exception as e2:
                results[url] = f"ERROR: {e2}"
    return results


def curl_check():
    try:
        with urllib.request.urlopen(BASE_URL + "index.html", timeout=10) as resp:
            return resp.status
    except Exception as e:
        return f"ERROR: {e}"


def node_syntax_check():
    html_path = os.path.join(PLAY_DIR, "index.html")
    with open(html_path, "r") as f:
        html = f.read()
    m = re.search(r'<script type="module">(.*?)</script>', html, re.S)
    if not m:
        return {"ok": False, "detail": "Could not find inline module script in index.html"}
    script_body = m.group(1)
    mjs_path = "/tmp/verify_play_module.mjs"
    with open(mjs_path, "w") as f:
        f.write(script_body)
    proc = subprocess.run(
        ["node", "--check", mjs_path], capture_output=True, text=True
    )
    return {
        "ok": proc.returncode == 0,
        "stdout": proc.stdout.strip(),
        "stderr": proc.stderr.strip(),
        "extracted_path": mjs_path,
    }


def run_playwright_verification():
    from playwright.sync_api import sync_playwright

    console_messages = []
    page_errors = []

    with sync_playwright() as p:
        browser = p.chromium.launch(args=["--use-gl=swiftshader", "--enable-webgl", "--ignore-gpu-blocklist"])
        page = browser.new_page(viewport={"width": 1280, "height": 800})

        page.on("console", lambda msg: console_messages.append({"type": msg.type, "text": msg.text}))
        page.on("pageerror", lambda exc: page_errors.append(str(exc)))

        page.goto(BASE_URL + "index.html", wait_until="load", timeout=30000)

        # Give the module time to load three.js from unpkg, parse the glb, and render frames.
        page.wait_for_timeout(4000)

        # Poll for either the loading screen hidden or the error screen visible, up to ~15s total.
        loading_hidden = False
        error_visible = False
        for _ in range(20):
            loading_hidden = page.eval_on_selector(
                "#loading-screen", "el => el.classList.contains('hidden')"
            )
            error_visible = page.eval_on_selector(
                "#error-screen", "el => el.classList.contains('visible')"
            )
            if loading_hidden or error_visible:
                break
            page.wait_for_timeout(500)

        # Let a good number of animation frames run for a settled screenshot.
        page.wait_for_timeout(1500)

        fps_text = page.eval_on_selector("#fps-val", "el => el.textContent")
        tri_text = page.eval_on_selector("#tri-val", "el => el.textContent")

        canvas_info = page.evaluate(
            """() => {
                const c = document.querySelector('canvas');
                if (!c) return null;
                return {width: c.width, height: c.height};
            }"""
        )

        page.screenshot(path=SCREENSHOT_PATH)
        browser.close()

    return {
        "console_messages": console_messages,
        "page_errors": page_errors,
        "loading_hidden": loading_hidden,
        "error_visible": error_visible,
        "fps_text": fps_text,
        "tri_text": tri_text,
        "canvas_info": canvas_info,
        "screenshot_path": SCREENSHOT_PATH,
    }


def main():
    report = {"play_dir": PLAY_DIR}

    if not os.path.isdir(PLAY_DIR):
        print(json.dumps({"error": f"play dir not found: {PLAY_DIR}"}, indent=2))
        sys.exit(1)

    httpd = start_server()
    try:
        report["curl_status"] = curl_check()
        report["importmap_url_status"] = check_importmap_urls()

        playwright_ok = False
        try:
            import playwright  # noqa: F401
            playwright_ok = True
        except ImportError:
            playwright_ok = False

        report["verification_path"] = "playwright" if playwright_ok else "fallback"

        if playwright_ok:
            try:
                pw_report = run_playwright_verification()
                report.update(pw_report)
            except Exception as e:
                report["playwright_error"] = str(e)
                report["verification_path"] = "fallback (playwright failed at runtime)"
                report["node_syntax_check"] = node_syntax_check()
        else:
            report["node_syntax_check"] = node_syntax_check()
            report["note"] = (
                "Playwright unavailable — used fallback path (curl + node --check "
                "+ importmap HEAD checks). Actual WebGL rendering was NOT verified."
            )
    finally:
        httpd.shutdown()

    print(json.dumps(report, indent=2, default=str))
    return report


if __name__ == "__main__":
    main()
