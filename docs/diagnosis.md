# Compatibility diagnosis

## Target environment
- Paper: 26.3-205
- Java: 25
- Plugins: AxyronAC 2.0.0 and Nemesis 2.1.2
- Standalone PacketEvents: 2.14.0

## Nemesis — experimental method-reference patch

The uploaded Nemesis JAR had Windows-style backslashes in ZIP entry paths. The previous helper only matched forward slashes, so it could silently skip all three `NMSManagerImpl.class` targets. The helper has now been fixed to normalize entry names when matching and when writing the output archive.

The three NMS manager call sites in `v1_21_R3`, `v1_21_R6`, and `v1_21_R11` reference `CraftBlockData.fromData(BlockState)`, which throws `NoSuchMethodError` on Paper 26.3. The experimental patch changes those constant-pool method names to `CraftBlockData.createData(BlockState)`.

Static checks on the latest candidate confirmed:
- all 3 NMS manager classes were patched;
- their disassembled bytecode references `CraftBlockData.createData(BlockState)`;
- output ZIP archive integrity passed;
- output ZIP entry paths use standard forward slashes.

These checks validate archive structure and the intended bytecode reference only. They do **not** establish runtime compatibility or successful Nemesis initialization. A runtime test must confirm that the NMS manager constructs and the `VisionModule` and other desired functions work on Paper 26.3 / Java 25.

## AxyronAC — PacketEvents refresh candidate

The original plugin embeds PacketEvents 2.12.2. An experimental candidate replaces its shaded PacketEvents classes with 2.14.0 classes, relocates them into AxyronAC's shaded namespace, and replaces PacketEvents mapping resources.

Structural validation is not proof of binary compatibility. The patched candidate must be tested for player join, channel injection, packet parsing, and gameplay before production use.

## Safe test checklist

1. Back up the server and keep untouched original JARs.
2. Test one candidate at a time on a separate Paper 26.3-205 server running Java 25.
3. For Nemesis, confirm the `NoSuchMethodError` is gone, the NMS manager initializes, and Vision/disguise/commands work.
4. For AxyronAC, confirm component bootstrap succeeds and players can join without PacketEvents channel-injection errors.
5. Review the full startup log and test actual features before production use.

Do not install experimental candidates on production. No runtime-success claim is made yet.
