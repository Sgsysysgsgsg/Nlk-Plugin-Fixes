# Compatibility diagnosis

## Target environment
- Paper: 26.3-205
- Java: 25
- Plugins: AxyronAC 2.0.0 and Nemesis 2.1.2
- Standalone PacketEvents: 2.14.0

## Nemesis — bytecode patch prepared

The prior candidate called `CraftBlockData.fromData(BlockState)`, which fails with `NoSuchMethodError` on the target runtime. Current Paper source exposes `CraftBlockData.createData(BlockState)` instead. A new experimental JAR now changes that method reference in all three bundled NMS manager classes (`v1_21_R3`, `v1_21_R6`, and `v1_21_R11`).

Bytecode inspection with `javap` confirms those three call sites now reference:

```text
CraftBlockData.createData(BlockState): CraftBlockData
```

This confirms the class-file patch was applied. It has **not** yet been run on Paper 26.3, so startup and gameplay remain unverified.

## AxyronAC — PacketEvents refresh candidate prepared

The original plugin embeds PacketEvents 2.12.2. A new experimental candidate replaces its shaded PacketEvents classes with the 2.14.0 classes, relocates package references to AxyronAC's shaded namespace, and replaces the PacketEvents mapping resources.

Archive validation confirms:
- 1,657 PacketEvents classes copied/relocated
- 130 mapping resources replaced
- embedded version marker is 2.14.0
- no duplicate ZIP entry names
- relocated `PacketEvents.class` can be read by `javap`

This is **structural validation only**. AxyronAC may rely on APIs or behavior changed between PacketEvents 2.12.2 and 2.14.0, so this candidate must be tested before use.

## Safe test checklist

1. Back up the server and keep original JARs.
2. Test one candidate at a time on a separate Paper 26.3-205 server running Java 25.
3. For Nemesis, confirm the NMS manager constructs and the previous `NoSuchMethodError` is gone.
4. For AxyronAC, confirm component bootstrap succeeds and there are no linkage or mapping errors.
5. Test actual plugin features, then review the complete startup log.

Do not install experimental candidates on production. No runtime-success claim is made yet.
