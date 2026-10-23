# NLK Plugin Fixes — Paper 26.3

Experimental compatibility work for AxyronAC 2.0.0 and Nemesis 2.1.2 on Paper 26.3-205 / Java 25.

## Experimental candidates

- **Nemesis:** patch helper now handles both normal `/` and Windows-style `\\` JAR entry paths; the supplied Nemesis JAR used Windows-style paths, which meant the earlier helper skipped all NMS classes and produced no actual bytecode patch. The method-reference replacement candidate is present separately, but Paper 26.3 runtime remains unverified.
- **AxyronAC:** refreshed shaded PacketEvents from 2.12.2 to 2.14.0 and relocated it into AxyronAC's shaded package. ZIP and class-structure checks passed; runtime/API compatibility not yet tested.

Detailed findings: [docs/diagnosis.md](docs/diagnosis.md).

Helper scripts are in [tools/](tools/). These JAR modifications are experimental and should only be tested on a separate backup server. Do not treat them as production-ready until startup and gameplay tests pass.
