#!/usr/bin/env python3
"""Combine the Doom firmware .bin and a .whx WAD into one UF2 for the RP2040.

usage: make_uf2.py firmware.bin doom1.whx out.uf2 [wad_addr_hex]

The RP2040 boot ROM tracks erased sectors by UF2 *block number* and assumes the
blocks are contiguous in flash, so the gap between the end of the firmware and
the WAD address is filled with 0xFF padding blocks. A sparse UF2 corrupts the
first WAD sector and the game panics with "No WXD".
"""
import struct, sys
fw_path, whx_path, out_path = sys.argv[1:4]
WAD_ADDR = int(sys.argv[4], 16) if len(sys.argv) > 4 else 0x10041000
FLASH_BASE = 0x10000000
FAMILY = 0xe48bff56
fw = open(fw_path, 'rb').read()
whx = open(whx_path, 'rb').read()
assert len(fw) <= WAD_ADDR - FLASH_BASE, 'firmware overlaps WAD slot'
assert WAD_ADDR - FLASH_BASE + len(whx) <= 0x200000, 'WAD too big for 2 MB flash'
image = fw + b'\xff' * (WAD_ADDR - FLASH_BASE - len(fw)) + whx     # contiguous
if len(image) % 256:
    image += b'\xff' * (256 - len(image) % 256)
n = len(image) // 256
out = bytearray()
for i in range(n):
    out += struct.pack('<IIIIIIII', 0x0A324655, 0x9E5D5157, 0x2000, FLASH_BASE + i * 256, 256, i, n, FAMILY)
    out += image[i * 256:(i + 1) * 256] + b'\0' * 220 + struct.pack('<I', 0x0AB16F30)
open(out_path, 'wb').write(out)
print('wrote %s: %d blocks, firmware %d B, padding %d B, WAD %d B at %#x' %
      (out_path, n, len(fw), WAD_ADDR - FLASH_BASE - len(fw), len(whx), WAD_ADDR))
