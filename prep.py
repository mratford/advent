from pathlib import Path

import nbformat

YEAR = "2024"

for day in range(1, 26):
    zeroday = f"day{day:02}"
    d = Path(YEAR) / zeroday
    d.mkdir(parents = True, exist_ok=True)
    
    nb = nbformat.v4.new_notebook()
    nb["cells"] = [
        nbformat.v4.new_markdown_cell(f"# Day {day}\n## Part 1\n"),
        nbformat.v4.new_code_cell()
    ]

    with open(Path(YEAR) / zeroday / f"{zeroday}.ipynb", "w") as f:
        nbformat.write(nb, f)
