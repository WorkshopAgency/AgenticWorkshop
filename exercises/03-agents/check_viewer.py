#!/usr/bin/env python3
"""Quick checks for a generated PDB viewer (Exercise 3a).

Usage:
    python3 exercises/03-agents/check_viewer.py outputs/bad-agent
    python3 exercises/03-agents/check_viewer.py outputs/good-agent --browser

Without --browser this only READS the files (static analysis): it looks for
evidence of each feature in the HTML/JS text. Finding a word is not proof that
the feature works, and an unusual but working page can be missed. Always open
the page yourself as well.

--browser additionally opens the page in headless Google Chrome/Chromium (if
installed), checks that a 3D canvas exists and that something was actually
drawn in it, and saves a screenshot. It does not click any controls, so it
cannot tell whether the toggles or "load another ID" work.

Standard library only; no installation needed.
"""

import argparse
import os
import re
import shutil
import struct
import subprocess
import sys
import tempfile
import zlib
from pathlib import Path

OK, BAD = "\u2705", "\u274c"
LIBRARIES = ["3dmol", "ngl", "molstar", "mol*", "litemol", "jsmol", "pv.min"]
VERSION = r"\d+\.\d+(?:\.\d+)?"


# ---------------------------------------------------------------- helpers
def read(path):
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def find_page(folder):
    """Return index.html if present, otherwise the largest .html file."""
    pages = [p for p in folder.rglob("*.html") if not p.name.startswith(".")]
    pages = sorted(pages, key=lambda p: (p.name != "index.html", -p.stat().st_size))
    return pages[0] if pages else None


def own_code(page, html):
    """The page plus small local .js files it loads (not big vendored libraries)."""
    code = html
    for src in re.findall(r"<script[^>]+src=[\"']([^\"']+)", html, re.I):
        local = (page.parent / src).resolve()
        if not src.startswith(("http:", "https:", "//")) and local.is_file() and local.stat().st_size < 200_000:
            code += "\n" + read(local)
    return code


# ---------------------------------------------------------------- the 7 checks
def check_library(page, html):
    srcs = re.findall(r"<script[^>]+src=[\"']([^\"']+)", html, re.I)
    imports = re.findall(r"import[^;]*?from\s+[\"']([^\"']+)", html)
    for src in srcs + imports:
        low = src.lower()
        if not any(lib in low for lib in LIBRARIES):
            continue
        if src.startswith(("http:", "https:", "//")):
            m = re.search(r"[@/-]v?(" + VERSION + r")(?=[/.-]|$)", src)
            if m and "latest" not in low:
                return True, f"{src} (version {m.group(1)})", m.group(1)
            return False, f"{src} has no version number, so it can change under you", None
        # A downloaded copy counts as pinned only if its version is written down
        # somewhere: in the library's own header, the page, or a README.
        local = page.parent / src
        if not local.is_file():
            return False, f"local file {src} is missing", None
        m = re.search(r"\bv?(" + VERSION + r")\b", read(local)[:300])
        if m:
            return True, f"local copy {src}, its header says version {m.group(1)}", m.group(1)
        notes = html + "".join(read(p) for p in page.parent.glob("README*"))
        m = re.search(r"(3dmol|ngl|mol\*|molstar)[^\n<]{0,15}?v?(" + VERSION + r")", notes, re.I)
        if m:
            return True, f"local copy {src}; version {m.group(2)} recorded in the page/README", m.group(2)
        return False, f"local copy {src}, but no version is recorded anywhere", None
    return False, "no known molecular library (3Dmol.js, NGL, Mol*) found in <script> tags", None


def check_chains(code):
    hardcoded = all(re.search(rf"[\"']{c}[\"']", code) for c in "ABCD") and re.search(r"chain", code, re.I)
    dynamic = re.search(r"\w\.chain\b|\[[\"']chain[\"']\]|auth_asym_id|chain_id|chainid", code, re.I)
    if dynamic:
        return True, "chains are read from the parsed structure (works for any PDB ID)"
    if hardcoded:
        return True, "chains A, B, C, D are written into the code (fine for 4HHB, wrong for other IDs)"
    return False, "no chain IDs and no code that reads chains from the structure"


def check_ligand(code):
    if re.search(r"\bHEM\b", code):
        return True, "HEM (heme) is referenced"
    if re.search(r"hetflag|hetero|ligand", code, re.I):
        return True, "ligands are selected generically (hetflag/ligand), HEM not named"
    return False, "no reference to HEM or to ligands"


