"""Generate 3D-printable STL/3MF files from a molecule using MolFidget."""

import os
import tempfile

from molfidget.config import load_mol_file
from molfidget.molecule import Molecule
from molfidget.molfidget import export_scene_as_colored_3mf


def run(avo_input):
    options = avo_input.get("options", {})
    sdf_content = avo_input.get("mol", "")

    if not sdf_content.strip():
        return {"error": "No molecule data received. Please open a molecule first."}

    output_dir = os.path.expanduser(options.get("output_dir", "~/molfidget-output"))
    scale = float(options.get("scale", 10.0))
    generate_3mf = bool(options.get("generate_3mf", True))

    # Extract molecule name from CJSON if available, else fall back to "molecule"
    cjson = avo_input.get("cjson", {})
    mol_name = cjson.get("name", "").strip() or _name_from_sdf(sdf_content) or "molecule"
    # sanitize for use as a directory/file name
    mol_name = "".join(c if c.isalnum() or c in "-_" else "_" for c in mol_name)

    output_subdir = os.path.join(output_dir, mol_name)
    os.makedirs(output_subdir, exist_ok=True)

    # Write SDF to a temp .mol file so molfidget can read it
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".mol", prefix=mol_name + "_", delete=False
    ) as tmp:
        tmp_path = tmp.name
        tmp.write(sdf_content)

    try:
        config = load_mol_file(tmp_path)
    except Exception as exc:
        return {"error": f"MolFidget could not parse the molecule: {exc}"}
    finally:
        os.unlink(tmp_path)

    # Override scale from user options
    config.molecule.scale = scale
    # Use the cleaned molecule name for output files
    config.molecule.name = mol_name

    try:
        molecule = Molecule(config.molecule, config.default)
        scene = molecule.create_trimesh_scene()
        scene.apply_scale(scale)

        if generate_3mf:
            three_mf_path = os.path.join(output_subdir, f"{mol_name}.3mf")
            export_scene_as_colored_3mf(scene, three_mf_path)

        molecule.save_stl_files(scale=scale, output_dir=output_subdir)
        molecule.merge_atoms()
        molecule.save_group_stl_files(scale, output_dir=output_subdir)
    except Exception as exc:
        return {"error": f"MolFidget failed to generate files: {exc}"}

    stl_files = [f for f in os.listdir(output_subdir) if f.endswith(".stl")]
    lines = [f"MolFidget export complete.\n\nOutput: {output_subdir}"]
    if generate_3mf:
        lines.append(f"  {mol_name}.3mf  (colored, all parts)")
    for f in sorted(stl_files):
        lines.append(f"  {f}")

    return {"message": "\n".join(lines)}


def _name_from_sdf(sdf_content: str) -> str:
    """Extract molecule name from the first line of an SDF/MOL block."""
    first_line = sdf_content.splitlines()[0].strip() if sdf_content else ""
    return first_line if first_line else ""
