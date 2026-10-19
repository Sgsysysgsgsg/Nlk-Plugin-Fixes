# NLK Plugin Fixes — Paper 26.3

Compatibility investigation workspace for AxyronAC 2.0.0 and Nemesis 2.1.2 on Paper 26.3-205 / Java 25.

## Status

This repository is an investigation and test documentation workspace; it does not yet contain patched plugin JARs. A candidate must not be described as fixed until it is validated on a test server.

## Current findings from the supplied startup log

### AxyronAC

A PacketEvents copy shaded inside the plugin fails while parsing newer item component data:

- `Failed to read StaticComponentType[minecraft:attribute_modifiers]`
- `Can't find mapped entity with id 38`

The separately installed PacketEvents 2.14.0 loading successfully does not automatically replace the version embedded in AxyronAC.

### Nemesis

The log reports an NMS version mismatch (`1.21.5 - 26.3.0`) and `NoSuchMethodError: CraftBlockData.fromData(BlockState)` in `net.luxcube.minecraft.nms.v1_21_R11.NMSManagerImpl`. This is a binary/API mismatch; renaming a version string alone is not a verified repair.

## Validation checklist

1. Preserve original plugin JARs and back up the server.
2. Test candidate builds only on a separate test server.
3. Confirm both initialization errors disappear from full logs.
4. Test each plugin's core features and inspect the full startup log for regressions.

No patched JAR has been produced or verified yet. Do not use experimental builds on a production server. Do not distribute proprietary plugin binaries without permission.
