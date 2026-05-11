# avogadro-molfidget

Export 3D-printable molecular models from Avogadro 2 using [MolFidget](https://github.com/longjie0723/molfidget/).

Adds **File → Export → MolFidget...** to generate STL and 3MF files ready
for 3D printing. Single bonds become rotating spin joints so the printed
model is a fidget toy with movable conformation — double and triple bonds
are printed as rigid connectors.

## Output files

- `<molecule>.3mf` — full colored model (one file, for multi-material or
  color printers such as Bambu Lab)
- `<atom>.stl` — one STL per atom sphere
- `<element>_group.stl` — merged STL per element (all carbons in one file,
  all oxygens in one, etc.)

## Options

| Option | Default | Description |
|--------|---------|-------------|
| Output Directory | `~/molfidget-output` | Where files are saved (a subdirectory named after the molecule is created inside) |
| Scale Factor | 10.0 | Scales angstroms → mm. 10× gives a typical desk-sized model |
| Also generate 3MF | on | Produce a colored 3MF in addition to the STL files |

## Installation

```bash
cd avogadro-molfidget
pixi install
```

Then register the plugin in Avogadro's Plugin Manager.

## Requirements

- Python ≥ 3.12
- [molfidget](https://pypi.org/project/molfidget/) ≥ 1.2.0 (installed automatically)

## License

BSD-3-Clause
