# Compatibility diagnosis

## Target environment
- Paper: 26.3-205
- Java: 25
- Plugins: AxyronAC 2.0.0 and Nemesis 2.1.2
- Standalone PacketEvents: 2.14.0 (reported by server)

## AxyronAC — verified artifact inspection

The original AxyronAC JAR reports PacketEvents **2.12.2** in both:
- `META-INF/packetevents_spigot_version.txt`
- `META-INF/packetevents_api_version.txt`

Its PacketEvents classes are shaded under `ac/axyron/axyronac/shaded/com/github/retrooper/packetevents/`.

The supplied candidate `AxyronAC-2.0.0-26.3-PE214-entity-registry-fix-TEST.jar` still reports embedded PacketEvents **2.12.2**. Its `assets/mappings/registries/entity_type.nbt` is 7,923 bytes, the same size as the standalone PacketEvents 2.14.0 resource; this shows a resource-level substitution was attempted, but the embedded implementation remains 2.12.2. This candidate's startup log still fails with:

```text
Failed to read StaticComponentType[minecraft:attribute_modifiers]
Can't find mapped entity with id 38
```

Therefore, swapping one mapping resource is not a verified fix. The next investigation should compare all required mappings and the shaded parser implementation against a compatible PacketEvents release, with careful relocation and dependency checks.

## Nemesis — verified bytecode inspection

The supplied `Nemesis-2.1.2-26.3-path-fix.jar` contains:
`net/luxcube/minecraft/nms/v1_21_R11/NMSManagerImpl.class`

Its bytecode calls:

```text
org/bukkit/craftbukkit/block/data/CraftBlockData.fromData(
  net/minecraft/world/level/block/state/BlockState
): org/bukkit/craftbukkit/block/data/CraftBlockData
```

The startup log reports:
```text
Using nms mapping with mismatched minor versions: 1.21.5 - 26.3.0
NoSuchMethodError: CraftBlockData.fromData(BlockState)
```

This confirms the candidate still contains the old method call. The Paperclip server JAR includes a patched server payload, while the embedded Paper API JAR does not contain the internal CraftBlockData implementation. A correct fix requires obtaining/deriving the actual runtime signature from the remapped 26.3 server and then patching or rebuilding the NMS implementation. Changing version strings alone is not sufficient.

## Test matrix

| Check | Required result |
|---|---|
| Server boot | Paper reaches ready state without either plugin initialization exception |
| AxyronAC enable | Embedded PacketEvents component bootstrap succeeds |
| Nemesis enable | NMS manager constructs without NoSuchMethodError |
| Gameplay smoke test | Core features of each plugin work on the private test server |
| Regression | No new linkage, mapping, or registry errors in full logs |

## Current result

No patched plugin JAR has been verified. Keep candidate changes experimental until the full test matrix passes.
