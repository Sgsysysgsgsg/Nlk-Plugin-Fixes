# Compatibility diagnosis

## Target environment
- Paper: 26.3-205
- Java: 25
- Plugins: AxyronAC 2.0.0 and Nemesis 2.1.2
- Standalone PacketEvents: 2.14.0 (reported by server)

## AxyronAC
Observed failure in PacketEvents shaded within the plugin:
```text
Failed to read StaticComponentType[minecraft:attribute_modifiers]
Can't find mapped entity with id 38
```

Likely area to investigate: mapping/registry data used by the shaded PacketEvents build when reading item component data for the newer protocol. This is a diagnosis, not a confirmed fix. Identify the embedded PacketEvents version and compare against compatible source/resources; do not assume replacing one registry resource fixes everything.

## Nemesis
Observed:
```text
Using nms mapping with mismatched minor versions: 1.21.5 - 26.3.0
NoSuchMethodError: CraftBlockData.fromData(BlockState)
```

Origin class:
```text
net.luxcube.minecraft.nms.v1_21_R11.NMSManagerImpl
```

This is a method linkage failure. A correct repair must verify the runtime method descriptor and patch/rebuild the NMS implementation against the correct API. Changing a version label alone is not enough.

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
