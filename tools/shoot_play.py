#!/usr/bin/env python3
"""Load the play surface in a real headless browser and capture it, so the
look can be judged rather than assumed. Also reports page errors."""
import asyncio, http.server, socketserver, threading, functools, sys, json

DIR = "/home/user/workspace/urm/docs/play"
PORT = 8912
OUT = "/home/user/workspace/urm/verification"

H = functools.partial(http.server.SimpleHTTPRequestHandler, directory=DIR)
socketserver.TCPServer.allow_reuse_address = True
srv = socketserver.TCPServer(("127.0.0.1", PORT), H)
threading.Thread(target=srv.serve_forever, daemon=True).start()


async def main():
    from playwright.async_api import async_playwright
    errs, logs = [], []
    async with async_playwright() as p:
        b = await p.chromium.launch(args=[
            "--use-gl=angle", "--use-angle=swiftshader",
            "--enable-unsafe-swiftshader", "--disable-gpu-sandbox"])
        pg = await b.new_page(viewport={"width": 1440, "height": 860})
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.on("console", lambda m: logs.append(f"{m.type}: {m.text}")
              if m.type in ("error", "warning") else None)
        await pg.goto(f"http://127.0.0.1:{PORT}/index.html")
        await pg.wait_for_timeout(9000)

        err_on = await pg.evaluate("document.getElementById('err').classList.contains('on')")
        tri = await pg.inner_text("#hTri")

        await pg.screenshot(path=f"{OUT}/play_01_start.png")

        # Enter the field, then look around and walk in.
        await pg.click(".start .go")
        await pg.wait_for_timeout(1200)
        await pg.screenshot(path=f"{OUT}/play_02_entered.png")

        # Walk toward Uriel.
        await pg.keyboard.down("w")
        await pg.wait_for_timeout(2600)
        await pg.keyboard.up("w")
        await pg.wait_for_timeout(1400)
        await pg.screenshot(path=f"{OUT}/play_03_approach.png")

        cap = await pg.evaluate(
            "document.getElementById('cap').classList.contains('on') ? "
            "document.getElementById('capText').textContent : null")

        # Turn to take in the gate ring.
        for _ in range(24):
            await pg.mouse.move(0, 0)
            await pg.wait_for_timeout(10)
        await pg.evaluate("window.scrollTo(0,0)")
        await pg.wait_for_timeout(600)
        await pg.screenshot(path=f"{OUT}/play_04_field.png")

        # Portraits: park the camera on each figure so the sculpting can be
        # judged at size instead of guessed at from a wide shot.
        await pg.evaluate('''() => {
          window.__portrait = (t) => {
            const s = window.__scene, c = window.__cam;
            if (!s || !c) return 'no handles';
            const o = s.getObjectByName(t);
            if (!o) return 'missing ' + t;
            const b = new window.__THREE.Box3().setFromObject(o);
            const ctr = b.getCenter(new window.__THREE.Vector3());
            const sz  = b.getSize(new window.__THREE.Vector3());
            const d = Math.max(sz.y, sz.x) * 1.55;
            window.__freeze = true;
            const q = new window.__THREE.Vector3(0, 0, 1).applyQuaternion(o.getWorldQuaternion(new window.__THREE.Quaternion()));
            const fx = q.x || 0, fz = q.z || 1;
            /* Stand in front of the figure, offset to one side. */
            c.position.set(ctr.x + fx * d * 0.92 + fz * d * 0.50,
                           ctr.y + sz.y * 0.16,
                           ctr.z + fz * d * 0.92 - fx * d * 0.50);
            c.lookAt(ctr.x, ctr.y, ctr.z);
            return 'ok h=' + sz.y.toFixed(2);
          };
        }''')
        r1 = await pg.evaluate("window.__portrait('Uriel')")
        await pg.wait_for_timeout(900)
        await pg.screenshot(path=f"{OUT}/play_06_uriel.png")
        r2 = await pg.evaluate("window.__portrait('PlayerAvatarLive')")
        await pg.wait_for_timeout(900)
        await pg.screenshot(path=f"{OUT}/play_07_avatar.png")
        portraits = [r1, r2]

        # Mobile.
        pg2 = None if "--nomobile" in sys.argv else await b.new_page(viewport={"width": 393, "height": 852},
                               is_mobile=True, has_touch=True,
                               device_scale_factor=2)
        if pg2:
            await pg2.goto(f"http://127.0.0.1:{PORT}/index.html")
            await pg2.wait_for_timeout(8000)
            await pg2.screenshot(path=f"{OUT}/play_05_mobile.png",
                                 timeout=90000, animations="disabled")

        await b.close()

    rep = {"page_errors": errs, "error_panel_shown": err_on,
           "triangles": tri, "caption_shown": cap, "portraits": portraits,
           "console_warnings": logs[:12]}
    open(f"{OUT}/play_report.json", "w").write(json.dumps(rep, indent=2))
    print(json.dumps(rep, indent=2)[:1400])
    return 1 if (errs or err_on) else 0


sys.exit(asyncio.run(main()))
