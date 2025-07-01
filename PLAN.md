# Token Counter CLI - Plan & TODOs

## 1. Project Goal

To create a user-friendly command-line interface (CLI) tool in Python that counts the number of tokens in a given text file. The tool should provide progress feedback and present the final count in a visually appealing format.

## 2. Core Features

- Count tokens from a specified file path.
- Display a progress bar while processing the file.
- Output the total token count, file path, and other relevant info in a styled table.
- Handle potential errors gracefully (e.g., file not found).
- Use a standard, efficient tokenization library.

## 3. Technology Stack

- **Language:** Python 3
- **Package/Venv Management:** `uv`
- **CLI Framework:** `typer`
- **Styled Output & Progress:** `rich`
- **Tokenization:** `tiktoken`

## 4. Project Structure

```
token-counter/
├── .gitignore
├── PLAN.md
├── pyproject.toml
├── README.md
└── src/
    └── token_counter/
        ├── __init__.py
        ├── main.py          # CLI logic using typer and rich
        └── counter.py       # Core token counting functionality
```

## 5. Development Plan & TODOs

- [x] **1. Setup Project Environment**
    - [x] Initialize `pyproject.toml` for the project.
    - [x] Add dependencies: `typer`, `rich`, `tiktoken`.
    - [x] Create the basic directory structure (`src/token_counter`).

- [x] **2. Implement Core Logic**
    - [x] Create `src/token_counter/counter.py`.
    - [x] Implement a function to read a file and count tokens using `tiktoken`.
    - [x] The function should be efficient for large files (e.g., reading in chunks).

- [x] **3. Build the CLI**
    - [x] Create `src/token_counter/main.py`.
    - [x] Set up a `typer` application.
    - [x] Add a CLI command that accepts a file path as an argument.
    - [x] Integrate the `rich` library for progress tracking (e.g., `rich.progress`).
    - [x] Call the core counting logic from `counter.py`.

- [x] **4. Refine Output & UX**
    - [x] Use `rich.table.Table` to display the final results neatly.
    - [x] Include: File Path, Token Count, and maybe model/encoding used.
    - [x] Implement robust error handling (e.g., `FileNotFoundError`) with user-friendly `rich`-styled error messages.

- [x] **5. Documentation**
    - [x] Create a `README.md` with installation and usage instructions.
    - [x] Add a `.gitignore` file.

- [ ] **6. Enhancements**
    - [x] Implement interactive encoding selection using `InquirerPy` for `tiktoken` model, triggered by `--select-encoding` or `-s` flag, with default to `cl100k_base`.
    - [x] Allow reading from `stdin` so text can be piped to the tool.
    - [x] Add support for counting tokens in multiple files or directories.
    - [ ] Update `README.md` with new features.
    - [ ] Commit final changes to git.
