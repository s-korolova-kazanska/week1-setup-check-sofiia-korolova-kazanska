"""CI runner: validate committed outputs, then re-execute check.ipynb.

Two checks, in order:

1. Committed-output check, on the notebook as committed (before any
   re-execution): every non-empty code cell must have saved, non-error
   output. This proves the student actually ran the cells on their own
   machine and saved the result — a blank or never-run notebook fails here.

2. Re-execution check: run the notebook top to bottom in a clean kernel.
   `jupyter nbconvert --execute` and `jupyter execute` both exit 0 even when
   cells raise (the conversion succeeds; the error is just recorded), so this
   uses ExecutePreprocessor directly and propagates CellExecutionError.

ExecutePreprocessor.preprocess mutates the notebook in place, regenerating
outputs — so check 1 MUST happen before check 2.
"""
import sys

import nbformat
from nbconvert.preprocessors import CellExecutionError, ExecutePreprocessor

NOTEBOOK = "check.ipynb"
TIMEOUT_SECONDS = 60

with open(NOTEBOOK) as f:
    nb = nbformat.read(f, as_version=4)

# Check 1: committed outputs.
problems = []
code_cell_no = 0
for cell in nb.cells:
    if cell.cell_type != "code" or not cell.source.strip():
        continue
    code_cell_no += 1
    first_line = cell.source.strip().splitlines()[0]
    label = f"cell #{code_cell_no} ({first_line!r})"
    if not cell.outputs:
        problems.append(f"{label}: no saved output — the cell was not run before commit")
    elif any(o.get("output_type") == "error" for o in cell.outputs):
        problems.append(f"{label}: the saved output contains an error")

if problems:
    print(
        "Check failed: the notebook must be executed top to bottom and saved "
        "before commit.\n\n"
        "Open check.ipynb, run every cell (Shift+Enter), save (Cmd+S / Ctrl+S), "
        "then commit and push again.\n\n"
        "Problem cells:",
        file=sys.stderr,
    )
    for p in problems:
        print(f"  - {p}", file=sys.stderr)
    sys.exit(1)

# Check 2: re-execution in a clean kernel.
ep = ExecutePreprocessor(timeout=TIMEOUT_SECONDS, kernel_name="python3")

try:
    ep.preprocess(nb)
except CellExecutionError as e:
    print(f"Check failed: a cell raised during re-execution.\n\n{e}", file=sys.stderr)
    sys.exit(1)

print("Setup check passed: outputs saved and the notebook re-executes cleanly.")
