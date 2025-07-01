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
├── tests/
│   ├── __init__.py
│   ├── test_cli.py          # Tests for CLI functionality
│   └── test_counter.py      # Tests for core logic
└── src/
    └── token_counter/
        ├── __init__.py
        ├── __main__.py      # Enables `python -m token_counter`
        ├── cli.py           # CLI logic using typer and rich
        ├── counter.py       # Core token counting functionality
        └── config/
            ├── allowed_extensions.json  # Default file extensions
            └── llm_limits.json         # LLM context window limits
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

- [x] **6. Enhancements**
    - [x] Implement interactive encoding selection using `InquirerPy` for `tiktoken` model, triggered by `--select-encoding` or `-s` flag, with default to `cl100k_base`.
    - [x] Allow reading from `stdin` so text can be piped to the tool.
    - [x] Add support for counting tokens in multiple files or directories.
    - [x] Add `--exclude` option for glob patterns in directory scanning.
    - [x] Add `--check-limits` option to compare token count against LLM context window limits.
    - [x] Externalize LLM limits to `llm_limits.json`.
    - [x] Externalize default file extensions (whitelist) to `allowed_extensions.json`.
    - [x] Add `--extension` flag: This flag allows users to **override** the default list of allowed file extensions loaded from `allowed_extensions.json`, meaning only files with the specified extensions will be processed. If both `--extension` and `--add-extensions` are provided, `--extension` will take precedence, and a warning will be displayed to the user.
    - [x] Add `--add-extensions` (or `-a`) flag: This flag allows users to **add** new file extensions to the default list of allowed extensions loaded from `allowed_extensions.json`. Files with these added extensions will be processed in addition to the default ones. This flag will be ignored if `--extension` is also provided.
    - [x] Update `README.md` with new features.
    - [x] Commit final changes to git.

- [x] **7. Repository Structure Cleanup**
    - [x] Remove redundant root-level `main.py` file.
    - [x] Rename `src/token_counter/main.py` to `src/token_counter/cli.py` for better clarity.
    - [x] Add `src/token_counter/__main__.py` to enable `python -m token_counter` execution.
    - [x] Create `src/token_counter/config/` directory for configuration files.
    - [x] Move `allowed_extensions.json` and `llm_limits.json` to `config/` subdirectory.
    - [x] Update import paths in code to reflect new structure.
    - [x] Update `pyproject.toml` entry point to use new CLI module name.
    - [x] Add `tests/` directory structure for future testing.
    - [x] Update project structure documentation in PLAN.md.
    - [x] Commit repository cleanup changes.
