#!/usr/bin/env python3
"""Experimental bytecode patch for Nemesis 2.1.2 on Paper 26.3.

Replaces CraftBlockData.fromData(BlockState) with createData(BlockState) in
known NMS manager classes. Always test on a backup server.
"""
import argparse
import struct
import zipfile

TARGET_SUFFIX = "/NMSManagerImpl.class"
TARGET_PREFIX = "net/luxcube/minecraft/nms/"
VERSIONS = ("v1_21_R3", "v1_21_R6", "v1_21_R11")

def normalize(name):
    return name.replace("\\\\", "/")
OLD = b"fromData"
NEW = b"createData"

def patch_class(data):
    if data[:4] != b"\xca\xfe\xba\xbe":
        return data, 0
    cp_count = struct.unpack_from(">H", data, 8)[0]
    pos = 10
    out = bytearray(data[:10])
    i = 1
    changes = 0
    while i < cp_count:
        tag = data[pos]
        out.append(tag)
        pos += 1
        if tag == 1:
            length = struct.unpack_from(">H", data, pos)[0]
            pos += 2
            raw = data[pos:pos + length]
            pos += length
            if raw == OLD:
                raw = NEW
                changes += 1
            out += struct.pack(">H", len(raw)) + raw
        elif tag in (3, 4):
            out += data[pos:pos + 4]; pos += 4
        elif tag in (5, 6):
            out += data[pos:pos + 8]; pos += 8
            i += 1
        elif tag in (7, 8, 16, 19, 20):
            out += data[pos:pos + 2]; pos += 2
        elif tag in (9, 10, 11, 12, 17, 18):
            out += data[pos:pos + 4]; pos += 4
        elif tag == 15:
            out += data[pos:pos + 3]; pos += 3
        else:
            raise ValueError(f"Unknown constant-pool tag {tag}")
        i += 1
    out += data[pos:]
    return bytes(out), changes

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_jar")
    parser.add_argument("output_jar")
    args = parser.parse_args()
    patched = []
    targets = {f"net/luxcube/minecraft/nms/{version}/NMSManagerImpl.class" for version in VERSIONS}
    with zipfile.ZipFile(args.input_jar) as src:
        normalized = {normalize(n): n for n in src.namelist()}
        found = targets.intersection(normalized)
        if not found:
            raise SystemExit("No NMSManagerImpl targets found; input JAR paths/layout are unexpected.")
        entries = []
        for info in src.infolist():
            content = src.read(info.filename)
            if normalize(info.filename) in found:
                content, count = patch_class(content)
                if count < 1:
                    raise SystemExit(f"No fromData UTF8 constant found in {info.filename}; refusing to write output.")
                patched.append((info.filename, count))
            entries.append((info, content))
    if not patched:
        raise SystemExit("No target method references found; output should not be treated as patched.")
    with zipfile.ZipFile(args.output_jar, "w", zipfile.ZIP_DEFLATED) as dst:
        for info, content in entries:
            dst.writestr(info, content)
    print("Patched constant-pool method names:")
    for name, count in patched:
        print(f"  {name}: {count}")
    print("This only validates bytecode string replacement, not runtime behavior.")

if __name__ == "__main__":
    main()