def check_error(code):
    handler = re.search(r"catch\s*\(|\.catch\s*\(|onerror|\.ok\b|status\s*[!=]==?\s*200", code)
    message = re.search(r"[\"'`][^\"'`\n]*(error|fail|could not|couldn't|unable|not found|invalid)[^\"'`\n]*[\"'`]", code, re.I)
    if handler and message:
        return True, "has a failure branch and a user-facing error message"
    if handler:
        return False, "catches failures but no visible error message text found"
    return False, "no error handling for a failed download or bad ID"


def check_controls(code):
    reset = re.search(r"reset", code, re.I)
    toggle = re.search(r"chain[\s\S]{0,300}(checkbox|toggle|visible|hidden|hide)|(checkbox|toggle|visible|hidden|hide)[\s\S]{0,300}chain", code, re.I)
    if reset and toggle:
        return True, "reset control and per-chain show/hide found"
    missing = [name for name, hit in (("reset", reset), ("per-chain toggle", toggle)) if not hit]
    return False, "missing: " + ", ".join(missing)


def check_provenance(html, version):
    # Ignore the <script src=...> tags so the library URL itself doesn't count.
    text = re.sub(r"<script[^>]*src=[^>]*>", "", html, flags=re.I)
    source = re.search(r"rcsb|wwpdb|files\.rcsb\.org|pdbe|\.cif|\.pdb", text, re.I)
    lib = version and re.search(re.escape(version), text)
    if source and lib:
        return True, f"page text names the data source and library version {version}"
    missing = [n for n, hit in (("data source", source), ("library version in visible text", lib)) if not hit]
    return False, "missing: " + ", ".join(missing)


# ---------------------------------------------------------------- optional browser check
def find_chrome(explicit):
    candidates = [explicit, os.environ.get("CHROME"),
                  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                  "/Applications/Chromium.app/Contents/MacOS/Chromium",
                  shutil.which("google-chrome"), shutil.which("chromium"), shutil.which("chromium-browser"),
                  r"C:\Program Files\Google\Chrome\Application\chrome.exe"]
    return next((c for c in candidates if c and Path(c).exists()), None)


