# NLK Plugin Fixes — Paper 26.3

Compatibility investigation for AxyronAC 2.0.0 and Nemesis 2.1.2 on Paper 26.3-205 with Java 25.

> **Status:** Diagnosis and test documentation only. No patched plugin JAR has been produced or verified.

## Findings from the supplied startup log

### AxyronAC

A PacketEvents copy shaded inside AxyronAC fails while parsing newer item component data:

- `Failed to read StaticComponentType[minecraft:attribute_modifiers]`
- `Can't find mapped entity with id 38`

The separately installed PacketEvents 2.14.0 loading successfully does not automatically replace the copy embedded in AxyronAC.

### Nemesis

The log reports an NMS mapping mismatch (`1.21.5 - 26.3.0`) and `NoSuchMethodError: CraftBlockData.fromData(BlockState)` in `net.luxcube.minecraft.nms.v1_21_R11.NMSManagerImpl`.

This is a binary/API mismatch. Changing a version string alone is not a verified repair.

## Test requirements

1. Preserve original plugin JARs and back up the server.
2. Test candidate builds only on a separate test server.
3. Confirm both initialization exceptions disappear from full logs.
4. Verify core plugin functionality and inspect logs for regressions.

Do not install experimental candidates on production. Do not publish proprietary plugin binaries unless redistribution rights are clear.
