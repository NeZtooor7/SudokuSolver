# SudokuSolver (Django)

A small web app that solves Sudoku puzzles in the browser using a classic **backtracking** solver. The UI is a 9×9 grid; you type the given numbers, click **Solve**, and the solved Sudoku is rendered back into the table.

---

## What is a “backtracking algorithm template”?

**Backtracking** is a general problem‑solving pattern for constraint problems (like Sudoku):

1. Pick an empty position (a “decision”).
2. Try a candidate value that doesn’t violate constraints.
3. Recurse to solve the rest of the problem.
4. If you reach a dead end, **undo** the choice and try the next candidate.

In this project, the solver looks for possible values for a cell (1–9 that don’t conflict with the row/column/3×3 box) and recursively explores choices until the puzzle is completed.

---

## Tech stack

- **Python**: 3.13.x (tested with 3.13.5)
- **Django**: 5.2.6
- **Frontend**:
  - Bootstrap 3.3.6
  - jQuery 1.12.4

---

## Project routes

- `GET /` → Shows an empty Sudoku grid.
- `POST /action/` → Validates input, solves the Sudoku, and re-renders the page (or shows an error modal).

---

## Setup and run

### 1) Create and activate a virtual environment (Windows)

```bat
python -m venv venv
venv\Scripts\activate
```

(macOS/Linux)

```bash
python3 -m venv venv
source venv/bin/activate
```

### 2) Install dependencies

If you have a `requirements.txt`:

```bash
pip install -r requirements.txt
```

If you don’t have one yet, the minimum dependency is:

```bash
pip install "Django==5.2.6"
```

(Optional) Generate `requirements.txt`:

```bash
pip freeze > requirements.txt
```

### 3) Run the server

From the folder containing `manage.py`:

```bash
python manage.py runserver
```

Then open:

- http://127.0.0.1:8000/

---

## How to solve a Sudoku using the interface

1. Go to the home page `/`.
2. Fill in the given Sudoku numbers in the 9×9 grid.
   - Leave empty cells blank.
3. Click **Solve**.
4. The app will either:
   - Show the solved puzzle in the grid, or
   - Show a Bootstrap modal with an error message.

Use **Clear** to reset the board back to an empty grid.

---

## Input validation performed before solving

When you submit the form (`POST /action/`), the backend performs these checks:

### 1) Cell format validation
Each submitted cell is read from `request.POST`:

- Empty string is treated as `0` (meaning “blank cell”).
- Each value must be **a single numeric character**.
- If a non-numeric value or multi-character string is found, an error is returned.

This logic is implemented in:

- `validate_the_numerical_values_and_fill_the_matrix(...)`

### 2) Sudoku consistency validation
Before solving, `is_valid_sudoku(matrix)` verifies:

- The grid is **9×9** (81 cells total).
- No duplicates (ignoring zeros) in:
  - any row,
  - any column,
  - any 3×3 sub-square.
- Every empty cell (`0`) still has **at least one possible value** available (so the puzzle isn’t already impossible).

Implementation:

- `is_valid_sudoku(...)` and `_get_posible_values_of_cell(...)`

If validation fails, the UI displays an error modal with a message such as **“The sudoku is invalid.”**

### 3) Solving
If validations pass, the solver runs:

- `solve_sudoku(matrix)` → recursive backtracking solution.

---

## Notes

- In the HTML, inputs use ids like `cell-11` and names like `cell_11` so the CSS can style Sudoku sub-grid borders and the backend can read each value predictably.
- Disabled inputs are styled with a grey background in CSS.

---

## License

Add a license here if you plan to publish the project.
