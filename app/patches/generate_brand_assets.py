from __future__ import annotations

import struct
import zlib
from pathlib import Path


def logo_png(size: int) -> bytes:
    scale = 4
    width = height = size * scale
    rows = bytearray()
    cx = cy = (size - 1) / 2

    def pixel(x: float, y: float) -> tuple[int, int, int, int]:
        dx, dy = abs(x - cx), abs(y - cy)
        rounded = max(dx, dy) + 0.4142 * min(dx, dy)
        if rounded > size * 0.48:
            return 0, 0, 0, 0
        # A nested diamond creates a compact, distinctive Ascend compass mark.
        manhattan = dx + dy
        if size * 0.18 < manhattan < size * 0.32:
            t = max(0.0, min(1.0, y / size))
            return round(108 - 30 * t), round(225 - 94 * t), round(212 - 38 * t), 255
        if manhattan <= size * 0.105:
            return 230, 255, 250, 255
        bg = max(0.0, min(1.0, (y / size) * 0.6 + 0.2))
        return round(11 + 12 * bg), round(16 + 23 * bg), round(24 + 35 * bg), 255

    for py in range(size):
        rows.append(0)
        for px in range(size):
            sums = [0, 0, 0, 0]
            for sy in range(scale):
                for sx in range(scale):
                    sample = pixel(px + (sx + 0.5) / scale, py + (sy + 0.5) / scale)
                    for channel in range(4):
                        sums[channel] += sample[channel]
            rows.extend(round(value / (scale * scale)) for value in sums)

    def chunk(kind: bytes, payload: bytes) -> bytes:
        body = kind + payload
        return struct.pack(">I", len(payload)) + body + struct.pack(">I", zlib.crc32(body) & 0xFFFFFFFF)

    header = struct.pack(">IIBBBBB", size, size, 8, 6, 0, 0, 0)
    return b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", header) + chunk(b"IDAT", zlib.compress(rows, 9)) + chunk(b"IEND", b"")


def wizard_bmp(width: int, height: int) -> bytes:
    pixels = bytearray()
    for y in range(height - 1, -1, -1):
        row = bytearray()
        for x in range(width):
            u = (x - width * 0.5) / max(width, height)
            v = (y - height * 0.5) / max(width, height)
            d = abs(u) + abs(v)
            if 0.16 < d < 0.25:
                color = (77, 196, 183)
            elif d < 0.075:
                color = (227, 255, 249)
            else:
                t = y / max(1, height - 1)
                color = (round(10 + 9 * t), round(15 + 21 * t), round(23 + 30 * t))
            row.extend((color[2], color[1], color[0]))
        row.extend(b"\0" * ((4 - len(row) % 4) % 4))
        pixels.extend(row)
    offset = 54
    header = b"BM" + struct.pack("<IHHI", offset + len(pixels), 0, 0, offset)
    dib = struct.pack("<IiiHHIIiiII", 40, width, height, 1, 24, 0, len(pixels), 2835, 2835, 0, 0)
    return header + dib + pixels


def write_assets(branding: Path) -> None:
    png_names = {
        "default16.png": 16,
        "default22.png": 22,
        "default24.png": 24,
        "default32.png": 32,
        "default48.png": 48,
        "default64.png": 64,
        "default128.png": 128,
        "default256.png": 256,
    }
    for name, size in png_names.items():
        (branding / name).write_bytes(logo_png(size))

    for name, dimensions in {"wizHeader.bmp": (150, 57), "wizWatermark.bmp": (164, 314)}.items():
        (branding / name).write_bytes(wizard_bmp(*dimensions))

    icon = logo_png(256)
    # Windows Vista+ accepts a PNG frame in a one-image ICO container.
    directory = struct.pack("<HHH", 0, 1, 1)
    entry = struct.pack("<BBBBHHII", 0, 0, 0, 0, 1, 32, len(icon), 22)
    for name in ("firefox.ico", "firefox64.ico", "newtab.ico", "newwindow.ico", "pbmode.ico"):
        (branding / name).write_bytes(directory + entry + icon)


if __name__ == "__main__":
    import sys

    write_assets(Path(sys.argv[1]))
