#!/usr/bin/env python3
"""把 icon.html / store.html 渲染成扩展图标和商店素材。

用法：
    python store-assets/design/render.py

依赖：本机安装 Chrome（或 Edge）、Python 3、Pillow。
Windows / macOS / Linux 都可以用；也可用环境变量 CHROME 指定浏览器路径。
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image

DESIGN = Path(__file__).resolve().parent
ROOT = DESIGN.parent.parent
OUT = ROOT / "store-assets"

CANDIDATES = [
    os.environ.get("CHROME", ""),
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    shutil.which("google-chrome") or "",
    shutil.which("chromium") or "",
    shutil.which("chromium-browser") or "",
]


def find_chrome() -> str:
    for path in CANDIDATES:
        if path and Path(path).exists():
            return path
    sys.exit("没有找到 Chrome / Edge，请用环境变量 CHROME 指定浏览器路径。")


CHROME = find_chrome()


def shoot(url: str, width: int, height: int, output: Path, transparent: bool = False) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        cmd = [
            CHROME,
            "--headless=new",
            "--disable-gpu",
            "--hide-scrollbars",
            "--allow-file-access-from-files",
            "--no-first-run",
            "--no-default-browser-check",
            "--disable-extensions",
            "--disable-background-networking",
            "--disable-sync",
            f"--user-data-dir={Path(tmp) / 'profile'}",
            "--force-device-scale-factor=1",
            f"--window-size={width},{height}",
            "--virtual-time-budget=3000",
            f"--screenshot={output}",
            url,
        ]
        if transparent:
            cmd.append("--default-background-color=00000000")
        subprocess.run(cmd, capture_output=True, timeout=60, check=False)
    if not output.exists():
        sys.exit(f"渲染失败：{output.name}")
    with Image.open(output) as image:
        if image.size != (width, height):
            sys.exit(f"渲染尺寸不符：{output.name} 得到 {image.size}，期望 {(width, height)}")


def render_icon(target: int, pad: int, output: Path) -> None:
    """按 512px 超采样绘制，再缩到目标尺寸，保证小图标边缘干净。"""
    scale = 512
    pad_scaled = pad * scale / target
    simple = "1" if target <= 32 else "0"
    tiny = "1" if target <= 16 else "0"
    url = f"{DESIGN.as_uri()}/icon.html?size={scale}&pad={pad_scaled:g}&simple={simple}&tiny={tiny}"
    with tempfile.TemporaryDirectory() as tmp:
        raw = Path(tmp) / "icon.png"
        shoot(url, scale, scale, raw, transparent=True)
        with Image.open(raw) as image:
            resized = image.convert("RGBA").resize((target, target), Image.LANCZOS)
            resized.save(output)


def flatten(output: Path) -> None:
    """商店要求 PNG 不带透明通道。"""
    with Image.open(output) as image:
        canvas = Image.new("RGB", image.size, "white")
        canvas.paste(image.convert("RGBA"), mask=image.convert("RGBA").getchannel("A"))
        canvas.save(output)


def main() -> None:
    for size, pad in ((128, 16), (48, 2), (32, 1), (16, 0)):
        render_icon(size, pad, ROOT / "icons" / f"icon{size}.png")
        print(f"icons/icon{size}.png")

    with tempfile.TemporaryDirectory() as tmp:
        raw = Path(tmp) / "icon-512.png"
        shoot(f"{DESIGN.as_uri()}/icon.html?size=512&pad=0", 512, 512, raw, transparent=True)
        shutil.copyfile(raw, DESIGN / "icon-512.png")
    print("store-assets/design/icon-512.png")

    views = [
        ("shot1", 1280, 800, OUT / "screenshot-1-1280x800.png"),
        ("shot2", 1280, 800, OUT / "screenshot-2-1280x800.png"),
        ("shot3", 1280, 800, OUT / "screenshot-3-1280x800.png"),
        ("shot4", 1280, 800, OUT / "screenshot-4-1280x800.png"),
        ("small", 440, 280, OUT / "small-promo-tile-440x280.png"),
        ("marquee", 1400, 560, OUT / "marquee-promo-tile-1400x560.png"),
    ]
    for view, width, height, output in views:
        url = f"{DESIGN.as_uri()}/store.html?view={view}"
        shoot(url, width, height, output)
        flatten(output)
        print(output.relative_to(ROOT).as_posix())

    print("done")


if __name__ == "__main__":
    main()
