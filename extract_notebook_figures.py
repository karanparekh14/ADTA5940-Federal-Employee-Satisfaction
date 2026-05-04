"""
Extract every PNG output cell from a Jupyter notebook into individual files.

Run AFTER you've executed the notebook end-to-end and saved it
(File > Save and Checkpoint, OR just Ctrl+S after Run All).

Usage:
  python extract_notebook_figures.py [optional_notebook_path]

Default target: Attrition_Pipeline_Cleaned.ipynb
"""
from pathlib import Path
import sys, json, base64, re

HERE = Path(__file__).resolve().parent
DEFAULT_NB = HERE / "Attrition_Pipeline_Cleaned.ipynb"
OUT_DIR = HERE / "figures_from_notebook"


def slugify(text: str, maxlen: int = 60) -> str:
    """Make a safe filename fragment from arbitrary cell text."""
    text = re.sub(r"[^A-Za-z0-9]+", "_", text).strip("_").lower()
    return text[:maxlen] or "untitled"


def extract(notebook_path: Path, out_dir: Path) -> int:
    if not notebook_path.exists():
        sys.exit(f"Notebook not found: {notebook_path}")
    out_dir.mkdir(exist_ok=True)
    # Clear stale extracts
    for p in out_dir.glob("*.png"):
        p.unlink()

    with notebook_path.open("r", encoding="utf-8") as f:
        nb = json.load(f)

    saved = 0
    for cell_idx, cell in enumerate(nb.get("cells", [])):
        if cell.get("cell_type") != "code":
            continue
        # Hint for filename: first non-comment line of source
        src_lines = cell.get("source", [])
        hint = ""
        for ln in src_lines:
            ln = ln.strip()
            if ln and not ln.startswith("#"):
                hint = slugify(ln, 50)
                break
        if not hint:
            for ln in src_lines:
                ln = ln.strip().lstrip("#").strip()
                if ln:
                    hint = slugify(ln, 50)
                    break
        hint = hint or "cell"

        outputs = cell.get("outputs", [])
        out_seq = 0
        for out in outputs:
            data = out.get("data", {})
            png_b64 = data.get("image/png")
            if not png_b64:
                continue
            out_seq += 1
            png_bytes = base64.b64decode(png_b64)
            fname = f"cell{cell_idx:02d}_{hint}{'' if out_seq == 1 else f'_{out_seq}'}.png"
            (out_dir / fname).write_bytes(png_bytes)
            print(f"  saved {fname}  ({len(png_bytes)//1024} KB)")
            saved += 1

    return saved


def main():
    nb_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_NB
    print(f"Extracting figures from: {nb_path}")
    print(f"Output dir:              {OUT_DIR}")
    n = extract(nb_path, OUT_DIR)
    print(f"\nDone. Extracted {n} figure(s) into {OUT_DIR}")
    if n == 0:
        print("\nNo figures found. Make sure you ran the notebook (Run All) AND saved it before running this extractor.")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
