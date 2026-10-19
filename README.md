# NLK Plugin Fixes — Paper 26.3

Compatibility investigation for AxyronAC 2.0.0 and Nemesis 2.1.2 on Paper 26.3-205 with Java 25.

> **Status:** Investigation and diagnosis only. No patched plugin JAR has been verified.

## Findings

- AxyronAC embeds PacketEvents **2.12.2**, despite standalone PacketEvents 2.14.0 being installed. The recent candidate still embeds 2.12.2 and still fails reading `minecraft:attribute_modifiers` because it cannot find mapped entity ID 38.
- Nemesis's `v1_21_R11/NMSManagerImpl` still calls the old `CraftBlockData.fromData(BlockState)` method, matching the observed `NoSuchMethodError` on Paper 26.3.

Detailed evidence and the test matrix are in [docs/diagnosis.md](docs/diagnosis.md).

## Safe test process

1. Keep untouched copies of the original JARs and a full server backup.
2. Test candidates only on a separate test server.
3. Confirm both initialization errors disappear from full logs.
4. Verify core features and inspect for regressions.

Do not install experimental candidates on production. Do not publish proprietary plugin binaries unless redistribution rights are clear.
