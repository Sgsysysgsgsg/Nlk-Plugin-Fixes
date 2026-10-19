#!/usr/bin/env python3
"""Experimental PacketEvents 2.14.0 relocation into AxyronAC's shaded package.

Usage:
  python relocate_packetevents.py axyronac.jar packetevents-spigot-2.14.0.jar output.jar

This is a test-build helper, not a guarantee of plugin/API compatibility.
"""
import argparse
import struct
import zipfile

OLD_SLASH = b"com/github/retrooper/packetevents"
NEW_SLASH = b"ac/axyron/axyronac/shaded/com/github/retrooper/packetevents"
OLD_DOT = b"com.github.retrooper.packetevents"
NEW_DOT = b"ac.axyron.axyronac.shaded.com.github.retrooper.packetevents"
SOURCE_PREFIX = "com/github/retrooper/packetevents/"
SHADED_PREFIX = "ac/axyron/axyronac/shaded/com/github/retrooper/packetevents/"

def relocate_class(data):
    if data[:4] != b"\xca\xfe\xba\xbe":
        return data
    cp_count = struct.unpack_from(">H", data, 8)[0]
    pos = 10
    out = bytearray(data[:10])
    i = 1
    while i < cp_count:
        tag = data[pos]
        out.append(tag)
        pos += 1
        if tag == 1:
            length = struct.unpack_from(">H", data, pos)[0]
            pos += 2
            raw = data[pos:pos + length]
            pos += length
            raw = raw.replace(OLD_SLASH, NEW_SLASH).replace(OLD_DOT, NEW_DOT)
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
    return bytes(out)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("axyronac_jar")
    parser.add_argument("packetevents_jar")
    parser.add_argument("output_jar")
    args = parser.parse_args()
    entries = {}
    with zipfile.ZipFile(args.axyronac_jar) as base:
        for info in base.infolist():
            if info.filename.startswith(SHADED_PREFIX) and info.filename.endswith(".class"):
                continue
            entries[info.filename] = (info, base.read(info.filename))
    classes = 0
    mappings = 0
    with zipfile.ZipFile(args.packetevents_jar) as pe:
        for info in pe.infolist():
            name = info.filename
            if name.startswith(SOURCE_PREFIX) and name.endswith(".class"):
                target = SHADED_PREFIX + name[len(SOURCE_PREFIX):]
                entries[target] = (zipfile.ZipInfo(target), relocate_class(pe.read(name)))
                classes += 1
            elif name.startswith("assets/mappings/"):
                entries[name] = (zipfile.ZipInfo(name), pe.read(name))
                mappings += 1
            elif name in ("META-INF/packetevents_spigot_version.txt", "META-INF/packetevents_api_version.txt"):
                entries[name] = (zipfile.ZipInfo(name), b"2.14.0\n")
    if classes < 1500:
        raise SystemExit(f"Unexpectedly few PacketEvents classes relocated: {classes}")
    with zipfile.ZipFile(args.output_jar, "w", zipfile.ZIP_DEFLATED) as out:
        for name, (info, data) in entries.items():
            out.writestr(info, data)
    print(f"Created test JAR with {classes} relocated PacketEvents classes and {mappings} mapping resources.")
    print("This does not prove binary compatibility or runtime correctness; test on a backup server.")

if __name__ == "__main__":
    main()
