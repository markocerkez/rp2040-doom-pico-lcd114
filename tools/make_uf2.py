#!/usr/bin/env python3
"""Combine the Doom firmware .bin and a .whx WAD into one UF2 for the RP2040."""
import struct, sys
fw_path, whx_path, out_path = sys.argv[1:4]
WAD_ADDR = 0x10041000
FAMILY = 0xe48bff56
def blocks(data, base):
    return [(base + i, (data[i:i + 256] + b'\0' * 256)[:256]) for i in range(0, len(data), 256)]
fw = open(fw_path, 'rb').read(); whx = open(whx_path, 'rb').read()
assert len(fw) <= WAD_ADDR - 0x10000000, 'firmware overlaps WAD slot'
assert WAD_ADDR - 0x10000000 + len(whx) <= 0x200000, 'WAD too big for 2 MB flash'
bl = blocks(fw, 0x10000000) + blocks(whx, WAD_ADDR)
out = bytearray()
for idx, (addr, chunk) in enumerate(bl):
    out += struct.pack('<IIIIIIII', 0x0A324655, 0x9E5D5157, 0x2000, addr, 256, idx, len(bl), FAMILY)
    out += chunk + b'\0' * 220 + struct.pack('<I', 0x0AB16F30)
open(out_path, 'wb').write(out)
print('wrote', out_path, len(bl), 'blocks')