def png_pixels(path):
    """Minimal PNG decoder (8-bit RGB/RGBA, non-interlaced, as Chrome writes them)."""
    data = Path(path).read_bytes()
    pos, idat, width = 8, b"", 0
    while pos < len(data):
        length, kind = struct.unpack(">I4s", data[pos:pos + 8])
        chunk = data[pos + 8:pos + 8 + length]
        if kind == b"IHDR":
            width, height, depth, ctype = struct.unpack(">IIBB", chunk[:10])
            channels = {2: 3, 6: 4}[ctype]
        elif kind == b"IDAT":
            idat += chunk
        pos += 12 + length
    raw, stride = zlib.decompress(idat), width * channels
    prev, rows, i = bytearray(stride), [], 0
    for _ in range(height):
        f, line = raw[i], bytearray(raw[i + 1:i + 1 + stride])
        i += 1 + stride
        for x in range(stride):
            a = line[x - channels] if x >= channels else 0
            b = prev[x]
            c = prev[x - channels] if x >= channels else 0
            if f == 1: line[x] = (line[x] + a) & 255
            elif f == 2: line[x] = (line[x] + b) & 255
            elif f == 3: line[x] = (line[x] + (a + b) // 2) & 255
            elif f == 4:
                p = a + b - c
                pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
                line[x] = (line[x] + (a if pa <= pb and pa <= pc else b if pb <= pc else c)) & 255
        rows.append(line)
        prev = line
    return rows, channels


def browser_check(page, chrome):
    # Render a temporary copy of the page, next to the original so relative
    # paths still work, with two additions:
    # 1. CSS transitions/animations off: headless Chrome runs on "virtual
    #    time", where a fading "Loading..." overlay may never disappear.
    # 2. A small script that records where the biggest <canvas> is, so we
    #    only look at the 3D view and not at colourful buttons around it.
    extra = ("<style>*,*::before,*::after{transition:none!important;animation:none!important}</style>"
             "<script>setInterval(function(){var c=[].slice.call(document.querySelectorAll('canvas'))"
             ".sort(function(a,b){return b.clientWidth*b.clientHeight-a.clientWidth*a.clientHeight})[0];"
             "if(c){var r=c.getBoundingClientRect();document.documentElement.setAttribute('data-canvas',"
             "[r.left,r.top,r.width,r.height].map(Math.round).join(','))}},500)</script>")
    copy = page.with_name(".check_viewer_tmp.html")
    copy.write_text(re.sub(r"(<head[^>]*>)", lambda m: m.group(1) + extra, read(page), count=1, flags=re.I),
                    encoding="utf-8")
    try:
        return render(page, copy.resolve().as_uri(), chrome)
    finally:
        copy.unlink()


def render(page, url, chrome):
    with tempfile.TemporaryDirectory() as tmp:
        base = [chrome, "--headless=new", "--no-first-run", "--enable-unsafe-swiftshader",
                f"--user-data-dir={tmp}", "--window-size=1000,700", "--virtual-time-budget=20000"]
        shot = Path(tmp) / "shot.png"
        try:
            dom = subprocess.run(base + ["--dump-dom", url], capture_output=True, text=True, timeout=90).stdout
            subprocess.run(base + [f"--screenshot={shot}", url], capture_output=True, timeout=90)
        except subprocess.TimeoutExpired:
            return [(False, "browser: Chrome timed out")]
        box = re.search(r'data-canvas="(\d+),(\d+),(\d+),(\d+)"', dom)
        if not box or int(box.group(3)) * int(box.group(4)) == 0:
            return [(False, "browser: no visible <canvas>, so no 3D view was created")]
        results = [(True, "browser: page has a visible <canvas> (where the 3D view is drawn)")]
        if not shot.exists():
            return results + [(False, "browser: no screenshot produced")]
        saved = page.parent / "check_viewer_screenshot.png"
        shutil.copy(shot, saved)

        # Inside the canvas: how many pixels clearly differ from the background?
        rows, ch = png_pixels(shot)
        left, top, width, height = (int(v) for v in box.groups())
        pixels = [tuple(row[x * ch:x * ch + 3])
                  for row in rows[top:top + height:2]
                  for x in range(left, min(left + width, len(row) // ch), 2)]
        counts = {}
        for p in pixels:
            counts[p] = counts.get(p, 0) + 1
        background = max(counts, key=counts.get)
        drawn = sum(1 for p in pixels if sum(abs(a - b) for a, b in zip(p, background)) > 90)
        share = 100 * drawn / max(len(pixels), 1)
        results.append((share >= 8, f"browser: {share:.0f}% of the canvas differs from its background "
                                    f"(>= 8% suggests a structure was drawn; an empty canvas is ~0%)"))
        results.append((True, f"browser: screenshot saved to {saved} - look at it"))
        return results


# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("folder", type=Path, help="output folder, e.g. outputs/good-agent")
    ap.add_argument("--browser", action="store_true", help="also render the page in headless Chrome")
    ap.add_argument("--chrome", help="path to a Chrome/Chromium executable")
    args = ap.parse_args()

    page = find_page(args.folder) if args.folder.is_dir() else None
    print(f"Checking {args.folder}")
    if page is None:
        print(f"{BAD} 1. HTML file exists: no .html file found\n\nScore: 0/7")
        return 1
    html = read(page)
    code = own_code(page, html)
    pinned, why_lib, version = check_library(page, html)
    results = [
        ("HTML file exists", True, str(page.relative_to(args.folder))),
        ("Molecular library pinned to a version", pinned, why_lib),
        ("Real chain IDs (A-D for 4HHB, or read from the structure)", *check_chains(code)),
        ("Heme (HEM) / ligands highlighted", *check_ligand(code)),
        ("Visible error message path", *check_error(code)),
        ("Reset + per-chain toggle controls", *check_controls(code)),
        ("Provenance caption (data source + library version)", *check_provenance(html, version)),
    ]
    for i, (name, passed, why) in enumerate(results, 1):
        print(f"{OK if passed else BAD} {i}. {name}: {why}")
    score = sum(1 for _, passed, _ in results if passed)
    print(f"\nScore: {score}/7 (static)")
    print("Static checks only find evidence in the code. They cannot tell whether the\n"
          "structure really loads or the buttons work: a page can score 7/7 and still\n"
          "crash. Open the page and click through it.")

    if args.browser:
        chrome = find_chrome(args.chrome)
        print()
        if not chrome:
            print("Browser check skipped: no Chrome/Chromium found (use --chrome PATH).")
        else:
            for passed, why in browser_check(page, chrome):
                print(f"{OK if passed else BAD} {why}")
            print("The browser check needs internet if the page loads data or the library online,\n"
                  "and it does not click any controls.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
